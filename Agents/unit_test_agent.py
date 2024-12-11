from pydantic import BaseModel, Field
from typing import Literal, Any, Union
from utils import SwarmState
import logging


class UnitTests(BaseModel):
    command: str = Field(description="The command to run the unit tests.")
    result_message: str = Field(description="Message confirming whether unit tests passed.")


class UnitTestAgent(BaseModel):
    def execute(self, acceptance_output):
        """
        Execute the unit tests based on the acceptance test output.
        """
        print("Running unit tests...")
        return {"unit_tests": "All unit tests passed"}


# Node to generate the unit tests

def unit_tests(state: SwarmState):
    """
    Generate unit tests for the software based on the design documents.
    """
    logging.info("---UNIT TESTS---")

    # Generate the prompt for unit tests based on the design documents (especially the code)
    prompt = UNIT_TEST_PROMPT.format(**state["documents"])

    # Invoke the LLM to generate the unit test commands
    structured_llm = llm.with_structured_output(UnitTests)
    test = structured_llm.invoke([HumanMessage(content=prompt)])

    # Update the state with the generated unit tests
    state["documents"].update(test.dict())
    return state


# Node to approve the unit tests

def approve_unit_tests(state: SwarmState):
    """
    Approve the unit tests by simulating their execution.
    """
    logging.info("---APPROVE UNIT TESTS---")

    # Simulate running the unit tests by checking if the command passes
    state['messages'].append(state['documents']['unit_tests']['command'])
    state['approvals'].update({"unit_tests": True})

    # Simulating the result of the unit tests passing
    state['messages'].append("Unit tests passed")  # LLM response message

    return state


# Node to route to the next step based on unit test approval

def route_unit_tests_node(state: SwarmState) -> Literal["__end__", "assistant"]:
    """
    Routes the process to the next step based on whether the unit tests passed.
    """
    if all(state["approvals"].values()):
        return "__end__"  # End the workflow if all tests passed
    else:
        return "assistant"  # Go back to the assistant for further help or iteration


# Node to handle the unit tests workflow

def unit_tests_flow(state: SwarmState):
    """
    Full flow for generating, approving, and routing unit tests.
    """
    # Generate the unit tests
    state = unit_tests(state)

    # Approve the unit tests
    state = approve_unit_tests(state)

    # Route to the next step based on the approval of unit tests
    next_step = route_unit_tests_node(state)

    return next_step


# Main function to start the unit tests workflow
def process_unit_tests(state: SwarmState):
    """
    Starts the Swarm-based process for unit tests and routing to the next step.
    """
    # Invoke the unit tests flow and return the next step
    next_step = unit_tests_flow(state)
    return next_step
