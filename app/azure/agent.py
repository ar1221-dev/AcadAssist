"""The ONE AcadAssist Agent Service.

Responsible for:
- Initializing and configuring the single 'AcadAssist' Foundry Agent
- Exact system prompt enforcement
- Binding all 11 tool contracts
- Handling the agent orchestration loop (send message, handle tool calls, feed tool outputs back, return grounded response)
- Preserving source citations and structured actions
- Graceful offline/test fallback when Azure cloud endpoints are unconfigured
"""

import json
import logging
from typing import Any, Dict, List, Optional

from config.settings import get_settings
from app.azure.foundry import FoundryProjectManager
from app.azure.tools import get_agent_tools
from app.azure.adapters import ToolDispatcher
from app.schemas.chat import ActionItem, ChatResponse, SourceItem

logger = logging.getLogger(__name__)

# EXACT system instructions required for AcadAssist Agent
ACADASSIST_SYSTEM_INSTRUCTIONS = (
    "You are AcadAssist, an AI academic study assistant. Your purpose is to help students understand their "
    "academic material, assess their learning, plan their studies, track their progress, and prepare for examinations.\n\n"
    "Use tools whenever information from the student's actual academic data is required.\n\n"
    "When answering questions about uploaded academic material, prefer retrieved knowledge-base content over unsupported general knowledge.\n\n"
    "Never invent a student's exam date, progress, quiz score, study history, course material, or weak topics. "
    "Use the appropriate tool to obtain this information.\n\n"
    "When creating study plans, consider upcoming exams, tests, weak topics, course progress, previous performance, and available study time.\n\n"
    "Do not modify persistent student data unless an appropriate tool explicitly allows the operation.\n\n"
    "Give concise, useful, student-friendly responses."
)


