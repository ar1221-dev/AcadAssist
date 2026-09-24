"""Unit tests for the RAG module in AcadAssist."""

import unittest

from app.rag import (
    BaseAIProvider,
    BaseRetriever,
    ContextBuilder,
    MockAIProvider,
    MockRetriever,
    RAGPipeline,
    RetrievedChunk,
    SourceReference,
    StudyResponse,
)


class TestRAGModule(unittest.TestCase):
    """Test suite for RAG models, retriever, context builder, provider, and pipeline."""

    def setUp(self) -> None:
        self.retriever = MockRetriever()
        self.context_builder = ContextBuilder()
        self.provider = MockAIProvider()
        self.pipeline = RAGPipeline.create_mock_pipeline()

    # 1. Retriever Tests
    def test_retriever_relevant_retrieval(self) -> None:
        """Test retrieving relevant chunks using keyword overlap."""
        results = self.retriever.retrieve("What is supervised learning?", top_k=2)
        self.assertGreater(len(results), 0)
        top_match = results[0]
        self.assertEqual(top_match.chunk_id, "chunk_ml_01")
        self.assertIn("Supervised learning", top_match.content)
        self.assertEqual(top_match.source, "Introduction to Machine Learning.pdf")
        self.assertEqual(top_match.page, 12)
        self.assertGreater(top_match.score, 0.0)

    def test_retriever_empty_query(self) -> None:
        """Test that empty queries or whitespace return an empty list."""
        self.assertEqual(self.retriever.retrieve(""), [])
        self.assertEqual(self.retriever.retrieve("   "), [])
        self.assertEqual(self.retriever.retrieve("??? !!!"), [])

    def test_retriever_no_relevant_results(self) -> None:
        """Test that queries with zero token overlap return an empty list."""
        results = self.retriever.retrieve("photosynthesis chloroplast chlorophyll")
        self.assertEqual(results, [])

    def test_retriever_top_k_limit(self) -> None:
        """Test that top_k restricts the number of returned chunks."""
        results = self.retriever.retrieve("machine learning data", top_k=2)
        self.assertLessEqual(len(results), 2)

    def test_retriever_custom_corpus(self) -> None:
        """Test retriever with a custom injected corpus."""
        custom_corpus = [
            RetrievedChunk(
                chunk_id="custom_01",
                content="Custom biology notes on cellular mitosis.",
                source="Biology101.pdf",
                page=5,
            )
        ]
        retriever = MockRetriever(corpus=custom_corpus)
        results = retriever.retrieve("mitosis")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk_id, "custom_01")

    # 2. Context Builder Tests
    def test_context_construction(self) -> None:
        """Test building structured context from retrieved chunks."""
        chunks = [
            RetrievedChunk(
                chunk_id="c1",
                content="Passage one text.",
                source="BookA.pdf",
                page=10,
            ),
            RetrievedChunk(
                chunk_id="c2",
                content="Passage two text.",
                source="BookB.pdf",
                page=None,
            ),
        ]
        context = self.context_builder.build_context(chunks)
        self.assertIn("--- [Document Passage 1] (Source: BookA.pdf, Page: 10) ---", context)
        self.assertIn("Passage one text.", context)
        self.assertIn("--- [Document Passage 2] (Source: BookB.pdf) ---", context)
        self.assertIn("Passage two text.", context)

    def test_context_builder_empty(self) -> None:
        """Test building context when no chunks are provided."""
        context = self.context_builder.build_context([])
        self.assertEqual(context, "")

    # 3. AI Provider Tests
    def test_mock_provider_with_context(self) -> None:
        """Test mock AI provider produces grounded answer when context is provided."""
        context = "--- [Document Passage 1] (Source: BookA.pdf) ---\nMachine learning is a subset of AI."
        answer = self.provider.generate_response("What is ML?", context)
        self.assertIn("Machine learning is a subset of AI", answer)
        self.assertIn("What is ML?", answer)

    def test_mock_provider_empty_context(self) -> None:
        """Test mock AI provider returns insufficient material notice when context is empty."""
        empty_answer = self.provider.generate_response("What is quantum computing?", "")
        self.assertEqual(empty_answer, MockAIProvider.INSUFFICIENT_MATERIAL_MESSAGE)
        whitespace_answer = self.provider.generate_response("What is quantum computing?", "   \n  ")
        self.assertEqual(whitespace_answer, MockAIProvider.INSUFFICIENT_MATERIAL_MESSAGE)

    # 4. End-to-End Pipeline & Source Mapping Tests
    def test_pipeline_end_to_end_success(self) -> None:
        """Test complete end-to-end RAG pipeline for an answerable academic query."""
        response = self.pipeline.run("What is supervised learning?", top_k=2)

        self.assertIsInstance(response, StudyResponse)
        self.assertEqual(response.question, "What is supervised learning?")
        self.assertIn("Supervised learning is a machine learning paradigm", response.answer)
        self.assertGreater(len(response.sources), 0)
        self.assertTrue(response.context_used)
        self.assertEqual(response.confidence, 1.0)

        # Verify source reference properties
        top_source = response.sources[0]
        self.assertIsInstance(top_source, SourceReference)
        self.assertEqual(top_source.source, "Introduction to Machine Learning.pdf")
        self.assertEqual(top_source.page, 12)
        self.assertEqual(top_source.chunk_id, "chunk_ml_01")
        self.assertTrue(top_source.snippet.startswith("Supervised learning"))

    def test_pipeline_end_to_end_no_context(self) -> None:
        """Test pipeline behavior when query has no matching materials."""
        response = self.pipeline.run("Explain quantum superposition and entanglement")

        self.assertIsInstance(response, StudyResponse)
        self.assertEqual(response.answer, MockAIProvider.INSUFFICIENT_MATERIAL_MESSAGE)
        self.assertEqual(response.sources, [])
        self.assertEqual(response.context_used, "")
        self.assertEqual(response.confidence, 0.0)

    def test_source_reference_deduplication(self) -> None:
        """Test source references deduplication when multiple chunks share source and page."""
        chunks = [
            RetrievedChunk(
                chunk_id="c1",
                content="First chunk.",
                source="DocA.pdf",
                page=5,
            ),
            RetrievedChunk(
                chunk_id="c1",
                content="Duplicate chunk.",
                source="DocA.pdf",
                page=5,
            ),
        ]
        sources = self.pipeline._create_source_references(chunks)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].chunk_id, "c1")


if __name__ == "__main__":
    unittest.main()
