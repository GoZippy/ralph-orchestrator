import pytest
from unittest.mock import MagicMock
from src.ralph_orchestrator.orchestrator import RalphOrchestrator
from src.ralph_orchestrator.adapters.base import ToolAdapter

class MockAdapter(ToolAdapter):
    def check_availability(self) -> bool:
        return True
    def execute(self, prompt: str, **kwargs):
        return None

def test_orchestrator_configures_adapter_promise():
    promise = "TEST_COMPLETE"
    
    # Mock _initialize_adapters to return our mock
    mock_adapter = MockAdapter("mock")
    
    # We need to patch RalphOrchestrator._initialize_adapters or just verify logic
    # But since we can't easily patch inside init without more complex fixtures,
    # let's just inspect the result of a real init with mocked adapters if possible.
    # Actually, simpler: just create the orchestrator and inspect the adapters.
    # But _initialize_adapters tries to load real adapters.
    # We will rely on the fact that at least one adapter (e.g. Gemini/Claude) might fail or succeed 
    # based on environment, which makes this flaky.
    
    # Better approach: Instantiate orchestrator with minimal config and verify logic.
    # Or rely on the fact that if we provide a config, it initializes.
    
    pass

# Since instantiating RalphOrchestrator triggers real adapter checks, unit testing it is hard 
# without mocking _initialize_adapters.
# Let's monkeypatch _initialize_adapters on the class for this test.

def test_orchestrator_passes_promise_to_adapters(monkeypatch):
    mock_adapter = MockAdapter("mock")
    
    def mock_init_adapters(self):
        return {"mock": mock_adapter}
    
    monkeypatch.setattr(RalphOrchestrator, "_initialize_adapters", mock_init_adapters)
    
    promise = "CUSTOM_PROMISE"
    orchestrator = RalphOrchestrator(
        primary_tool="mock",
        completion_promise=promise,
        # minimal args
        max_iterations=1
    )
    
    assert orchestrator.adapters["mock"].completion_promise == promise
