import psycopg2
import os
from dotenv import load_dotenv
from load_excel import *
from calculations import *
import openpyxl

load_dotenv()


class FirstDb:
    def __init__(self):
        """initialization of connection with db"""
        self.connection = psycopg2.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        self.create_first_table()
        self.create_second_table()

    def create_first_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS rand (
                amount INTEGER,
                measure TEXT,
                arithmetic double precision,
                minimal double precision,
                maximal double precision,
                deviation double precision,
                variation double precision,
                error double precision);"""
            )
        return "Таблиця готова до роботи"

    def get_list_of_colnames(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM rand""")
            colnames = [desc[0] for desc in cursor.description]
        print(colnames)

    def check_if_exists_measure(self, measure):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT measure FROM rand WHERE measure = %s;""",
                (measure,),
            )
            result = cursor.fetchall()
        return bool(len(result))

    def check_if_exists_measure1(self, measure):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT measure FROM rand2 WHERE measure = %s;""",
                (measure,),
            )
            result = cursor.fetchall()
        return bool(len(result))

    def insert_arithmetic(self, amount, measure, value):
        if not self.check_if_exists_measure(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand (amount, measure, arithmetic) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand SET amount = %s, arithmetic = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_minimal(self, amount, measure, value):
        if not self.check_if_exists_measure(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand (amount, measure, minimal) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand SET amount = %s, minimal = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_maximal(self, amount, measure, value):
        if not self.check_if_exists_measure(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand (amount, measure, maximal) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand SET amount = %s, maximal = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_deviation(self, amount, measure, value):
        if not self.check_if_exists_measure(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand (amount, measure, deviation) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand SET amount = %s, deviation = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_variation(self, amount, measure, value):
        if not self.check_if_exists_measure(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand (amount, measure, variation) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand SET amount = %s, variation = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_error(self, amount, measure, value):
        if not self.check_if_exists_measure(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand (amount, measure, error) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand SET amount = %s, error = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def create_second_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS rand2 (
                amount INTEGER,
                measure TEXT,
                covariance double precision,
                pearson double precision,
                t_test double precision);"""
            )
        return "Таблиця готова до роботи"

    def insert_covariance(self, amount, measure, value):
        if not self.check_if_exists_measure1(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand2 (amount, measure, covariance) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand2 SET amount = %s, covariance = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_pearson(self, amount, measure, value):
        if not self.check_if_exists_measure1(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand2 (amount, measure, pearson) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand2 SET amount = %s, pearson = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def insert_t_test(self, amount, measure, value):
        if not self.check_if_exists_measure1(measure):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO rand2 (amount, measure, t_test) VALUES (%s, %s, %s)""",
                    (
                        amount,
                        measure,
                        value,
                    ),
                )
                self.connection.commit()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE rand2 SET amount = %s, t_test = %s WHERE measure = %s;""",
                    (
                        amount,
                        value,
                        measure,
                    ),
                )
                self.connection.commit()

    def get_rand_excel(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM rand""")
            results = cursor.fetchall()
            book = openpyxl.Workbook()
            sheet = book.active
            k = 1
            for row in [
                "Кількість елементів",
                "Показник",
                "Середнє арифметичне",
                "Мінімальне значення",
                "Максимальне значення",
                "Середньоквадратичне відхилення по вибірці",
                "Коефіцієнт варіації",
                "Помилка середнього",
            ]:
                cell = sheet.cell(row=1, column=k)
                cell.value = row
                k += 1
            i = 1
            for row in results:
                i += 1
                j = 1
                for col in row:
                    cell = sheet.cell(row=i, column=j)
                    cell.value = col
                    j += 1
            book.save("rand.xlsx")

    def get_rand2_excel(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM rand2""")
            results = cursor.fetchall()
            book = openpyxl.Workbook()
            sheet = book.active
            k = 1
            for row in [
                "Кількість елементів",
                "Показник",
                "Коваріація",
                "Коефіцієнт кореляції Пірсона",
                "Т-критерий Стюдента",
            ]:
                cell = sheet.cell(row=1, column=k)
                cell.value = row
                k += 1
            i = 1
            for row in results:
                i += 1
                j = 1
                for col in row:
                    cell = sheet.cell(row=i, column=j)
                    cell.value = col
                    j += 1
            book.save("rand2.xlsx")