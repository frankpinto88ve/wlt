from sqlite import SQLiteClient

client = SQLiteClient('test.db')
#Returns Count of all Tweets associated to Justin Beiber
print(client.table_getter("SELECT COUNT(*) TWEET_COUNT FROM JB_TWEETS"))

#Returns count of unique tweets related to Justin Beiber, that dont have words related to his music
print(client.table_getter("SELECT COUNT(DISTINCT TWEET_ID) TWEET_COUNT FROM JB_TWEETS"))
