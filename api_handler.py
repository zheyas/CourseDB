
import requests


class ApiHandler:
    def __init__(self):
        self.base_url = 'https://api.hh.ru/'

    def search_companies(self, keyword, count=10):
        """Поиск компаний по ключевому слову."""
        url = f'{self.base_url}employers'
        params = {
            'text': keyword,
            'per_page': count
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            companies = response.json()
            return [company['id'] for company in companies['items']]
        else:
            print(f"Ошибка {response.status_code} при поиске компаний.")
            return []

    def fetch_companies_and_vacancies(self, company_ids):
        """Извлечение данных о компаниях и их вакансиях."""
        data = []
        for comp_id in company_ids:
            company_data = self.get_company_data(comp_id)
            if company_data is not None:
                vacancies_data = self.get_company_vacancies(comp_id)
                data.append({
                    'company': company_data,
                    'vacancies': vacancies_data
                })
        return data

    def get_company_data(self, company_id):
        """Получение данных о компании по ID."""
        url = f'{self.base_url}employers/{company_id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Ошибка {response.status_code} при'
                  f' получении данных компании с ID {company_id}')
            return None

    def get_company_vacancies(self, company_id):
        """Получение вакансий компании по ID."""
        url = f'{self.base_url}vacancies?employer_id={company_id}&per_page=10'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f'Ошибка {response.status_code}'
                  f' при получении вакансий компании с ID {company_id}')
            return []

# Пример использования класса
