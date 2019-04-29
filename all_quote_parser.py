# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', id='navigation')
    last_page_href = divs.find_all('a')[-1].get('href')
    total_pages = last_page_href.split('/')[-1]
    return int(total_pages)


def write_csv(quotes):
    data = {'Question': quotes, 'Answer': quotes}
    df = pd.DataFrame(data, columns = ['Question', 'Answer'])
    df.to_csv('quotes_all.csv', index=False, escapechar=';')


def quote_is_ok(quote):
    if (len(quote) > 400) or (quote[0] == chr(226)) or (quote[0] == chr(45)):
        return False
    else:
	return True


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    quotes = list()
    for temp_quote in soup.find_all('div', 'quote-text-inner'):
        if temp_quote.find('p'):
            quote = temp_quote.find('p').text
            quote = str(quote.encode(encoding='UTF-8'))
            if quote_is_ok(quote):
                quotes.append(quote)
    return quotes

        
def main():

    rubrics = ['book', 'film', 'life', 'love', 'woman', 
                'friendship', 'aphorism', 'proverb', 'funny']
    base_url = "https://quote-citation.com/" 
    page_part = "page/"
	
    data_set = set()
    for rubric in tqdm(rubrics):
	rubric_part = rubric + "/"
	url = base_url + rubric_part 
	total_pages = get_total_pages(get_html(url))		
		
	rubric_data = list()
	for j in tqdm(range(1, total_pages + 1)):
	    url_gen = url + page_part + str(j) 
	    html = get_html(url_gen)
            page_data = get_page_data(html)
	    rubric_data.extend(page_data)

	    data_set.update(rubric_data)
        
    
    data = list(data_set)
    write_csv(data)

if __name__ == '__main__':
    main()
