from vosk import Model, KaldiRecognizer
import pyaudio
from AppOpener import open, close
from gtts import gTTS
from playsound import playsound
import os
import pyautogui
import time

def speak(text):
    # Create a gTTS object
    tts = gTTS(text)
    # Save the speech to a temporary file
    temp_file = "temp_audio.mp3"
    tts.save(temp_file)
    # Play the audio file
    playsound(temp_file)
    # Delete the temporary file
    os.remove(temp_file)

#speak("Hello, this is a test.")

def program(hotkeys, appname):
    try:
        open(appname)
    except FileNotFoundError:
        print(f"Application '{appname}' not found.")
        return

    time.sleep(2)

    for key in hotkeys:
        pyautogui.keyDown(key)
    for key in reversed(hotkeys):
        pyautogui.keyUp(key)

program(["alt", "tab"], "discord")

def strtoarr(input_str):
    key_mapping = {
        'alt': 'alt','control': 'ctrl','ctrl': 'ctrl','delete': 'del','see': 'c',  'be' : 'b', 
        'bee': 'b', 'tee': 't', 'queue' : 'q', 'are':'r', 'why':'y', 'you':'u', 'pee':'p', 'jay':'j', 'out':'alt'
    }
    
    words = input_str.split()
    mapped_words = []
    for word in words:
        normalized_word = word.lower()
        if normalized_word in key_mapping:
            mapped_words.append(key_mapping[normalized_word])
        else:
            mapped_words.append(word)
    return mapped_words

# create a model from the model directory
directory = "vosk-model-small-en-us-0.15"
model = Model(directory)

# recognizer object does the actual speech recognition
recognizer = KaldiRecognizer(model, 16000)

# use the mic object to get audio
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=256)
stream.start_stream()

# loop through the stream and get the audio
print("Listening...")
text = ""
new = False

while True:
    data = stream.read(256)

    if recognizer.AcceptWaveform(data):
        if not new:
            text = recognizer.Result()[14:-3]
            print(text)

            if "open" in text:
                # extract the name of the app to open
                nameOfApp = ', '.join(text.split("open")[1:]).strip()
                open(nameOfApp)
            
            if "close" in text:
                # extract the name of the app to close
                nameOfApp = ', '.join(text.split("close")[1:]).strip()
                close(nameOfApp)

            if text == "exit":
                break

            if "activate new hotkey instructions" in text or "activate new hot key instructions" in text:
                new = True
                print("which buttons")
        else:
            print("which buttons")
            text = recognizer.Result()[14:-3]
            print(text)    
            program(strtoarr(text), "")
            new = False


print("Done")


