from classes import Superjob,HH
from utils import save_to_file, print_top_10


if __name__ == '__main__':
    vacancies = []
    search = input('Введите вакансию для поиска\n')
    if search == '': search = 'python'
    vacancies_count = 1000
    # поиск на https://russia.superjob.ru
    superjob = Superjob(search ,int(vacancies_count/2))
    vacancies = superjob.parser()

    # поиск на https://api.hh.ru/vacancies
    hh = HH(search , vacancies_count - len(vacancies))
    vacancies.extend(hh.parser())
    save_to_file(vacancies)
    print_top_10(vacancies)



