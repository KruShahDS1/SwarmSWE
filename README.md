
![image](https://github.com/user-attachments/assets/6a2a6076-50fd-422b-8515-cf912e0cdcf7)

**AutoSWE with SWARM**
We are benchmarking the performance of automated software engineering against DevBench using SWARM AI for decision-making and task execution.
The 5 evaluations in DevBench serve as the primary nodes in the system. Progression to the next node is determined by hardcoded logic or SWARM AI agents in "approve_" prefixed nodes.<br>
**Tasks/Nodes** <br>
1.	Software Design
2.	Environment Setup
3.	Implementation
4.	Acceptance Testing
5.	Unit Testing <br>

**Control Flow.**
In this system, SWARM AI handles the orchestration and decision-making at every stage of the software development cycle. Decision nodes, prefixed with approve_, are powered by SWARM agents to ensure context-aware and adaptive control flow.<br>

**Key Features:** <br>
•	**SWARM Decision Nodes**: Multi-agent intelligence drives decisions at approved_ nodes, ensuring robust control flow.<br>
•	**Dynamic Execution:** Nodes are processed sequentially, with SWARM agents managing transitions based on task completion and input conditions.<br>
•	**Output Aggregation:** The system accumulates artifacts generated at each node into a final state for delivery.<br>

**Requirements**
1.	Obtain access to SWARM AI and its API keys.<br>
2.	Create a .env file to store your configuration (see .env.example).<br>
The .env file should include the following:<br>

**How to Use** <br>
Running a Custom PRD
To execute the program with a custom PRD.md file:
 
Running the Example PRD
To use the included example PRD.md file in the repo:
<br> 
________________________________________
**What is SWARM AI?** <br>
**SWARM AI** is a cutting-edge multi-agent framework designed for intelligent decision-making and task automation. <br>
In this project, SWARM agents:<br>
•	Analyze Tasks: Understand and process the requirements of each node.<br>
•	Drive Decisions: Use context and logic to determine the workflow at approve_ nodes.<br>
•	Adapt Dynamically: Respond to changes in input, task status, or conditions during execution. <br>
This enables autoSWE to go beyond static workflows, providing adaptability and scalability in software engineering tasks.<br>
________________________________________
**Outputs** <br>
The final state of the system includes all artifacts produced during the process, such as:<br>
•	Design Documentation <br>
•	Environment Configuration Files (e.g., .env) <br>
•	Source Code <br>
•	Test Results (Unit and Acceptance Testing) <br>
These outputs are saved in the specified output directory.
________________________________________
**Advantages of Using SWARM AI** <br>
•	Decentralized Decision-Making: SWARM agents collaborate to ensure robust, distributed task management.<br>
•	Dynamic Workflows: SWARM enables flexible transitions between nodes, eliminating rigid, predefined logic.<br>
•	Scalability: SWARM’s multi-agent architecture makes it ideal for handling complex and large-scale software engineering workflows.<br>
•	Efficiency: SWARM optimizes task execution by learning from context and improving with feedback.<br>
________________________________________
**Graph Visualization** <br>
Below is an example of how the control flow is managed by SWARM AI agents.
 
________________________________________
**Future Directions** <br>
This implementation can be extended to:
1.	Incorporate advanced SWARM learning algorithms to improve decision-making.
2.	Enable real-time visualization of the SWARM decision flow.
3.	Optimize node execution using parallel processing with SWARM agents.
Contact the development team or consult SWARM AI's documentation for more information.
