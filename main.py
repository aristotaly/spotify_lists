import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load configuration from JSON file
with open('config.json', 'r') as file:
    config = json.load(file)

username = config['username']
createnewplaylist = config['createnewplaylist']
newplaylistname = config['newplaylistname']
oldplaylistID = config['oldplaylistID']
dataFile = config['dataFile']

my_client_id = config['spotify']['client_id']
my_client_secret = config['spotify']['client_secret']
redirect_uri = config['spotify']['redirect_uri']

# Spotify API scope
scope = 'user-library-read playlist-modify-public playlist-modify-private'

# Read data file
with open(dataFile, 'r') as file:
    data = file.readlines()

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=my_client_id,
                                               client_secret=my_client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

notfound = []

# Playlist creation or selection
if createnewplaylist:
    playlist = sp.user_playlist_create(username, newplaylistname, False)
    playlistID = playlist['id']
else:
    playlistID = oldplaylistID

# Process each line in the data file
for line in data:
    if line.strip() == "":
        continue

    parts = line.strip().split('-')
    trackTitle = parts[0].strip()
    artist = '-'.join(parts[1:]).strip()

    results = sp.search(q='artist:' + artist + ' track:' + trackTitle, type='track')

    tracks = results['tracks']['items']
    if tracks:
        trackID = tracks[0]['id']
        sp.user_playlist_add_tracks(username, playlistID, [trackID])
        print(f'Added song {trackTitle} by artist {artist}')
    else:
        notfound.append(trackTitle + '-' + artist)

print("\nSongs not added:")
for line in notfound:
    print(line)
