from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from tkinter import Tk, Label, Button, Checkbutton, IntVar
from load_excel import *
from calculations import *
from db import FirstDb


class Prog:
    window = Tk()
    db = FirstDb()
    window["bg"] = "#DDCE84"
    window.title("Добро пожаловать!")
    window.geometry("750x450+350+125")
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
    excel_columnames = "                                                                                      "
    excel_columnames_dict = {}
    funcs_dict = {}
    func_value = IntVar()
    data_x = []

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
        Prog.file_path = path_entry.get()
        Prog.excel_columnames = read_excel_columnames(Prog.file_path)
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
        for i in enumerate(self.funcs):
            btn = Checkbutton(
                text=f"{i[1]}",
                variable=Prog.func_value,
                onvalue=x,
                offvalue=[],
                width=100,
                anchor="w",
                bg="#DDCE84",
                font=("Helvetica bold", 10),
            )
            x += 1
            btn.pack()
        Canvas(self.window, height=1, width=900, bg="yellow").pack()
        Label(
            self.window,
            text=f"{Prog.excel_columnames}",
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
            font=("Helvetica bold", 10),
            bg="#FFF9DB",
        ).pack()

    @Decorators
    def show(self, pokaz_entry):
        Prog.pokaz_entry = pokaz_entry.get()
        if Prog.funcs_dict[Prog.func_value.get()] == "Середнє арифметичне":
            Prog.db.insert_arithmetic(
                amount=amount_n(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
                measure=Prog.pokaz_entry,
                value=average(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
            )
            Prog.db.get_rand_excel()
        elif Prog.funcs_dict[Prog.func_value.get()] == "Мінімальне значення":
            Prog.db.insert_minimal(
                amount=amount_n(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
                measure=Prog.pokaz_entry,
                value=minimal(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
            )
            Prog.db.get_rand_excel()
        elif Prog.funcs_dict[Prog.func_value.get()] == "Максимальне значення":
            Prog.db.insert_maximal(
                amount=amount_n(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
                measure=Prog.pokaz_entry,
                value=maximal(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
            )
            Prog.db.get_rand_excel()
        elif (
            Prog.funcs_dict[Prog.func_value.get()]
            == "Середньоквадратичне відхилення по вибірці"
        ):
            Prog.db.insert_deviation(
                amount=amount_n(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
                measure=Prog.pokaz_entry,
                value=deviation(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
            )
            Prog.db.get_rand_excel()
        elif Prog.funcs_dict[Prog.func_value.get()] == "Коефіцієнт варіації":
            Prog.db.insert_variation(
                amount=amount_n(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
                measure=Prog.pokaz_entry,
                value=variation(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
            )
            Prog.db.get_rand_excel()
        elif Prog.funcs_dict[Prog.func_value.get()] == "Помилка середнього":
            Prog.db.insert_error(
                amount=amount_n(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
                measure=Prog.pokaz_entry,
                value=std_error(
                    read_column_by_colname(
                        Prog.file_path,
                        read_excel_columnames(Prog.file_path)[
                            Prog.excel_columnames_dict[Prog.pokaz_entry]
                        ],
                    )
                ),
            )
            Prog.db.get_rand_excel()
        elif Prog.funcs_dict[Prog.func_value.get()] == "Коваріація":
            val = Prog.pokaz_entry.split(",")
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
        elif Prog.funcs_dict[Prog.func_value.get()] == "Коефіцієнт кореляції Пірсона":
            val = Prog.pokaz_entry.split(",")
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
        elif Prog.funcs_dict[Prog.func_value.get()] == "Т-критерий Стюдента":
            val = Prog.pokaz_entry.split(",")
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

    @Decorators
    def widgets(self):
        btn = Button(
            self.window,
            text=("Вставити файл"),
            command=self.scrape_file,
            font=("Helvetica bold", 10),
            bg="#FFF9DB",
        )
        btn.pack()

    @Decorators
    def start(self):
        self.rad_button()
        self.widgets()
        Prog.window.mainloop()


p = Prog()
p.start()
