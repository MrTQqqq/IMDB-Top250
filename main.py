import requests
from bs4 import BeautifulSoup
import json
import string

# 请求地址
def request_url(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36'}
		response = requests.get(url, headers = headers)
		response.encoding = 'GBK'
		if response.status_code == 200:
			return response.text
	except requests.RequestException:
		print("CODE ERROR")
		return None


# 写入文件
def write_to_txt(item):
	print("write to file =======>")
	with open('list.txt', 'a', encoding = 'UTF-8') as f:
		print(json.dumps(item, indent = 4, ensure_ascii = False))
		f.write(json.dumps(item, indent = 4, ensure_ascii = False))



# 整理top250网页信息
def tiny_base_web_info(soup):
	infos = soup.find(class_ = 'list').find_all('li')
	ret = []
	for info in infos:
		movie_info = {}
		movie_info['address'] = str(info.a['href']) 
		movie_info['name'] = str(info.find('a').text)
		ret.append(movie_info)
	return ret


def tiny_each_movie_web(soup):
	infos = soup.find(class_ = 'box').find(id = 'endText').find('table').find('tbody')
	ret = []
	download_info = {}
	for info in infos:
		if info.find('a') and info.find('a') != -1 and info.find('td').text != '' and info.find('a')['href'] != '':
			download_info[info.find('td').text] = info.find('a')['href']
	return download_info

	
	


# 根据下载地址获取种子链接
def get_linkaget(movie_list):
	for info in movie_list:
		url = info['address']

		html = request_url(url)
		soup = BeautifulSoup(html, 'lxml')

		download_info = tiny_each_movie_web(soup)

		data = {}
		data['name'] =  info['name']
		data['address'] = info['address']
		data['download_info'] = download_info
		
		write_to_txt(data)





def main(page):
	# 6vhao的地址很诡异，第一页的地址和后面的不一样，不能直接用 index_1
	if page == 1:
		url = 'http://www.hao6v.net/s/gf250/index.html'
	else:
		url = 'http://www.hao6v.net/s/gf250/index_' + str(page) + '.html'

	html = request_url(url)
	soup = BeautifulSoup(html, "lxml")
	# 整理top250网页信息
	result = tiny_base_web_info(soup)
	# 获取磁链
	get_linkaget(result)




if __name__ == '__main__':
	# 清空文件夹
	with open('list.txt', 'a', encoding = 'UTF-8') as f:
		f.truncate(0)
	# 每一页只显示25个,这个数据按理应该取网页上的，但是因为获取的是top250就写死了
	for i in range(1,11):
		main(i)




