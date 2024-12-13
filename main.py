import os
import webbrowser
import pyttsx3
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import json
import pygame  # Importing pygame for playing songs

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set speech rate
engine.setProperty("rate", 195)

# Path to the Vosk model directory
model_path = r"E:\Python\Codes\Mega_project_jervise\modles\vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(
        "Please download a model from https://alphacephei.com/vosk/models and unpack it to the 'modles' folder."
    )
    exit(1)

# Path to the folder containing your songs
songs_folder = r"E:\Python\Codes\Mega_project_jervise\songs"  # Set your songs folder here

# Load Vosk model
vosk_model = Model(model_path)

# Initialize pygame mixer for playing music
pygame.mixer.init()

# Text-to-speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to play music from the songs folder
def play_song(song_name):
    # Construct the full path for the song file
    song_path = os.path.join(songs_folder, song_name + ".mp3")  # Assuming your songs are in .mp3 format
    
    if os.path.exists(song_path):
        # Stop any currently playing music
        pygame.mixer.music.stop()
        
        # Load and play the song
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        speak(f"Playing {song_name}")
    else:
        speak(f"Sorry, I couldn't find the song {song_name}")

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()
    speak("Music stopped.")

# Command processing function
def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open github" in command.lower():
        webbrowser.open("https://www.github.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ", 1)[1]  # Get the song name after "play"
        play_song(song)  # Play the song
    elif "stop playing" in command.lower():
        stop_music()  # Stop playing music

if __name__ == "__main__":
    speak("Initializing Luna...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("Listening for wake word 'Luna'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

                # Use Google API for detecting wake word "Luna"
                word = recognizer.recognize_google(audio)

                if word.lower() == "luna":
                    speak("Yes, how can I help?")

                    # Switch to Vosk for offline command recognition
                    print("Luna is active and listening for your command...")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                        # Convert speech audio to a Vosk recognizer object
                        recognizer_vosk = KaldiRecognizer(vosk_model, source.SAMPLE_RATE)

                        if recognizer_vosk.AcceptWaveform(audio.get_wav_data()):
                            result = recognizer_vosk.Result()
                            result_json = json.loads(result)  # Parse the JSON safely
                            command_text = result_json.get("text", "")  # Extract the recognized text

                            if command_text:
                                print(f"Recognized command: {command_text}")
                                speak(f"You said: {command_text}")
                                processCommand(command_text)
                            else:
                                print("No recognizable command detected.")
                                speak("Sorry, I didn't understand the command.")

        except Exception as e:
            print(f"Error: {e}")
