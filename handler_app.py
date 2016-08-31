#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	handler app changes and mail to you
#	include the following:
#	* app is not available in appstore any more
#	* app come back to appstore
#	* app cut price
#	* app get a new version
#	please add this script to crontab
#
############################################################
import os,sys
import json
import api
import re
from datetime import datetime

def main():
	root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	cache_path = os.path.join(root_path, "handler.cache")
	config_path = os.path.join(root_path, "config.ini")

	# read cache file
	f = None
	try:
		f = open(cache_path, 'r')
		cache_list = json.loads(f.read())
	except Exception as e:
		cache_list = []
	finally:
		if f:
			f.close()
	if len(cache_list) == 0:
		print("no cache, please run search_app.py first")
		return

	# read config file
	f = None
	try:
		f = open(config_path, 'r')
		config = json.loads(f.read())
		sender = config['sender']
		password = config['password']
		receiver = config['receiver']
		app_lost_mail = config['app_lost_mail']
		app_update_mail = config['app_update_mail']
		app_cut_price_mail = config['app_cut_price_mail']
		mail_title = "App Store Reminder"
		regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
		if not re.match(regex, sender):
			raise Exception("sender is not a email address")
		if not re.match(regex, receiver):
			raise Exception("receiver is not a email address")
	except Exception as e:
		print('config.ini error')
		print(e)
		if f:
			f.close()
		sys.exit()
			

	client = api.Client()

	# test connect
	if not client.test_email_connect(sender, password):
		sys.exit()

	has_change = False
	for item in cache_list:
		app_id = item['trackId']
		country = item['country']
		new_item = client.get_app_info(app_id, country)
		if new_item == None or len(new_item) == 0:
			# app lost in appstore
			if item['available'] == True:
				item['available'] = False
				has_change = True
				content = "{} is not available in appstore any more".format(app_id)
				print(content)
				if app_lost_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)
		else:
			new_item['available'] = True
			new_item['country'] = item['country']

			if item['available'] == False:
				# app come back to appstore
				has_change = True
				content = "{} is come back to appstore".format(app_id)
				print(content)
				if app_lost_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)

			if new_item['price'] != item['price']:
				# app cut prices
				has_change = True
				content = "{} cut prices, hurry to buy!".format(new_item['trackName'])
				print(content)
				if app_cut_price_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)

			if new_item['version'] < item['version']:
				# app get a new version
				has_change = True
				content = "{} got new version!".format(new_item['trackName'])
				print(content)
				if app_update_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)

			for key in item.keys():
				item[key] = new_item[key]

	f = open(cache_path, 'w')
	f.write(json.dumps(cache_list))
	f.close()

	if not has_change:
		print(datetime.now(), "nothing changed")


if __name__ == '__main__':
	main()
