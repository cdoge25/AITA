import pandas as pd
import json
import requests
from pandas import json_normalize
import os
import time
#from aita_clean:
#100 before last: 1580540276 - 2020-02-01 07:00:00
#last known datetime: 1580577998 - 2020-02-01 17:00:00

#which is 100 posts every 10 hours

if __name__ == "__main__":
    try:
        inserted_num = 0
        loop_num = 0
        while True:
            # Pickup current progress
            with open("current_progress.json", mode="r") as f:
                current_progress = json.loads(f.read())
            start_epoch = current_progress["start_epoch"]
            end_epoch = current_progress["end_epoch"]
            if end_epoch > 1700000000:
                break
            
            # API call
            subreddit_name = "AmItheAsshole"
            pullpush_api_url = f"https://api.pullpush.io/reddit/search/submission/?subreddit={subreddit_name}&after={start_epoch}&before={end_epoch}"
            response = requests.get(pullpush_api_url)
            data = response.json()['data']
            
            # Save data
            df_raw = pd.DataFrame.from_dict(data)
            df_raw = df_raw[::-1].reset_index(drop=True)
            df_new = df_raw[df_raw['link_flair_text'].notna()]
            df_new = df_new[df_new['selftext'] != "[deleted]"]
            keep_cols = ['id', 'created_utc', 'title', 'selftext', 'edited', 'link_flair_text', 'score', 'num_comments']
            df_new = df_new[keep_cols]
            df_new.rename(columns={
                'created_utc': 'timestamp',
                'selftext': 'body',
                'link_flair_text': 'verdict',
            }, inplace=True)
            
            path_new = "aita_new.csv"
            if not os.path.exists(path_new):
                df_new.to_csv(path_new, mode="w", index=False, header=True)
            else:
                df_new.to_csv(path_new, mode="a", index=False, header=False)
            
            # Update current progress
            replace_progress = {
                "start_epoch": end_epoch,
                "end_epoch": end_epoch + 3600
            }
            with open('current_progress.json', 'w') as f:
                json.dump(replace_progress, f, indent=4)

            inserted_num += len(df_new.index)
            loop_num += 1
            print(f"gone through {loop_num} loops, inserted {inserted_num} items")
            
            time.sleep(1)
    except:
        with open("current_progress.json", mode="r") as f:
            current_progress = json.loads(f.read())
        start_epoch = current_progress["start_epoch"]
        print(f"error at epoch: {start_epoch}")
