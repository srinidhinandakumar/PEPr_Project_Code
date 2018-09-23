import json
import helper
from collections import OrderedDict

class TwitterCleaning:
	def __init__(self):
		self.inputfilename = "data/alltweets-srinidhi.json"
		self.outputfilename = "hashtags.json"

	def extractHashtag(self, data, hashtags):
		for item in data:
			hashtag = item["entities"]["hashtags"]
			if hashtag is not []:
				for h in hashtag:
					if h["text"] not in hashtags:
						hashtags[h["text"]]=0
					hashtags[h["text"]]+=1
		return hashtags

	def main(self):
		try:
			#check if hashtags file already exits
			try:
				hashtags = helper.readJson(outputfilename)
			except FileNotFoundError:
				hashtags = dict()
			except Exception as e:
				print(str(e))

			data = helper.readJson(inputfilename)
			new_hashtags = t.extractHashtag(data, hashtags)
			new_hashtags = OrderedDict(sorted(new_hashtags.items(), key=lambda x: x[1], reverse=True))
			helper.writeJson(outputfilename, new_hashtags)
		except Exception as e:
			print(str(e))

if __name__ == "__main__":
	t = TwitterCleaning()
	try:
		t.main()
	except KeyboardInterrupt:
		exit(0)
	
	
