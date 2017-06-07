#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	search app and add to handler list
#
############################################################
import os,sys
import json
import api

def main():
	root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	cache_path = os.path.join(root_path, "handler.json")
	f = None
	try:
		f = open(cache_path, 'r', encoding='utf-8')
		cache_list = json.loads(f.read())
	except Exception as e:
		cache_list = []
	finally:
		if f:
			f.close()
	client = api.Client()
	print("America = us, China = cn, Japan = jp ...")
	print("-" * 60)
	country = input("please choose country: ")
	country = country.strip()
	while True:	
		keywords = input("please input app name to search: ")
		print("searching...")
		data = client.search_app(keywords, country, 10)
		if data == None or len(data) == 0:
			print("404 not found")
			continue
		print("-" * 60)
		format_str = "%-5s%-15s%-10s%-10s%-10s%s"
		print(format_str % ("", "APPID", "VERSION", "APPSIZE", "PRICE", "APPNAME"))
		for index, item in enumerate(data):
			size = int(item['fileSizeBytes']) / 1024 / 1024
			size_str = "%.2fMb" % size
			app_name = item['trackName']
			if len(app_name) > 20:
				app_name = app_name[:20] + "..."
			print(format_str % (str(index), item['trackId'], item['version'], size_str, item['formattedPrice'], app_name))
		print("-" * 60)
		select = input("please select one to save: ")
		try:
			select_index = int(select)
			select_item = data[select_index]
			save_data = {}
			save_data['trackName'] = select_item['trackName']
			save_data['trackId'] = select_item['trackId']
			save_data['version'] = select_item['version']
			save_data['price'] = select_item['price']
			save_data['available'] = True
			save_data['country'] = country
			cache_list.append(save_data)
			content = json.dumps(cache_list, indent=4, sort_keys=True, ensure_ascii=False)
			f = open(cache_path, 'w', encoding='utf-8')
			f.write(content)
			f.close()
			print("{} save finished, you can run handler_app.py to handle app changes\n\n".format(select_item['trackId']))
		except Exception as e:
			print("input error ", e)
			continue


if __name__ == '__main__':
	main()
