def save_to_file(vacancies):
    with open('vacancies.txt','w',encoding="utf-8") as f:
        vacancy_sam = ''
        for vacancy in vacancies:
            vacancy_sam += str(vacancy)+'\n'
        f.write(vacancy_sam)
        print('Вакансии сохранены в текстовый документ «vacancies.txt» расположенный в корне проекта')