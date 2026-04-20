import requests
import io
import pygame
import config
import logging

logger = logging.getLogger("slovio")

def get_speech_recognition():
    try:
        import speech_recognition as sr
        return sr
    except ImportError:
        return None

def get_pyttsx3():
    try:
        import pyttsx3
        return pyttsx3
    except ImportError:
        return None

def listen():
    sr = get_speech_recognition()
    if not sr:
        logger.warning("Speech recognition library not found.")
        return None
    
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                text = r.recognize_google(audio)
                return text.lower()
            except Exception:
                return None
    except Exception as e:
        logger.warning(f"Microphone or speech source not available: {e}")
        return None

def listen_for_wake_word():
    while True:
        text = listen()
        if text and config.WAKE_WORD.lower() in text:
            return True

def speak(text):
    if config.VOICE_ENGINE == "pyttsx3":
        pyttsx3 = get_pyttsx3()
        if not pyttsx3:
            logger.warning("pyttsx3 library not found. Speech disabled.")
            return
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logger.warning(f"pyttsx3 initialization failed: {e}")
    elif config.VOICE_ENGINE == "elevenlabs":
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config.ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            play_audio(response.content)

def play_audio(audio_bytes):
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
