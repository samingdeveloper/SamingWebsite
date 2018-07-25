'''import urllib.parse
import requests

ywc_api = "https://ywc15.ywc.in.th/api/interview"

json_data = requests.get(ywc_api).json()

for i in json_data:
	print("asd")

print()
print(json_data)'''

import urllib.request
import json
ywc_api = "https://ywc15.ywc.in.th/api/interview"

response = urllib.request.urlopen(ywc_api).read()
json_obj = str(response,'utf-8')
data = json.loads(json_obj)



def search(first_name):
	for item in data:
		if item['interviewRef'] == 'PG42':
			return item

print(search('PG43'))