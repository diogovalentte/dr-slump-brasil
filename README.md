# Dr. Slump Brasil Downloader
This is a project to download episodes from the [Dr. Slump Brasil site](https://drslumpbrasil.blogspot.com) with PT-BR fansub. If you like the episodes, you can donate to the site owner, more about it on the Dr. Slump Brasil site.

# How to run:
1. Install [MEGAcmd](https://github.com/meganz/MEGAcmd) CLIs, they'll be used because some episodes are available on [MEGA.nz](https://mega.nz).
2. Start the mega-cmd-server:
```
mega-cmd-server
```
3. Install the Python requirements. It'll download some of my own libraries from my Github repositories using SSH with Github, so you need to configure an SSH key with Github, or change the `git+ssh://git@github.com/` to `git+https://git@github.com/` to use HTTPS in the **requirements.txt** file.
```sh
pip install -r requirements.txt
```
4. Export the environment variables needed:
```sh
# Where to download the episodes 
export DOWNLOAD_FOLDER=/abs/path/to/folder
# SQLite database to be used to keep track of already downloaded episodes
export DB_PATH=/abs/path/to/file.db
# Filter to decide what types of episodes to download. Can be: 80show, 90show, special, movie
export DOWNLOAD_FILTER=
``` 
5. Execute the script:
```sh
python3 main.py
```
6. You can also enable notifications to the a [Ntfy](https://ntfy.sh) topic by exporting the following environment variables:
```sh
export NTFY_DOMAIN=https://sub.domain.com
export NTFY_TOPIC=topic_name
export NTFY_TOKEN=token
```
