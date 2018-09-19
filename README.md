# PEPr_Project_Code
Code repository for Presidential Election Predictions. 

Step 1: Create conda environment or any virtual environment of your choice:

`conda create -n twitter-scraper python=3.6`

Step 2: Activate conda environment

`source activate twitter-scraper`

Step 3: Download all requirements

`conda install --yes --file requirements.txt `

Step 4: Install tweepy separately

`pip install tweepy`

Step 5: Run twitter_scraper.py

`python twitter_scraper.py`


**FAQs:**

*Types of errors encountered:-*

If you encounter this error: 

```
------Error Encountered:  Expecting value: line X column Y (char 0) ------
******Check your JSON File:  data/alltweets.json ******
```
- Check the alltweets.json file. 
- Scroll to the very end to make sure that the JSOn file is correct. 
- If the file has an incomplete JSON (encounterd if the process was killed mid-way) remove the last json object from the list, close the list, save the file and run again. 
- You can cross check to see that the lastId.txt file must now hold the id of the last JSON object in the alltweets.json file.

