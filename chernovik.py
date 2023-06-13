from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from tkinter import Tk, Label, Button, Checkbutton, IntVar
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from load_excel import *
from calculations import *
from db import FirstDb
from matplotlib import pyplot as plt
from prettytable import PrettyTable
from datetime import date

# -*- coding: utf8 -*-


class Prog:
    window = Tk()
    db = FirstDb()
    window["bg"] = "#DDCE84"
    window.title("троянський кінь")
    window.geometry("800x650+350+125")
    funcs = [
        "Середнє арифметичне",
        "Мінімальне значення",
        "Максимальне значення",
        "Середньоквадратичне відхилення по вибірці",
        "Коефіцієнт варіації",
        "Помилка середнього",
        "Коваріація",
        "Коефіцієнт кореляції Пірсона",
        "Т-критерий Стюдента",
    ]
    file_path = ""
    pokaz_entry = ""
    excel_columnames = [
        "",
        "Вік",
        "АП",
        "Зріст",
        "Вага",
        "Група крові",
        "Цукор крові",
        "АТС",
        "АТД",
        "ПАТ",
        "Атсер",
        "Затр дих1",
        "и кетле",
        "и кердо",
    ]
    excel_columnames_dict = {}
    funcs_dict = {}
    func_value = IntVar()
    data_x = []
    names_dict = {}
    bd_dict = dict(zip(excel_columnames, list(range(len(excel_columnames)))))
    flag = False

    def __init__(self):
        self.start()

    def Decorators(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except FileNotFoundError:
                showinfo("Помилка", "Такого файлу не існує")
            except KeyError:
                showinfo("Помилка", "Ви ввели некоректне значення")
            except IndexError:
                showinfo("Помилка", "Ви ввели недостатньо значень")
            except ValueError:
                showinfo("Помилка", "Вибірки мають бути однакової довжини")
            except TypeError:
                showinfo("Помилка", "В файлі некоректний формат даних")

        return inner

    @Decorators
    def scrape_file(self):
        win_scrape = Toplevel(self.window)
        win_scrape.wm_title("Вставити файл")
        win_scrape["bg"] = "#DDCE84"
        Label(
            win_scrape,
            text="Вкажіть абсолютний шлях до файлу:",
            bg="#DDCE84",
            font=("Helvetica bold", 10),
        ).grid(row=0, column=0)
        path_entry = Entry(win_scrape)
        path_entry.insert(0, Prog.file_path)
        path_entry.grid(row=0, column=1, padx=50, pady=35)
        Button(
            win_scrape,
            text="Ок",
            command=lambda: self.apply_file_path(path_entry),
            bg="#FFF9DB",
        ).grid(row=0, column=3, columnspan=2)

    @Decorators
    def apply_file_path(self, path_entry: Entry):
        self.flag = True
        Prog.file_path = path_entry.get()
        # Prog.excel_columnames = read_excel_columnames(Prog.file_path)
        Prog.funcs_dict = dict(zip(list(range(len(Prog.funcs))), Prog.funcs))
        Prog.excel_columnames_dict = dict(
            zip(Prog.excel_columnames, list(range(len(Prog.excel_columnames))))
        )
        self.close_window()

    @Decorators
    def close_window(self):
        [i.destroy() for i in self.window.winfo_children()]
        self.__init__()

    @Decorators
    def rad_button(self):
        x = 0
        for  i, food_item in enumerate(self.funcs):
            self.funcs_dict[food_item] = Checkbutton(text=food_item, bg="#DDCE84")

            # Create a new instance of IntVar() for each checkbutton
            self.funcs_dict[food_item].var = IntVar()

            # Set the variable parameter of the checkbutton
            self.funcs_dict[food_item]['variable'] = self.funcs_dict[food_item].var

            # Arrange the checkbutton in the window
            self.funcs_dict[food_item].pack(anchor='w')
        Canvas(self.window, height=1, width=900, bg="yellow").pack()
        Label(
            self.window,
            text=f"{Prog.excel_columnames[1:]}",
            bg="#DDCE84",
            font=("Helvetica bold", 10),
        ).pack()
        Label(
            self.window,
            text=f"Введіть показник який хочете обрахувати",
            bg="#DDCE84",
            font=("Helvetica bold", 12),
        ).pack()
        pokaz_entry = Entry(self.window)
        pokaz_entry.insert(0, Prog.pokaz_entry)
        pokaz_entry.pack()
        Button(
            self.window,
            text="Рахувати",
            command=lambda: self.show(pokaz_entry),
            font=("Helvetica bold", 15),
            bg="#FFF9DB",
            height=1,
            width=17,
        ).pack(padx=5, pady=8)
        Button(
            self.window,
            text="Звіт",
            command=self.zvit_wind,
            font=("Helvetica bold", 15),
            bg="#FFF9DB",
            height=1,
            width=17,
        ).pack(padx=5, pady=8)
        Button(
            self.window,
            text="Імпортувати дані з файлу",
            command=self.insertion,
            font=("Helvetica bold", 13),
            bg="#FFF9DB",
            height=1,
            width=21,
        ).pack(padx=5, pady=8)
        Button(
            self.window,
            text="Отримати повний звіт",
            command=self.get_zvit,
            font=("Helvetica bold", 14),
            bg="#FFF9DB",
            height=1,
            width=17,
        ).pack(padx=5, pady=8)
        Button(
            self.window,
            text="Імпортувати гугл форми",
            command=self.load_google,
            font=("Helvetica bold", 13),
            bg="#FFF9DB",
            height=1,
            width=21,
        ).pack(padx=5, pady=8)

    def load_google(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "data-project.json", scopes=scopes
        )
        file = gspread.authorize(creds)
        workbook = file.open("data_file")
        sheet = workbook.sheet1
        users = [i for i in sheet.get_all_records()]
        if len(users) != 0:
            for i in users:
                self.db.insert_user(
                    i["Введіть ім'я"],
                    i["Введіть вік"],
                    i["Введіть АП"],
                    i["Введіть зріст"],
                    i["Введіть вагу"],
                    i["Введіть групу крові"],
                    i["Введіть цукор крові"],
                    i["Введіть АТС"],
                    i["Введіть АТД"],
                    i["Введіть ПАТ"],
                    i["Введіть Атсер"],
                    i["Введіть затримку дихання"],
                    i["Введіть індекс Кетле"],
                    i["Введіть індекс Кердо"],
                )
                sheet.delete_row(2)
        else:
            print("nothing")

    @Decorators
    def get_zvit(self):
        self.db.get_full_zvit()

    @Decorators
    def insertion(self):
        self.db.insert_full_excel(self.file_path)

    @Decorators
    def zvit_wind(self):
        win_zvit = Toplevel(self.window)
        win_zvit.wm_title("Меню формування звіту")
        win_zvit["bg"] = "#DDCE84"
        Label(
            win_zvit,
            text=f"{read_column_by_colname_names(Prog.file_path, Prog.excel_columnames[0])}",
            bg="#DDCE84",
            font=("Helvetica bold", 10),
        ).pack()
        Label(
            win_zvit,
            text=f"Введіть ім'я пацієнта",
            bg="#DDCE84",
            font=("Helvetica bold", 12),
        ).pack()
        patient_entry = Entry(win_zvit)
        patient_entry.insert(0, Prog.pokaz_entry)
        patient_entry.pack()
        Button(
            win_zvit,
            text="Ок",
            command=lambda: self.show2(patient_entry),
            font=("Helvetica bold", 10),
            bg="#FFF9DB",
        ).pack()

    @Decorators
    def show2(self, patient_entry):
        Prog.names_dict = dict(
            zip(
                list(
                    read_column_by_colname_names(
                        Prog.file_path, Prog.excel_columnames[0]
                    )
                ),
                list(
                    range(
                        len(
                            read_column_by_colname_names(
                                Prog.file_path, Prog.excel_columnames[0]
                            )
                        )
                    )
                ),
            )
        )
        patient_entry = patient_entry.get()
        res = patient_entry
        todays_date = date.today()
        values = []
        for i in read_excel_columnames(Prog.file_path)[1:]:
            values.append(
                read_column_by_colname(Prog.file_path, i)[
                    Prog.names_dict[patient_entry]
                ]
            )
        table = PrettyTable()
        table.field_names = [
            "         Найменування показників         ",
            "            Результат           ",
        ]
        table.add_row(["АП", f"{values[1]}"])
        table.add_row(["Зріст", f"{values[2]}"])
        table.add_row(["Вага", f"{values[3]}"])
        table.add_row(["Група крові", f"{values[4]}"])
        table.add_row(["Цукор крові", f"{values[5]}"])
        table.add_row(["АТС", f"{values[6]}"])
        table.add_row(["АТД", f"{values[7]}"])
        table.add_row(["ПАТ", f"{values[8]}"])
        table.add_row(["Атсер", f"{values[9]}"])
        table.add_row(["Затримка дихання", f"{values[10]}"])
        table.add_row(["Індекс Кетле", f"{values[11]}"])
        table.add_row(["Індекс Кердо", f"{values[12]}"])
        table.align["Колонка 1"] = "l"
        table.align["Колонка 2"] = "l"
        with open(f"Картка пацієнта_{res}.txt", "w", encoding="utf-16") as new_data:
            new_data.write(
                "\t\t\t\tКартка пацієта\t\t\t\t\n"
                f"{'-' * 80}\n"
                f"\t\t\t\tдата {todays_date}\t\t\t\t\n"
                f"\t\t\t{'-' * 32}\t\t\t\n"
                f"\t\t\tІм'я: {res}\t\t\tВік: {values[0]}\t\t\t\t\n"
                f"{'-' * 80}\n"
                f"\t\t\tЗаклад:\t\t\t\tВідділення:\t\t\t\t\n"
                f"{table.get_string()}"
            )


    def show333(self):
        for cb in self.funcs_dict.values():
            if cb.var.get():
                print(cb['text'])

    @Decorators
    def show(self, pokaz_entry):
        for cb in self.funcs_dict.values():
            if cb.var.get():
                if self.flag:
                    Prog.pokaz_entry = pokaz_entry.get()
                    if cb['text'] == "Середнє арифметичне":
                        res = Prog.pokaz_entry.split(",")
                        for i in res:
                            self.show_histo(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                ),
                                i.strip(),
                            )
                            value = average(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                )
                            )
                            Prog.db.insert_arithmetic(
                                amount=amount_n(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                                measure=i.strip(),
                                value=value,
                            )
                            Prog.db.get_rand_excel()
                    elif cb['text'] == "Мінімальне значення":
                        res = Prog.pokaz_entry.split(",")
                        for i in res:
                            self.show_histo(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                ),
                                i.strip(),
                            )
                            Prog.db.insert_minimal(
                                amount=amount_n(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                                measure=i.strip(),
                                value=minimal(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                            )
                            Prog.db.get_rand_excel()
                    elif cb['text'] == "Максимальне значення":
                        res = Prog.pokaz_entry.split(",")
                        for i in res:
                            self.show_histo(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                ),
                                i.strip(),
                            )
                            Prog.db.insert_maximal(
                                amount=amount_n(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                                measure=i.strip(),
                                value=maximal(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                            )
                            Prog.db.get_rand_excel()
                    elif (
                        cb['text']
                        == "Середньоквадратичне відхилення по вибірці"
                    ):
                        res = Prog.pokaz_entry.split(",")
                        for i in res:
                            self.show_histo(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                ),
                                i.strip(),
                            )
                            Prog.db.insert_deviation(
                                amount=amount_n(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                                measure=i.strip(),
                                value=deviation(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                            )
                            Prog.db.get_rand_excel()
                    elif cb['text'] == "Коефіцієнт варіації":
                        res = Prog.pokaz_entry.split(",")
                        for i in res:
                            self.show_histo(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                ),
                                i.strip(),
                            )
                            Prog.db.insert_variation(
                                amount=amount_n(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                                measure=i.strip(),
                                value=variation(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                            )
                            Prog.db.get_rand_excel()
                    elif cb['text'] == "Помилка середнього":
                        res = Prog.pokaz_entry.split(",")
                        for i in res:
                            self.show_histo(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[i.strip()]
                                    ],
                                ),
                                i.strip(),
                            )
                            Prog.db.insert_error(
                                amount=amount_n(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                                measure=i.strip(),
                                value=std_error(
                                    read_column_by_colname(
                                        Prog.file_path,
                                        read_excel_columnames(Prog.file_path)[
                                            Prog.excel_columnames_dict[i.strip()]
                                        ],
                                    )
                                ),
                            )
                            Prog.db.get_rand_excel()
                    elif cb['text'] == "Коваріація":
                        val = Prog.pokaz_entry.split(",")
                        res = str(val[0]) + " " + str(val[1])
                        self.cor_graph(
                            read_column_by_colname(
                                Prog.file_path,
                                read_excel_columnames(Prog.file_path)[
                                    Prog.excel_columnames_dict[val[0].strip()]
                                ],
                            ),
                            read_column_by_colname(
                                Prog.file_path,
                                read_excel_columnames(Prog.file_path)[
                                    Prog.excel_columnames_dict[val[1].strip()]
                                ],
                            ),
                            res,
                        )
                        Prog.db.insert_covariance(
                            amount=amount_n(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[0].strip()]
                                    ],
                                )
                            ),
                            measure=Prog.pokaz_entry,
                            value=covariance(
                                data_x=read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[0].strip()]
                                    ],
                                ),
                                data_y=read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[1].strip()]
                                    ],
                                ),
                            ),
                        )
                        Prog.db.get_rand2_excel()
                    elif (
                        cb['text'] == "Коефіцієнт кореляції Пірсона"
                    ):
                        val = Prog.pokaz_entry.split(",")
                        res = str(val[0]) + " " + str(val[1])
                        self.cor_graph(
                            read_column_by_colname(
                                Prog.file_path,
                                read_excel_columnames(Prog.file_path)[
                                    Prog.excel_columnames_dict[val[0].strip()]
                                ],
                            ),
                            read_column_by_colname(
                                Prog.file_path,
                                read_excel_columnames(Prog.file_path)[
                                    Prog.excel_columnames_dict[val[1].strip()]
                                ],
                            ),
                            res,
                        )
                        Prog.db.insert_pearson(
                            amount=amount_n(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[0].strip()]
                                    ],
                                )
                            ),
                            measure=Prog.pokaz_entry,
                            value=pearson(
                                data_x=read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[0].strip()]
                                    ],
                                ),
                                data_y=read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[1].strip()]
                                    ],
                                ),
                            ),
                        )
                        Prog.db.get_rand2_excel()
                    elif cb['text'] == "Т-критерий Стюдента":
                        val = Prog.pokaz_entry.split(",")
                        res = str(val[0]) + " " + str(val[1])
                        self.cor_graph(
                            read_column_by_colname(
                                Prog.file_path,
                                read_excel_columnames(Prog.file_path)[
                                    Prog.excel_columnames_dict[val[0].strip()]
                                ],
                            ),
                            read_column_by_colname(
                                Prog.file_path,
                                read_excel_columnames(Prog.file_path)[
                                    Prog.excel_columnames_dict[val[1].strip()]
                                ],
                            ),
                            res,
                        )
                        Prog.db.insert_t_test(
                            amount=amount_n(
                                read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[0].strip()]
                                    ],
                                )
                            ),
                            measure=Prog.pokaz_entry,
                            value=t_test(
                                data_x=read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[0].strip()]
                                    ],
                                ),
                                data_y=read_column_by_colname(
                                    Prog.file_path,
                                    read_excel_columnames(Prog.file_path)[
                                        Prog.excel_columnames_dict[val[1].strip()]
                                    ],
                                ),
                            ),
                        )
                        Prog.db.get_rand2_excel()
                else:
                    if cb['text'] == "Середнє арифметичне":
                        res = pokaz_entry.get().split(",")
                        for i in res:
                            self.show_histo(
                                self.db.get_list_all(self.bd_dict[i.strip()]), i.strip()
                            )
                            self.db.insert_arithmetic(
                                len(self.db.get_list_all(self.bd_dict[i.strip()])),
                                i.strip(),
                                average(self.db.get_list_all(self.bd_dict[i.strip()])),
                            )
                    elif cb['text'] == "Мінімальне значення":
                        res = pokaz_entry.get().split(",")
                        for i in res:
                            self.show_histo(
                                self.db.get_list_all(self.bd_dict[i.strip()]), i.strip()
                            )
                            self.db.insert_minimal(
                                len(self.db.get_list_all(self.bd_dict[i.strip()])),
                                i.strip(),
                                minimal(self.db.get_list_all(self.bd_dict[i.strip()])),
                            )
                    elif cb['text'] == "Максимальне значення":
                        res = pokaz_entry.get().split(",")
                        for i in res:
                            self.show_histo(
                                self.db.get_list_all(self.bd_dict[i.strip()]), i.strip()
                            )
                            self.db.insert_maximal(
                                len(self.db.get_list_all(self.bd_dict[i.strip()])),
                                i.strip(),
                                maximal(self.db.get_list_all(self.bd_dict[i.strip()])),
                            )
                    elif cb['text'] == "Середньоквадратичне відхилення по вибірці":
                        res = pokaz_entry.get().split(",")
                        for i in res:
                            self.show_histo(
                                self.db.get_list_all(self.bd_dict[i.strip()]), i.strip()
                            )
                            self.db.insert_deviation(
                                len(self.db.get_list_all(self.bd_dict[i.strip()])),
                                i.strip(),
                                deviation(self.db.get_list_all(self.bd_dict[i.strip()])),
                            )
                    elif cb['text'] == "Коефіцієнт варіації":
                        res = pokaz_entry.get().split(",")
                        for i in res:
                            self.show_histo(
                                self.db.get_list_all(self.bd_dict[i.strip()]), i.strip()
                            )
                            self.db.insert_variation(
                                len(self.db.get_list_all(self.bd_dict[i.strip()])),
                                i.strip(),
                                variation(self.db.get_list_all(self.bd_dict[i.strip()])),
                            )
                    elif cb['text'] == "Помилка середнього":
                        res = pokaz_entry.get().split(",")
                        for i in res:
                            self.show_histo(
                                self.db.get_list_all(self.bd_dict[i.strip()]), i.strip()
                            )
                            self.db.insert_error(
                                len(self.db.get_list_all(self.bd_dict[i.strip()])),
                                i.strip(),
                                std_error(self.db.get_list_all(self.bd_dict[i.strip()])),
                            )
                    elif cb['text'] == "Коваріація":
                        val = pokaz_entry.get().split(",")
                        res = str(val[0]) + " " + str(val[1])
                        self.cor_graph(
                            self.db.get_list_all(self.bd_dict[val[0].strip()]),
                            self.db.get_list_all(self.bd_dict[val[1].strip()]),
                            res,
                        )
                        self.db.insert_covariance(
                            len(self.db.get_list_all(self.bd_dict[val[0].strip()])),
                            pokaz_entry.get(),
                            covariance(
                                self.db.get_list_all(self.bd_dict[val[0].strip()]),
                                self.db.get_list_all(self.bd_dict[val[1].strip()]),
                            ),
                        )
                    elif cb['text'] == "Коефіцієнт кореляції Пірсона":
                        val = pokaz_entry.get().split(",")
                        res = str(val[0]) + " " + str(val[1])
                        self.cor_graph(
                            self.db.get_list_all(self.bd_dict[val[0].strip()]),
                            self.db.get_list_all(self.bd_dict[val[1].strip()]),
                            res,
                        )
                        self.db.insert_pearson(
                            len(self.db.get_list_all(self.bd_dict[val[0].strip()])),
                            pokaz_entry.get(),
                            pearson(
                                self.db.get_list_all(self.bd_dict[val[0].strip()]),
                                self.db.get_list_all(self.bd_dict[val[1].strip()]),
                            ),
                        )
                    elif cb['text'] == "Т-критерий Стюдента":
                        val = pokaz_entry.get().split(",")
                        res = str(val[0]) + " " + str(val[1])
                        self.cor_graph(
                            self.db.get_list_all(self.bd_dict[val[0].strip()]),
                            self.db.get_list_all(self.bd_dict[val[1].strip()]),
                            res,
                        )
                        self.db.insert_t_test(
                            len(self.db.get_list_all(self.bd_dict[val[0].strip()])),
                            pokaz_entry.get(),
                            t_test(
                                self.db.get_list_all(self.bd_dict[val[0].strip()]),
                                self.db.get_list_all(self.bd_dict[val[1].strip()]),
                            ),
                        )

    def show_histo(self, data, name):
        plt.hist(data, bins=20, alpha=0.5)
        plt.title("Гістограма")
        plt.xlabel(f"{name}")
        plt.ylabel("Кількість")
        plt.savefig(f"Гістограма {name}.png")
        plt.close()

    def cor_graph(self, data_x, data_y, name):
        correlation_matrix = np.corrcoef(data_x, data_y)
        correlation = correlation_matrix[0, 1]
        plt.scatter(data_x, data_y)
        res = name.split()
        plt.xlabel(f"{res[0]}")
        plt.ylabel(f"{res[1]}")
        plt.title("Кореляція: " + str(round(correlation, 2)))
        plt.savefig(f"Графік кореляції {name}.png")
        plt.close()

    @Decorators
    def widgets(self):
        btn = Button(
            self.window,
            text=("Обробити дані"),
            command=self.scrape_file,
            font=("Helvetica bold", 15),
            bg="#FFF9DB",
            height=1,
            width=17,
        )
        btn.pack(pady=8)

    @Decorators
    def start(self):
        self.rad_button()
        self.widgets()
        Prog.window.mainloop()


p = Prog()