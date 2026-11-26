from flask import Flask, jsonify, render_template, request
from task_manager import TaskManager
import random
import time

app = Flask(__name__)
manager = TaskManager()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/graph")
def get_graph():
    return jsonify({"graph": manager.graph})


@app.post("/api/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()
    if not task:
        return jsonify({"error": "Please enter a task name."}), 400
    if task in manager.graph:
        return jsonify({"error": "This task already exists."}), 409
    manager.add_task(task)
    return jsonify({"message": f"Task '{task}' added.", "graph": manager.graph})


@app.delete("/api/tasks/<path:task>")
def delete_task(task):
    if task not in manager.graph:
        return jsonify({"error": "Task not found."}), 404
    manager.remove_task(task)
    return jsonify({"message": f"Task '{task}' removed.", "graph": manager.graph})


@app.post("/api/dependencies")
def add_dependency():
    data = request.get_json(silent=True) or {}
    prerequisite = str(data.get("prerequisite", "")).strip()
    dependent = str(data.get("dependent", "")).strip()

    if not prerequisite or not dependent:
        return jsonify({"error": "Choose both tasks."}), 400
    if prerequisite not in manager.graph or dependent not in manager.graph:
        return jsonify({"error": "Both tasks must exist first."}), 404
    if prerequisite == dependent:
        return jsonify({"error": "A task cannot depend on itself."}), 400
    if dependent in manager.graph[prerequisite]:
        return jsonify({"error": "This dependency already exists."}), 409
    if manager.has_path(dependent, prerequisite):
        return jsonify({"error": "Circular dependency rejected. This connection would create a cycle."}), 400

    manager.graph[prerequisite].append(dependent)
    manager.save_to_file()
    return jsonify({"message": f"{prerequisite} → {dependent} dependency added.", "graph": manager.graph})


@app.delete("/api/dependencies")
def delete_dependency():
    data = request.get_json(silent=True) or {}
    prerequisite = str(data.get("prerequisite", "")).strip()
    dependent = str(data.get("dependent", "")).strip()
    if prerequisite not in manager.graph or dependent not in manager.graph[prerequisite]:
        return jsonify({"error": "Dependency not found."}), 404
    manager.remove_dependency(prerequisite, dependent)
    return jsonify({"message": "Dependency removed.", "graph": manager.graph})


@app.get("/api/order/<algorithm>")
def get_order(algorithm):
    algorithm = algorithm.lower()
    if algorithm == "bfs":
        result = manager.topological_sort_bfs()
    elif algorithm == "dfs":
        result = manager.topological_sort_dfs()
    else:
        return jsonify({"error": "Unknown algorithm."}), 404

    if result is None:
        return jsonify({"error": "A circular dependency exists. A valid execution order cannot be generated."}), 400
    return jsonify({"algorithm": algorithm.upper(), "order": result})


@app.get("/api/cycle")
def check_cycle():
    return jsonify({"has_cycle": manager.has_cycle()})


@app.get("/api/benchmark")
def benchmark():
    sizes = [100, 300, 500, 1000]
    rows = []
    random.seed(42)

    for size in sizes:
        tasks = [f"Task-{i}" for i in range(size)]
        graph = {task: [] for task in tasks}
        # Generate the same directed acyclic graph for both algorithms.
        for i in range(size):
            for j in range(i + 1, size):
                if random.random() < 0.01:
                    graph[tasks[i]].append(tasks[j])

        test_manager = TaskManager()
        test_manager.graph = graph

        start = time.perf_counter()
        test_manager.topological_sort_bfs()
        bfs_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        test_manager.topological_sort_dfs()
        dfs_ms = (time.perf_counter() - start) * 1000

        rows.append({"tasks": size, "bfs": round(bfs_ms, 4), "dfs": round(dfs_ms, 4)})

    return jsonify({"results": rows})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
