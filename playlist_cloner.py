import configparser

import spotipy
import spotipy.util as util

SCOPE = 'playlist-modify-public'

#########################################################################
# Settings
FROM_USERNAME = ''  # Username of copy from playlist
FROM_PLAYLIST_ID = ''  # Clone from playlist id

TO_USERNAME = ''  # Authenticated user's username
TO_PLAYLIST_ID = ''  # Clone to playlist id
#########################################################################


def recently_added(tracks):
    temp = "0000-00-00T00:00:00Z"
    for track in tracks['items']:
        added_at = track['added_at']
        if added_at > temp:
            temp = added_at
    return temp


def track_id_list(tracks):
    temp = []
    for track in tracks['items']:
        temp.append(track['track']['id'])
    return temp

# Load sensitive.ini & values
settings = configparser.ConfigParser()
settings.read('instance/sensitive.ini')

spotify_client_id = settings.get('SPOTIFY_CLIENT', 'ID')
spotify_client_secret = settings.get('SPOTIFY_CLIENT', 'SECRET')
spotify_client_redirect_uri = settings.get('SPOTIFY_CLIENT', 'REDIRECT_URI')

# Setup spotipy
token = util.prompt_for_user_token(TO_USERNAME, SCOPE, client_id=spotify_client_id,
                                   client_secret=spotify_client_secret, redirect_uri=spotify_client_redirect_uri)
sp = spotipy.Spotify(auth=token)

# Get current original playlist tracks
from_tracks = sp.user_playlist_tracks(FROM_USERNAME, FROM_PLAYLIST_ID)
from_date_added = recently_added(from_tracks)

# Get current user playlist tracks
to_tracks = sp.user_playlist_tracks(TO_USERNAME, TO_PLAYLIST_ID)
to_date_added = recently_added(to_tracks)

# Check last modified time instead of modifying every time run
if to_date_added >= from_date_added:
    print('Nothing to change. Exiting...')
    exit(0)

# Compile list to remove
remove_tracks = track_id_list(to_tracks)

# Clear to playlist
sp.user_playlist_remove_all_occurrences_of_tracks(TO_USERNAME, TO_PLAYLIST_ID, remove_tracks)

# Compile list to add
add_tracks = track_id_list(from_tracks)

# Add all songs
sp.user_playlist_add_tracks(TO_USERNAME, TO_PLAYLIST_ID, add_tracks)

print('Playlist successfully cloned!')
