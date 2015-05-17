# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2,re,json
import time
import os



def query_movie_info(Moive_Title):
    movieurlbase = "http://api.douban.com/v2/movie/search"
    DOUBAN_APIKEY = "0bb9e4f945380805232daeebcfa8180f"  # 这里需要填写你自己在豆瓣上申请的应用的APIKEY
    movieinfo = Moive_Title
    searchkeys = urllib2.quote(movieinfo.encode("utf-8"))  # 如果Content中存在汉字，就需要先转码，才能进行请求
    url = '%s?q=%s&apikey=%s' % (movieurlbase, searchkeys, DOUBAN_APIKEY)
    resp = urllib2.urlopen(url)
    movie = json.loads(resp.read())
    return movie


# DB QUERY BASED NAMES
def DBquery_movie_rate(Moive_Title):
	movieurlbase = "http://api.douban.com/v2/movie/subject/"
	DOUBAN_APIKEY = "0bb9e4f945380805232daeebcfa8180f"  # 这里需要填写你自己在豆瓣上申请的应用的APIKEY
	id = query_movie_info(Moive_Title)
	if id["subjects"] == []:
		return 0, []
	url = '%s%s?apikey=%s' % (movieurlbase, id["subjects"][0]["id"], DOUBAN_APIKEY)
	resp = urllib2.urlopen(url)
    
	description = json.loads(resp.read())
	rate = description["rating"]["average"]
	
	
	movie_url = "http://movie.douban.com/subject/"+id["subjects"][0]["id"]
	
    
	return rate, movie_url
	


# IMDB QUERY BASED NAMES
def IMquery_movie_rate(Moive_Title):
	movie_search = '+'.join(Moive_Title.split())
    
	base_url = 'http://www.imdb.com/find?q='
	url = base_url+movie_search+'&s=all'
	html = urllib2.urlopen(url).read()
	match = re.findall('<a href="(.+?)" >',html)
	#print match
	match = match[0]
	movid_id = re.split(r'/',match)[2]
	if not re.match('^tt[0-9]+$',movid_id):
		return 0, []

	url_base = 'http://www.imdb.com/title/'
	movie_url = url_base+movid_id
	html_movie = urllib2.urlopen(movie_url).read()
	soup = BeautifulSoup(html_movie)
	tt = soup.findAll('div', attrs={'class': 'titlePageSprite star-box-giga-star'})
	if tt == []:
		score = 0
	else:
		score = (tt[0].get_text().split()[0])
	
	return score, movie_url



def parsing_html(html_base,IMDB_query, DB_query):
	infor_movie = {}
	soup = BeautifulSoup(html_base)
	struc_name = soup.findAll('title')
	name_info = struc_name[0].get_text()
	name_info = name_info.split('cinemaonline.sg: ')
	movie_name = ' '.join(name_info[1].split())
	infor_movie['name'] = movie_name.encode('utf8')    # parsing movie name

	score_im, url_im = IMDB_query(infor_movie['name'])
	score_db, url_db = DB_query(infor_movie['name'])
	infor_movie['IM_rating'] = score_im
	infor_movie['DB_rating'] = score_db
	infor_movie['IM_url'] = url_im
	infor_movie['DB_url'] = url_db
	largeinfo = soup.find('div', attrs={'class': 'section_content'})
	tableinfor = largeinfo.find("table")
	infor = tableinfor.findAll('td')
	link = infor[0].find('img')['src']   
	infor_movie['pic'] = link          #parsing movie name
	text = infor[2].renderContents()   #information
	text = re.split('</b>: ', text)
	num_llist = [1,2,3,4,5,9]
	name = ['Language','Classification','Release Date', 'Genre','Running Time','Format']
	for index, i in enumerate(num_llist):
		infor = " ".join(re.split('<br/>', text[i])[0].split())
		infor_movie[name[index]] = infor

	return infor_movie




# RETURN A LIST OF DICTIONARIES CONTAINING MOVIES' INFORMATION
def query_moive_onshow(moive_url,IMDB_query, DB_query):
	html_base = urllib2.urlopen(moive_url).read()
	soup = BeautifulSoup(html_base)
	movie_links = soup.findAll('tr', attrs={'style': 'vertical-align: top'})
	movies_inf = []
	
	url_tickets = 'http://www.popcorn.sg/incinemas'
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url_tickets,headers=hdr)
	html_tickets = urllib2.urlopen(req).read()
	soup_tickets = BeautifulSoup(html_tickets)
	tickets = soup_tickets.find_all('div', attrs={'class': 'col-xs-6 col-sm-3 col-md-3'})
	movienames = []
	web_tickets = []
	for ticket in tickets:
		name = ' '.join(ticket.get_text().split())
		movienames.append(name)
		url = "http://www.popcorn.sg/" + ticket.find('a', href=True)['href']
		web_tickets.append(url)


	for movie_link in movie_links:
		link_pre = movie_link.findAll('a', href=True)
		link_final = link_pre[0]['href']
		url_base = 'http://www.cinemaonline.sg/movies/'
		link_final = url_base+link_final
		html_movie = urllib2.urlopen(link_final).read()
		movie_struc = parsing_html(html_movie,IMDB_query,DB_query)
		
		if movie_struc['name'] in movienames:
			movie_struc['ticket'] = web_tickets[movienames.index(movie_struc['name'])]
			movies_inf.append(movie_struc)
		else:
			continue

	#print movie_names
	return movies_inf







#HTML GENERATEING (BASED ON THE RATING)
def movie_post_generate(movie_list):
	time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	time_now = time_now+'.html'
	
	post_path = time_now
	post = open(post_path,'w')

	filepath = 'html_init'
	file_read = open(filepath,'r')
	for line in file_read.readlines():
		post.write(line)
	

	filepath = 'html_temp'
	file_read = open(filepath,'r')
	temp = file_read.readlines()
	#print temp
	#movie = movie_list[1]
	for movie in movie_list:
		score_im = float(movie['IM_rating'])
		score_db = float(movie['DB_rating'])
		if (score_im>7.0) or (score_db>7.0):
			temp_curr = temp[:]
			row_h = [3,4,5,6,7,10]
			namelist = ['Running Time','Release Date', 'Language','Genre','Format','ticket']
			for index,i in enumerate(row_h):
				temp_curr[i] = re.sub('ruiruicool', movie[namelist[index]],temp_curr[i])
			row_h2 = [1,2,8,9]
			namelist2 = ['pic','pic','name', 'Classification','IM_url','IM_rating','DB_url','DB_rating']
			
			for index,i in enumerate(row_h2):
				temp_curr[i] = re.sub('ruiruicool',str(movie[namelist2[int(index*2)]]),temp_curr[i])
				temp_curr[i] = re.sub('ruicool',str(movie[namelist2[int(index*2+1)]]),temp_curr[i])
			for line in temp_curr:
				post.write(line)
		else:
			continue
		

	filepath = 'html_end'
	file_read = open(filepath,'r')
	for line in file_read.readlines():
		post.write(line)

	post.close()


movie_url = 'http://www.cinemaonline.sg/movies/nowshowing.aspx'

movie_list = query_moive_onshow(movie_url,IMquery_movie_rate,DBquery_movie_rate)
movie_post_generate(movie_list)


