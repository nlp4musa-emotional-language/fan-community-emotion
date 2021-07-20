import json 
import re
from nrclex import NRCLex



genres = ['Metal', 'electronicmusic', 'folk', 'Rock', 'blues', 'punk',\
        'rap', 'rnb', 'Jazz', 'country']

outfile_handle = open(f'/pushshift_data/results/comment_stats.txt', 'w')

sample_comment_num = 10

for genre in genres:
	print(genre)
	in_dict_file = f'/pushshift_data/comments_by_genre/{genre}_comments_pushshift.json'
	all_comment = 0
	good_comment = 0
	removed_comment = 0
	comment_samples = []
	sample_authors = []
	comment_lengs = []
	with open(in_dict_file, 'r') as infile:
		n = 0
		for json_line in infile:
			all_comment+=1
			json_object = json.loads(json_lisne)
			body = json_object['body']
			author = json_object['author']
			if body == '[deleted]' or body=='[removed]' or author=='AutoModerator' or 'i am a bot' in body.lower() or 'i\'m a bot' in body.lower():
				removed_comment+=1
			else:
				body = re.sub(r"http\S+", "<URL_here>", body)
				body = re.sub("[@$*%#]" , "", body)
				nrc = NRCLex(body)
				good_comment+=1
				comment_lengs.append(len(nrc.words))
				if n < sample_comment_num:
					comment_samples.append(body)
					sample_authors.append(author)
					n+=1
	total_words = sum(comment_lengs)
	avg_leng = total_words/good_comment
	outfile_handle.write(f'Genre : {genre}\n')
	outfile_handle.write(f'Number of all comments collected: {all_comment}\n')
	outfile_handle.write(f'Number of good comments collected: {good_comment}\n')
	outfile_handle.write(f'Number of removed comments: {removed_comment}\n')
	outfile_handle.write(f'Average length of a comment: {avg_leng}\n')
	outfile_handle.write('Sample Comments:\n')
	for i in range(len(comment_samples)):
		outfile_handle.write(f'{sample_authors[i]}: ')
		outfile_handle.write(f'{comment_samples[i]}\n')
		outfile_handle.write('======================\n')
	outfile_handle.write('==============================================================================\n')
	outfile_handle.write('==============================================================================\n\n\n')

outfile_handle.close()