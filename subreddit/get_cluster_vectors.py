#sscript for getting counts for each emotion for all subreddits

import json
import sys
import time
import re
import pickle as pkl

from nrclex import NRCLex

genres = ['Metal', 'electronicmusic', 'folk', 'Rock', 'blues', 'punk',\
        'rap', 'rnb', 'Jazz', 'country']
emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust', 'positive', 'negative']

prohib_word = {'Metal': ['black metal', 'death metal', 'doom metal', 'trash metal', 'pirate metal', 'folk metal', 'progressive metal', 'traditional heavy metal'],\
                'electronicmusic':['electronic music', 'intelligent dance music', 'idm', 'goa trance', 'acid trance', 'hypnagogic pop', 'electronic rock', 'bubblegum dance',\
                'snap music', 'house music', 'city pop', 'russ music', 'danger music', 'hard trance', 'bass music', 'balearic trance', 'alternative dance',\
                'neoclassical dark wave', 'noise music', 'italo dance', 'trance music', 'video game music', 'uplifting trance', 'vocal trance',\
                'industrial rock', 'trip rock', 'electronic body music',  'ebm', 'tech trance', 'hip hop fusion genres', 'progressive trance',\
                'berlin school', 'melodic funk', 'afro music', 'cosmic music', 'jungle terror', 'electroacoustic improvisation', 'acousmatic music',\
                'liquid funk', 'electroacoustic music', 'new rave', 'dream trance', 'funk fusion genres', 'neo trance', 'psychedelic trance',\
                'space music', 'new romantic', 'harsh noise', 'african electronic dance music', 'ragga jungle', 'power noise', 'dancehall pop',\
                'sequencer music', 'future funk', 'space rock', 'harsh noise wall'],\
                'folk': ['progressive folk'],\
                'Rock': ['rock', 'acid rock', 'alternative dance', 'americana music', 'art punk', 'art rock', 'baroque pop', 'bandana thrash', 'beach music',\
                'beat music', 'blackened death metal', 'black metal', 'blues rock', 'brazilian thrash metal', 'britpop revival', 'bubblegum music', 'crossover thrash',\
                'dance-rock', 'dark cabaret', "death 'n' roll", 'death metal', 'deathrock', 'doom metal', 'dream pop', 'drone metal', 'emo pop', 'emo revival', \
                'ethereal wave', 'funk metal', 'funk rock', 'gypsy punk', 'horror punk', 'indie pop', 'instrumental rock', 'italian occult psychedelia', 'jangle pop', \
                'melodic death metal', 'mod revival', 'neoclassical dark wave', 'neon pop', 'new rave', 'new weird america', 'noise pop', 'noise rock', 'occult rock', \
                'outlaw country', 'peace punk', 'pirate metal', 'pop punk', 'pop rock', 'post-punk revival', 'power pop', 'progressive metal', 'progressive metalcore', \
                'progressive pop', 'progressive rock', 'psychedelic funk', 'psychedelic pop', 'pub rock (united kingdom)', 'punk blues', 'red dirt', 'riot grrrl', \
                'rock against communism', 'rock in opposition', 'shock rock', 'sludge metal', 'sunshine pop', 'surf music', 'swamp pop', 'swamp rock', 'swedish death metal', \
                'symphonic black metal', 'technical death metal', 'thrash metal', 'wizard rock', 'wonky pop', 'youth crew'],\
                'blues': ['blues', 'classic female blues', 'country blues', 'delta blues', 'dirty blues', 'electric blues', 'hokum blues', 'jump blues'],\
                'punk': ['punk blues'],\
                'rap': ['trap music', 'drill music', 'chopped and screwed', 'snap music'],\
                'rnb': ['rnb'],\
                'Jazz': ['country', 'acid jazz', 'cool jazz', 'dance jazz', 'dark jazz', 'free funk', 'gypsy jazz', 'jazz blues', 'jazz fusion', 'jazz rock', 'west coast jazz' ],\
                'country': ['classic country', 'country blues', 'country pop', 'country rock', 'cowboy pop', 'instrumental country', 'cosmopolitan country', 'old-time music',\
                'outlaw country', 'progressive country', 'southern rock', 'talking blues', 'traditional country music', 'new mexico music', 'red dirt']}

start_time = time.time()

all_counts = {}
for genre in genres:
    big_regex = re.compile('|'.join(map(re.escape, prohib_word[genre])))
    emo_counts = {j:0 for j in emotions}
    print(genre, emo_counts)
    with open(f'/home/is/vipul-mi/pushshift_data/comments_by_genre/{genre}_comments_pushshift.json', 'r') as infile:
        removed_comment=0
        n=0
        for jsonline in infile.readlines():
            if n>0 and n%10000==0:
                print(n)
            n+=1
            json_object = json.loads(jsonline)
            body__ = json_object['body'].strip()
            body_ = re.sub("[@$*%#()<>[]]" , "", body__)
            body_pre = re.sub(r"http\S+", "link", body_)
            body =  big_regex.sub('', body_pre)
            author = json_object['author']
            if author=='AutoModerator' or body=='[removed]' and body=='[deleted]' or 'i am a bot' in body.lower() or 'i\'m a bot' in body.lower():
                removed_comment+=1
            else:
                nrc = NRCLex(body).raw_emotion_scores
                for emo in nrc.keys():
                    emo_counts[emo] += nrc[emo]
            
        for i, j in emo_counts.items():
            print(i, j)
        all_counts[genre] = emo_counts
        print(f'{genre} done!')
        print("total time passed")
        print(time.time()-start_time)


with open(f"pushshift_data/results/subreddit_emotion_counts.pkl", 'wb') as outfile:
	pkl.dump(all_counts , outfile)

