import requests
from bs4 import BeautifulSoup
from data_category import *
import urllib.request


#create a directory and retrieve the csv + images of all books in all categories
def get_url_categories(url_categories):
	if not os.path.isdir('./categories'):
		os.mkdir('./categories')

	response = requests.get(url_categories)

	if response.ok:
		links = []
		soup = BeautifulSoup(response.content, 'lxml')
		url_categories_book = soup.find('div', {'class': 'side_categories'}).findAll('li')[1:]
	
	
	for li in url_categories_book:
		a = li.find('a')
		link = a['href']
		removed_dots = link[0:]
		url_category = 'https://books.toscrape.com/' + removed_dots.replace('index.html','')
		get_books_category(url_category)
		
		
get_url_categories('https://books.toscrape.com')
