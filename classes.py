import json
import time
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def parser(self):
        pass

class Superjob(Engine):
    """
    поиск на https://russia.superjob.ru
    """
    def __init__(self,search:str, vacancy_count:int):
        self.__vacancy_count = vacancy_count
        self.__search = search
        self.__URL = 'https://russia.superjob.ru/vacancy/search/'
        self.__HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84'}

    def get_request(self, url:str, params:dict) -> str:
        r = requests.get(url, headers= self.__HEADERS, params=params)
        return r

    def get_content(self, html:str) -> list:
        vacancies = []
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='f-test-search-result-item')
        for item in items:
            try:

                vacancies.append(Vacancy(item))

            except Exception:
                pass
        return vacancies

    def parser(self) -> list:
        page = 1
        vacancies = []
        html = self.get_request(self.__URL, params={'keywords': self.__search, 'page': page})
        print(f'parser superjob.ru search {self.__search}')
        while html.status_code == 200:
            vacancy = self.get_content(html.text)
            if len(vacancy) == 0 or len(vacancies) >= self.__vacancy_count: break
            vacancies.extend(vacancy)
            print(f'parser page {page} vacancies {len(vacancy)}')
            page += 1
            html = self.get_request(self.__URL, params={'keywords': self.__search, 'page': page})

        return vacancies

class HH(Engine):
    """
    поиск на https://api.hh.ru/vacancies
    """
    def __init__(self,search:str, vacancy_count:int):
        self.__vacancy_count = vacancy_count
        self.__search = search
        self.__URL = 'https://api.hh.ru/vacancies/'

    def get_request(self, url:str, params:dict) -> str:
        r = requests.get(url, params=params)
        data = r.content.decode()
        r.close()
        return data

    def parser(self) -> list:
        vacancies = []
        page = 0
        print(f'parser hh.ru search {self.__search}')
        while True:
            page += 1
            params = {'text': self.__search, 'page': page, 'per_page': 100, 'area':'113'}
            api = self.get_request(self.__URL, params)
            js_obj = json.loads(api)
            for obj in js_obj["items"]:
                vacancies.append(Vacancy(obj, True))
            print(f'parser page {page} vacancies {len(js_obj["items"])}')
            if len(vacancies) >= self.__vacancy_count or js_obj['pages'] - page <= 1: break
            time.sleep(0.25)

        return vacancies



class Vacancy():
    """
     класс вакансии
    """
    def __init__(self, item, hh = False ):
        if hh:
            self.parser_hh(item)
        else:
            self.parser_superjob(item)

    def __repr__(self) -> str:
        s = f'source = {self.source}\nname = {self.name}\nhref = {self.href}\ndescription = {self.description}\nsalary = {self.salary}\n'+('-----'*10)
        return s
    def parser_superjob(self, item):
        self.source = 'superjob.ru'
        self.name = item.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').get_text()
        self.href = 'https://russia.superjob.ru' + item.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').find('a').get('href')
        self.description = item.find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').get_text()
        self.salary = item.find('span', class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').get_text().replace(' ', ' ')

    def parser_hh(self, obj):
        self.source = 'hh.ru'
        self.name = obj["name"]
        self.href = obj["apply_alternate_url"]
        self.description = (str(obj["snippet"]["requirement"]) + ' ' + str(obj["snippet"]["responsibility"])).replace('<highlighttext>', '').replace('</highlighttext>', '')
        self.salary = self.salary(obj)

    def salary(self, obj: str) -> str:
        str_salary = ''
        if obj["salary"] != None:
            if obj["salary"]["from"] != None:
                str_salary += 'от ' + str(obj["salary"]["from"])
            if obj["salary"]["to"] != None:
                str_salary += ' до ' + str(obj["salary"]["to"])
            if obj["salary"]["currency"] != None:
                str_salary += ' ' + obj["salary"]["currency"]
        else:
            str_salary = 'По договорённости'
        return str_salary





