# Shows crypto currency + how many times its been mentioned on twitter within 24hrs + trade symbol +
# percentage of change in mentions + sentiment from twitter by breaking each sentence the coin has been
# mentioned in into individual words then rating the words using a lexicon of words and feelings a score
# has been assigned from -1 to 1, then based on the score a rating of POSITIVE or NEGITIVE is given 
# using a threshold. Results are saved in a txt file and printed to terminal

# RUN: python3 coins.py
# OUTPUT: terminal + output.txt

# http://NimbusCapital.Ltd
# Scott@NimbusCapital.Ltd
# @NimbusCapital


# Usefull for adding to trade strategies using internet sentiment and tweet mentions can help spot, 
# ie: Pump And Dump
#


import codecs
from bs4 import BeautifulSoup
import requests
import tweepy
from textblob import TextBlob
import sys
import csv

#Authenticate / Digital login to twitter
# USE YOUR OWN TWITTER TOKENS PLEASE NOT MINE
# http://apps.twitter.com TO REGISTER FOR TOKEN DONT USE MINE !

consumer_key= '' 
consumer_secret= ''

access_token=''
access_token_secret=''

# We set the above varibles to our API keys from TWITTER
# Below we use the TWEEYP libary we imported to auth to twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# We set up a varible containing a url of a API i reversed for a trading platform using HTTP HEADERS
url = 'http://cryptrader.com/W/tweets' # They try stop us using it so we spoof our user agent below
#Picking random useragent / telling user and setting below to use
print("Grabing a random useragent from random useragent API....")
userAgent = requests.get("http://labs.wis.nu/ua/") # grab the page / html
randuserAgent = str(userAgent.content).replace('{',"").replace('}',"").replace('"ua"',"").replace("b':","").replace('"',"").replace("'","") # clean string, lol.... json...
print(randuserAgent)#
#
headers = {'User-Agent': randuserAgent} # spoof user agent to stop the block 
page = requests.get(url, headers=headers) # grab the page / html
#print(page.content)
#print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser') # use BEAUTIFULSOUP libary we imported to pass the HTML
tabulka = soup.find("table", {"class" : "data-table"}) # use beautifulsoup libary to get table from the "api"
records = [] # store all of the records in this list

for row in tabulka.findAll('tr'): # we are reversing the "API" basicly from cryptrader here to get "list of altcoins"
    col = row.findAll('td')
    name = col[0].string.strip()
    symbol = col[1].string.strip()
    tweetsLastHour = col[2].string.strip()
    try:
        change = col[3].string.strip()
    except:
        change = "NULL"

    #check for tiwtter sendiment
    #Search for tweets
    public_tweets = api.search("#" + name)# we use tweepy libary again to search for HASHTAG + NAME 

    #Sentiment
    for tweet in public_tweets: # for every tweet we find mentioned...
        text = tweet.text
        cleanedtext = text	
        analysis = TextBlob(cleanedtext) # break it into single words
        sentiment = analysis.sentiment.polarity # work out sentiment
        if sentiment >= 0: # give it english
            polarity = 'Positive'
        else:
            polarity = 'Negative'
        #print(cleanedtext, polarity)
    
    record = '%s|%s|%s|%s|%s' % (name, symbol, tweetsLastHour,change,polarity) # get string ready for output file
    records.append(record)
    print(name + "|" + symbol + "|" + tweetsLastHour + "|" + change + "|" + polarity) # print to screen !!

fl = codecs.open('output.txt', 'wb', 'utf8') #store to output file
line = ';'.join(records)
fl.write(line + u'\r\n')
fl.close() #end store to output file


# FIN - Scott 




		
