#import spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#import file with API credentials 
from creds import *
#other imports
from array import *

#SONG CLASS
class Song:

    def __init__(self, idd, name, artist, uri, length, key, bpm, danceability, energy, lyricism, playlistsize):
        self.id = idd
        self.name = name
        self.artist = artist
        self.uri = uri
        self.length = length

        #needed for algorithm
        self.key = key
        self.bpm = bpm
        self.danceability = danceability
        self.energy = energy
        self.lyricism = lyricism

        #applying the algorithm

        self.closeness = []
        for i in range(6):
            a = []
            for j in range(playlistsize):
                a.append(-1)
            self.closeness.append(a)

#authentication
def auth():
    client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SECRET)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

def createSongsFromPlaylist(l, sp):
    playlist_URI = l.split("/")[-1].split("?")[0]

    playlistlength = len(sp.playlist_tracks(playlist_URI)["items"])
    energy = 0
    danceability = 0
    i = 0

    list_of_songs = []

    for song in sp.playlist_tracks(playlist_URI)["items"]:
   
        #id = i

        #uri
        track_uri = song["track"]["uri"]

        #name
        track_name = song["track"]["name"]

        #artist
        artist = song["track"]["artists"]
        
        #length
        length = sp.audio_features(track_uri)[0]["duration_ms"]

        #key
        key = sp.audio_features(track_uri)[0]["key"]

        #bpm
        bpm = sp.audio_features(track_uri)[0]["tempo"]

        #danceability
        d = sp.audio_features(track_uri)[0]["danceability"]

        #energy
        e = sp.audio_features(track_uri)[0]["energy"]

        #lyricism
        l = sp.audio_features(track_uri)[0]["acousticness"]

        #create instance of Song class
        song = Song(i, track_name, artist, track_uri, length, key, bpm, d, e, l, playlistlength)

        list_of_songs.append(song)

        i+= 1

    return (list_of_songs)

def setClosenessScores(songs):

    #sort based on categories
    #keylist should be sorted based on music theory
    keylist = sorted(songs, key=lambda x: x.key, reverse=True)
    #others sorted based on pure number
    bpmlist = sorted(songs, key=lambda x: x.bpm, reverse=True)
    danceabilitylist = sorted(songs, key=lambda x: x.danceability, reverse=True)
    energylist = sorted(songs, key=lambda x: x.energy, reverse=True)
    lyricismlist = sorted(songs, key=lambda x: x.lyricism, reverse=True)
    
    #for each song...
    numsongs = len(songs)
    for song in songs:

        #song's index in each list
        keyindex = keylist.index(song)
        bpmindex = bpmlist.index(song)
        danceabilityindex = danceabilitylist.index(song)
        energyindex = energylist.index(song)
        lyricismindex = lyricismlist.index(song)

        #look at how far away the other songs are on 
        # the 5 sorted lists...
        for i in range(numsongs):

            #song closeness for a given category at the index=idd
            # is the absolute val of the difference of the 
            # indecies of each song


            #key
            song.closeness[0][keylist[i].id] = abs(i-keyindex)
            #bpm
            song.closeness[1][bpmlist[i].id] = abs(i-bpmindex)
            #danceability
            song.closeness[2][danceabilitylist[i].id] = abs(i-danceabilityindex)
            #energy
            song.closeness[3][energylist[i].id] = abs(i-energyindex)
            #lyricism
            song.closeness[4][lyricismlist[i].id] = abs(i-lyricismindex)

def calcScores(songs):

    for song in songs:

        #SET WEIGHTS HERE
        keyweight = 5
        bpmweight = 8
        danceabilityweight = 1
        energyweight = 2
        lyricismweight = 4

        #find sum of each column
        numsongs = len(songs)
        for i in range(numsongs):

            
            s = 0
            #key
            s += (song.closeness[0][i] * keyweight)
            #bpm
            s += (song.closeness[1][i] * bpmweight)
            #danceability
            s += (song.closeness[2][i] * danceabilityweight)
            #energy
            s += (song.closeness[3][i] * energyweight)
            #lyricism
            s += (song.closeness[4][i] * lyricismweight)

            song.closeness[5][i] = s

def findFirstBestMatch(songs):

    lowestscore = -1

    song1 = None
    song2 = None

    numsongs = len(songs)

    for song in songs:

        for i in range(numsongs):

            if song.closeness[5][i] > 0 and (song.closeness[5][i] < lowestscore or lowestscore == -1):
                lowestscore = song.closeness[5][i]
                song1 = song
                song2 = songs[i]

    return (song1, song2)

def findBestMatch(song1, song2, ul):

    lowestscore = -1
    applytosong1 = False
    bestmatch = None

    numsongs = len(ul)

    #see best score for song1
    for i in range(numsongs):

        if song1.closeness[5][i] > 0 and (song1.closeness[5][i] < lowestscore or lowestscore == -1):
            lowestscore = song1.closeness[5][i]
            applytosong1 = True
            bestmatch = ul[i]

    #see best score for song2
    for i in range(numsongs):

        if song2.closeness[5][i] > 0 and (song2.closeness[5][i] < lowestscore or lowestscore == -1):
            lowestscore = song2.closeness[5][i]
            applytosong1 = False
            bestmatch = ul[i]

    #return
    return bestmatch, applytosong1

def organize(songs):

    #unordered list
    ul = songs
    #ordered list
    ol = list()

    #get the starting two songs
    song1, song2 = findFirstBestMatch(ul)
    #add them to ol, remove from ul
    ol.append(song1)
    ol.append(song2)
    ul.remove(song1)
    ul.remove(song2)

    #add songs onto the end of the list
    while(len(ul) > 0):
        song, applytosong1 = findBestMatch(song1, song2, ul)
        ul.remove(song)

        if(applytosong1):
            ol.insert(0,song)
            song1 = song
        else:
            ol.append(song)
            song2 = song

    return ol



#MAIN FUNCTION
def dj(link="https://open.spotify.com/playlist/1ZwFb8shIDE5ko3mkpIFb7?si=0e486a76e27f4d6c&pt=f4c3d7b466ea9b3b2c4ccff26916d007"):
    print("Spotify Playlist Creator")

    #authenticate
    sp = auth()

    #get data from playlist
    songs = createSongsFromPlaylist(link, sp)

    #set closeness scores for each song
    setClosenessScores(songs)

    #calculate weighted sum score for each song
    calcScores(songs)

    #organize songs based on closeness scores
    organizedlist = organize(songs)

    for song in organizedlist:
        print(song.name + " --", song.key, song.bpm)

dj()