# Simple todo list manager

def add_task(tasks, task):
    tasks.append(task)
    print(f"Task added: {task}")

def remove_task(tasks, index):
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        print(f"Task removed: {removed}")
    else:
        print("Invalid index")

def show_tasks(tasks):
    if not tasks:
        print("No tasks!")
    else:
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")

# Example usage
my_tasks = []
add_task(my_tasks, "Buy groceries")
add_task(my_tasks, "Walk the dog")
show_tasks(my_tasks)
