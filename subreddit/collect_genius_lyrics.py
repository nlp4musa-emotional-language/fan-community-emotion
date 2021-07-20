import lyricsgenius
import pandas as pd
import time
import traceback
import json

#setting up api parameters
token = '<genius api token>'
genius = lyricsgenius.Genius(token)
genius.skip_non_songs = True
genius.remove_section_headers = True
genius.verbose = False

# this file is avaliable from tagtraum annotations attached to the million song dataset
genre_data = pd.read_csv("msd_tagtraum_cd2c.cls", sep="\t", skiprows=7, header=None)
genre_data.columns = ['track_id', 'genre']

# this file is avaliable from the million song dataset
track_data = pd.read_csv('unique_tracks.txt', sep="<SEP>", header=None)
track_data.columns = ['track_id', 'song_id', 'artist_name', 'title']

genreID = list(genre_data['track_id'])
filename = 'genius_lyrics_info.json'
artists = []
tracks = []
results = []
no_lyric = 0
erroneous = 0
total = 0
start_time = time.time()
handle = open(filename, 'w')
sleep_time = 1
for i in genreID:
    track_info = track_data[track_data['track_id'] == i]
    artist_name = track_info['artist_name'].iloc[0]
    track_name = track_info['title'].iloc[0]
    genre = genre_data[genre_data['track_id']==i]['genre'].iloc[0]
    artists.append(artist_name)
    tracks.append(track_name)
    try:
        result = genius.search_song(track_name, artist_name)
        if not result:
            erroneous+=1
        elif result.lyrics.strip() == '':
            no_lyric+=1
        else:
            track_deet = result.__dict__
            del track_deet['_client']
            del track_deet['primary_artist']
            del track_deet['stats']
            track_deet['genre'] = genre
            track_deet['msd_id'] = i
            track_deet['msd_artist_name'] = artist_name
            track_deet['msd_title'] = track_name
        #try:
            jsonString = json.dumps(track_deet)
            handle.write(jsonString)
            handle.write('\n')
        #except Exception as err:
        #    print(f"Couldn't save lyrics of track {i}")
        #    print(traceback.format_exc())
            results.append(result)
    except:
        erroneous+=1
        time.sleep(sleep_time)
        sleep_time = max([1, (sleep_time+1) % 15])

    total+=1
    if total%100==0:
        print(f'total is {total}, successful is {total-erroneous-no_lyric}')
        print(f'no_result is {erroneous}, and no_lyric is {no_lyric}')
        print(f'avg time per song is {round((time.time()- start_time)/total, 2)}')
        print('--------------------------')

handle.close()
