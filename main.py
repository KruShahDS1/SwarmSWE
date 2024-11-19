import json
from agents.design_agent import DesignAgent
from agents.setup_agent import SetupAgent
from agents.implementation_agent import ImplementationAgent
from agents.acceptance_agent import AcceptanceAgent
from agents.unit_test_agent import UnitTestAgent

def main(prd_path, output_path):
    # Load the PRD
    with open(prd_path, "r") as prd_file:
        prd_content = prd_file.read()

    # Initialize SWARM agents
    design_agent = DesignAgent()
    setup_agent = SetupAgent()
    implementation_agent = ImplementationAgent()
    acceptance_agent = AcceptanceAgent()
    unit_test_agent = UnitTestAgent()

    # Execute the workflow
    results = {}
    results['Software Design'] = design_agent.execute(prd_content)
    results['Environment Setup'] = setup_agent.execute(results['Software Design'])
    results['Implementation'] = implementation_agent.execute(results['Environment Setup'])
    results['Acceptance Testing'] = acceptance_agent.execute(results['Implementation'])
    results['Unit Testing'] = unit_test_agent.execute(results['Acceptance Testing'])

    # Save results
    with open(output_path, "w") as output_file:
        json.dump(results, output_file, indent=4)

    print("Development cycle completed. Results saved to", output_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Software Development Cycle using SWARM agents")
    parser.add_argument("--prd_path", type=str, required=True, help="Path to the PRD.md file")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save output results")

    args = parser.parse_args()
    main(args.prd_path, args.output_path)
