# May 3, 2021
# @author:          Larissa Caldeira
# @email:           Caldeira@uw.edu
# @organization:    Department of Sociology, University of Washington, Seattle
# @description:     Search existing tweets
# @reference: https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/twitter-data-in-python/

# EXECUTE 01.TWSEARCH.PY
from selenium import webdriver
from bs4 import Beautiful Soup
import time, datetime, json

url = "https://twitter.com/search?q=catholic%20sex%20abuse&src=typed_query"

#use chrome core
bot = webdriver.Chrome(executable_path="assets/chromedriver")
bot.get(url)

f = open("assets/tweets.csv", "a", encoding="utf-8")
f.write('user_id, user_name, screen_name, status_id, created_at, time_integer, reply_num, favorite_num, content \n')
start = datetime.datetime.now()
time_limit= 60
texts = []

while len(bot.find_elements_by_xpath('//div[contains(text(), "Back to top ↑")]')) != 1:
    time.sleep(5)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    tweets = soup.find_all('li', class_="stream-item")[-20:] # only process the newly-acquired tweets.
    if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than a minute, then stop scrolling.
        break
    for tweet in tweets:
        try:
            user_json = json.loads(tweet.div.attrs["data-reply-to-users-json"])
            user_id = int(user_json[0]['id_str'])
            user_name = user_json[0]['screen_name']
            screen_name = user_json[0]['name']
            status_id = int(tweet.attrs["data-item-id"])
            text = tweet.find("p").text.strip().replace("\n", "")
            created_at = tweet.find("small", class_="time").a.attrs["title"]
            time_integer = tweet.find("small", class_="time").a.span["data-time-ms"]
            reply_num = tweet.find("div", class_="ProfileTweet-action--reply").find("span", class_="ProfileTweet-actionCountForPresentation").text
            retweet_num = tweet.find("div", class_="ProfileTweet-action--retweet").find("span", class_="ProfileTweet-actionCountForPresentation").text
            favorite_num = tweet.find("div", class_="ProfileTweet-action--favorite").find("span", class_="ProfileTweet-actionCountForPresentation").text
            inst_url = ""
            if "www.instagram.com" in text:
                inst_url = tweet.p.a.attrs["title"]
            record = '%d, %s, %s, %d, %s， %s， %s， %s， %s， %s \n' % (user_id, user_name, screen_name, status_id, created_at, time_integer, reply_num, retweet_num, favorite_num, text)
            print(record)
            if (text not in texts):
                f.write(record)
            texts.append(text)
        except:
            pass
f.close()
bot.close()
print("finished")

if __name__ == "__main__":
    pass


###########
############
#end of 01_twsearch code
########
########

#Run 02_geosearch.py

import tweepy, json, time, csv

class StreamListener(tweepy.StreamListener):
    """tweepy.StreamListener is a class provided by tweepy used to access
    the Twitter Streaming API to collect tweets in real-time.
    """

    def __init__(self, time_limit=60, file=""):
        """class initialization"""
        self.start_time = time.time()
        self.limit = time_limit
        self.f = open(file, "w", newline='', encoding="utf-8") # mode a, r, w
        fieldnames = ['id', 'username', 'created_at', 'lng', 'lat', 'text']
        self.writer = csv.DictWriter(self.f, fieldnames=fieldnames)
        self.writer.writeheader()
        super(StreamListener, self).__init__()

    def on_data(self, data):
        """This is called when data are streamed in."""
        if (time.time() - self.start_time) < self.limit:
            datajson = json.loads(data)
            print (datajson)
            id = datajson['id']
            username = datajson['user']['screen_name']
            created_at = datajson['created_at']
            text = datajson['text'].strip().replace("\n", "")

            # process the geo-tags
            if datajson['coordinates'] == None:
                bbox = datajson['place']['bounding_box']['coordinates'][0]
                lng = (bbox[0][0] + bbox[2][0]) / 2.0
                lat = (bbox[0][1] + bbox[1][1]) / 2.0
            else:
                lng = datajson['coordinates']['coordinates'][0]
                lat = datajson['coordinates']['coordinates'][1]
            row = {
                'id': id,
                'username': username,
                'created_at': created_at,
                'lng': lng,
                'lat': lat,
                'text': text
            }

            print (row)
            self.writer.writerow(row)
        else:
            self.f.close()
            print ("finish.")
            return False


