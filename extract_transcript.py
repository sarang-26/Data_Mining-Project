import whisper

#loading the model for coverting  speech to text
model = whisper.load_model("base")


#fucntion to convert speech to text

def speech_to_text(file):
    #loading the audio file
    audio = whisper.load_audio(file)
    #converting the speech to text
    text = whisper.convert_audio_to_text(model, audio)
    return text



