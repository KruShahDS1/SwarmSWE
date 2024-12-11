from pydantic import BaseModel, Field
from typing import Union, Literal, Any
from Agents.prompts import *
from utils import SwarmState
import logging


class Implementation(BaseModel):
    code: str = Field(description="Code for the implemented core functionality")
    implementation_message: str = Field(description="Message confirming the implementation has been completed")


class ApproveImplementation(BaseModel):
    implementation: bool
    message: str


class ImplementationAgent(BaseModel):
    def execute(self, setup_output):
        """
        Execute the implementation process based on the setup output.
        """
        print("Executing implementation...")
        return {"implementation": "Core functionality implemented based on setup"}


# Node to implement the software design
@Node
def implementation_node(state: SwarmState, IMPLEMENTATION_PROMPT=None):
    """
    Implement the software design based on the setup output and design documents.
    """
    logging.info("---IMPLEMENTATION---")

    # Generate the prompt dynamically based on the current design documents
    prompt = [HumanMessage(content=IMPLEMENTATION_PROMPT.format(**state["documents"]))]

    # If there is already a rejection for implementation, add the last message from the controller
    if 'implementation' in state['approvals']:
        if not state['approvals']['implementation']:
            prompt.append(state['messages'][-1])  # add the last rejection message

    # Invoke LLM to get the implementation details
    structured_llm = llm.with_structured_output(Implementation)
    code = structured_llm.invoke(prompt)

    # Update the state with the generated code
    state["messages"].append(prompt)
    state['documents'].update(code.dict())

    return state


# Node to approve the implementation
@Node
def approve_implementation(state: SwarmState):
    """
    Approve the implementation by reviewing the generated code.
    """
    logging.info("---APPROVE IMPLEMENTATION---")

    # Generate the approval prompt based on the architecture design and the generated code
    prompt = APPROVE_IMPLEMENTATION_PROMPT.format(architecture_design=state["documents"]['architecture_design'],
                                                  code=list(state["documents"]['code'].keys()))

    # Send the approval prompt to the LLM
    state['messages'].append(HumanMessage(content=prompt))

    # Invoke LLM to get the approval message and decision
    structured_llm = llm.with_structured_output(ApproveImplementation)
    approval = structured_llm.invoke([HumanMessage(content=prompt)])

    # Update the state with approval status
    state['approvals'].update({"implementation": approval.implementation})
    state['messages'].append(AIMessage(content=approval.message))

    return state


# Node to route to the next step based on implementation approval

def route_implementation(state: SwarmState) -> Literal['acceptance_tests', 'implementation']:
    """
    Routes the process to the next step based on whether the implementation has been approved.
    """
    if all(state["approvals"].values()):
        return "acceptance_tests"
    else:
        return "implementation"


# Node to handle the implementation workflow

def implementation_flow(state: SwarmState):
    """
    Full flow for implementing and approving the software design.
    """
    # First, implement the design based on the setup
    state = implementation_node(state)

    # Then, approve the implementation based on the generated code
    state = approve_implementation(state)

    # Finally, route to the next step based on the approval status
    next_step = route_implementation(state)

    return next_step


# Main function to initiate the implementation workflow
def process_implementation(state: SwarmState):
    """
    Starts the Swarm-based process for implementing and routing the implementation approval.
    """
    # Invoke the full implementation flow and return the next step
    next_step = implementation_flow(state)
    return next_step
