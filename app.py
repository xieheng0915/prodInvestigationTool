from  utils import *
import os
from bs4 import BeautifulSoup as bs

# get all urls from sitemap.xml and save to html files
#get_urls_from_sitemap('sitemap.xml')

# clear data.csv, write file headers
with open(r'data.csv', 'w') as data_file:
  csv_writer = csv.writer(data_file)
  csv_writer.writerow(["title", "content", "video_url","video_description"])


# extract data from html files and save to data.csv
for path, subdirs, files in os.walk('htmls'):
  for file in files:
    extract_data(os.path.join(path, file))


# download videos and extract audio, convert to text and add to data.csv


# clean all the files







