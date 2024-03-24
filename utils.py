from xml.dom.minidom import parse
from bs4 import BeautifulSoup as bs
import requests
import csv
import argparse
from pytube import YouTube
import youtube_dl
import subprocess


def  get_urls_from_sitemap(xml_file_path):
  document = parse(xml_file_path)
  for group in document.getElementsByTagName('url'):
    for node in group.childNodes:
      if node.nodeName == 'loc':
        save_html(node.firstChild.nodeValue)

def save_html(url):
  html_response = requests.get(url=url) 
  target_html = "htmls/" + url.split("/")[-1] + ".html"
  with open(target_html, "w") as html_file: 
	  html_file.write(html_response.text) 
  
def extract_data(target_html):   
    data = open(target_html)
    soup = bs(data, "lxml")
    json_ = {}
    json_["title"] = soup.title.string
    #json_["content"] = soup.get_text().replace("\n", " ").replace("\t", " ").replace("\r", " ")
    json_["content"] = walker_content(soup)
    json_["video_url"] = walker_video(soup)
    data_file = open(r'data.csv', 'a')
    csv_writer = csv.writer(data_file)  
    csv_writer.writerow([json_["title"], json_["content"], json_["video_url"]])
    data_file.close()
    
    
def walker(soup):
  elements = {}
  if soup.name is not None:
     for child in soup.children:
        childName = str(child.name)
        if childName != 'None':
           if childName not in elements:
              elements[childName] = [child]
           else:
              elements[childName].append(child)
           walker(child)
  print(elements)
  #return elements

def walker_content(soup):
   elements = {}
   for p in soup.find_all('p'):
      if p.get_text() is not None:
         if "content" not in elements:
            elements["content"] = p.get_text()
   return elements["content"]

# get video url from html file
def walker_video(soup): 
   video_url = ""
   for a in soup.find_all('a'):
      if a.get('href') is not None and "video" in a.get('href'):
        video_url = str(a.get('href')).strip().split("/?")[0]
   return video_url
        
# download video and save as mp4 file to videos folder
def video_downloader(video_url):
  ydl_opts = {
     'outtmpl': "./videos/%(title)s.%(ext)s"
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
  print("video downloaded")
  
# extract audio from video function
def convert_video_to_audio_ffmpeg(video_file, output_ext='mp3'):
   path_filename = os.path.split(video_file)
   filename, ext = os.path.splitext(path_filename[1])
   st.write("Converts video file " + path_filename[1] + " to audio file..")

   output_path = "./audiofile"
   
   subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{output_path}/{filename}.{output_ext}"],
                  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
   
   audio_file_name = output_path + "/" +filename + "." +output_ext
   return audio_file_name 


# transcribe_audio function
def transcribe_audio(audio_file, client):
  path, filename = os.path.split(audio_file)
  filename, ext = os.path.splitext(filename)

  audio_file= open(audio_file, "rb")
  transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format = "text"
  )

  outputfile = "./output/" + filename +".txt"
  st.text_area("Your Transcription:", transcript, max_chars=50)
  try:
    with open(outputfile, "w") as text_file:
        text_file.write(transcript)
  except:
    print("Error writing to file")

# clean all the folders
def clean_files():
   return 