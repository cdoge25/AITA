import pandas as pd
import json
import requests
from pandas import json_normalize
#from aita_clean:
#100 before last: 1580540276 - 2020-02-01 07:00:00
#last known datetime: 1580577998 - 2020-02-01 17:00:00

#which is 100 posts every 10 hours

if __name__ == "__main__":
    try:
        start_epoch = 1580580000
        end_epoch = start_epoch + 36000
        subreddit_name = "AmItheAsshole"
        pullpush_api_url = f"https://api.pullpush.io/reddit/search/submission/?subreddit={subreddit_name}&after={start_epoch}&before={end_epoch}"

        response = requests.get(pullpush_api_url)
        data = response.json()['data']
        
        df = pd.DataFrame.from_dict(data)
        df = df[df['link_flair_text'].notna()]
        
    except:
        print("error")
