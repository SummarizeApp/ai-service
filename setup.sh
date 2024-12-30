#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install transformers
pip install datasets
pip install rouge-score
pip install flask
pip install sentencepiece
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
pip install pynvml
pip install psutil
pip install prometheus-client

echo "Setup tamamlandı. Sanal ortamı etkinleştirmek için 'source venv/bin/activate' komutunu kullanın."