if __name__ == "__main__":
    # These are provided to you through the Twitter API after you create a account
    # register a Twitter App to get the keys and access tokens.
    output_file = "assets/geotags.csv"

    # Apply for your own Twitter API keys at https://developer.twitter.com/en/apply-for-access
    consumer_key = "iGLeDbWuEmJc1Y4Y373rdC8xl"
    consumer_secret = "V0mdIfmFAA97H3ImGLS0ODprP3ZADWGyv46LyvrGkjE6W1xS93"
    access_token = "14324013-1uLpCg1HnX1AjWFD2tQCydq9sbAaWU1bXd2xz7dgG"
    access_token_secret = "Qq2Frieih7y0WrMwZz9yWPZXkfDbFBuWJ7u5r2cUEhkPE"


    myauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    myauth.set_access_token(access_token, access_token_secret)

    # LOCATIONS are the longitude, latitude coordinate corners for a box that restricts the
    # geographic area from which you will stream tweets. The first two define the southwest
    # corner of the box and the second two define the northeast corner of the box.
    LOCATIONS = [-124.7771694, 24.520833, -66.947028, 49.384472,  # Contiguous US
                 -164.639405, 58.806859, -144.152365, 71.76871,  # Alaska
                 -160.161542, 18.776344, -154.641396, 22.878623]  # Hawaii

    stream_listener = StreamListener(time_limit=60, file=output_file)
    stream = tweepy.Stream(auth=myauth, listener=stream_listener)
    stream.filter(locations=LOCATIONS)


#######
#######
#End of 02_geosearch.py
######
######


#my own Bot


import csv

import tweepy

# Create a csv file to store the structured data after processing.
csvfile = open("assets/searched_tweets.csv", "w", newline='', encoding="utf-8") # mode a, r, w

# All the fields of each data entry that I want to collect.
fieldnames = ['username', 'userid', 'profile_location', 'created_at', 'text', 'retweet_count', 'source', 'coordinates']

# Create a writer to write the structured data to the csv file.
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# Write the header to the csv file
writer.writeheader("geo_hist_tweets")


# Apply for your own Twitter API keys at https://developer.twitter.com/en/apply-for-access
consumer_key = "iGLeDbWuEmJc1Y4Y373rdC8xl"
consumer_secret = "V0mdIfmFAA97H3ImGLS0ODprP3ZADWGyv46LyvrGkjE6W1xS93"
access_token = "14324013-1uLpCg1HnX1AjWFD2tQCydq9sbAaWU1bXd2xz7dgG"
access_token_secret = "Qq2Frieih7y0WrMwZz9yWPZXkfDbFBuWJ7u5r2cUEhkPE"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "Clergy Abuse", "Sex Abuse Scandal", "Catholic Sex Abuse", "abused by priest"
LOCATIONS = [-124.7771694, 24.520833, -66.947028, 49.384472,  # Contiguous US
             -164.639405, 58.806859, -144.152365, 71.76871,  # Alaska
             -160.161542, 18.776344, -154.641396, 22.878623] #Hawaii
# read the Twitter API document to look for other ways to customize your queries.
# refer to https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
# for example: you can ignore all the retweets by #wildfires -filter:retweets
# Geolocalization: the search operator “near” isn’t available in the API, but there is a more precise way to restrict
# your query by a given location using the geocode parameter specified with the template “latitude,longitude,radius”,
# for example, “47.6138893,-122.3107869,10mi” (capitol hill at Seattle). When conducting geo searches, the search API will first attempt to find Tweets、
# which have lat/long within the queried geocode, and in case of not having success, it will attempt to find Tweets created
# by users whose profile location can be reverse geocoded into a lat/long within the queried geocode, meaning that is possible
# to receive Tweets which do not include lat/long information.

date_since = "2009-01-01"


# Collect tweets
# tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since).items(100)
tweets = tweepy.Cursor(api.search, q=search_words, geocode=location, lang="en", since=date_since).items(100)

# Iterate and print tweets
for tweet in tweets:
    row = {
        'username': tweet.author.name,
        'userid': tweet.author.id,
        'profile_location': tweet.author.location,
        'created_at': str(tweet.author.created_at),
        'text': tweet.text,
        'retweet_count': tweet.retweet_count,
        'source': tweet.source,
        'coordinates': tweet.coordinates
    }
    writer.writerow(row)
    print(row)


csvfile.close()
# notify the completion of the program in the console.
print("finished")
