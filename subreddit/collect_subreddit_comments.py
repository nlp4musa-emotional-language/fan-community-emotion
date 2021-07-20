import requests
from datetime import datetime
import traceback
import time
import json
import sys


# replace subreddit name here to collect all comments from the pushshift reddit api
subreddit = "subreddit=electronicmusic"

url= "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&{}&before="
start_time = datetime.utcnow()

def downloadFromUrl(filename):
	print(f"saving comments to {filename}")
	count=0
	handle = open(filename, 'w')
	previous_epoch = int(start_time.timestamp())
	while True:
		new_url = url.format('comment', subreddit) + str(previous_epoch)
		json_text = requests.get(new_url, headers={'User-Agent': "comment collector by vivivivi"})
		time.sleep(1)
		try:
			json_data = json_text.json()
		except json.decoder.JSONDecodeError:
			time.sleep(1)
			continue
		
		if 'data' not in json_data:
			break
		comments = json_data['data']
		if len(comments)==0:
			break

		previous_epoch = comments[-1]['created_utc'] - 1
		for comment in comments:
			count+=1	   
			try:
				jsonString = json.dumps(comment)
				handle.write(jsonString)
				handle.write('\n')
			except Exception as err:
				print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
				print(traceback.format_exc())
		print("Saved {} {}s through {}".format(count, 'comment', datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))
		
	print(f"Saved {count} comments")
	handle.close()			

downloadFromUrl("/pushshift_data/comments_by_genre/electronicmusic_comments.json") 	
