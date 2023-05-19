import psycopg2
import os
from dotenv import load_dotenv
from load_excel import *
from calculations import *

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

db = FirstDb()
# db.get_list_of_colnames()
# db.insert_arithmetic(amount_n((read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2]))),read_excel_columnames("Лист Microsoft Excel.xlsx")[2], average(read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2])))
# db.insert_arithmetic(read_excel_columnames("Лист Microsoft Excel.xlsx")[3], average(read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[3])))
# db.insert_minimal(amount_n((read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2]))),read_excel_columnames("Лист Microsoft Excel.xlsx")[2], minimal(read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2])))
# db.insert_variation(amount_n((read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2]))),read_excel_columnames("Лист Microsoft Excel.xlsx")[2], variation(read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2])))
# db.insert_error(amount_n((read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2]))),read_excel_columnames("Лист Microsoft Excel.xlsx")[2], std_error(read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[2])))
