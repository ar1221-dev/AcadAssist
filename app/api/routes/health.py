"""FastAPI router for health and Azure diagnostic endpoints.

Provides /api/health and /api/health/azure without requiring Azure CLI.
Never exposes keys, tokens, client secrets, or sensitive headers.
"""

import logging
from typing import Any, Dict
from fastapi import APIRouter
from sqlalchemy import text

from app.config import settings
from app.database.session import SessionLocal

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


def check_database() -> str:
    """Check database connectivity with a lightweight ping query."""
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        return "connected"
    except Exception as exc:
        logger.warning("Database connectivity check failed: %s", exc)
        return "unreachable"


def check_azure_blob_storage() -> Dict[str, str]:
    """Lightweight read-only check for Azure Blob Storage connectivity."""
    storage_account = getattr(settings, "AZURE_STORAGE_ACCOUNT", None)
    conn_string = getattr(settings, "AZURE_STORAGE_CONNECTION_STRING", None)
    if not storage_account and not conn_string:
        return {
            "status": "not_configured",
            "message": "Azure Blob Storage is not configured (local storage fallback active).",
        }

    try:
        from azure.core.exceptions import (
            ClientAuthenticationError,
            HttpResponseError,
            ServiceRequestError,
            ServiceResponseTimeoutError,
        )
        from app.azure.storage import AzureStorageClient

        client = AzureStorageClient()
        container_client = client.get_container_client()
        # Read-only container existence check with quick timeout
        exists = container_client.exists(timeout=3.0)
        return {
            "status": "connected",
            "message": f"Azure Blob Storage connected (container '{client.container_name}' exists: {exists}).",
        }
    except ImportError:
        return {"status": "not_implemented", "message": "Azure Storage SDK not installed."}
    except ClientAuthenticationError:
        return {
            "status": "authentication_failed",
            "message": "Azure Blob Storage authentication failed. Check credentials.",
        }
    except (ServiceRequestError, ServiceResponseTimeoutError):
        return {
            "status": "unreachable",
            "message": "Azure Blob Storage endpoint is unreachable.",
        }
    except HttpResponseError as hre:
        if hre.status_code in (401, 403):
            return {
                "status": "authentication_failed",
                "message": "Azure Blob Storage access forbidden or unauthorized.",
            }
        return {
            "status": "error",
            "message": "Azure Blob Storage returned an error response.",
        }
    except Exception as exc:
        logger.debug("Azure Blob Storage diagnostic error: %s", type(exc).__name__)
        return {
            "status": "error",
            "message": "Azure Blob Storage check encountered an error.",
        }


def check_azure_search() -> Dict[str, str]:
    """Lightweight read-only check for Azure AI Search connectivity."""
    search_endpoint = getattr(settings, "AZURE_SEARCH_ENDPOINT", None) or getattr(
        settings, "AZURE_SEARCH_SERVICE_ENDPOINT", None
    )
    if not search_endpoint:
        return {
            "status": "not_configured",
            "message": "Azure AI Search is not configured (local hybrid index active).",
        }

    try:
        from azure.core.exceptions import (
            ClientAuthenticationError,
            HttpResponseError,
            ServiceRequestError,
            ServiceResponseTimeoutError,
        )
        from app.azure.search import AzureSearchManager

        mgr = AzureSearchManager()
        index_client = mgr.get_index_client()
        # Read-only index check with quick timeout
        _ = next(iter(index_client.list_index_names(timeout=3.0)), None)
        return {
            "status": "connected",
            "message": "Azure AI Search connected (search service reachable).",
        }
    except ImportError:
        return {"status": "not_implemented", "message": "Azure Search SDK not installed."}
    except ClientAuthenticationError:
        return {
            "status": "authentication_failed",
            "message": "Azure AI Search authentication failed. Check search keys / credentials.",
        }
    except (ServiceRequestError, ServiceResponseTimeoutError):
        return {
            "status": "unreachable",
            "message": "Azure AI Search service is unreachable.",
        }
    except HttpResponseError as hre:
        if hre.status_code in (401, 403):
            return {
                "status": "authentication_failed",
                "message": "Azure AI Search authentication or permission denied.",
            }
        return {
            "status": "error",
            "message": "Azure AI Search service returned an error response.",
        }
    except Exception as exc:
        logger.debug("Azure AI Search diagnostic error: %s", type(exc).__name__)
        return {
            "status": "error",
            "message": "Azure AI Search check encountered an error.",
        }


