"""
Unit and integration test suite for Task 1: Knowledge Brain.
"""
import unittest
import json
from app.database import db
from retrieval.chunker import chunker
from retrieval.embedder import embedder
from retrieval.vector_store import vector_store
from multimodal.image_analyzer import image_analyzer

class TestTask1KnowledgeBrain(unittest.TestCase):
    def test_database_counts(self):
        counts = db.get_counts()
        self.assertGreater(counts["active_articles"], 0)
        self.assertGreater(counts["total_chunks"], 0)

    def test_semantic_chunker(self):
        sample_article = {
            "url": "https://example.com/test-article",
            "title": "Test Integration Article",
            "category": "Testing",
            "folder": "Integration",
            "clean_text": "## Heading A\nThis is section A content.\n\n## Heading B\nThis is section B content.",
            "sections": [
                {"heading": "Heading A", "content": "This is section A content."},
                {"heading": "Heading B", "content": "This is section B content."}
            ]
        }
        chunks = chunker.chunk_article(sample_article)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertIn("Article: Test Integration Article", chunks[0]["text"])
        self.assertIn("Heading A", chunks[0]["text"])

    def test_embedder_normalization(self):
        vec = embedder.embed_text("Stripe payment gateway integration")
        self.assertEqual(len(vec), 384)
        norm_sq = sum(x * x for x in vec)
        self.assertAlmostEqual(norm_sq, 1.0, places=2)

    def test_hybrid_retrieval(self):
        results = vector_store.search("How to setup Stripe webhook?", top_k=3)
        self.assertGreater(len(results), 0)
        top_result = results[0]
        self.assertIn("stripe", top_result["article_url"].lower())
        self.assertGreater(top_result["relevance_score"], 0.40)

    def test_multimodal_screenshot_analysis(self):
        analysis = image_analyzer.analyze_screenshot(
            image_url="https://example.com/test.png",
            alt_text="Stripe API keys and webhook settings panel",
            context_text="Enter publishable key and toggle test mode switch.",
            article_title="Stripe Setup"
        )
        self.assertIn("image_url", analysis)
        self.assertIn("ui_elements", analysis)
        self.assertLessEqual(analysis["uncertainty_score"], 0.5)

    def test_escalation_feedback_loop(self):
        # 1. Create escalation
        esc_id = db.create_escalation(
            question="Can Brilliant Directories integrate with Custom Web3 Wallets?",
            context="User requested Solana wallet connection",
            user_id="test_user_01"
        )
        self.assertIsNotNone(esc_id)

        # 2. Resolve escalation with human expert answer
        expert_answer = "Brilliant Directories does not natively support Web3/Solana wallets out of the box. However, custom JavaScript can be injected into Settings > Design Settings > Custom Scripts to load Phantom wallet SDK."
        success = db.resolve_escalation(esc_id, expert_answer)
        self.assertTrue(success)

        # 3. Verify in escalations list
        open_esc = db.get_escalations(status="resolved")
        matched = [e for e in open_esc if e["id"] == esc_id]
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["expert_answer"], expert_answer)

    def test_article_deactivation(self):
        test_url = "https://support.brilliantdirectories.com/support/solutions/test-temp-page"
        db.upsert_article(
            url=test_url,
            title="Temporary Deprecated Page",
            category="Temp",
            folder="Deprecated",
            content_hash="temp_hash_1",
            raw_html="<p>Deprecated</p>",
            clean_text="Deprecated text"
        )
        # Verify active
        chunks = db.get_all_active_chunks()
        active_urls = {c["article_url"] for c in chunks}
        
        # Deactivate
        db.deactivate_article(test_url)
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM articles WHERE url = ?", (test_url,))
            status = cursor.fetchone()[0]
            self.assertEqual(status, "deactivated")

if __name__ == "__main__":
    unittest.main()
