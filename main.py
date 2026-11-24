
from task_manager import TaskManager
from benchmark import measure_performance


def main():

    # Load previously saved tasks automatically
    manager = TaskManager()

    while True:

        print("\n" + "=" * 50)
        print("       SMART DEPENDENCY MANAGER")
        print("=" * 50)

        print("1. Add New Task")
        print("2. Add Task Dependency")
        print("3. Display All Tasks")
        print("4. Generate Execution Order (BFS)")
        print("5. Generate Execution Order (DFS)")
        print("6. Check Circular Dependencies")
        print("7. Compare Algorithm Performance")
        print("8. Remove Task")
        print("9. Remove Task Dependency")
        print("10. Exit")

        choice = input("\nEnter your choice (1-10): ").strip()

        if choice == "1":

            task = input("Enter task name: ").strip()

            if task:
                manager.add_task(task)
            else:
                print("Task name cannot be empty.")

        elif choice == "2":

            prerequisite = input("Enter prerequisite task: ").strip()
            task = input("Enter dependent task: ").strip()

            if prerequisite and task:
                manager.add_dependency(prerequisite, task)
            else:
                print("Task names cannot be empty.")

        elif choice == "3":

            manager.display_graph()

        elif choice == "4":

            manager.display_execution_order("BFS")

        elif choice == "5":

            manager.display_execution_order("DFS")

        elif choice == "6":

            if manager.has_cycle():
                print("Circular dependency detected!")
            else:
                print("No circular dependencies found.")

        elif choice == "7":

            measure_performance()

        elif choice == "8":

            task = input("Enter task name to remove: ").strip()
            manager.remove_task(task)

        elif choice == "9":

            prerequisite = input("Enter prerequisite task: ").strip()
            task = input("Enter dependent task: ").strip()

            manager.remove_dependency(prerequisite, task)

        elif choice == "10":

            print("Thank you for using Smart Dependency Manager!")
            break

        else:

            print("Invalid choice! Please enter 1 to 10.")


if __name__ == "__main__":
    main()
