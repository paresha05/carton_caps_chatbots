import pytest
from graph import build_graph

@pytest.mark.asyncio
async def test_graph_flow(sample_user):
    workflow = build_graph()
    state = {
        "user_id": sample_user,
        "input": "Tell me about referral program"
    }
    result = workflow.invoke(state)
    assert "response" in result
    assert isinstance(result["response"], str)
