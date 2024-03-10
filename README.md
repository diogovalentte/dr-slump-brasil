# Dr. Slump Brasil Downloader
This is a project to download episodes from the [Dr. Slump Brasil site](https://drslumpbrasil.blogspot.com) with PT-BR fansub. If you like the episodes, you can donate to the site owner, more about it on the Dr. Slump Brasil site.

# Requirements
- Install [MEGAcmd](https://github.com/meganz/MEGAcmd) CLIs, they'll be used because some episodes are available on [MEGA.nz](https://mega.nz).
- Install the Python dependencies:
```sh
pip install -r requirements.txt
```

# How to run:
## Docker
1. Build the Docker image:
```sh
docker build -t dr-slump-brasil .
```
2. Run:
```sh
docker run --name dr-slump-brasil dr-slump-brasil
```

## Manually
1. Start the mega-cmd-server:
```
mega-cmd-server
```
2. Export the environment variables needed:
```sh
# Where to download the episodes 
export DOWNLOAD_FOLDER=/abs/path/to/folder
# SQLite database to be used to keep track of already downloaded episodes
export DB_PATH=/abs/path/to/file.db
# Filter to decide what types of episodes to download. Can be: 80show, 90show, special, movie
export DOWNLOAD_FILTER=
``` 
3. (Optional) You can enable notifications to a [Ntfy](https://ntfy.sh) topic by exporting the following environment variables. They'll notify when an episode is downloaded or an error occurs in the execution:
```sh
export NTFY_ADDRESS=https://sub.domain.com
export NTFY_TOPIC=topic_name
export NTFY_TOKEN=token
```
4. Execute the script:
```sh
python3 main.py
```

# Limitations
## Download from OneDrive
Some files are available on OneDrive, but the project won't use the OneDrive URL to directly download the file (maybe it could, but I don't know how and I spent too much time testing how). Instead, I accessed each link to get the "real" download URL and created a map variable between the OneDrive URL available on the site and the "real" download URL, **manually**. I did this because currently, only a few episodes are in OneDrive (episodes 62-74 of the 90's show), so it wasn't so much trouble.
- The map is on the file `src/download.py`, with the variable name `ONEDRIVE_MAP`.
