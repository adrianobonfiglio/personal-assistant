from google.cloud import texttospeech
import pygame
from speech_recognition import UnknownValueError, RequestError
from config import TTS_GEMINI_API_KEY

def audio_recognition(source, recognizer,timeout=5, phrase_time_limit=3):
    try:
        audio = recognizer.listen(source, timeout, phrase_time_limit)
        return recognizer.recognize_google(audio)   
    except UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except RequestError as e:
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

def start_recognition(source, recognizer):
    text = audio_recognition(source, recognizer, timeout=10, phrase_time_limit=10)
    print(f"You said: {text}")
    return text