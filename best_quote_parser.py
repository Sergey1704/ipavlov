# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from operator import itemgetter
import sys


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
    filename = 'quotes_' + str(len(quotes)) + '.csv'
    df.to_csv(filename, index=False, escapechar=';') 


def quote_is_ok(quote):
    if (len(quote) > 400) or (quote[0] == chr(226)) or (quote[0] == chr(45)):
        return False
    else:
	return True


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    quotes = dict()
    for temp_quote in soup.find_all('div', 'quote'):
        quote_text = '-'
        quote_score = 0
        if temp_quote.find('div', 'quote-text-inner'):
            quote_text = temp_quote.find('div', 'quote-text-inner')
            if quote_text.find('p'):
                quote_text = quote_text.find('p').text
                quote_text = str(quote_text.encode(encoding='UTF-8'))
        if temp_quote.find('div', 'rating-score'):
            quote_score = temp_quote.find('div', 'rating-score').text
	    quote_score = int(quote_score)
        if quote_is_ok(quote_text):
            quotes.update({quote_text: quote_score})
    return quotes


def top_quotes(data, n):
    sorted_data = sorted(data.items(), key=itemgetter(1), reverse=True)
    top_data = dict(sorted_data[0:n])
    return list(top_data.keys())

        
def main():

    rubrics = ['life']
    base_url = "https://quote-citation.com/" 
    page_part = "page/"
    n_quotes = int(sys.argv[1])
	
    data_set = dict()
    for rubric in tqdm(rubrics):
	rubric_part = rubric + "/"
	url = base_url + rubric_part 
	total_pages = get_total_pages(get_html(url))		
		
	rubric_data = dict()
	for j in tqdm(range(1, total_pages + 1)):
	    url_gen = url + page_part + str(j) 
	    html = get_html(url_gen)
            page_data = get_page_data(html)
	    rubric_data.update(page_data)

	    data_set.update(rubric_data)


    quotes = top_quotes(data_set, n_quotes)
    write_csv(quotes)

if __name__ == '__main__':
    main()
