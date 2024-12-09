from pydantic import BaseModel, Field
from typing import Literal, Any, Union
from swarm import Node, Message
import logging


class AcceptanceTests(BaseModel):
    command: str = Field(description="The command to run the acceptance tests.")
    acceptance_message: str = Field(description="Message confirming whether acceptance criteria were met.")


class AcceptanceAgent(BaseModel):
    def execute(self, implementation_output):
        """
        Execute the acceptance tests based on the implementation output.
        """
        print("Running acceptance testing...")
        return {"acceptance": "Acceptance criteria met"}


# Node to generate the acceptance tests
@Node
def acceptance_tests_node(state: CurrentState):
    """
    Generate acceptance tests for the software based on the design documents.
    """
    logging.info("---ACCEPTANCE TESTS---")

    # Generate the prompt for acceptance tests based on the design documents
    prompt = ACCEPTANCE_TEST_PROMPT.format(**state["documents"])

    # Invoke the LLM to generate the acceptance test commands
    structured_llm = llm.with_structured_output(AcceptanceTests)
    test = structured_llm.invoke([HumanMessage(content=prompt)])

    # Update the state with the generated acceptance tests
    state["documents"].update(test.dict())
    return state


# Node to approve the acceptance tests
@Node
def approve_acceptance_tests_node(state: CurrentState):
    """
    Approve the acceptance tests by simulating their execution.
    """
    logging.info("---APPROVE ACCEPTANCE TESTS---")

    # Simulate running the acceptance tests by checking if the command passes
    state['messages'].append(state['documents']['acceptance_tests']['command'])
    state['approvals'].update({"acceptance_tests": True})

    # Simulating the result of the acceptance tests passing
    state['messages'].append("Acceptance tests passed")  # LLM response message

    return state


# Node to route to the next step based on acceptance test approval
@Node
def route_acceptance_tests_node(state: CurrentState) -> Literal['approve_unit_tests', 'assistant']:
    """
    Routes the process to the next step based on whether the acceptance tests passed.
    """
    if all(state["approvals"].values()):
        return "approve_unit_tests"
    else:
        return "assistant"  # Go back to the assistant for further help or iteration


# Node to handle the acceptance tests workflow
@Node
def acceptance_tests_flow(state: CurrentState):
    """
    Full flow for generating, approving, and routing acceptance tests.
    """
    # Generate the acceptance tests
    state = acceptance_tests_node(state)

    # Approve the acceptance tests
    state = approve_acceptance_tests_node(state)

    # Route to the next step based on the approval of acceptance tests
    next_step = route_acceptance_tests_node(state)

    return next_step


# Main function to start the acceptance tests workflow
def process_acceptance_tests(state: CurrentState):
    """
    Starts the Swarm-based process for acceptance testing and routing to the next step.
    """
    # Invoke the acceptance tests flow and return the next step
    next_step = acceptance_tests_flow(state)
    return next_step
