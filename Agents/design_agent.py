from pydantic import BaseModel, Field
from typing import Union, Literal, Any
from software_workflow import SoftwareDesignWorkflow
import logging
from swarm import Node, Message


class DesignAgent(BaseModel):
    UML_class: str = Field(description="UML class diagram using mermaid syntax")
    UML_sequence: str = Field(description="UML sequence diagram using mermaid syntax")
    architecture_design: str = Field(description="architecture design as a text-based representation of the file tree")

    def execute(self, prd_content):
        """
        Example: Extract design details from the PRD.
        In the Swarm framework, this could be broken into separate nodes if needed.
        """
        print("Executing Software Design...")
        return {"design": "Basic architecture created based on PRD"}

    @Node
    def generate_design_node(self, prd_content: str):
        """
        Generates a design based on the PRD content.
        """
        return self.execute(prd_content)


# Function to handle software design process using Swarm nodes
def software_design(state: CurrentState):
    """
    Designs the markdown files for the software design using Swarm, including prompt handling.
    """
    logging.info("---SOFTWARE DESIGN (Swarm-based with prompt)---")

    # If there are approvals, check if all are True, otherwise invoke assistant to handle rejection cases
    @Node
    def approval_check_node(state: CurrentState):
        if "approvals" in state:
            if not all(state['approvals'].values()):  # Rejection case
                assistant(state)
        return state

    # Generate the prompt dynamically based on state
    @Node
    def prompt_generation_node(state: CurrentState) -> str:
        prompt = DESIGN_PROMPT.format(**state['documents'])  # Assuming DESIGN_PROMPT is pre-defined or imported
        return prompt

    # Structured LLM node to invoke and process the prompt
    @Node
    def structured_llm_node(state: CurrentState, prompt: str):
        structured_llm = llm.with_structured_output(Design)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        return response

    # Define the processing flow with Swarm
    @Node
    def software_design_flow(state: CurrentState):
        state = approval_check_node(state)  # Perform approval check first
        prompt = prompt_generation_node(state)  # Generate the design prompt
        response = structured_llm_node(state, prompt)  # Invoke the structured LLM with the prompt
        state["documents"].update(response.dict())  # Update the state with the generated design
        return state

    # Start the swarm node execution
    result = software_design_flow(state)
    return result


# Function to determine the next step for software design using Swarm nodes
def software_design_condition(state: Union[list[Any], dict[str, Any], BaseModel], messages_key: str = "messages") -> \
Literal["tools", "approve_software_design"]:
    """
    Determines the next step for software design based on the last AI message.
    In Swarm format.
    """
    @Node
    def get_last_message_node(state: Union[list[Any], dict[str, Any], BaseModel], messages_key: str):
        """
        Retrieves the last AI message from the input state.
        """
        ai_message = self.get_last_message(state, messages_key)
        if not ai_message:
            raise ValueError(f"No messages found in input state: {state}")
        return ai_message

    @Node
    def determine_route_node(ai_message):
        """
        Determines the next step (route) based on the AI message content.
        """
        return self.determine_route(ai_message, "approve_software_design")

    # Start the Swarm processing flow
    @Node
    def software_design_condition_flow(state: Union[list[Any], dict[str, Any], BaseModel], messages_key: str):
        """
        Process the state to determine the software design condition route.
        """
        ai_message = get_last_message_node(state, messages_key)  # Retrieve the last message
        next_step = determine_route_node(ai_message)  # Determine the next step
        return next_step

    # Invoke the processing flow and return the result
    result = software_design_condition_flow(state, messages_key)
    return result

-------------------------------------------------------------------------------------------------------------------------------------------------

class ApproveDesign(BaseModel):
    UML_class: bool
    UML_sequence: bool
    architecture_design: bool
    message: str


# Function to approve software design using Swarm nodes
@Node
def approve_software_design_node(state: CurrentState):
    """
    LLM-as-a-judge to review the design documents.
    This will check the design's validity and append the approval details.
    """
    logging.info("---APPROVE SOFTWARE DESIGN---")

    # Generate the prompt dynamically from the design documents
    prompt = APPROVE_DESIGN_PROMPT.format(**state['documents'])

    # Structured LLM that processes the prompt and outputs the approval
    structured_llm = llm.with_structured_output(ApproveDesign)
    approval = structured_llm.invoke([HumanMessage(content=prompt)])

    # Update the approvals in the state based on the approval response
    state['approvals'] = {
        "UML_class": approval.UML_class,
        "UML_sequence": approval.UML_sequence,
        "architecture_design": approval.architecture_design
    }

    # Append the approval message to the state messages
    state['messages'].append(approval.message)
    return state


# Function to route the software design process based on approvals
@Node
def route_software_design_node(state: CurrentState) -> Literal['implementation', 'software_design']:
    """
    Routes to the next step based on the approval status.
    If all approvals are True, route to implementation. Otherwise, return to software design.
    """
    if all(state["approvals"].values()):
        return "implementation"
    else:
        return "software_design"


# Main software design flow with Swarm nodes
@Node
def software_design_flow(state: CurrentState):
    """
    The main flow that will invoke the approve_software_design_node and route_software_design_node.
    """
    # First, approve the software design
    state = approve_software_design_node(state)

    # Then, route the software design based on approvals
    next_step = route_software_design_node(state)

    return next_step


# Usage of the Swarm-based software design flow
def process_software_design(state: CurrentState):
    """
    Starts the Swarm-based process for reviewing and routing the software design.
    """
    # Invoke the full flow of approving the design and routing the next step
    next_step = software_design_flow(state)
    return next_step
