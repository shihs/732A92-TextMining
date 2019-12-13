from azlyrics import Song
import csv
from langdetect import detect
import time





def open_file(file_name):
    song_list = []
    with open(file_name) as f:
        for i in f.readlines()[1:]:
            row = i.split(",")
            song = row[0].strip()
            artist = row[1].strip()
            song_list.append([song, artist])
    return song_list


def save_file(file_name, save_list):
    '''saving file
    '''
    with open(file_name, "w") as f:
        w = csv.writer(f)
        w.writerows(save_list)



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
            file_name = file_name.split(".csv")[0] + "_" + str(start) + "_" + str(i+1) + "_lyrics.csv"
            save_file(file_name, song_info)
            break

        if lyrics != None:
            song_info.append([song, artist, song_url, lyrics, song_year])
        print ("--------------------------------------------")

        if count % 20 == 0:
        	print ("Sleep a minute......be patient:)............")
        	time.sleep(60)
        	print ("--------------------------------------------")
        count += 1



    file_name = "../lyrics/"+ file_name.split("/")[2].replace(".csv", "") + "_" + str(start) + "_" + str(i+1) + "_lyrics.csv"
    save_file(file_name, song_info)





if __name__ == "__main__":

	file_name = "../data/happy.csv"
	main(file_name, 601, 1000)
	# main()


    # song_url, lyrics, song_year = crawler(artist='kendrick lamar', song='humble')
    # print (song_url, lyrics, song_year)
    

