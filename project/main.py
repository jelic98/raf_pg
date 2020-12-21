import os
import sys
import numpy as np
from pathlib import Path
from os.path import exists, join, basename, splitext
from encoder import inference as encoder
from synthesizer import inference as synthesizer
from vocoder import inference as vocoder

encoder.load_model(Path('encoder/saved_models/pretrained.pt'))
vocoder.load_model(Path('vocoder/saved_models/pretrained/pretrained.pt'))
synthesizer = Synthesizer(Path('synthesizer/saved_models/logs-pretrained/taco_pretrained'))

RATE = 44100
embedding = None

def compute_embedding(audio):
    global embedding
    display(Audio(audio, rate=RATE, autoplay=True))
    embedding = encoder.embed_utterance(encoder.preprocess_wav(audio, RATE))

def click_record(button):
    clear_output()
    audio = record_audio(duration, sample_rate=RATE)
    compute_embedding(audio)

def click_upload(button):
    clear_output()
    audio = upload_audio(sample_rate=RATE)
    compute_embedding(audio)

if source == "Record":
    button = widgets.Button(description="Record your voice")
    button.on_click(click_record)
    display(button)
else:
    button = widgets.Button(description="Upload voice file")
    button.on_click(click_upload)
    display(button)

text = "Companies scramble to define the future of work as COVID-19 lingers"
specs = synthesizer.synthesize_spectrograms([text], [embedding])
generated_wav = vocoder.infer_waveform(specs[0])
generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
clear_output()
display(Audio(generated_wav, rate=synthesizer.sample_rate, autoplay=True))
