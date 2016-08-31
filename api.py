#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	appstore api
#
############################################################
import os,sys
import requests
import json
import urllib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

class Client():
	def __init__(self):
		self.session = requests.Session()
		self.session.headers = headers

	################################
	# get app info
	# @param 	app_id 		app track id in appstore
	# @param 	country		country code
	# @return 	app info
	#################################
	def get_app_info(self, app_id, country):
		response = self.session.get('https://itunes.apple.com/lookup?id={}&country={}'.format(app_id, country))
		data = json.loads(response.content.decode('utf-8'))
		# -- main keys --
		# trackId
		# trackName
		# price
		# formattedPrice
		# version
		# bundleId
		# releaseDate
		# currentVersionReleaseDate
		# fileSizeBytes
		try:
			return data['results'][0]
		except Exception as e:
			if 'errorMessage' in data:
				print('errorMessage', data['errorMessage'])
			else:
				print(e)

	################################
	# search app
	# @param 	keyword 	search keyword
	# @param 	max_count	allow max data
	# @return 	app info list
	#################################
	def search_app(self, keyword, country, max_count):
		# keyword = urllib.parse.urlencode(keyword)
		response = self.session.get('https://itunes.apple.com/search?term={}&country={}&media=software'.format(keyword, country))
		data = json.loads(response.content.decode('utf-8'))
		try:
			return data['results'][:max_count]
		except Exception as e:
			if 'errorMessage' in data:
				print('errorMessage', data['errorMessage'])
			else:
				print(e)

	def test_email_connect(self, sender, password):
		success = False
		try:
			smtp_address = "smtp.{}".format(sender.split("@")[1])
			smtp = SMTP_SSL(smtp_address)
			smtp.login(sender, password)
			print('email login successfully')
			success = True
		except Exception as e:
			print('email login fail')
			print(e)
		finally:
			smtp.close()
		return success

	def send_email(self, sender, password, receiver, title, content):
		try:
			smtp_address = "smtp.{}".format(sender.split("@")[1])
			msg = MIMEText(content,'plain','utf-8')
			msg['Subject'] = Header(title, 'utf-8')
			msg["from"] = sender
			msg["to"] = receiver
			smtp = SMTP_SSL(smtp_address)
			# smtp.set_debuglevel(1)
			# smtp.ehlo(sender)
			smtp.login(sender, password)
			smtp.sendmail(sender, receiver, msg.as_string())
			print('email send successfully')
		except Exception as e:
			print('send email fail')
			print(e)
		finally:
			smtp.close()
