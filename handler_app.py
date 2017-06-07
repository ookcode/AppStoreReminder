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
	cache_path = os.path.join(root_path, "handler.json")
	config_path = os.path.join(root_path, "config.ini")

	# read cache file
	f = None
	try:
		f = open(cache_path, 'r', encoding='utf-8')
		content = f.read()
		f.close()
		cache_list = json.loads(content)
	except Exception as e:
		print("read handler.json error")
		return

	# read config file
	allow_email = False
	try:
		f = open(config_path, 'r')
		content = f.read()
		f.close()
		config = json.loads(content)
		sender = config['sender']
		password = config['password']
		receiver = config['receiver']
		app_lost_mail = config['app_lost_mail']
		app_update_mail = config['app_update_mail']
		app_cut_price_mail = config['app_cut_price_mail']
		mail_title = "App Store Reminder"
		regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
		if not re.match(regex, sender):
			raise Exception("'sender' is not a email address")
		if not re.match(regex, receiver):
			raise Exception("'receiver' is not a email address")
		allow_email = True
	except Exception as e:
		print('read config.ini error:', e)
		print('script will not send email for you.')
			
	client = api.Client()

	# test connect
	if allow_email and not client.test_email_connect(sender, password):
		sys.exit()

	has_change = False
	for item in cache_list:
		app_id = item['trackId']
		country = item['country']
		trackName = item['trackName']
		new_item = client.get_app_info(app_id, country)
		now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if new_item == None or len(new_item) == 0:
			# app lost in appstore
			if item['available'] == True:
				item['available'] = False
				has_change = True
				content = "{} {} is not available in appstore any more".format(now_time, trackName)
				print(content)
				if allow_email and app_lost_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)
		else:
			new_item['available'] = True
			new_item['country'] = item['country']

			if item['available'] == False:
				# app come back to appstore
				has_change = True
				content = "{} {} is come back to appstore".format(now_time, trackName)
				print(content)
				if allow_email and app_lost_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)

			elif new_item['price'] != item['price']:
				# app cut prices
				has_change = True
				content = "{} {} cut prices, hurry to buy!".format(now_time, new_item['trackName'])
				print(content)
				if allow_email and app_cut_price_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)

			elif new_item['version'] < item['version']:
				# app get a new version
				has_change = True
				content = "{} {} got new version!".format(now_time, new_item['trackName'])
				print(content)
				if allow_email and app_update_mail == True:
					client.send_email(sender, password, receiver, mail_title, content)

			for key in item.keys():
				item[key] = new_item[key]

			if not has_change:
				print(now_time, trackName, "has not changed")

	f = open(cache_path, 'w')
	f.write(json.dumps(cache_list))
	f.close()

if __name__ == '__main__':
	main()
