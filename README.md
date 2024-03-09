# Dr. Slump Brasil Downloader
This is a project to download episodes from the [Dr. Slump Brasil site](https://drslumpbrasil.blogspot.com) with PT-BR fansub. If you like the episodes, you can donate to the site owner, more about it on the Dr. Slump Brasil site.

# How to run:
1. Install the Python requirements:
```sh
pip install -r requirements.txt
```
2. Export the environment variable DOWNLOAD_FOLDER specifing where to download the episodes:
```sh
export DOWNLOAD_FOLDER=/abs/path/to/folder
``` 
3. Execute the script:
```sh
python3 main.py
```
4. You can also enable notifications to the a [Ntfy](https://ntfy.sh) topic by exporting the following environment variables:
```sh
export NTFY_DOMAIN=https://sub.domain.com
export NTFY_TOPIC=topic_name
export NTFY_TOKEN=token
```
