from tweeter_streamer import *

#Tweeter creds required to authenticate
consumer_key = ''
consumer_secret = ''
acccess_key = ''
access_secret = ''

# Initiate StreamWriter Object
stream = StreamWriter(consumer_key, consumer_secret, access_key, access_secret, 'test.db')
#Changes the table where tweets will be saved from default "tweets" to "jb_tweets"
stream.set_table_name('jb_tweets')
# Adds filter keywords to avoid before saving in "jb_tweets" table. These words are associated
#to his music and CD
stream.set_filter_keywords(keywords_filters)
# Kickstarts tweet stream related to "Justin Beiber"
stream.filter(track=["Justin Bieber"])
