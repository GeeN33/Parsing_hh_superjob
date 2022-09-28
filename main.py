from classes import Superjob

if __name__ == '__main__':
     superjob = Superjob('python',300)
     vacancies = superjob.parser()

     for vacancy in vacancies:
          print(vacancy)


