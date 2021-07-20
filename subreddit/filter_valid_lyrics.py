import json
from collections import defaultdict
from nrclex import NRCLex
import pickle as pkl
import statistics

filename = 'genius_lyrics_collected.json'
data = None
with open(filename, 'r') as inf:
    data = inf.readlines()
emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust', 'positive', 'negative']
replace_dic = {'_': ',', '\'': '', '’': '', 'é': 'e', 'ó': 'o', 'á': 'a', 'â': 'a',\
     'ú': 'u','(':'', ')': '', 'í': 'i', '.': '', '!': '', 'ï': 'i', 'ö': 'o'}

def track_info_match(msd_art, msd_tit, gen_art, gen_tit):
    msdA = msd_art.lower().strip()
    genA = gen_art.lower().strip()
    msdT = msd_tit.lower().strip()
    genT = gen_tit.lower().strip()

    for a, b in replace_dic.items():
        msdA = msdA.replace(a, b)
        genA = genA.replace(a, b)
        msdT = msdT.replace(a, b)
        genT = genT.replace(a, b)

    genT_ = genT.replace(' ', '')
    title_match = all([(part_ in genT_) for part_ in msdT.split()])
    artist_match = all([(part_ in genA) for part_ in msdA.split()])
    artist_match_rev = all([(part_ in msdA) for part_ in genA.split()])
    artist_match_ = all([(part_ in genA) for part_ in msdA.replace('&', 'and').split()])
    return (artist_match or artist_match_ or artist_match_rev) and title_match


genre_counts_filter = {}

counter=1
handle =  open('valid_lyrics_genius.json', 'w')
for track_line in data:
    track_info = json.loads(track_line)
    msd_artist = track_info['msd_artist_name']
    msd_title =  track_info['msd_title']
    genius_artist = track_info['artist']
    genius_title =track_info['title']
    genre = track_info['genre']
    track_lyrics = track_info['lyrics'] 

    if genre not in genre_counts_filter:
        genre_counts_filter[genre] = {i:0 for i in emotions}


    if track_info_match(msd_artist, msd_title, genius_artist, genius_title):
        jsonString = json.dumps(track_info)
        handle.write(jsonString)
        handle.write('\n')


        counter+=1
        if counter%1000==0 and counter>0:
            print(f'{counter} done')

handle.close()
print(genre_counts_filter)
