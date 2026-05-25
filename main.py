import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
from google import genai
import os
from dotenv import load_dotenv


load_dotenv()
# Init recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init("sapi5")  # force Windows driver
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  
engine.setProperty("rate", 170)

def speak(text):
    if not text:
        text = "Sorry, I couldn't generate a response."
    print("AI:", text)
    # Break long text into sentences so pyttsx3 can handle it
    for part in text.split(". "):
        engine.say(part)
    engine.runAndWait()


client = genai.Client()
def aiprocess(command):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=command
        )
        return response.text
    except Exception as e:
        return f"AI service is busy right now. Please try again later. Error: {e}"

def ProcessCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open x" in c:
        webbrowser.open("https://x.com")
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in musiclibrary.music:
            webbrowser.open(musiclibrary.music[song])
        else:
            speak("Song not found")
    else:
        ai = aiprocess(c)
        speak(ai)
if __name__ == "__main__":
    speak("Initializing Jack...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Say 'Jack' for activation...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)

            if word.lower() == "jack":
                speak("Yes")

                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                ProcessCommand(command)

        except Exception as e:
            print("Error:", e)
