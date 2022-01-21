import tweepy
from tweepy import Stream
from sqlite import SQLiteClient
#from creds import *
from jb_filters import *

class StreamWriter(Stream, SQLiteClient):
    """
    StreamWrite objects used to stream tweets that meet certain criteria and
    save it directly to the SQLite DB of choice.
    """
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, db_name, table_name = 'tweets'):
        """
        params:
            consumer_key (string): Twitter Credentials obtained from the Developer Portal
            consumer_secret (string): Twitter Credentials obtained from the Developer Portal
            access_key (string): Twitter Credentials obtained from the Developer Portal
            consumer_key (string): Twitter Credentials obtained from the Developer Portal
            db_name (string): SQLite database where tweets that are streamed will be stored
            table_name (string, optional): table name where tweets that are streamed will be stored.
                                           If no name is provided, it will default to 'tweets'
        """
        Stream.__init__(self,consumer_key, consumer_secret, access_key, access_secret)
        SQLiteClient.__init__(self,db_name)
        self.table_name = table_name
        try:
            self.table_creator(self.table_name,
                            ['TWEET_ID TEXT NOT NULL',
                            'TWEET_TEXT TEXT',
                            'CREATED_AT TEXT NOT NULL',
                            'USER_NAME TEXT NOT NULL'])
        except Error as e:
            print(e)
        else:
            print('Ready to Stream Tweets into {} Table'.format(self.table_name))


    def on_status(self, status):
        """
        params:
            status (JSON): status object returned through the stream that carries
                           an actual tweet
        """
        try:

            if not any(value in status.text for value in self.filter_keywords):
                data = [status.id_str, status.text,
                        status.created_at, status.user.id_str]
                self.table_updater(self.table_name, data)
            else:
                pass
        except Error as e:
            print("Error saving tweet ID: {}".format(status.id_str))
        else:
            return True
    def on_error(self, status):
        """
        params:
            status (JSON): status object returned through the stream whenever there's
                           error

        """
        print(status)
        return False

    def set_table_name(self, table_name):
        """
        params:
            table_name (string): table name where streamed tweets will be stored
        """
        self.table_name = table_name
        try:
            self.table_creator(self.table_name,
                            ['TWEET_ID TEXT NOT NULL',
                            'TWEET_TEXT TEXT',
                            'CREATED_AT TEXT NOT NULL',
                            'USER_NAME TEXT NOT NULL'])
        except Error as e:
            print(e)
        else:
            print('Ready to Stream Tweets into {} Table'.format(self.table_name))
        return None

    def set_filter_keywords(self, filters = []):
        """
        params:
            filters (list[String]): list of words to be use to filter out tweets
        """
        self.filter_keywords = filters


if __name__ == "__main__":
    stream = StreamWriter(consumer_key, consumer_secret, access_key, access_secret, 'test.db')
    stream.set_table_name('jb_tweets')
    stream.set_filter_keywords(keywords_filters)
    stream.filter(track=["Justin Bieber"])
