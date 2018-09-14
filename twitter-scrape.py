from tweepy import StreamListener, OAuthHandler, Stream, API
import json
import time 

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

class Tweet:
	def authenitcate(self):
		auth = OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = API(auth)
		return api

	def readtext(self, filename):
		with open(filename, "r") as fp:
			data = fp.read()

		return data

	def processData(self, tweetIds, api):
		allTweets = ""
		errorTweets = ""
		for id in tweetIds:
			try:
				tweet = api.get_status(id,tweet_mode="extended")
				allTweets+=tweet.full_text+"\n"
				print(id)
			except Exception as e:
				print("ERROR: ",str(e), " ID: ",id)
				errorTweets+=id+"\n"
				
				if type(e).__name__ == "RateLimitError":
					print("SLEEP")
					time.sleep(200)
				# print("ERROR: ",str(e), " ID: ",id)
				# errorTweets+=id+"\n"
				continue
		return allTweets, errorTweets


if __name__ == "__main__":
	tw = Tweet()
	api = tw.authenitcate()
	inputfilename = "data/tweetids.txt"
	outputfilename = "data/alltweets3.json"
	tweetids = tw.readtext(inputfilename)
	l = 0
	r = 800
	n = len(tweetids)
	tweetids = tweetids.split("\n")
	errors =""
	allT = ""
	# try:
	# with open(outputfilename, "w") as fp:
	# 	fp.write("")

	while l<r and r<n:
		alltweets, errort = tw.processData(tweetids[l:r], api)
		l = r
		r +=800
		with open(outputfilename, "a") as fp:
			fp.write(alltweets)
		allT+=alltweets
		errors+=errort
		print(len(alltweets))
		print("**************************")
		time.sleep(200)
	# except:
	# 	print("Break")

	with open("alltweetstotal.txt", "w") as fp:
		fp.write(allT)
	with open("data/errortweets.txt", "w") as fq:
		fq.write(errors)
	print(len(allT))
# tweet = api.get_status(788530547593211904,tweet_mode="extended")
# print(tweet.full_text)
