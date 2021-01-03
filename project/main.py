# CONSTANTS BEGIN

TEXT = "Companies like Google and Facebook scramble to define the future of work as COVID-19 lingers"

SAMPLE_IN = 'data/1.wav'
SAMPLE_OUT = 'out/1.wav'

LIB_DIR = 'Real-Time-Voice-Cloning'

MODEL_ENCODER = f'{LIB_DIR}/encoder/saved_models/pretrained.pt'
MODEL_VOCODER = f'{LIB_DIR}/vocoder/saved_models/pretrained/pretrained.pt'
MODEL_SYNTESIZER = f'{LIB_DIR}/synthesizer/saved_models/logs-pretrained/taco_pretrained'

# LOCALLY TRAINED MODELS
# MODEL_SYNTESIZER = f'{LIB_DIR}/synthesizer/saved_models/logs-my_run/taco_pretrained'
# MODEL_VOCODER = f'{LIB_DIR}/vocoder/saved_models/my_run/my_run.pt'

# CONSTANTS END

import os
import sys
import numpy as np
import scipy.io.wavfile as wf
from pathlib import Path

sys.path.insert(0, LIB_DIR)

from encoder import inference as encoder
from vocoder import inference as vocoder
from synthesizer.inference import Synthesizer

encoder.load_model(Path(MODEL_ENCODER))
vocoder.load_model(Path(MODEL_VOCODER))
synthesizer = Synthesizer(Path(MODEL_SYNTESIZER))

data, rate = encoder.preprocess_wav(Path(SAMPLE_IN))
embed = encoder.embed_utterance(data)
specs = synthesizer.synthesize_spectrograms([TEXT], [embed])
data = vocoder.infer_waveform(specs[0])

wf.write(SAMPLE_OUT, rate, data)
