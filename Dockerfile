FROM python:3.12.6-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Proje dosyalarını ve requirements.txt'yi kopyala
COPY . /app
COPY requirements.txt /app/requirements.txt

# Pip'i güncelle ve bağımlılıkları yükle
RUN python3.12 -m pip install --upgrade pip
RUN python3.12 -m pip install --no-cache-dir -r requirements.txt

CMD ["python3.12", "app.py"]
