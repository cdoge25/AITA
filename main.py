#from aita_clean:
#100 before last: 1580540276 - 2020-02-01 07:00:00
#last known datetime: 1580577998 - 2020-02-01 17:00:00

#which is 100 posts every 10 hours

#now start from 1580580000 - 2020-02-01 18:00:00
#end epoch - start epoch = 36000s
start_epoch = 1
end_epoch = start_epoch + 36000
subreddit_name = "AmItheAsshole"
example_api_url = f"https://api.pullpush.io/reddit/search/submission/?subreddit={subreddit_name}&after={start_epoch}&before={end_epoch}"

#main
