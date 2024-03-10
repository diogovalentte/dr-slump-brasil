FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt upgrade -y

RUN wget https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb && apt install "$PWD/megacmd-xUbuntu_22.04_amd64.deb" -y

CMD ["mega-cmd-server"]

ENTRYPOINT ["python", "main.py"]
