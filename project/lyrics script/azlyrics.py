import requests
from bs4 import BeautifulSoup
import bs4 
import time
import re
import unicodedata
import csv
import random
import json
from tools import transfer_text
from langdetect import detect

# reference 
# https://github.com/brianchesley/Lyrics
# https://github.com/elmoiv/azapi


class Requester():

    USER_AGENTS = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36']

    def __init__(self):
        self.proxies = {}

    def get_request(self, url, user_agent=True):
    
        if user_agent:
            return requests.get(url, headers={'User-Agent': random.choice(self.USER_AGENTS)}, proxies=self.proxies)
        return requests.get(url, proxies=self.proxies) 




class Song(Requester):
    '''getting the information of a song. The song page url, song lyrics, the year of the song(album)
    '''

    def __int__(self, song, artist, proxies=None):
        self.song = song
        self.artist = artist
        self.proxies = proxies 
        # self.url = 'http://www.azlyrics.com'

    def get_song_page(self, song, artist):
        song = transfer_text(song)

        # "The" always been delete for artist name in song page link
        if artist[:4] == "The ":
            artist = artist[4:]

        artist = transfer_text(artist)
        song_url = "https://www.azlyrics.com/lyrics/"+artist+"/"+song+".html"

        return song_url


    # def get_soup(self, song, artist):
        # song_url = self.get_song_page(song, artist)
    def get_soup(self, song_url, try_times = 10):
        '''get the connection of the song page
        args: 
            song_url: the url of the song
            try_times: the trying time for connecting if the connection is fail
        return:
            soup: the Beautiful aboject for the song page
        '''

        # sleep is necessary! or got banned easily
        time.sleep(random.randint(10, 15))
        trying = 0
        while trying < try_times:
            try:
                trying += 1
                res = self.get_request(song_url)
                print("HTTP status code is " + str(res.status_code))

                # the song page is not existing
                if res.status_code == 404:
                    return None
                # you are banned! you will need to wait couple hours or change your ip address
                if res.status_code == 403:
                    return "Banned!"

                # if can't connect for some reason? retry for 10 times
                if res.status_code != 200:
                    if trying > try_times:
                        return None
                    time.sleep(30)
                    continue

                soup = BeautifulSoup(res.text, "lxml")
                return soup
            except:
                continue

        


    def get_lyrics(self, soup):
        # get the lyrics for the song
        try:
            lyrics = soup.select(".col-xs-12")[1].select("div")[5].text.strip()
        except:
            lyrics = None

        return(lyrics)
	

    def get_song_year(self, soup):
        # get album year for the song
        try:
            # the class for the whole album
            album_div = soup.find('div', {"class":"songlist-panel"})
            # delete child tags text
            for child in album_div.find_all('a'):
                child.decompose()
            for child in album_div.find_all('b'):
                child.decompose()
            # year is in the remaining text
            year = album_div.get_text().replace("album:", "").strip()[1:5]
            # print (year)
        except:
            year = ""
        return year



### test
# api = Song()
# # song_url = api.get_song_page(artist='Mary Juane Clair', song='The Gentle Rain')
# song_url = api.get_song_page(artist='kendrick lamar', song='humble')
# print (song_url)
# api.get_soup(song_url)
# soup = api.get_soup(song_url)
# print (api.get_lyrics(soup))
# print (api.get_song_year(soup))


