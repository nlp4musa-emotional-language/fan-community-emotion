import json
import numpy as np
from collections import Counter
import pickle as pkl
import random

target_genres_com = ['blues', 'country', 'electronicmusic',  'folk', 'Jazz', 'Metal', 'punk', 'rap', 'rnb', 'Rock']

# number of unique commenters in r/rnb is 4276, the least number
sample_num = 4276

all_authors = []
for genre in target_genres_com:
    unique_authors = set()
    authors = []
    with open(f'pushshift_data/comments_by_genre/{genre}_comments_pushshift.json', 'r') as infile:
        for json_line in infile.readlines():
            json_info = json.loads(json_line)
            unique_authors.add(json_info['author'])
            authors.append(json_info['author'])
        all_authors.append(set(random.sample(list(unique_authors), sample_num)))


print(len(all_authors))


shared_user_propor = np.eye(len(target_genres_com))
for i in range(len(shared_user_propor)):
    for j in range(i, len(shared_user_propor[0])):
        if shared_user_propor[i][j]==0.0:
            shared_user_propor[i][j] = shared_user_propor[j][i] = len(all_authors[i]&all_authors[j])

with open('/pushshift_data/results/user_network_sampled.pkl', 'wb') as outf:
    pkl.dump([shared_user_propor, {target_genres_com[i]: len(all_authors[i]) for i in range(len(target_genres_com))}], outf)
print(shared_user_propor)
