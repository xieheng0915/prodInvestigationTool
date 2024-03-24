import xmltojson
import json 
import requests
import re
from bs4 import BeautifulSoup as bs
import csv


# Sample URL to fetch the html page 
url = "https://experienceleague.adobe.com/en/docs/campaign-standard/using/communication-channels/push-notifications/about-push-notifications"


# Get the page through get() method 
html_response = requests.get(url=url) 

# Save the page content as sample.html 
with open("sample.html", "w") as html_file: 
	html_file.write(html_response.text)


with open("sample.html", "r") as html_file: 
  html = html_file.read() 
  soup = bs(html, "html.parser")
  json_ = {}
  json_["title"] = soup.title.string
  json_["content"] = soup.get_text().replace("\n", " ").replace("\t", " ").replace("\r", " ")
	
'''
with open("data.json", "w") as file: 
	json.dump(json_, file)


with open("data.json", "r") as file: 
  data = json.load(file)

'''

data_file = open('data.csv', 'w')
csv_writer = csv.writer(data_file)  

csv_writer.writerow(["title", "content"])
csv_writer.writerow([json_["title"], json_["content"]])
 
data_file.close()
