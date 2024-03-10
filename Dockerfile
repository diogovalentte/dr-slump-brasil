FROM python:3.10

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

RUN apt update && apt upgrade -y

RUN wget https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb && apt install "$PWD/megacmd-xUbuntu_22.04_amd64.deb" -y

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "/app/scripts/login-mega.sh && python main.py"]
