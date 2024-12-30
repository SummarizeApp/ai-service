FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY setup.sh .
RUN chmod +x setup.sh

RUN bash setup.sh

ENV PATH="/app/venv/bin:$PATH"

COPY . .

CMD ["python3", "app.py"]
