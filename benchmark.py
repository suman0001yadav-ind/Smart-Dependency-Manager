
import time
import random
from task_manager import TaskManager

def generate_graph(number_of_tasks):

    manager = TaskManager()

    tasks = [
        f"Task-{i}" for i in range(number_of_tasks)
    ]

    for task in tasks:
        manager.add_task(task)

    # Generate a random DAG
    # Edges always go from a lower index to a higher index
    for i in range(number_of_tasks):
        for j in range(i + 1, number_of_tasks):

            if random.random() < 0.03:
                manager.add_dependency(
                    tasks[i], tasks[j]
                )

    return manager

def measure_performance():

    sizes = [100, 300, 500, 1000]

    print("\nALGORITHM PERFORMANCE ANALYSIS")
    print("=" * 65)

    print(
        f"{'Tasks':<12}"
        f"{'BFS Time (ms)':<20}"
        f"{'DFS Time (ms)':<20}"
    )

    print("-" * 65)

    for size in sizes:

        manager = generate_graph(size)

        # Measure BFS
        start = time.perf_counter()

        manager.topological_sort_bfs()

        bfs_time = (
            time.perf_counter() - start
        ) * 1000

        # Measure DFS
        start = time.perf_counter()

        manager.topological_sort_dfs()

        dfs_time = (
            time.perf_counter() - start
        ) * 1000

        print(
            f"{size:<12}"
            f"{bfs_time:<20.4f}"
            f"{dfs_time:<20.4f}"
        )

if __name__ == "__main__":
    measure_performance()