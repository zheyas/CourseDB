from api_handler import ApiHandler
from db_handler import DBHandler


def main():
    # Настройте параметры подключения к базе данных
    db_name = 'Course3'
    user = 'postgres'
    password = '123456789'

    api_handler = ApiHandler()
    db_handler = DBHandler(db_name=db_name, user=user, password=password)

    # Создаем таблицы
    db_handler.create_tables()

    # Запрашиваем у пользователя ключевое слово
    keyword = input("Введите ключевое слово для поиска компаний: ")

    # Получаем ID компаний на основе ключевого слова
    company_ids = api_handler.search_companies(keyword=keyword, count=10)
    if not company_ids:
        print("Не удалось найти компании по указанному ключевому слову.")
        return

    print(f"Найдено компаний по ключевому слову '{keyword}':", company_ids)

    # Получаем данные о работодателях и их вакансиях
    data = api_handler.fetch_companies_and_vacancies(company_ids)

    # Загружаем данные в базу данных
    db_handler.insert_data(data)

    # Используем методы для работы с данными
    print("Компании и количество вакансий:")
    print(db_handler.get_companies_and_vacancies_count())

    print("Все вакансии:")
    print(db_handler.get_all_vacancies())

    print("Средняя зарплата:")
    print(db_handler.get_avg_salary())

    print("Вакансии с зарплатой выше средней:")
    print(db_handler.get_vacancies_with_higher_salary())

    print("Вакансии с ключевым словом 'Тимлид':")
    print(db_handler.get_vacancies_with_keyword('Тимлид'))

    # Закрываем соединение с базой данных
    db_handler.close()


if __name__ == "__main__":
    main()
