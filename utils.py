def save_to_file(vacancies:list):
    """
     сохранение в текстовый документ «vacancies.txt»
    """
    with open('vacancies.txt','w',encoding="utf-8") as f:
        vacancy_sam = ''
        for vacancy in vacancies:
            vacancy_sam += str(vacancy)+'\n'
        f.write(vacancy_sam)
        print('Вакансии сохранены в текстовый документ «vacancies.txt» расположенный в корне проекта')

def print_top_10(vacancies:list):
    i = 1
    print('======'*20)
    print('TOP 10 вакансий, 5 superjob.ru и 5 hh.ru')
    print('---' * 20)
    for vacancy in vacancies:
        if i <= 5 and vacancy.source == 'superjob.ru':
            print(vacancy)
            i += 1
        elif i > 5 and vacancy.source == 'hh.ru':
            print(vacancy)
            i += 1

        if i > 10: break