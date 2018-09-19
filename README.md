# PEPr_Project_Code
Code repository for Presidential Election Predictions. 

### Steps to run the project

Step 0: Create twitter applications on https://developer.twitter.com/content/developer-twitter/en.html and Fill in the tokens and secrets from the app - in the twitter_scraper.py file

Step 1: Create conda environment or any virtual environment of your choice:

`conda create -n twitter-scraper python=3.6`

Step 2: Activate conda environment

`source activate twitter-scraper`

Step 3: Download all requirements

`conda install --yes --file requirements.txt`

Step 4: Install tweepy separately

`pip install tweepy`

Step 5: Run twitter_scraper.py

`python twitter_scraper.py`


### Notes

**Types of errors encountered:-**

1. If you encounter this error: 

```
------Error Encountered:  Expecting value: line X column Y (char 0) ------
******Check your JSON File:  data/alltweets.json ******
```
- Check the alltweets.json file. 
- Scroll to the very end to make sure that the JSON file is correct. 
- If the file has an incomplete JSON (encounterd if the process was killed mid-way) remove the last json object from the list, close the list, save the file and run again. 
- You can cross check to see that the lastId.txt file must now hold the id of the last JSON object in the alltweets.json file.

2. It is common to face errors while scraping tweets data for the following reasons:
- {'code': 63, 'message': 'User has been suspended.'}
- {'code': 144, 'message': 'No status found with that ID.'}
- {'code': 179, 'message': 'Sorry, you are not authorized to see this status.'}
- {'code': 88, 'message': 'Rate limit exceeded'}

In the last case, the program will execute a sleep of 200s and automatically continue hence.
All other errors are ignored and the tweetids skipped.

**Stopping/Pausing the program**

You can stop the process when ever needed. To continue, just run the program again. It will resume from the last end point.

To deactivate your venv:

`source deactivate`

To remove your venv:

`conda env remove -n twitter-scraper`
