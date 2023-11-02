import requests
import json
import os
from bs4 import BeautifulSoup
from fake_headers import Headers
from Logger_2 import logger

headers_gen = Headers(os='win', browser='chrome')

def connect(url, headers):
    main=requests.get(url, headers=headers)
    return main

url_hh='https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&ored_clusters=true&area=2&hhtmFrom=vacancy_search_list'
main_hh=connect(url_hh, headers=headers_gen.generate())

main_soup=BeautifulSoup(main_hh.text,'lxml')

articles_tags=main_soup.find_all(class_='vacancy-serp-item__layout')
parsed_data = []
def get_articles():
    paths=('log_1.log', 'log_2.log', 'log_3.log')
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def get_article():
            for article_tag in articles_tags:
                title_tag=article_tag.find(class_='serp-item__title')
                link=title_tag["href"]
                salary = article_tag.find('span', class_='bloko-header-section-2')
                if salary is not None:
                    salary=salary.text
                else:
                    salary=''
                city=article_tag.find('div', attrs={"data-qa": 'vacancy-serp__vacancy-address'}).text
                company = article_tag.find('div', class_='vacancy-serp-item__meta-info-company').text

                parsed_data.append({
                    'link': link,
                    "salary": salary.replace("\u202f", ""),
                    "company": company.replace("\xa0", " "),
                    'city': city
                })
            return parsed_data
        get_article()

if __name__ == '__main__':
    get_articles()
    with open("parsed.json", "w", encoding="utf8") as file:
        json.dump(parsed_data, file, ensure_ascii=False, indent=2)