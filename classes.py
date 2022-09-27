from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

class Superjob(Engine):
    def __init__(self, search):
        self.search = search
        self.HOST = 'https://russia.superjob.ru'
        self.URL = 'https://russia.superjob.ru/vacancy/search/'
        self.HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84'}

    def get_request(self, url, params=''):
        r = requests.get(url, headers= self.HEADERS, params=params)
        return r

    def get_content(self, html):
        vacancies = []
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='f-test-search-result-item')
        for item in items:
            try:
                item1 = item.find('div', class_='_8zbxf f-test-vacancy-item _3HN9U hi8Rr _3E2-y _1k9rz'). \
                    find('div', class_='_2lp1U _2J-3z _3B5DQ')
                item2 = item1.find_all('div', class_='_3gyJS')
                name = item2[3].find('div', class_='_2J-3z _3B5DQ').find('div', class_='_3gyJS'). \
                    find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').find('a').get_text()
                href = item2[3].find('div', class_='_2J-3z _3B5DQ').find('div', class_='_3gyJS'). \
                    find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').find('a').get('href')
                Description = item2[10].find('div', class_='_2d_Of _2J-3z _3B5DQ').find('div', class_='_3gyJS'). \
                    find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').get_text()

                Salary = item2[3].find('div', class_='_2J-3z _3B5DQ').find_all('div', class_='_3gyJS')[1]. \
                    find('span', class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').get_text()

                vacancies.append({
                    'name': name,
                    'href': self.HOST + href,
                    'Description': Description,
                    'Salary': Salary.replace('\xa0', ' ')

                })

            except Exception:
                pass
        return vacancies

    def parser(self):
        page = 1
        vacancies = []
        html = self.get_request(self.URL, params={'keywords': self.search, 'page': page})
        print(f'parser superjob.ru search {self.search}')
        while html.status_code == 200:
            vacancy = self.get_content(html.text)
            if len(vacancy) == 0: break
            vacancies.extend(vacancy)
            print(f'parser page {page} vacancies {len(vacancy)}')
            page += 1
            html = self.get_request(self.URL, params={'keywords': self.search, 'page': page})

        for vacancy in vacancies:
            print(vacancy)


class HH(Engine):
    def get_request(self):
        pass