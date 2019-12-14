import requests
from bs4 import BeautifulSoup
import csv
import time

'''
This script is for scraping song tags from last.fm(https://www.last.fm/home)

## Author: Min-Chun Shih
## Email: mcshihs@gmail.com
'''


def get_track(tags):
	'''get tracks by tags from last.fm(https://www.last.fm/home)
	args:
		tags: a list with all tags(str) want to be crawled to save in a list
	returns:
		tracks: a list, save all the song's names and artist from the tags page
	'''

	if isinstance(tags, list) == False:
		print ("tags must be a list!")
		return ""

	tracks = [["song name", "artist"]]

	for tag in tags:
		url = "https://www.last.fm/tag/"+"+".join(tag.split())+"/tracks"
		print (url)
		res = requests.get(url)
		soup = BeautifulSoup(res.text, "lxml")
		try:
			pages = int(soup.select(".pagination-page")[-1].text)
		except:
			pages = 1
		
		for page in range(1, pages+1):
			print (page)
			url = "https://www.last.fm/tag/"+"+".join(tag.split())+"/tracks?page=" + str(page)
			
			res = requests.get(url)
			soup = BeautifulSoup(res.text, "lxml")
			songs = soup.select("tbody")[0].select(".chartlist-row")
	
			for i in songs:
				song_name = i.select(".chartlist-name")[0].text.strip()
				artist = i.select(".chartlist-artist")[0].text.strip()
				print (song_name, artist)
				if [song_name, artist] not in tracks:
					tracks.append([song_name, artist])
	
			time.sleep(1)
	
	return(tracks)			



def save_file(file_name, tracks):
	'''saving file
	'''
	with open(file_name, "w") as f:
		w = csv.writer(f)
		w.writerows(tracks)



def main(file_name, tags):
	'''run the process and save the file
	'''
	tracks = get_track(tags)
	if tracks == "":
		print ("give a list for tags")
		return ""
	save_file(file_name, tracks)
	print ("Done!")





if __name__ == "__main__":
	main("data/happy.csv", ["happy", "happy song", "happiness"])
	main("data/sad.csv", ["sad", "sad song", "sad mood", "sadness"])














