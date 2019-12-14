from azlyrics import Song
import csv
from langdetect import detect
import time
import os
from os import listdir





def open_file(file_name):
    '''save the song and artist data to a list
    args:
        file_name: string, the name of the file
    return:
        song_list: list, save all the song and artist in the file
    '''
    song_list = []
    with open(file_name) as f:
        for i in f.readlines()[1:]:
            row = i.split(",")
            song = row[0].strip()
            artist = row[1].strip()
            song_list.append([song, artist])
    return song_list


def save_file(file_name, save_list):
    '''saving the final result list
    '''
    with open(file_name, "w") as f:
        w = csv.writer(f)
        w.writerows(save_list)


def crawled_songs(path, keyword):
    urls = []
    files = [file for file in listdir(path) if file.startswith(keyword)]
    # print (files)
    for file in files:
        with open(path + file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                urls.append(row[2])
    return urls






# def crawler(song, artist):
#     api = Song()
#     song_url = api.get_song_page(song, artist)
#     # print (song_url)
#     soup = api.get_soup(song_url)
#     # print (soup)
#     if soup == None:
#         return None, None, None

#     lyrics = api.get_lyrics(soup)
#     song_year = api.get_song_year(soup)

#     return song_url, lyrics, song_year



def main(file_name, start, end):
    '''run the crawling process
    args:
        file_name: string, the name of file with song and artist data
        start: integer, the number of the start (index + 1) for crawling song
        end: integer, the number of the end (index + 1) for crawling song. If end = -1, it will crawl from start to the end
    '''
    
    # open the song list file
    song_list = open_file(file_name)

    # song_info saves the information for the songs, which will be saved
    song_info = [["song", "artist", "url", "lyrics", "year"]]
    if end == -1:
        end = len(song_list)
    num_song = end - start + 1    	
    print ("There are " + str(num_song) + " songs!")
    print ("=======================================")

    count = 1


    for i in range(start-1, end):

        print (str(i-start+2) + " song is getting lyrics......")
        song = song_list[i][0]
        artist = song_list[i][1]
        print (song + " - "+  artist)

        # detect if the song is english. 
        # only guess from the song name, it can be wrong, just fast checking
        # update: found out the detect() skips many english song's names :((
        # but if find any better library, the code can be replaced here!
        # better not sending too many requests!
        # if detect(song) != "en":
        # 	continue
        
        try:
            # url, lyrics, year = crawler(song, artist)
            api = Song()

            song_url = api.get_song_page(song = song, artist = artist)
            print (song_url)
            soup = api.get_soup(song_url)
            if soup == None:
                print ("--------------------------------------------")
                continue
            if soup == "Banned!":
            	break

            lyrics = api.get_lyrics(soup)
            song_year = api.get_song_year(soup)
            # print (song_url, lyrics, song_year)
        
        except:
            file_name = "../lyrics/"+ file_name.split("/")[2].replace(".csv", "") + "_" + str(start) + "_" + str(i+1) + "_lyrics.csv"
            save_file(file_name, song_info)
            break

        if lyrics != None:
            song_info.append([song, artist, song_url, lyrics, song_year])
        print ("--------------------------------------------")

        # avoid being banned QQ
        if count % 20 == 0:
        	print ("Sleep a minute......be patient:)............")
        	time.sleep(60)
        	print ("--------------------------------------------")
        count += 1


    # saving file name: "[mood]_[start]_[end]_lyrics.csv"
    # it's quite easy to be banned... so record the start and end index for every saving file
    file_name = "../lyrics/"+ file_name.split("/")[2].replace(".csv", "") + "_" + str(start) + "_" + str(i+1) + "_lyrics.csv"
    save_file(file_name, song_info)









if __name__ == "__main__":

	file_name = "../data/happy.csv"
	main(file_name, 1501, -1)
	# final_check("happy")
	



