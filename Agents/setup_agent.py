from pydantic import BaseModel, Field
from typing import Literal
from swarm import Node, Message
import logging


class EnvironmentSetup(BaseModel):
    requirements_txt: str = Field(description="Content for the requirements.txt file based on the design")
    setup_message: str = Field(description="Message confirming that the environment has been set up")


class SetupAgent(BaseModel):
    def execute(self, design_output):
        """
        Execute the setup of the environment based on design output.
        """
        requirements: str = Field(
            description="All the expected dependencies that can be written to a file named requirements.txt")
        print("Setting up the environment...")
        return {"setup": "Development environment configured based on design"}


# Function to generate the requirements.txt content based on the design
@Node
def environment_setup(state: CurrentState):
    """
    Based on the design documents, determine the requirements.txt file.
    """
    logging.info("---ENVIRONMENT SETUP---")

    # Generate the prompt dynamically using the code from the design documents
    code = '\n'.join(state['documents']['code'].values())
    prompt = ENVIRONMENT_SETUP_PROMPT.format(code=code)  # Assuming ENVIRONMENT_SETUP_PROMPT is predefined

    # Invoke LLM to get the environment setup details
    structured_llm = llm.with_structured_output(EnvironmentSetup)
    reqs = structured_llm.invoke([HumanMessage(content=prompt)])

    # Update the state with the requirements and setup message
    state["documents"].update(reqs.dict())
    return state


# Function to approve the environment setup by testing the requirements.txt
@Node
def approve_environment_setup(state: CurrentState):
    """
    Test the requirements.txt file.
    A shell or script could be used to run the requirements file, but for now we mock the approval.
    """
    logging.info("---APPROVE ENVIRONMENT SETUP---")

    # For demonstration, we hardcode the approval of requirements (in real case, we would run a script to validate)
    state['approvals'].update({"requirements": True})

    return state


# Function to route the environment setup process based on approvals
@Node
def route_environment_setup(state: CurrentState) -> Literal['approve_acceptance_tests', 'environment_setup']:
    """
    Routes the process to the next step based on whether the environment setup has been approved.
    """
    if all(state["approvals"].values()):
        return "approve_acceptance_tests"
    else:
        return "environment_setup"


# Main flow for setting up the environment and routing based on approvals
@Node
def environment_setup_flow(state: CurrentState):
    """
    Full flow for environment setup, which includes setting up the environment and approving the setup.
    """
    # First, set up the environment by generating the requirements.txt content
    state = environment_setup(state)

    # Then, approve the environment setup by testing the requirements.txt (or mock the approval in this case)
    state = approve_environment_setup(state)

    # Finally, route to the next step based on approvals
    next_step = route_environment_setup(state)

    return next_step


# Usage of the Swarm-based environment setup flow
def process_environment_setup(state: CurrentState):
    """
    Starts the Swarm-based process for environment setup and routing.
    """
    # Invoke the full flow for environment setup and return the next step based on approvals
    next_step = environment_setup_flow(state)
    return next_step
