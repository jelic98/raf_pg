# Clone repository
rm -rf Real-Time-Voice-Cloning
git clone git@github.com:jelic98/Real-Time-Voice-Cloning.git
cd Real-Time-Voice-Cloning

# Install libraries
pip install -q -r requirements.txt
pip install -q gdown
brew install portaudio

# Download models
gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc
unzip pretrained.zip

# Download dataset
wget https://www.openslr.org/resources/12/train-other-500.tar.gz
tar -xvf train-other-500.tar.gz
