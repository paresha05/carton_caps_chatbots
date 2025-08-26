"""
Test PDF context retrieval for Capper chatbot.
Ensures that semantic search returns non-empty results for valid queries.
"""

from embeddings import load_pdf_context


def test_pdf_context_nonempty():
    # a query that should match something
    snippet = load_pdf_context("referral bonus")
    assert isinstance(snippet, str)
    assert len(snippet) > 0
