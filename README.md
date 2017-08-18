# Spotify Playlist Utils
Currently this repo includes one util that can be used for cloning playlists. 
Very basic tool at the moment but if there is interest I will continue to improve and add more features.

## Requirements
1. Python 3.3+

## How to Use
1. Clone/Download repo
1. Create a folder named 'instance'
1. Copy the sensitive.ini.template to the instance folder
1. Rename to sensitive.ini
1. Correct the settings. (redirect is typically going to be localhost)
1. Run 'pip install -r requirements.txt'
1. Run 'python playlist_cloner.py'
1. Follow the steps to authenticate the first time. (Subsequent uses will used the cached refresh token if it has not expired.)

## Improvements
If you would like to contribute or suggest ideas for other tools, submit an issue.