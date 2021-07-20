import json
from collections import Counter
from nrclex import NRCLex

target_lyric = ['Rock', 'Jazz', 'Electronic', 'Country', 'Metal', 'Folk', 'Blues', 'Punk','Rap', 'RnB']

json_file = '/valid_lyrics_genius.json'

props = {'track_count':0, 'token_count':0, 'sample': None}
stats_dic = {i: {j:k for j, k in props.items()} for i in target_lyric}

n=0
with open(json_file, 'r') as infile:
    for json_line in infile.readlines():
        if n and not n%1000:
            print(n)
        n+=1
        track_data = json.loads(json_line)
        genre = track_data['genre']
        lyric = track_data['lyrics']
        if genre in target_lyric:
            nrc = NRCLex(lyric)
            stats_dic[genre]['token_count'] +=len(nrc.words)
            if not stats_dic[genre]['track_count']:
                stats_dic[genre]['sample'] = [lyric, track_data['msd_artist_name'], track_data['msd_title']]
            stats_dic[genre]['track_count']  += 1

out_handle = open('/results/lyric_stats.txt', 'w')
try:
    for i, j in stats_dic.items():
        # print(j)
        out_handle.write(f'Genre: {i}\n')
        track_cnt = j['track_count']
        avg_token = j['token_count']/j['track_count']
        out_handle.write(f'Total number of tracks: {track_cnt}\n')
        out_handle.write(f'Average number of tokens: {avg_token}\n')
        out_handle.write('Sample Track: {0} - {1}\n'.format(j['sample'][2], j['sample'][1]))
        out_handle.write('{0}\n'.format(j['sample'][0]))
        out_handle.write('======================================================\n')
        out_handle.write('======================================================\n\n\n')
except Exception as e:
    print(e)

out_handle.close()