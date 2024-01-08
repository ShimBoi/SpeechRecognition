from vosk import Model, KaldiRecognizer
import pyaudio
from AppOpener import open, close

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
while True:
    data = stream.read(256)

    if recognizer.AcceptWaveform(data):
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
print("Done")
