import swarm
from swarm import Swarm, Agent
from Agents.tools import *
import logging
from Agents.prompts import *
from Agents.design_agent import *
from Agents.implementation_agent import *
from Agents.setup_agent import *
from Agents.software_workflow import *
from Agents.acceptance_agent import *
from Agents.unit_test_agent import *
import os
import openai as OpenAI


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






# OpenAI LLM for model tasks
llm = OpenAI(model_name="gpt-4o", temperature=0)




# Assistant Workflow
from typing import Any, Callable, List, Dict
import logging

class AssistantWorkflow:
    def __init__(self):
        # Tools available in the workflow
        self.tools: List[Callable] = []

    def bind_tools(self, tools: List[Callable]) -> None:
        """Bind tools to the workflow."""
        self.tools = tools

    def invoke(self, messages: List[dict]) -> dict:
        """Simulate invoking a workflow using system and user messages."""
        # Example processing logic (this can be customized for specific use cases)
        response_content = f"Processed: {messages[-1]['content']}"
        return {"role": "assistant", "content": response_content}

    def assistant(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """The assistant helps to fix documents based on feedback."""
        logging.info("---ASSISTANT---")

        # Define system message
        sys_message = {"role": "system", "content": "Please fix the documents based on the reviewer's feedback. Use the tools available."}

        # Bind tools to the workflow (view, update, add, delete documents)
        self.bind_tools([self.view_document, self.update_document, self.add_document, self.delete_document])

        # Retrieve the last message
        last_message = state.get("messages", [])[-1] if "messages" in state and state["messages"] else None
        if not last_message:
            raise ValueError("No messages found in the state to process.")

        # Invoke the workflow with the system and last user message
        updated_message = self.invoke([sys_message, last_message])

        # Update the state with the new message
        state["messages"] = state.get("messages", []) + [updated_message]
        return state


class WorkflowGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_name, task_function):
        """Add a node to the workflow."""
        self.nodes[node_name] = task_function
        self.edges[node_name] = []

    def add_edge(self, from_node, to_node):
        """Add a directed edge between two nodes."""
        if from_node in self.nodes and to_node in self.nodes:
            self.edges[from_node].append(to_node)
        else:
            raise ValueError("Both nodes must exist in the graph.")

    def execute(self, start_node, context):
        """Execute the workflow starting from a given node."""
        if start_node not in self.nodes:
            raise ValueError(f"Start node {start_node} does not exist in the graph.")

        current_node = start_node
        while current_node:
            task_function = self.nodes[current_node]
            print(f"Executing task: {current_node}")
            next_node = task_function(context, self.edges[current_node])
            current_node = next_node if next_node in self.nodes else None

    def compile(self):
        """Validate and prepare the workflow graph."""
        # Check for unreachable nodes and cycles using Depth-First Search (DFS)
        visited = set()
        visiting = set()
        all_nodes = set(self.nodes.keys())
        start_nodes = all_nodes - {n for edges in self.edges.values() for n in edges}
        unreachable_nodes = all_nodes.copy()

        def dfs(node):
            if node in visited:
                return True  # Already processed
            if node in visiting:
                raise ValueError("Cycle detected in the graph.")  # Cycle found

            visiting.add(node)
            unreachable_nodes.discard(node)

            for neighbor in self.edges[node]:
                dfs(neighbor)

            visiting.remove(node)
            visited.add(node)

        # Process all start nodes
        if not start_nodes:
            raise ValueError("No start nodes detected. The graph may contain a cycle.")

        for start_node in start_nodes:
            dfs(start_node)

        # Check for any remaining unreachable nodes
        if unreachable_nodes:
            raise ValueError(f"Unreachable nodes detected: {unreachable_nodes}")

        print("Workflow graph compiled successfully.")


## Define a generic Task class for workflow nodes
class Task:
    def __init__(self, name, function):
        self.name = name
        self.function = function

# Build the workflow graph
def build_swarm_graph(from_node=None):
    # Create a state graph to manage the workflow
    graph = WorkflowGraph()

    # Define tasks (nodes in the workflow)
    graph.add_node("software_design", Task("software_design", software_design))
    graph.add_node("approve_software_design", Task("approve_software_design", approve_software_design))
    graph.add_node("environment_setup", Task("environment_setup", environment_setup))
    graph.add_node("implementation", Task("implementation", implementation_node))
    graph.add_node("approve_implementation", Task("approve_implementation", approve_implementation))
    graph.add_node("acceptance_tests", Task("acceptance_tests", acceptance_tests))
    graph.add_node("approve_acceptance_tests", Task("approve_acceptance_tests", approve_acceptance_tests))
    graph.add_node("unit_tests", Task("unit_tests", unit_tests))
    graph.add_node("approve_unit_tests", Task("approve_unit_tests", approve_unit_tests))

    # Define edges (transitions between tasks)
    graph.add_edge("START", "software_design")
    graph.add_edge("software_design", "approve_software_design")
    graph.add_edge("approve_software_design", "route_software_design")
    graph.add_edge("implementation", "approve_implementation")
    graph.add_edge("approve_implementation", "route_implementation")
    graph.add_edge("acceptance_tests", "unit_test s")
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