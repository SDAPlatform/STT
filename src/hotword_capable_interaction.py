import pyaudio
import wave
import whisper


i = 0
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "voice.wav"

p = pyaudio.PyAudio()
model = whisper.load_model("base")
print("* Waiting for hot word...")
while True:
        
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)



    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    #p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    audio = whisper.pad_or_trim(whisper.load_audio("voice.wav"))
    text = (whisper.transcribe(model, audio)["text"])
    if text.lower().__contains__("wake")  :
        print ("detected")
        stream.stop_stream()
        stream.close()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
        frames = []
        for i in range(0, int(RATE / CHUNK * 7)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        wf = wave.open("command.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        audio = whisper.pad_or_trim(whisper.load_audio("command.wav"))
        text = (whisper.transcribe(model, audio)["text"])
        print("command : " + text)