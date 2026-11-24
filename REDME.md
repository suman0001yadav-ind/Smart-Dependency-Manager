
# Smart Dependency and Project Execution Manager

A Python-based project dependency management system that schedules tasks according to their dependencies using graph algorithms.

## Project Overview

This project represents tasks as vertices and dependencies as directed edges in a graph.

It implements two Topological Sorting algorithms:
- BFS (Kahn's Algorithm)
- DFS (Depth First Search)

The system detects circular dependencies, prevents invalid dependency creation, and compares the performance of both algorithms.

## Features

- Add new tasks
- Add dependencies between tasks
- Remove tasks and dependencies
- Display the task dependency graph
- Generate execution order using BFS
- Generate execution order using DFS
- Detect circular dependencies
- Prevent circular dependency creation
- Save and load tasks using JSON
- Compare algorithm execution times

## Technologies Used

- Python 3
- Graph Data Structure
- BFS (Kahn's Algorithm)
- DFS
- JSON
- Time module

## Project Structure

Smart-Dependency-Manager/
|
|-- main.py
|-- task_manager.py
|-- benchmark.py
|-- tasks.json
|-- README.md
|-- requirements.txt

## How to Run

1. Install Python 3.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run:

   py main.py

To run performance comparison:

   py benchmark.py

## Algorithms

### 1. BFS - Kahn's Algorithm

- Calculate the in-degree of every vertex.
- Add all zero in-degree vertices to a queue.
- Remove vertices from the queue and update their neighbors.
- If all vertices are processed, a valid topological order exists.
- Otherwise, a cycle exists.

### 2. DFS - Depth First Search

- Visit each vertex using recursion.
- Track visited vertices and the recursion stack.
- Detect a cycle if a vertex is encountered again in the recursion stack.
- Reverse the finishing order to obtain topological ordering.

## Complexity Analysis

Let:
- V = Number of vertices (tasks)
- E = Number of edges (dependencies)

| Algorithm | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |

## Performance Analysis

The benchmark tests graphs containing 100, 300, 500 and 1000 tasks.

Actual execution times depend on the computer, graph structure and Python environment.

Run `py benchmark.py` to generate your own results.

## Data Storage

The application stores tasks and dependencies in `tasks.json`.

Previously saved tasks are automatically loaded when the program starts.

## Author

Suman Kumar Yadav

BCA (AI & Data Science)
