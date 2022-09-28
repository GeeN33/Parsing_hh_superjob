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
        self.vacancy_count = vacancy_count
        self.search = search
        self.HOST = 'https://russia.superjob.ru'
        self.URL = 'https://russia.superjob.ru/vacancy/search/'
        self.HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84'}

    def get_request(self, url:str, params:dict) -> str:
        r = requests.get(url, headers= self.HEADERS, params=params)
        return r

    def get_content(self, html:str) -> list:
        vacancies = []
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='f-test-search-result-item')
        for item in items:
            try:
                name = item.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').get_text()
                href = item.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').find('a').get('href')
                description = item.find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').get_text()
                salary =  item.find('span', class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').get_text()

                vacancies.append(Vacancy('superjob.ru' ,name, self.HOST + href, description, salary.replace('\xa0', ' ')))

            except Exception:
                pass
        return vacancies

    def parser(self) -> list:
        page = 1
        vacancies = []
        html = self.get_request(self.URL, params={'keywords': self.search, 'page': page})
        print(f'parser superjob.ru search {self.search}')
        while html.status_code == 200:
            vacancy = self.get_content(html.text)
            if len(vacancy) == 0 or len(vacancies) >= self.vacancy_count: break
            vacancies.extend(vacancy)
            print(f'parser page {page} vacancies {len(vacancy)}')
            page += 1
            html = self.get_request(self.URL, params={'keywords': self.search, 'page': page})

        return vacancies

class HH(Engine):
    """
    поиск на https://api.hh.ru/vacancies
    """
    def __init__(self,search:str, vacancy_count:int):
        self.vacancy_count = vacancy_count
        self.search = search
        self.URL = 'https://api.hh.ru/vacancies/'

    def get_request(self, url:str, params:dict) -> str:
        r = requests.get(url, params=params)
        data = r.content.decode()
        r.close()
        return data

    def parser(self) -> list:
        vacancies = []
        page = 0
        print(f'parser hh.ru search {self.search}')
        while True:
            page += 1
            params = {'text': self.search, 'page': page, 'per_page': 100}
            api = self.get_request(self.URL, params)
            js_obj = json.loads(api)
            for obj in js_obj["items"]:
                name = obj["name"]
                href = obj["apply_alternate_url"]
                description = (str(obj["snippet"]["requirement"])+ ' ' +str(obj["snippet"]["responsibility"])).replace('<highlighttext>','').replace('</highlighttext>','')
                salary =  self.salary(obj)
                vacancies.append(
                Vacancy('hh.ru', name,  href, description, salary))

            print(f'parser page {page} vacancies {len(js_obj["items"])}')
            if len(vacancies) >= self.vacancy_count or js_obj['pages'] - page <= 1: break
            time.sleep(0.25)

        return vacancies

    def salary(self, obj:str) -> str:
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

class Vacancy():
    """
     класс вакансии
    """
    def __init__(self, source:str, name:str , href:str, description:str, salary:str):
        self.source = source
        self.name = name
        self.href = href
        self.description = description
        self.salary =  salary
    def __repr__(self) -> str:
        s = f'source = {self.source}\nname = {self.name}\nhref = {self.href}\ndescription = {self.description}\nsalary = {self.salary}\n'+('-----'*10)
        return s













