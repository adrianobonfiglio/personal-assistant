from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from config import SERPER_API_KEY
from tool_management import todo


@tool
def get_search_results(query: str):
    """Returns search results for a given query. This tool needs to be used when the user asks for information that requires web search."""
    print(f"--- Invoking get_search_results tool with query: {query} ---")
    search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
    return search.run(query)
    # search = DuckDuckGoSearchRun()
    # return search.invoke(query)

@tool
def get_user_preference():
    """Returns the current user's preferences, including language, topics of interest, location, etc."""
    print("--- Invoking get_user_preference tool ---")
    return {
        "language": "Portuguese",
        "topics_of_interest": ["technology", "science", "artificial intelligence", "jogo do Grêmio"],
        "location": "Exton, PA",
        "temperature_unit": "Celsius",
        "distance_unit": "kilometers"
    }

@tool
def manage_todo_list(action: str, item: str = None) -> str:
    """Manages a todo list by actions: add, remove, list. and the item"""
    print(f"--- Invoking to-do tool with item: {item} and action: {action}---")
    action = action.lower().strip()
    if action == "add":
        return todo.add_todo(item)
    elif action == "remove":
        return todo.remove_todo(item)
    elif action == "list":
        return todo.list_todos()
    else:
        return "Invalid action. Please use 'add', 'remove', or 'list'."