class AcadAssistAgentService:
    """Orchestration service for the ONE AcadAssist Agent."""

    def __init__(
        self,
        foundry_manager: Optional[FoundryProjectManager] = None,
        tool_dispatcher: Optional[ToolDispatcher] = None,
    ):
        self.settings = get_settings()
        self.foundry_manager = foundry_manager or FoundryProjectManager()
        self.tool_dispatcher = tool_dispatcher or ToolDispatcher()
        self.agent_name = self.settings.foundry_agent_name
        self.model_deployment = self.settings.foundry_model_deployment
        self.system_instructions = ACADASSIST_SYSTEM_INSTRUCTIONS
        self.tools = get_agent_tools()

    def chat(self, user_id: str, message: str) -> ChatResponse:
        """Execute chat interaction for a student through the AcadAssist Agent."""
        logger.info("Chat request received for user_id=%s, message='%s'", user_id, message)

        # If Microsoft Foundry cloud project is configured, run through Azure Foundry OpenAI client
        if self.foundry_manager.is_configured:
            return self._execute_cloud_agent(user_id, message)

        # Otherwise execute through local test orchestrator (deterministic demo/test mode)
        logger.info("Foundry cloud not configured; executing via local AcadAssist orchestrator")
        return self._execute_local_agent(user_id, message)

    def _execute_cloud_agent(self, user_id: str, message: str) -> ChatResponse:
        """Run agent interaction using Microsoft Foundry Project LLM deployment."""
        client = self.foundry_manager.get_openai_client()

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_instructions},
            {"role": "user", "content": f"[User ID: {user_id}] {message}"},
        ]

        collected_sources: List[SourceItem] = []
        collected_actions: List[ActionItem] = []

        # Maximum 5 tool-calling turns
        for _ in range(5):
            response = client.chat.completions.create(
                model=self.model_deployment,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message

            # Check if model requested tool calls
            if response_message.tool_calls:
                messages.append(response_message)
                for tool_call in response_message.tool_calls:
                    fn_name = tool_call.function.name
                    try:
                        fn_args = json.loads(tool_call.function.arguments)
                    except Exception:
                        fn_args = {}
                    # Guarantee user_id is injected
                    fn_args["user_id"] = user_id

                    tool_result = self.tool_dispatcher.dispatch(fn_name, fn_args)

                    if "sources" in tool_result and tool_result["sources"]:
                        collected_sources.extend(tool_result["sources"])

                    output_str = json.dumps(tool_result.get("output", {}))
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": fn_name,
                            "content": output_str,
                        }
                    )
            else:
                # Final response generated
                final_content = response_message.content or ""
                return ChatResponse(
                    message=final_content,
                    sources=collected_sources,
                    actions=collected_actions,
                )

        # Fallback if loop exceeded
        return ChatResponse(
            message="I completed processing your request using your course tools.",
            sources=collected_sources,
            actions=collected_actions,
        )

    def _execute_local_agent(self, user_id: str, message: str) -> ChatResponse:
        """Deterministic local agent execution for tests and offline development."""
        msg_lower = message.lower()
        collected_sources: List[SourceItem] = []
        collected_actions: List[ActionItem] = []

        # Knowledge retrieval intent
        if any(term in msg_lower for term in ["explain", "what is", "paging", "virtual memory", "concept", "lecture", "search"]):
            tool_res = self.tool_dispatcher.dispatch(
                "search_knowledge",
                {"user_id": user_id, "query": message, "top_k": 3},
            )
            if "sources" in tool_res:
                collected_sources.extend(tool_res["sources"])

            # Formulate grounded response based on retrieved knowledge
            chunks = tool_res.get("output", {}).get("results", [])
            if chunks:
                primary_chunk = chunks[0]
                answer = (
                    f"{primary_chunk['content']}\n\n"
                    f"**Source:** {primary_chunk['document_title']} ({primary_chunk['filename']}, "
                    f"Page {primary_chunk['page_number']})."
                )
            else:
                answer = f"I searched your knowledge base for '{message}' but found no relevant materials."

            return ChatResponse(
                message=answer,
                sources=collected_sources,
                actions=collected_actions,
            )

        # Quiz generation intent
        elif "quiz" in msg_lower or "practice" in msg_lower:
            topic = "Operating Systems Paging" if "paging" in msg_lower else "General Review"
            tool_res = self.tool_dispatcher.dispatch(
                "generate_quiz",
                {"user_id": user_id, "topic": topic, "count": 5},
            )
            quiz_data = tool_res.get("output", {})
            collected_actions.append(
                ActionItem(
                    type="quiz_generated",
                    description=f"Generated {quiz_data.get('question_count', 5)} practice questions on {topic}.",
                    payload=quiz_data,
                )
            )
            return ChatResponse(
                message=f"I have prepared a practice quiz on {topic} for you. Select your answers to test your knowledge.",
                sources=collected_sources,
                actions=collected_actions,
            )

        # Study plan or exam intent
        elif any(term in msg_lower for term in ["plan", "schedule", "exam", "today"]):
            exam_res = self.tool_dispatcher.dispatch("get_upcoming_exams", {"user_id": user_id})
            plan_res = self.tool_dispatcher.dispatch("get_today_plan", {"user_id": user_id})
            today_tasks = plan_res.get("output", {}).get("tasks", [])
            task_list = "\n".join(f"- {t['task']} ({t['duration_minutes']} mins)" for t in today_tasks)

            return ChatResponse(
                message=f"Here is your study plan for today:\n\n{task_list}\n\nKeep up the great work!",
                sources=collected_sources,
                actions=[ActionItem(type="study_plan_retrieved", description="Retrieved today's study plan", payload=plan_res.get("output", {}))],
            )

        # Default student-friendly response
        return ChatResponse(
            message=(
                f"Hello! I am AcadAssist, your AI study assistant. I can help you review your course materials, "
                f"take practice quizzes, and plan your study sessions for upcoming exams. What would you like to work on?"
            ),
            sources=collected_sources,
            actions=collected_actions,
        )
