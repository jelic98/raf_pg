rm -rf Real-Time-Voice-Cloning
git clone -q --recursive https://github.com/jelic98/Real-Time-Voice-Cloning.git
cd Real-Time-Voice-Cloning
pip install -q -r requirements.txt
pip install -q gdown
apt-get install -qq libportaudio2
pip install -q https://github.com/tugstugi/dl-colab-notebooks/archive/colab_utils.zip
gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc && unzip pretrained.zip
cd ..
python main.py
