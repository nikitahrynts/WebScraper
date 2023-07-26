import os
import shutil
import string

import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://www.nature.com'
WEBSITE_URL = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
list_of_articles = list()


def extract_links(pages_number, articles_type):
    for page_number in range(pages_number):
        request = requests.get(WEBSITE_URL + f'&page={page_number + 1}')

        if request.status_code == 200:
            soup = BeautifulSoup(request.content, 'html.parser')

            if os.access(f'./Page_{page_number + 1}', os.F_OK):
                print('Ok')
                shutil.rmtree(f'./Page_{page_number + 1}')
            os.mkdir(f'./Page_{page_number + 1}')

            articles = soup.find_all('article')
            for article in articles:
                article_type = article.find('span', attrs={'c-meta__item'}).text
                if article_type == articles_type:
                    list_of_articles.append(article.find('a').get('href'))

            search_for_details(page_number)
            list_of_articles.clear()
        else:
            print('URL is incorrect!')

    print('Saved all articles.')


def search_for_details(page_number):
    for article in list_of_articles:
        request = requests.get(DOMAIN + article)

        if request.status_code == 200:
            soup = BeautifulSoup(request.content, 'html.parser')

            article_title = (soup.find('title')
                             .text
                             .translate(str.maketrans('', '', string.punctuation))
                             .replace(' ', '_')
                             .strip())

            if soup.find('p', {'class': 'article__teaser'}) is None:
                article_content = ''
            else:
                article_content = (soup.find('p', {'class': 'article__teaser'})
                                   .text
                                   .strip())

            file = open(f'./Page_{page_number + 1}/' + article_title + '.txt',
                        mode='w',
                        encoding='UTF-8')
            file.write(article_content)
            file.close()
        else:
            print('URL is incorrect!')


number_of_pages = int(input())
type_of_articles = input()
extract_links(number_of_pages, type_of_articles)
