from classes import Superjob,HH
from utils import save_to_file


if __name__ == '__main__':
    vacancies = []
    search = 'python'
    vacancies_count = 1000
    superjob = Superjob(search ,int(vacancies_count/2))
    vacancies = superjob.parser()

    hh = HH(search , vacancies_count - len(vacancies))
    vacancies.extend(hh.parser())
    save_to_file(vacancies)



