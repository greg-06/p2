import requests
from bs4 import BeautifulSoup
import urllib.request 


#retrieves information from the url of a book
def get_book_info(url_product):
	
	response = requests.get(url_product)

	if response.ok:
		soup = BeautifulSoup(response.content, 'lxml') 

		#title
		bookTitle = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1')
		
		#extract some data
		infos = [] 
		all_tr = soup.findAll('tr')
		
		for tr in all_tr:
			td = tr.find('td')
			infos.append(td.text)
			
		universal_product_code = infos[0]
		price_excluding_tax = infos[2]
		price_including_tax = infos[3]
		number_available = infos[5]			
	
		#product_description
		if soup.find('div', id = 'product_description') is not None: #Add the description if it exists
			description = soup.findAll('p')[3].text
		else:
			description = ""

		#category
		category = soup.find('ul', {'class': 'breadcrumb'}).select('a')[2]		
		
		#review_rating
		star_rating = soup.find('div',{'col-sm-6 product_main'}).findAll('p')[2]['class']

		#image_url
		image_url = soup.find('div', {'class': 'item active'}).select('img')[0]['src']		
		
		removed_dots = image_url[6:]
		final_image_page_url = str('http://books.toscrape.com/' + removed_dots)	

		#dictionary
		book_infos = {
		'product_page_url': url_product,
		'universal_product_code': universal_product_code,
		'title': bookTitle.text,
		'price_including_tax': price_including_tax,
		'price_excluding_tax': price_excluding_tax,
		'number_available': number_available,
		'product_description': description,
		'category': category.text,
		'review_rating': star_rating[1],
		'image_url': final_image_page_url
		}
		
		return book_infos

#info = get_book_info('https://books.toscrape.com/catalogue/unicorn-tracks_951/index.html') 
#print(info)
