#import spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#import file with API credentials 
from creds import *

#authentication
def auth():
    client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SECRET)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

def getDataFromPlaylist(l, sp):
    playlist_URI = l.split("/")[-1].split("?")[0]

    playlistlength = len(sp.playlist_tracks(playlist_URI)["items"])
    energy = 0
    danceability = 0

    playlisturis = []

    for song in sp.playlist_tracks(playlist_URI)["items"]:
   
        #URI
        track_uri = song["track"]["uri"]
        playlisturis.append(track_uri)

        #Track name
        track_name = song["track"]["name"]
        print(track_name)

        #FEATURES
        #dancability
        d = sp.audio_features(track_uri)[0]["danceability"]
        danceability += float(d)
        print("Danceability:", str(d))

        #energy
        e = sp.audio_features(track_uri)[0]["energy"]
        energy += float(e)
        print("Energy:", str(e))

        #whitespace
        print("\n")

        # #features
        # features = sp.audio_features(track_uri)[0]
        # print(features)

    danceability /= playlistlength
    energy /= playlistlength

    #idek

    genre = 'rock'
    year = '2003'
    s = sp.search(q='genre:' + genre + '&year:' + year, type='track',market='GB',limit=50, offset=0)
    print(s)

    return (danceability, energy)


#MAIN FUNCTION
def main():
    print("Spotify Playlist Creator")

    l = "https://open.spotify.com/playlist/1ZwFb8shIDE5ko3mkpIFb7?si=0e486a76e27f4d6c&pt=f4c3d7b466ea9b3b2c4ccff26916d007"

    #authenticate
    sp = auth()

    #get data from playlist
    d = getDataFromPlaylist(l, sp)

    print(d)


if __name__ == "__main__":
    main()