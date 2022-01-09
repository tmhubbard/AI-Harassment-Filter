# This script was written by Trevor Hubbard; its purpose is to better understand
# how to use the Tweepy library, so that I can scrape data for the AI Harassment
# Filter project

# =========================
#        * SETUP *
# =========================

# Some import statements
import tweepy
import json
import datetime
from time import sleep
import os

# Setting up the API authentication
API_key = os.getenv("TWITTER_API_KEY")
API_secret = os.getenv("TWITTER_API_SECRET")
auth = tweepy.AppAuthHandler(API_key, API_secret)

# Declaring the instance of Tweepy we'll use
twitter = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Declaring a "DEBUG" variable
DEBUG = True

# =========================
#       * METHODS *
# =========================

# This method will print something if *condition* is true
def printIf(message, condition):
    if (condition):
        print(message)


# This method will return a tuple of (followerCt, followingCt) for *username*
def getFollowerFollowingCt(username):
    try:
        users = twitter.lookup_users(screen_name=username)[0]
        followerCt = users._json["followers_count"]
        followingCt = users._json["friends_count"]
        return (followerCt, followingCt)
    except:
        return (0, 0)


# This method will return a list of the IDs of the users that *username* is following
def getFollowingIDs(username):
    ids = []
    for page in tweepy.Cursor(twitter.friends_ids, screen_name=username).pages():
        ids = ids + page
    return ids


# This method will return a list of the IDs that are following *username*
def getFollowerIDs(username):
    ids = []
    for page in tweepy.Cursor(twitter.followers_ids, screen_name=username).pages():
        ids = ids + page
    return ids


# This method will return a list of the most recent *numTweets* Tweets from *username*
def getRecentTweets(username, numTweets):
    tweets = []
    for tweet in tweepy.Cursor(twitter.user_timeline, screen_name=username, tweet_mode="extended").items(numTweets):
        tweets.append(tweet._json)
    return tweets


# This method will return a list of *username*'s *numTweets* most recent liked Tweets
def getRecentLikes(username, numTweets):
    tweets = []
    for tweet in tweepy.Cursor(twitter.favorites, screen_name=username).items(numTweets):
        tweets.append(tweet._json)
    return tweets


# This method will return the username of a user whose ID is userID
def getUsername(userID):
    return twitter.get_user(userID).screen_name


# This method will return the User object of a user whose ID is userID
def getUser(userID):
    return twitter.get_user(userID)


# This method will scrape a bunch of data from the given account
def scrapeAccounts(usernameList=[], tweetsToScrape=10, likesToScrape=10, userIDList=None):

    # Iterate through the scraping for each username in the usernameList
    for username in usernameList:

        # Wrapping things in a continous "Try / Except" to retry errors
        while True:
            try:

                # Figure out the follower/following count for this user
                counts = getFollowerFollowingCt(username)
                totalIDs = counts[0] + counts[1]

                # Get the following of a given user
                printIf("\n\nScraping %s's 'Following' list..." % username, DEBUG)
                following = getFollowingIDs(username)

                # Waiting 15min between the following / followers
                if (totalIDs > 65000):
                    now = datetime.datetime.now()
                    time = str(now.hour) + ":" + str(now.minute)
                    printIf("Finished scraping @ %s... waiting ~15min to scrape %s's 'Followers' list..." % (
                    time, username), DEBUG)

                # Get the followers of a given user
                printIf("Scraping %s's 'Follower' list..." % username, DEBUG)
                followers = getFollowerIDs(username)

                # Get the recent Tweets of a given user
                printIf("Scraping %s's %d most recent Tweets..." % (username, tweetsToScrape), DEBUG)
                tweets_and_RTs = getRecentTweets(username, tweetsToScrape)

                # Sorting between Tweets and retweets
                tweets = []
                retweets = []
                for status in tweets_and_RTs:
                    if ("retweeted_status" in status):
                        retweets.append(status)
                    else:
                        tweets.append(status)

                # Get the recent Likes of a given user
                printIf("Scraping %s's %d most recent Likes..." % (username, likesToScrape), DEBUG)
                likes = getRecentLikes(username, likesToScrape)

                # Create a dict of the scraped information
                printIf("Saving the information to %s.json" % username, DEBUG)
                accountDict = {"username": username, "following": following,
                               "followers": followers, "tweets": tweets,
                               "retweets": retweets, "likes": likes}

                break

            except tweepy.TweepError as e:
                print(e.reason)
                if (e.reason == "Not authorized."):
                    return "private"
                print("\n\n\nWAITING 16MIN")
                sleep(960)

        # Save the accountDict as a .json
        with open(username + ".json", "w", encoding="utf-8") as jsonFile:
            json.dump(accountDict, jsonFile)

            return "scraped"

    # If the usernameList was empty and userIDList isn't None, scrape *those* accounts
    if (userIDList is not None):
        for userID in userIDList:

            # Wrapping things in a continous "Try / Except" to retry errors
            while True:
                try:

                    # Get the account's username
                    print("Searching for username...")
                    username = getUsername(userID)
                    print(username)

                    # Figure out the follower/following count for this user
                    counts = getFollowerFollowingCt(username)
                    totalIDs = counts[0] + counts[1]

                    # Get the following of a given user
                    printIf("\n\nScraping %s's 'Following' list..." % username, DEBUG)
                    following = getFollowingIDs(username)

                    # Waiting 15min between the following / followers
                    if (totalIDs > 65000):
                        now = datetime.datetime.now()
                        time = str(now.hour) + ":" + str(now.minute)
                        printIf("Finished scraping @ %s... waiting ~15min to scrape %s's 'Followers' list..." % (
                        time, username), DEBUG)

                    # Get the followers of a given user
                    printIf("Scraping %s's 'Follower' list..." % username, DEBUG)
                    followers = getFollowerIDs(username)

                    # Get the recent Tweets of a given user
                    printIf("Scraping %s's %d most recent Tweets..." % (username, tweetsToScrape), DEBUG)
                    tweets_and_RTs = getRecentTweets(username, tweetsToScrape)

                    # Sorting between Tweets and retweets
                    tweets = []
                    retweets = []
                    for status in tweets_and_RTs:
                        if ("retweeted_status" in status):
                            retweets.append(status)
                        else:
                            tweets.append(status)

                    # Get the recent Likes of a given user
                    printIf("Scraping %s's %d most recent Likes..." % (username, likesToScrape), DEBUG)
                    likes = getRecentLikes(username, likesToScrape)

                    # Create a dict of the scraped information
                    printIf("Saving the information to %s.json" % username, DEBUG)
                    accountDict = {"username": username, "following": following,
                                   "followers": followers, "tweets": tweets,
                                   "retweets": retweets, "likes": likes}

                    break

                except tweepy.TweepError as e:
                    print(e.reason)
                    if (e.reason == "Not authorized."):
                        return "private"
                    print("\n\n\nWAITING 16MIN")
                    sleep(960)

            # Save the accountDict as a .json
            with open(username + ".json", "w", encoding="utf-8") as jsonFile:
                json.dump(accountDict, jsonFile)

                return "scraped"
