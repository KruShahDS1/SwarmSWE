from swarm import Swarm, Agent, Node, StateGraph, Message
import logging
from swarm.workflow import Workflow
from swarm.message import SystemMessage
from swarm_models import OpenAI
from agents.design_agent import DesignAgent
from agents.setup_agent import SetupAgent
from agents.implementation_agent import ImplementationAgent
from agents.acceptance_agent import AcceptanceAgent
from agents.unit_test_agent import UnitTestAgent


# Hand-off functions (for agent routing)
def handoff_to_design_agent():
    """Transfer to the design agent for design queries."""
    print("Handing off to Design Agent")
    return design_agent


def handoff_to_setup_agent():
    """Transfer to the setup agent for setup queries."""
    print("Handing off to Setup Agent")
    return setup_agent


def handoff_to_acceptance_agent():
    """Transfer to the acceptance agent for acceptance queries."""
    print("Handing off to Acceptance Agent")
    return acceptance_agent


def handoff_to_unit_test_agent():
    """Transfer to the unit test agent for unit test queries."""
    print("Handing off to Unit Test Agent")
    return unit_test_agent


def handoff_to_implementation_agent():
    """Transfer to the implementation agent for implementation queries."""
    print("Handing off to Implementation Agent")
    return implementation_agent


# Initialize agents
setup_agent = Agent(
    name="Setup Agent",
    instructions="You handle only setup-related queries.",
    functions=[handoff_to_setup_agent]
)

design_agent = Agent(
    name="Design Agent",
    instructions="You handle only design-related queries.",
    functions=[handoff_to_design_agent]
)

acceptance_agent = Agent(
    name="Acceptance Agent",
    instructions="You handle only acceptance-related queries.",
    functions=[handoff_to_acceptance_agent]
)

unit_test_agent = Agent(
    name="UnitTest Agent",
    instructions="You handle only unit-tests-related queries.",
    functions=[handoff_to_unit_test_agent]
)

implementation_agent = Agent(
    name="Implementation Agent",
    instructions="You handle only implementation-related queries.",
    functions=[handoff_to_implementation_agent]
)

# Set logging level
logging.basicConfig(level=logging.INFO)


import os




# OpenAI LLM for model tasks
llm = OpenAI(model_name="gpt-4o", temperature=0)




# Assistant Workflow
class AssistantWorkflow(Workflow):
    def assistant(self, state: dict[str, Any]) -> dict[str, Any]:
        """The assistant helps to fix documents based on feedback."""
        logging.info("---ASSISTANT---")

        # Define system message
        sys_message = SystemMessage(
            content="Please fix the documents based on the reviewer's feedback. Use the tools available.")

        # Bind tools to the workflow (view, update, add, delete documents)
        self.bind_tools([self.view_document, self.update_document, self.add_document, self.delete_document])

        # Retrieve the last message
        last_message = state.get('messages', [])[-1] if 'messages' in state else None
        if not last_message:
            raise ValueError("No messages found in the state to process.")

        # Invoke the workflow with the system and last user message
        updated_message = self.invoke([sys_message, last_message])

        # Update the state with the new message
        state['messages'] = [updated_message]
        return state


# Build the workflow graph
def build_swarm_graph():
    # Create a state graph to manage the workflow
    graph = StateGraph()

    # Define nodes (tasks in the workflow)
    graph.add_node("software_design", Node(software_design))
    graph.add_node("approve_software_design", Node(approve_software_design))
    graph.add_node("environment_setup", Node(environment_setup))
    graph.add_node("implementation", Node(implementation))
    graph.add_node("approve_implementation", Node(approve_implementation))
    graph.add_node("acceptance_tests", Node(acceptance_tests))
    graph.add_node("approve_acceptance_tests", Node(approve_acceptance_tests))
    graph.add_node("unit_tests", Node(unit_tests))
    graph.add_node("approve_unit_tests", Node(approve_unit_tests))

    # Define edges (transitions between nodes)
    graph.add_edge("START", "software_design")
    graph.add_edge("software_design", "approve_software_design")
    graph.add_conditional_edges("approve_software_design", route_software_design)
    graph.add_edge("implementation", "approve_implementation")
    graph.add_conditional_edges("approve_implementation", route_implementation)
    graph.add_edge("acceptance_tests", "unit_tests")
    graph.add_edge("unit_tests", "approve_unit_tests")
    graph.add_edge("approve_unit_tests", "END")

    # Returning the compiled graph for execution
    return graph.compile()

def create_graph():
    """
    Creates a new graph for the workflow, integrating nodes and edges.
    This function is separate to allow for customization and extension.
    """
    # Build the workflow graph
    workflow_graph = build_swarm_graph()

    # You can log or manipulate the graph here if needed
    logging.info("Graph created successfully.")

    return workflow_graph