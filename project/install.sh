rm -rf Real-Time-Voice-Cloning
git clone git@github.com:jelic98/Real-Time-Voice-Cloning.git
cd Real-Time-Voice-Cloning
pip install -q -r requirements.txt
pip install -q gdown
brew install portaudio
gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc
unzip pretrained.zip
