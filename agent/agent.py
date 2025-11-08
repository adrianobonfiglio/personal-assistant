from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from google.cloud import texttospeech
import pygame
import json
import subprocess
from time import sleep
import speech_recognition as sr
from tool_management.todo import manage_todo_list
from config import LLM_GEMINI_API_KEY, TTS_GEMINI_API_KEY, SERPER_API_KEY
from urllib.parse import quote
from tools import get_search_results, get_user_preference


# Initialize the recognizer
r = sr.Recognizer()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=LLM_GEMINI_API_KEY)

def text_to_speech(text:str, language:str="en-US"):
    """Converts text to speech using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient(client_options={"api_key": TTS_GEMINI_API_KEY})

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language,
        model_name="gemini-2.5-pro-tts"

    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0,
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio content to a file
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    play_audio("output.mp3")

def play_audio(file_path: str):
    """Plays an audio file using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def recognize_audio(source, recognizer):
    """Listens for the wake word 'Hey Jarvis' and triggers the assistant."""
    text = audio_recognition(source, recognizer)
    print(f"You said: {text}")
    return text


def listen_to_user():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        print("Say something!")
        while True:
            # Listen for the user's input
            print("Listening...")
            text = recognize_audio(source, r)
            if(text is not None and text.lower().strip().startswith("jarvis")):
                text = text.lower().strip()
                open_assisent_page("loader")
                print("Listening sequence...")
                text = recognize_audio(source, r)
                text = text.lower().strip()
                if(text == "home"):
                    open_assisent_page("home")

                elif(text.startswith("play")):
                    text = text.replace("play", "")
                    text = quote(text)
                    open_assisent_page("youtube-music", text)

                else:
                    print("calling agent...")
                    execute_agent(text)

def open_assisent_page(page_name: str, params: str = None):
    command = f"open assistant://{page_name}"
    if params:
        command += f"/param={params}"
    print(f"--- Opening assistant page with command: {command} ---")
    subprocess.call(command, shell=True)


def audio_recognition(source, recognizer,timeout=4, phrase_time_limit=4):
    try:
        audio = r.listen(source, timeout, phrase_time_limit)
        return recognizer.recognize_google(audio)   
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def open_agent_ear(source, recognizer):
    text = audio_recognition(source, recognizer, 10, 10)
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
