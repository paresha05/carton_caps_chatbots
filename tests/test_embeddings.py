from embeddings import load_pdf_context

def test_pdf_context_nonempty():
    # a query that should match something
    snippet = load_pdf_context("referral bonus")
    assert isinstance(snippet, str)
    assert len(snippet) > 0
