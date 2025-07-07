FROM python:3.10-slim

ENV DOWNLOAD_FOLDER=/downloads \
    DOWNLOAD_FILTER=all \
    FILES_UID=1000 \
    FILES_GID=1000 \
    DB_PATH=/data/dr-slump-brasil.db \
    NTFY_ADDRESS=\
    NTFY_TOPIC=\
    NTFY_TOKEN=\
    MEGA_EMAIL=\
    MEGA_PASSWORD=

WORKDIR /app

COPY . .

RUN apt update && apt install -y --no-install-recommends \
    wget \
    libfuse2 \
    fuse \
    gpg \
    procps \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb && apt install "$PWD/megacmd-xUbuntu_22.04_amd64.deb" -y
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "/app/scripts/login-mega.sh && python main.py"]
