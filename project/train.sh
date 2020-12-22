cd Real-Time-Voice-Cloning
python3 encoder_preprocess.py librispeech_other \
&& python3 encoder_train.py my_run librispeech_other/SV2TTS/encoder \
&& python3 synthesizer_preprocess_audio.py librispeech_other --subfolders train-other-500 \
&& python3 synthesizer_preprocess_embeds.py librispeech_other/SV2TTS/synthesizer --n_processes 2 \
&& python3 synthesizer_train.py my_run librispeech_other/SV2TTS/synthesizer
#python3 vocoder_preprocess.py librispeech_other
#python3 vocoder_train.py my_run librispeech_other
