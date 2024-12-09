from typing import Union, Literal, Any
from pydantic import BaseModel
from swarm.workflow import Workflow

class SoftwareDesignWorkflow(Workflow):
    @staticmethod
    def get_last_message(state: Union[list[Any], dict[str, Any], BaseModel], messages_key: str):
        """Retrieve the last message from the state."""
        if isinstance(state, list):
            return state[-1]
        elif isinstance(state, dict):
            messages = state.get(messages_key, [])
            return messages[-1] if messages else None
        elif hasattr(state, messages_key):
            messages = getattr(state, messages_key, [])
            return messages[-1] if messages else None
        raise ValueError("Invalid state structure")

    @staticmethod
    def determine_route(ai_message: Any, approve_route: str) -> Literal["tools", str]:
        """Determine the next route based on tool calls."""
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return approve_route


