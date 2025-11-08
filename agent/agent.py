from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import speech_recognition as sr
from tool_management.todo import manage_todo_list
from config import LLM_GEMINI_API_KEY
from urllib.parse import quote
from tools import get_search_results, get_user_preference
from speech import start_recognition, text_to_speech, audio_recognition
from assitant_ui import open_assisent_page


# Initialize the recognizer
r = sr.Recognizer()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=LLM_GEMINI_API_KEY)

def listen_to_user():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        print("Say something!")
        while True:
            # Listen for the user's input
            print("Listening...")
            text = audio_recognition(source, r)
            if(text is not None and text.lower().strip().startswith("jarvis")):
                text = text.lower().strip()
                open_assisent_page("loader")
                print("Listening sequence...")
                text = start_recognition(source, r)
                if(text is not None and text == "home"):
                    open_assisent_page("home")

                elif(text is not None and text.lower().strip().startswith("play")):
                    text = text.replace("play", "")
                    text = quote(text)
                    open_assisent_page("youtube-music", text)

                elif(text is not None):
                    print("calling agent...")
                    execute_agent(text)

agent = create_agent(
    model=llm,
    system_prompt="""
    #CONTEXT:
    You are a helpful assistant, that always knows the current user's name and responds accordingly.
    You always sumarize the response and try to keep it short, no additional information is needed only the answer in simple text.

    #TOOLS:
    - get_user_preference: Use this tool to get the current user's preferences including the name of the user
    - get_search_results: Use this tool to get search results for a given query.
    - manage_todo_list: Use this tool to add, remove or list to-do items.

    #INSTRUCTIONS:
    - if no additional information is provided assume user's preferences to respond
    - Try to find the answer and use the tools only if necessary
    - Reply uing JSON format as follows:
    {"text": "your response here", "language": "language code here (e.g., en-US, pt-BR)"}
    """,
    tools=[get_user_preference, get_search_results, manage_todo_list]
)

def execute_agent(query: str = None):
    print(f"--- Executing agent with query: {query} ---")
    llm_response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    result = json.loads(llm_response["messages"][-1].content[0]['text'])
    
    ## If the respone requires opening a specific page in the assistant UI
    open_assisent_page("second")
    
    text_to_speech(result['text'], result['language'])
    # Continue to listen to user after end of agent execution
    listen_to_user()

# Start listening to user
listen_to_user()
