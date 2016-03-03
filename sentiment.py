# sentiment.py
# Demonstrates connecting to the twitter API and accessing the twitter stream
# Author: Josh Graves
# Version 1.1
# Date: February 17, 2016

import twitter

print 'Establishing Authentication Credentials...'
CONSUMER_KEY = '42ET4zizA6SWjiqLNUdoWHMBq'
CONSUMER_SECRET = 'qUKLiJA3t5BXwFQ5UvLVrCK4uMa1q3FfEgEgPBDIS0AB0RArNf'
OAUTH_TOKEN = '1675098541-fRROoFH59t792EtLf4i1qOOo4ulyxsfDJg1M1OA'
OAUTH_TOKEN_SECRET = 'PYqpq7bnXaocWVWiQcPQ9DLY3Dc7DZTSnLCwAjSCadM7I'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)
print 'Credentials approved'

from urllib import unquote

# XXX: Set this variable to a trending topic, or anything else for that matter.
def calculateSentiment(userInput):
    count = 1000
    search_results = twitter_api.search.tweets(q=userInput, count=count)
    statuses = search_results['statuses']
    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
        # Create a dictionary from next_results, which has the following form:

        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    status_texts = [ status['text']
                     for status in statuses ]
    words = [ w
              for t in status_texts
                  for w in t.split() ]

    sent_file = open('AFINN-111.txt')

    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited
        scores[term] = int(score)  # Convert the score to an integer.

    score = 0

    for word in words:
        uword = word.encode('utf-8')
        if uword in scores.keys():
            score = score + scores[word]

    print 'Sentiment of ' + userInput + ':'
    print float(score)
    return score

term1 = raw_input('Enter a search term: ')
term2 = raw_input('Enter a second search term: ')

sentimentScore1 = calculateSentiment(term1)
sentimentScore2 = calculateSentiment(term2)

if sentimentScore1 > sentimentScore2:
    print term1 + ' had a higher sentiment value than ' + term2
elif sentimentScore2 > sentimentScore1:
    print term2 + ' had a higher sentiment value than ' + term1
else:
    print term1 + ' had the same sentiment value as ' + term2
