import requests
from bs4 import BeautifulSoup
from get_infos import * 
import os #allows me to interact with my OS
import csv
import re #regular expression (line 72)


#save the images in a folder and a csv file containing the information
def save_product_info(book_infos, category):

	header = [u'product_page_url',
			  u'universal_product_code',
			  u'title',
			  u'price_including_tax',
			  u'price_excluding_tax',
			  u'number_available',
			  u'category',
			  u'review_rating',
			  u'image_url',
			  u'product_description',]

	header_line = ";".join(header) + '\n'
	
	
	if not os.path.isdir('./categories/' + category):
		os.mkdir('./categories/' + category) # création du répertoire
	
	#Check if category file exists
	if os.path.isfile('./categories/' + category + '/' + category +'.csv'):
	 #os.path.isfile return true if path is an existing regular file.
		with open('./categories/' + category + '/' + category + ".csv", "a",newline="", encoding="utf-8-sig") as category_file:
			
			csv_writer = csv.writer(category_file)
			
			csv_writer.writerow([
			book_infos['product_page_url'], 
			book_infos['universal_product_code'], 
			book_infos['title'], 
			book_infos['price_including_tax'], 
			book_infos['price_excluding_tax'], 
			book_infos['number_available'], 
			book_infos['product_description'], 
			book_infos['category'], 
			book_infos['review_rating'], 
			book_infos['image_url']
			])
	else:
		with open('./categories/' + category + '/' + category +".csv","a",  newline="", encoding="utf-8-sig") as category_file:
			
			csv_writer = csv.writer(category_file)
			
			csv_writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

			csv_writer.writerow([
			book_infos['product_page_url'], 
			book_infos['universal_product_code'], 
			book_infos['title'], 
			book_infos['price_including_tax'], 
			book_infos['price_excluding_tax'], 
			book_infos['number_available'], 
			book_infos['product_description'], 
			book_infos['category'], 
			book_infos['review_rating'], 
			book_infos['image_url']
			])

	response = urllib.request.urlopen(book_infos['image_url'])
	my_image = response.read()

	image_name = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,*]", "", book_infos['title'])

	with open('./categories/' + category + '/' + image_name + ".jpg", 'wb') as file:
		file.write(my_image)

			
#retrieve the URL of all books in a category and perform the pagination
def get_books_category(url_category):
	url_category_next_page = url_category
	while url_category_next_page is not None:    
		response = requests.get(url_category_next_page)

		if response.ok:

			links = []
			soup = BeautifulSoup(response.content, 'lxml')
			link_book_category = soup.find('ol', {'class': 'row'}).findAll('li')
			category = soup.find('div', {'class':'page-header action'}).find('h1')
			category = category.text


		for li in link_book_category:
			a = li.find('a')
			link = a['href']
			removed_dots = link[9:]
			book_url = ('http://books.toscrape.com/catalogue/' + removed_dots)
			links.append(book_url)
			book_infos = get_book_info(book_url)
			save_product_info(book_infos, category) #appel de ma fonction
		
		next_page = soup.find('li', {'class': 'next'})
		
		if next_page is not None:
			url_category_next_page = url_category + next_page.find('a')['href']
		else:
			break


		#print(links)
#get_books_category('https://books.toscrape.com/catalogue/category/books/romance_8/index.html')
