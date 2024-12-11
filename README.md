# AutoSWE with SWARM AI


![Alt Text](C:\SwarmSWE\assets\Devbench_workflow.png "Devbench workflow")





## Overview
AutoSWE benchmarks the performance of automated software engineering against DevBench using SWARM AI for decision-making and task execution. The DevBench evaluation criteria serve as the primary nodes, with SWARM AI agents orchestrating decision-making and task progression.

### Tasks/Nodes
- **Software Design**
- **Environment Setup**
- **Implementation**
- **Acceptance Testing**
- **Unit Testing**

## What is SWARM AI?
SWARM AI is a cutting-edge multi-agent framework for intelligent decision-making and task automation. SWARM agents analyze tasks, drive decisions, and adapt dynamically to changing conditions. This ensures adaptability and scalability in automated software engineering tasks.

### Control Flow
SWARM AI handles orchestration and decision-making at each stage of the software development cycle. Decision nodes (prefixed with `approve_`) use SWARM agents to ensure context-aware and adaptive control flow.

### Key Features
- **SWARM Decision Nodes:** Multi-agent intelligence ensures robust control flow.
- **Dynamic Execution:** Sequential node processing with SWARM-driven transitions based on task completion and conditions.
- **Output Aggregation:** Artifacts generated at each node are accumulated into a final deliverable state.

## Requirements

1. **SWARM AI Access:** Obtain access to SWARM AI and its API keys.
2. **Configuration File:** Create a `.env` file to store configuration values. Refer to `.env.example` for guidance.

### Example `.env` File
```plaintext
SWARM_API_KEY=your_api_key_here
OUTPUT_DIR=path_to_output_directory
```

## Project Directory Structure
```plaintext
SwarmSWE/
├── Agents/                   # Contains SWARM AI agent modules
│   ├── Agent.py              # Base class for SWARM agents
│   ├── design_agent.py       # Agent for software design tasks
│   |── implementation_agent.py # Agent for implementation tasks  
│   └── acceptance_agent.py   # Agent for acceptance testing tasks
|   |── unit_test_Agent.py    # Agent for unit testing tasks
├── Output/                   # Directory for generated artifacts
├── assets/                   # Assets used in the project
├── benchmark_data/python/    # Benchmark data for testing
├── README.md                 # Project documentation
├── eval.py                   # Evaluation script for analyzing results
├── eval_collect.py           # Collects evaluation metrics
├── eval_config.yml           # Configuration file for evaluation settings
├── eval_report.py            # Generates evaluation reports
├── main.py                   # Invokes the main function to start execution
├── prd.md                    # Product Requirements Document
├── prompts.py                # Handles prompts and interactions
├── requirements.txt          # Python dependencies
```

## Python Files

### `main.py`
- Entry point for invoking the main function to start the workflow.

### `eval.py`
- Contains evaluation logic to analyze performance.

### `eval_collect.py`
- Collects metrics and results for comprehensive analysis.

### `eval_report.py`
- Generates reports based on evaluation metrics.

### `prompts.py`
- Handles user prompts and input management.

### `Agents/Agent.py`
- Defines the base class for SWARM agents, providing core functionalities like task registration and communication.



## How to Use

### Running a Custom PRD
To execute the program with a custom `prd.md` file:
```bash
python main.py --prd_path path_to_custom_prd.md
```

### Running the Example PRD
To use the included example `prd.md`:
```bash
python main.py
```

## Outputs
The system generates the following outputs in the specified output directory:
- **Design Documentation**
- **Environment Configuration Files (e.g., `.env`)**
- **Source Code**
- **Test Results (Unit and Acceptance Testing)**

## Advantages of Using SWARM AI
- **Decentralized Decision-Making:** Robust and distributed task management.
- **Dynamic Workflows:** Flexible transitions between nodes.
- **Scalability:** Ideal for handling complex and large-scale workflows.
- **Efficiency:** Context-aware learning improves execution with feedback.

## Future Directions
- Incorporate advanced SWARM learning algorithms for enhanced decision-making.
- Enable real-time visualization of SWARM decision flow.
- Optimize node execution using parallel processing with SWARM agents.

## Environment Setup
To set up the environment:
1. Clone the repository:
    ```bash
    git clone https://github.com/KruShahDS1/SwarmSWE.git
    cd SwarmSWE
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure the `.env` file:
    - Copy `.env.example` to `.env`.
    - Add the necessary API keys and configurations.


