import json
import time

from classes import Superjob,HH
import requests


URL = 'https://api.hh.ru/vacancies/'

def get_request(url, params=''):
    r = requests.get(url, params=params)
    data = r.content.decode()
    r.close()
    return data
def parser():
    page = 1
    params = {'text': 'python', 'page': page, 'per_page': 100}
    api = get_request(URL, params)

    while True:
        page += 1
        params={'text': 'python','page': page, 'per_page' : 100}
        api = get_request(URL, params)
        js_obj = json.loads(api)
        for obj in js_obj["items"]:
             print(obj["name"])
             print(obj["apply_alternate_url"])
             print(obj["snippet"]["requirement"])
             print(obj["snippet"]["responsibility"])
             print(salary(obj))

             print('-----'*10)
        if js_obj['pages']-page <= 1: break
        time.sleep(0.25)
    vacancies = []

    return vacancies

def salary(obj):
    str_salary = ''
    if obj["salary"] != None:
        if obj["salary"]["from"] != None:
            str_salary += 'от '+ str(obj["salary"]["from"])
        if obj["salary"]["to"] != None:
            str_salary += ' до '+ str(obj["salary"]["to"])
        if obj["salary"]["currency"] != None:
            str_salary += ' '+ obj["salary"]["currency"]
    else:
        str_salary ='По договорённости'
    return str_salary

if __name__ == '__main__':

    superjob = Superjob('python',100)
    vacancies = superjob.parser()

    hh = HH('python', 200)
    vacancies.extend(hh.parser())


    for vacancy in vacancies:
      print(vacancy)


