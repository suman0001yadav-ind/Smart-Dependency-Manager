
import json
import os
from collections import deque


class TaskManager:

    def __init__(self):
        self.graph = {}
        self.filename = "tasks.json"
        self.load_from_file()

    def save_to_file(self):
        with open(self.filename, "w") as file:
            json.dump(self.graph, file, indent=4)

    def load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.graph = json.load(file)
                print("Previous tasks loaded successfully!")
            except (json.JSONDecodeError, OSError):
                print("Could not load saved tasks.")
                self.graph = {}

    def add_task(self, task):
        if task in self.graph:
            print("This task already exists!")
            return

        self.graph[task] = []
        self.save_to_file()
        print("Task added successfully!")

    def has_path(self, start, destination):
        visited = set()
        stack = [start]

        while stack:
            current = stack.pop()

            if current == destination:
                return True

            if current not in visited:
                visited.add(current)
                stack.extend(self.graph.get(current, []))

        return False

    def add_dependency(self, prerequisite, task):
        if prerequisite not in self.graph or task not in self.graph:
            print("Both tasks must exist first.")
            return

        if prerequisite == task:
            print("A task cannot depend on itself!")
            return

        if task in self.graph[prerequisite]:
            print("This dependency already exists!")
            return

        if self.has_path(task, prerequisite):
            print("Cannot add dependency: circular dependency!")
            return

        self.graph[prerequisite].append(task)
        self.save_to_file()
        print("Dependency added successfully!")

    def remove_task(self, task):
        if task not in self.graph:
            print("Task not found!")
            return

        del self.graph[task]

        for dependencies in self.graph.values():
            if task in dependencies:
                dependencies.remove(task)

        self.save_to_file()
        print("Task removed successfully!")

    def remove_dependency(self, prerequisite, task):
        if prerequisite not in self.graph:
            print("Prerequisite task not found!")
            return

        if task not in self.graph[prerequisite]:
            print("Dependency not found!")
            return

        self.graph[prerequisite].remove(task)
        self.save_to_file()
        print("Dependency removed successfully!")

    def display_graph(self):
        if not self.graph:
            print("No tasks available.")
            return

        print("\nPROJECT TASK DEPENDENCIES")
        print("-" * 45)

        for task, dependencies in self.graph.items():
            print(f"{task} --> {dependencies}")

    # BFS: Kahn's Algorithm
    def topological_sort_bfs(self):
        indegree = {task: 0 for task in self.graph}

        for task in self.graph:
            for dependent in self.graph[task]:
                indegree[dependent] += 1

        queue = deque(
            task for task in indegree
            if indegree[task] == 0
        )

        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            for dependent in self.graph[current]:
                indegree[dependent] -= 1

                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(self.graph):
            return None

        return result

    # DFS: Depth First Search
    def topological_sort_dfs(self):
        visited = set()
        recursion_stack = set()
        result = []

        def dfs(task):
            visited.add(task)
            recursion_stack.add(task)

            for dependent in self.graph[task]:
                if dependent in recursion_stack:
                    return False

                if dependent not in visited:
                    if not dfs(dependent):
                        return False

            recursion_stack.remove(task)
            result.append(task)
            return True

        for task in self.graph:
            if task not in visited:
                if not dfs(task):
                    return None

        result.reverse()
        return result

    def has_cycle(self):
        return self.topological_sort_bfs() is None

    def display_execution_order(self, algorithm):
        if algorithm == "BFS":
            result = self.topological_sort_bfs()
        else:
            result = self.topological_sort_dfs()

        if result is None:
            print("ERROR: Circular dependency detected!")
            return

        print(f"\n{algorithm} EXECUTION ORDER")
        print("-" * 35)

        for number, task in enumerate(result, start=1):
            print(f"{number}. {task}")
