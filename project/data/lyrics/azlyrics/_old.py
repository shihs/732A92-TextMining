# def get_agent():
# 	with open("agent.txt", "r") as f:
# 		return f.read().split("\n")

# https://getproxylist.com
# def get_proxy():
# 	url = "https://api.getproxylist.com/proxy"
# 	res = requests.get(url)
# 	js = json.loads(res.text)
# 	ip = js["ip"]

# 	while True:
# 		http = js["protocol"]
# 		if http in ["http", "https"]:
# 			break

# 	return ({http:http+"://"+ip})


# https://www.proxy-list.download/api/v1
# def get_proxy():
# 	url = "https://www.proxy-list.download/api/v1/get?type=http"
# 	res = requests.get(url)
# 	http = res.text.split("\r\n")[:-1]

# 	url = "https://www.proxy-list.download/api/v1/get?type=https"
# 	res = requests.get(url)
# 	https = res.text.split("\r\n")[:-1]

# 	return(http, https)
	





def get_requests(song, artist, user_agents = False, proxy = False):
	
	url = "https://www.azlyrics.com/lyrics/"+artist+"/"+song+".html"
	print (url)

	while True:
		headers = {
			'User-Agent': random.choice(user_agents)
		}
		
		proxy = {
			"http":"http://"+random.choice(http), 
			"https":"https://"+random.choice(https) 
		}

		print (proxy)
		try:
			res = requests.get(url, headers = headers, proxies = proxy, timeout = 30)
			print (res)
		except:
			print ("QQ....Bannedddddd")
			time.sleep(10)
			continue
		
		if res.status_code == 200:
			break

		time.sleep(120)

	soup = BeautifulSoup(res.text, "lxml")

	return(soup, url)


def transfer_text(text):
	'''Transfer the text format. Delete all text except alphabet and numbers, 
		and transfer all latin alphabet to english alphabet. Becasue this is how the link needed.
	
	args:
		text: string, the text that wants to be transfer
	retrun:
		link_text: string, the transfered format
	'''
	# only keep alphabet and numbers
	combine = re.sub('[^A-Za-z0-9]', '', text).lower()
	# transfer latin alphabet to english alphabet
	link_text = ''.join(char for char in unicodedata.normalize('NFKD', combine) if unicodedata.category(char) != 'Mn')
	return link_text



def get_lyrics(song, artist, user_agents = False, proxy = False):
	'''get lyrics and album year from https://www.azlyrics.com/
	args:
		song: string, the song name
		artist: string, the name of the singer

	return:
		url: the url of the song lyrics
		lyrics: the lyrics of the song
		year: the year of the song(album) released

	'''

	# transform song and artist to link form
	song = transfer_text(song)
	artist = transfer_text(artist)
	soup, url = get_requests(song, artist, user_agents, http, https)

	# get the lyrics
	try:
		lyrics = soup.select(".col-xs-12")[1].select("div")[5].text.strip()
	except:
		return None, None, None
	
	# get album year
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

	return url, lyrics, year


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







def main(file_name):

	# user_agents = get_agent()
	# http, https = get_proxy()

	# open the song list file
	song_list = open_file(file_name)
	# song_info saves the information for the songs, which will be saved
	song_info = [["song", "artist", "url", "lyrics", "year"]]
	num_song = len(song_list)
	
	print ("There are " + str(num_song) + " songs!")

	for i in range(num_song):
		print (str(i+1) + " song is getting lyrics......")
		song = song_list[i][0]
		artist = song_list[i][1]
		url, lyrics, year = get_lyrics(song, artist, user_agents = False, proxy = False)
		# print (url, lyrics, year)
		if url != None:
			song_info.append([song, artist, url, lyrics, year])

		time.sleep(random.randint(1, 5))

		if (i+1)%20 == 0:
			time.sleep(60)

	file_name = file_name.split(".csv")[0] + "_lyrics.csv"
	save_file(file_name, song_info)




user_agents = get_agent()
http, https = get_proxy()
song = "gravity"
artist = "johnmayer"
url, lyrics, year = get_lyrics(song, artist, user_agents, http, https)
print (lyrics)

# file_name = "data/sad.csv"
# main(file_name)
# file_name = "data/happy.csv"
# main(file_name)

# main()