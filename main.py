import sys
sys.path.append('C:\\Users\\npsom\\anaconda3\\Lib\\site-packages')
import swarm
from swarm import Swarm, Agent
help(swarm)  # Lists all the modules, classes, and functions in swarm
from Agents.Agent.py import *  # Assuming all agents are imported from the Agents module
import openai
import json
import os
from dotenv import load_dotenv
import logging
from prompts import * # Assuming these contain the prompts for design
import argparse

# set logging level
logging.basicConfig(level=logging.INFO)


def main():
    """
    Main entry point to invoke the SWEGraph.
    """
    parser = argparse.ArgumentParser(description="Run the SWEGraph with a specified PRD.")
    parser.add_argument("--prd_path", type=str, default="PRD.md", help="Path to the PRD file")
    parser.add_argument("--out_path", type=str, default="output.json", help="Path to the output file")
    args = parser.parse_args()

    # Load the PRD content
    if args.prd_path is None:
        prd_content = SAMPLE_PRD  # Fallback to sample PRD content if no file is provided
    else:
        with open(args.prd_path, 'r', encoding="utf-8") as prd_file:
            prd_content = prd_file.read()

    # Initialize the Swarm framework
    swarm_object: Swarm()
    # Call BuildSwarmGraph() to set up the agent graph
    logging.info("Building the Swarm graph...")
    build_graph = build_swarm_graph()  # Assuming BuildSwarmGraph is available in Agent.py
    build_graph.create_graph()  # Assuming this is how it works


    # Start the process by handing off to the Design Agent with the PRD content
    logging.info("Handing off to Design Agent with PRD content.")
    design_agent = handoff_to_design_agent()  # This assumes this function is defined in Agent.py
    design_agent_response = design_agent.handle_prd(prd_content)  # Assuming there's a method in the agent for handling PRD

    # If design is successful, pass it to setup agent or other agents depending on your flow
    if design_agent_response["status"] == "approved":
        logging.info("Design approved. Handing off to Setup Agent.")
        setup_agent = handoff_to_setup_agent()
        setup_agent_response = setup_agent.handle_setup(design_agent_response["design"])

        # You can now proceed with more agent handoffs or complete the workflow
        if setup_agent_response["status"] == "setup_complete":
            logging.info("Setup completed. Handing off to Implementation Agent.")
            implementation_agent = handoff_to_implementation_agent()
            implementation_agent_response = implementation_agent.handle_implementation(setup_agent_response["setup"])

            # After implementation, move to acceptance agent
            if implementation_agent_response["status"] == "implemented":
                logging.info("Implementation successful. Handing off to Acceptance Agent.")
                acceptance_agent = handoff_to_acceptance_agent()
                acceptance_agent_response = acceptance_agent.handle_acceptance(implementation_agent_response["implementation"])

                # After acceptance, handoff to unit test agent
                if acceptance_agent_response["status"] == "accepted":
                    logging.info("Acceptance successful. Handing off to Unit Test Agent.")
                    unit_test_agent = handoff_to_unit_test_agent()
                    unit_test_agent_response = unit_test_agent.handle_unit_test(acceptance_agent_response["accepted"])

                    # At this point, save the final state
                    if unit_test_agent_response["status"] == "unit_test_passed":
                        logging.info("Unit tests passed. Workflow complete.")
                        final_state = unit_test_agent_response
                    else:
                        logging.error("Unit tests failed.")
                        final_state = unit_test_agent_response

    # Save the final state to a JSON file
    with open(args.out_path, 'w') as file:
        json.dump(final_state, file, indent=4)


if __name__ == "__main__":
    load_dotenv(dotenv_path=".env", override=True)
    # Provide a default value if SWARM_PROJECT is not set
    project_name = os.environ.get("SWARM_PROJECT", "default_project_name")
    logging.info("Project Name: %s", project_name)
    logging.info('Tracing Enabled: %s', str(utils.tracing_is_enabled()))
    main()
