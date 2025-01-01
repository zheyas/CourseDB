import psycopg2


class DBHandler:
    def __init__(self, db_name, user, password,
                 host='localhost'):
        self.conn = psycopg2.connect(dbname=db_name,
                                     user=user, password=password, host=host)

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                industry VARCHAR(255),
                site_url VARCHAR(255)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                salary INTEGER,
                currency VARCHAR(10),
                company_id INTEGER REFERENCES companies(id),
                url VARCHAR(255)
            );
        """)
        self.conn.commit()
        cur.close()

    def insert_data(self, data):
        cur = self.conn.cursor()

        for item in data:
            company = item['company']
            cur.execute("""
                INSERT INTO companies
                 (name, description, industry, site_url)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (company['name'], company.get('description'),
                  company.get('industry_name'), company.get('site_url')))
            company_id = cur.fetchone()[0]

            vacancies = item['vacancies']
            for vacancy in vacancies:
                salary = vacancy.get('salary')
                salary_value = salary['from']\
                    if salary else None
                cur.execute("""
                    INSERT INTO vacancies (name, salary,
                     currency, company_id, url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (vacancy['name'],
                      salary_value,
                      salary.get('currency') if salary else None,
                      company_id, vacancy['alternate_url']))

        self.conn.commit()
        cur.close()

    def get_companies_and_vacancies_count(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.name, COUNT(v.id) FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_all_vacancies(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.name, v.name, v.salary, v.url FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """)
        result = cur.fetchall()
        cur.close()
        return result

    def get_avg_salary(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT AVG(salary) FROM vacancies
        """)
        avg_salary = cur.fetchone()[0]
        cur.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        cur = self.conn.cursor()
        cur.execute("""
            SELECT v.name, v.salary, v.url FROM vacancies v
            WHERE v.salary > %s
        """, (avg_salary,))
        result = cur.fetchall()
        cur.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT v.name, v.salary, v.url
             FROM vacancies v
            WHERE v.name ILIKE %s
        """, (f'%{keyword}%',))
        result = cur.fetchall()
        cur.close()
        return result

    def close(self):
        self.conn.close()
