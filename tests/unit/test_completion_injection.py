import pytest
from src.ralph_orchestrator.adapters.base import ToolAdapter, ToolResponse

class MockAdapter(ToolAdapter):
    def check_availability(self) -> bool:
        return True
    
    def execute(self, prompt: str, **kwargs) -> ToolResponse:
        # No arguments passed here, relies on instance state
        enhanced = self._enhance_prompt_with_instructions(prompt)
        return ToolResponse(success=True, output=enhanced)

@pytest.fixture
def adapter():
    return MockAdapter("mock")

def test_injects_promise_from_state(adapter):
    prompt = "Do a task"
    promise = "LOOP_COMPLETE"
    
    # Configure state
    adapter.completion_promise = promise
    
    response = adapter.execute(prompt)
    
    assert "## Completion Promise" in response.output
    assert f"output this exact line:\n{promise}" in response.output

def test_skips_injection_when_present(adapter):
    promise = "LOOP_COMPLETE"
    adapter.completion_promise = promise
    
    prompt = f"Do a task\n\n## Completion Promise\noutput this exact line:\n{promise}"
    response = adapter.execute(prompt)
    
    # Should not appear twice
    assert response.output.count("## Completion Promise") == 1
    assert response.output.count(promise) == 1

def test_skips_injection_when_none(adapter):
    prompt = "Do a task"
    adapter.completion_promise = None
    response = adapter.execute(prompt)
    
    assert "## Completion Promise" not in response.output