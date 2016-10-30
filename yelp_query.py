#!/usr/bin/python
#SEARCHING YELP BY PHONE NUMBERS

import csv
import sys
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key= 'XXXXXXXXXXXXXXXXXXXXXX',
    consumer_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXX',
    token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    token_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXX'
)

client = Client(auth)

phones = []
phone_file  = sys.argv[1]
with open(phone_file,'r') as fh:
	for line in fh:
		line = line.rstrip()
		if len(line) == 12:
			phones.append(line)

responses = []
for i,phone in enumerate(phones):

	try:	
		#print i+1
		response = client.phone_search(phone) 
		if len(response.businesses) > 0:
			biz = response.businesses[0]
			catg =  biz.categories[0].alias if biz.categories else ''	
			print('%s\t%s\t%s\t%s\t%s\t%s'  %( biz.name,biz.id, catg, biz.rating, biz.review_count, biz.phone))
	except:
		pass
