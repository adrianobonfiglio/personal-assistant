from google.cloud import texttospeech
import pygame
import speech_recognition as sr
from config import TTS_GEMINI_API_KEY
from assitant_ui import open_assisent_page

# Initialize the recognizer
r = sr.Recognizer()

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
    """Listens for the wake word 'jarvis' and triggers the assistant."""
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
                return text.strip()