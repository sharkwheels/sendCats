#!/usr/bin/env python

# Py Script run from a cron job, runs four times a day
# Scours @EmergencyKittens on twitter
# pulls a tweet, strips the picture
# sends it to your phone over twillio

## IMPORTS AND LOGGING #########################################################################

import os, random, logging
import json

from sys import exit
from random import choice

from twython import Twython, TwythonError
from twilio.rest import TwilioRestClient


logging.basicConfig(filename='twitterWarn.log',level=logging.INFO)

### GET KEYS #########################################################################

keys = []

with open('keys.txt','r') as my_file:
	keys = my_file.read().splitlines()

### TWITTER DATA #########################################################################

APP_KEY = keys[0]
APP_SECRET = keys[1]
OAUTH_TOKEN = keys[2]
OAUTH_TOKEN_SECRET = keys[3]

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### TWILIO DATA ##########################################################################

account_sid = keys[4]
auth_token = keys[5]

client = TwilioRestClient(account_sid, auth_token)

### TASK FUNCTIONS  ########################################################################################

def getCat():

	cats =[]

	try:
		user_timeline = twitter.get_user_timeline(screen_name='EmrgencyKittens', count=4)
	except TwythonError as e:
		logging.info(e)

	print len(user_timeline)

	tweets = user_timeline

	for tweet in tweets:
		#print tweet['text']
		media = tweet['entities']['media']
		#print media  #cripes twitter, way to barf...
		for mediaItem in media:
			if 'media_url' in mediaItem.keys():
				zeCat = mediaItem['media_url']
				#print zeCat 
				cats.append(zeCat)
	#print cats
	return cats
	

def sendCat():
	twilTo = "+XXXXXXXXXX"
	twilFrom = "+XXXXXXXXXX"
	twilBody = "Cat Delivery!"
	toSendOut = getCat()
	
	beepCat = random.choice(toSendOut)
	print beepCat

	try:
		message = client.messages.create(to=twilTo, 
			from_=twilFrom, 
			body=twilBody, 
			media_url=[beepCat])

		print "sent"

	except twilio.TwilioRestException as f:
		print f
		logging.info(f)
	
### SEND THAT THING ###############################################

sendCat()