def check_microsoft_foundry() -> Dict[str, str]:
    """Lightweight check for Microsoft Foundry / Azure OpenAI configuration and connectivity."""
    try:
        from app.azure.foundry import FoundryProjectManager
        import openai

        f_mgr = FoundryProjectManager()
        if not f_mgr.is_configured:
            return {
                "status": "not_configured",
                "message": "Microsoft Foundry / Azure OpenAI is not configured (local orchestrator active).",
            }

        client = f_mgr.get_openai_client()
        # Read-only model list query without generating any completions or tokens
        _ = client.models.list(timeout=3.0)
        return {
            "status": "connected",
            "message": f"Microsoft Foundry / OpenAI connected (model: {f_mgr.model_deployment or 'default'}).",
        }
    except ImportError:
        return {"status": "not_implemented", "message": "Azure AI Projects or OpenAI SDK not installed."}
    except Exception as exc:
        logger.debug("Foundry check exception: %s", type(exc).__name__)
        exc_str = str(exc).lower()
        if "auth" in exc_str or "key" in exc_str or "credential" in exc_str or "401" in exc_str or "403" in exc_str:
            return {
                "status": "authentication_failed",
                "message": "Microsoft Foundry authentication failed. Check configured API key or Entra ID credentials.",
            }
        if "connect" in exc_str or "timeout" in exc_str or "unreachable" in exc_str:
            return {
                "status": "unreachable",
                "message": "Microsoft Foundry endpoint is unreachable.",
            }
        return {
            "status": "error",
            "message": "Microsoft Foundry check encountered an error.",
        }


def compute_aggregate_status(services: Dict[str, Dict[str, str]]) -> str:
    """Derive top-level status from individual service statuses."""
    statuses = [s["status"] for s in services.values()]

    if "authentication_failed" in statuses:
        return "authentication_failed"
    if "unreachable" in statuses:
        return "unreachable"
    if "error" in statuses:
        return "error"
    if all(s == "not_configured" for s in statuses):
        return "not_configured"
    if all(s in ("connected", "not_configured") for s in statuses) and any(s == "connected" for s in statuses):
        return "connected"
    if all(s == "not_implemented" for s in statuses):
        return "not_implemented"
    return "connected"


@router.get("/health", summary="Application health status")
def get_application_health() -> Dict[str, Any]:
    """Unified application health check reporting subsystem readiness and database state."""
    db_status = check_database()
    foundry_configured = getattr(settings, "is_foundry_configured", False)
    storage_configured = getattr(settings, "is_storage_configured", False)
    search_configured = getattr(settings, "is_search_configured", False)
    embedding_configured = bool(
        getattr(settings, "AZURE_OPENAI_API_KEY", None)
        or getattr(settings, "AZURE_API_KEY", None)
        or getattr(settings, "OPENAI_API_KEY", None)
    )

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "AcadAssist API",
        "environment": settings.ENVIRONMENT,
        "app": "AcadAssist",
        "version": settings.app_version if hasattr(settings, "app_version") else "2.0.0",
        "database": db_status,
        "subsystems": {
            "knowledge_rag": "operational",
            "assessment": "operational",
            "study_intelligence": "operational",
        },
        "foundry": {
            "mode": "cloud_foundry" if foundry_configured else "local_orchestrator",
            "configured": foundry_configured,
        },
        "azure_storage": {
            "mode": "azure_blob" if storage_configured else "local_storage",
            "configured": storage_configured,
        },
        "azure_search": {
            "mode": "azure_ai_search" if search_configured else "local_hybrid_index",
            "configured": search_configured,
        },
        "embeddings": {
            "mode": "azure_openai" if embedding_configured else "local_deterministic",
            "configured": embedding_configured,
            "model": settings.EMBEDDING_MODEL,
            "dimensions": settings.EMBEDDING_DIMENSIONS,
        },
        "embedding_model": settings.EMBEDDING_MODEL,
        "embedding_dimensions": settings.EMBEDDING_DIMENSIONS,
    }


@router.get("/health/azure", summary="Azure service connectivity diagnostics")
def get_azure_diagnostics() -> Dict[str, Any]:
    """Run lightweight, read-only diagnostic checks for Azure services.

    Distinguishes:
    - not_configured
    - connected
    - authentication_failed
    - unreachable
    - error
    - not_implemented

    Does NOT expose keys, secrets, tokens, or credentials.
    """
    blob_diag = check_azure_blob_storage()
    search_diag = check_azure_search()
    foundry_diag = check_microsoft_foundry()

    services = {
        "azure_blob_storage": blob_diag,
        "azure_ai_search": search_diag,
        "microsoft_foundry": foundry_diag,
    }

    aggregate_status = compute_aggregate_status(services)

    return {
        "status": aggregate_status,
        "services": services,
        "message": (
            "All configured Azure services are communicating successfully."
            if aggregate_status == "connected"
            else (
                "Azure services are not configured; running in local mode."
                if aggregate_status == "not_configured"
                else f"Azure connectivity diagnostic status: {aggregate_status}."
            )
        ),
    }
