from typing import Union, Literal, Any
from pydantic import BaseModel


from typing import Any, Union, Dict, List, Literal

class SoftwareDesignWorkflow:
    @staticmethod
    def get_last_message(state: Union[List[Any], Dict[str, Any]], messages_key: str) -> Any:
        """Retrieve the last message from the state."""
        if isinstance(state, list):
            # If the state is a list, return the last element
            return state[-1] if state else None
        elif isinstance(state, dict):
            # If the state is a dictionary, extract the messages using the key
            messages = state.get(messages_key, [])
            return messages[-1] if messages else None
        else:
            raise ValueError("Invalid state structure. State must be a list or a dictionary.")

    @staticmethod
    def determine_route(ai_message: Dict[str, Any], approve_route: str) -> Literal['tools', str]:
        """Determine the next route based on tool calls."""
        if "tool_calls" in ai_message and len(ai_message["tool_calls"]) > 0:
            return "tools"
        return approve_route


# Example Usage
if __name__ == "__main__":
    # Example state and AI message
    example_state = {
        "messages": [
            {"content": "Initial feedback", "tool_calls": []},
            {"content": "Additional input", "tool_calls": [{"tool_name": "document_viewer"}]},
        ]
    }

    example_ai_message = {"content": "AI processed input", "tool_calls": [{"tool_name": "document_editor"}]}

    # Retrieve last message
    last_message = SoftwareDesignWorkflow.get_last_message(example_state, "messages")
    print("Last message:", last_message)

    # Determine route
    next_route = SoftwareDesignWorkflow.determine_route(example_ai_message, "approve_route")
    print("Next route:", next_route)



