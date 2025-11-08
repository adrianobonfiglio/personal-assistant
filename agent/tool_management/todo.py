from langchain.tools import tool

@tool
def manage_todo_list(action: str, item: str = None) -> str:
    """Manages a todo list by actions: add, remove, list. and the item"""
    print(f"--- Invoking to-do tool with item: {item} and action: {action}---")
    action = action.lower().strip()
    if action == "add":
        return add_todo(item)
    elif action == "remove":
        return remove_todo(item)
    elif action == "list":
        return list_todos()
    else:
        return "Invalid action. Please use 'add', 'remove', or 'list'."

def add_todo(item: str) -> str:
    """Add a todo item to the list."""
    print(f"--- Invoking add_todo tool with item: {item} ---")
    return f'Todo item "{item}" added and will be save in the database.'

def remove_todo(item: str) -> str:
    """Remove a todo item from the list."""
    print(f"--- Invoking remove_todo tool with item: {item} ---")
    return f'Todo item "{item}" removed.'

def list_todos() -> str:
    """List all todo items."""
    print(f"--- Invoking list_todos tool ---")
    return "Here are your todo items: 1. Buy groceries 2. Call Alice 3. Finish the report."