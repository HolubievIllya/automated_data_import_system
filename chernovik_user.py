from functools import partial
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import Tk, Label, Button, Checkbutton, IntVar
from db import FirstDb

class Users:
    window = Tk()
    db = FirstDb()
    window["bg"] = "#DDCE84"
    window.title("Програма!")
    window.geometry("750x450+350+125")


    def __init__(self, login):
        self.login = login
        self.start()


    def main_window(self):
        Label(
            self.window,
            text=f"Вітаємо!",
            bg="#DDCE84",
            font=("Helvetica bold", 15),
        ).pack(padx=15, pady=20)
        Button(
            self.window,
            text="Внести свої дані",
            command=self.apply,
            font=("Helvetica bold", 13),
            bg="#FFF9DB",
            height=3,
            width=15
        ).pack(padx=15, pady=20)
        Button(
            self.window,
            text="Звіт",
            command=self.hello,
            font=("Helvetica bold", 13),
            bg="#FFF9DB",
            height=3,
            width=20
        ).pack(padx=15, pady=20)

    def apply(self):
        win_reg = Toplevel(self.window)
        win_reg.wm_title("Внесення даних")
        win_reg["bg"] = "#DDCE84"
        nameLabel = Label(win_reg, text="Ім'я", bg="#DDCE84").grid(
            row=0, column=0
        )
        name = StringVar()
        nameEntry = Entry(win_reg, textvariable=name, bg="#DDCE84").grid(
            row=0, column=1
        )
        ageLabel = Label(win_reg, text="Вік", bg="#DDCE84").grid(
            row=1, column=0
        )
        age = IntVar()
        ageEntry = Entry(
            win_reg, textvariable=age, bg="#DDCE84"
        ).grid(row=1, column=1)
        apLabel = Label(win_reg, text="АП", bg="#DDCE84").grid(
            row=2, column=0
        )
        ap = IntVar()
        apEntry = Entry(win_reg, textvariable=ap, bg="#DDCE84").grid(
            row=2, column=1
        )
        heightLabel = Label(win_reg, text="Зріст", bg="#DDCE84").grid(
            row=3, column=0
        )
        height = StringVar()
        heightEntry = Entry(win_reg, textvariable=height, bg="#DDCE84").grid(
            row=3, column=1
        )
        weightLabel = Label(win_reg, text="Вага", bg="#DDCE84").grid(
            row=4, column=0
        )
        weight = StringVar()
        weightEntry = Entry(win_reg, textvariable=weight, bg="#DDCE84").grid(
            row=4, column=1
        )
        bloodgroupLabel = Label(win_reg, text="Група крові", bg="#DDCE84").grid(
            row=5, column=0
        )
        bloodgroup = IntVar()
        bloodgroupEntry = Entry(win_reg, textvariable=bloodgroup, bg="#DDCE84").grid(
            row=5, column=1
        )
        bloodsugarLabel = Label(win_reg, text="Цукор крові", bg="#DDCE84").grid(
            row=6, column=0
        )
        bloodsugar = StringVar()
        bloodsugarEntry = Entry(win_reg, textvariable=bloodsugar, bg="#DDCE84").grid(
            row=6, column=1
        )
        atsLabel = Label(win_reg, text="АТС", bg="#DDCE84").grid(
            row=7, column=0
        )
        ats = IntVar()
        atsEntry = Entry(win_reg, textvariable=ats, bg="#DDCE84").grid(
            row=7, column=1
        )
        atdLabel = Label(win_reg, text="АТД", bg="#DDCE84").grid(
            row=8, column=0
        )
        atd = IntVar()
        atdEntry = Entry(win_reg, textvariable=atd, bg="#DDCE84").grid(
            row=8, column=1
        )
        patLabel = Label(win_reg, text="ПАТ", bg="#DDCE84").grid(
            row=9, column=0
        )
        pat = IntVar()
        patEntry = Entry(win_reg, textvariable=pat, bg="#DDCE84").grid(
            row=9, column=1
        )
        ataverageLabel = Label(win_reg, text="Атсер", bg="#DDCE84").grid(
            row=10, column=0
        )
        ataverage = StringVar()
        ataverageEntry = Entry(win_reg, textvariable=ataverage, bg="#DDCE84").grid(
            row=10, column=1
        )
        breathlessnessLabel = Label(win_reg, text="Затримка дихання", bg="#DDCE84").grid(
            row=11, column=0
        )
        breathlessness = IntVar()
        breathlessnessEntry = Entry(win_reg, textvariable=breathlessness, bg="#DDCE84").grid(
            row=11, column=1
        )
        indketleLabel = Label(win_reg, text="Індекс Кетле", bg="#DDCE84").grid(
            row=12, column=0
        )
        indketle = StringVar()
        indketleEntry = Entry(win_reg, textvariable=indketle, bg="#DDCE84").grid(
            row=12, column=1
        )
        indkerdoLabel = Label(win_reg, text="Індекс Кердо", bg="#DDCE84").grid(
            row=13, column=0
        )
        indkerdo = StringVar()
        indkerdoEntry = Entry(win_reg, textvariable=indkerdo, bg="#DDCE84").grid(
            row=13, column=1
        )
        validate = partial(self.validate, name, age, ap, height, weight, bloodgroup, bloodsugar, ats, atd, pat, ataverage, breathlessness, indketle, indkerdo)
        loginButton = Button(
            win_reg, text="Застосувати", command=validate, bg="#FFF9DB"
        ).grid(row=14, column=1)


    def validate(self, name, age, ap, height, weight, bloodgroup, bloodsugar, ats, atd, pat, ataverage, breathlessness, indketle, indkerdo):
        try:
            if self.db.check_if_excists_user(self.login):
                showinfo("Помилка", "Ви вже записали свої дані")
            else:
                self.db.insert_user_login(name.get(), age.get(), ap.get(), float(height.get()), float(weight.get()), bloodgroup.get(), float(bloodsugar.get()), ats.get(), atd.get(), pat.get(), float(ataverage.get()), breathlessness.get(), float(indketle.get()), float(indkerdo.get()), self.login)
                self.db.insert_user(name.get(), age.get(), ap.get(), float(height.get()), float(weight.get()), bloodgroup.get(), float(bloodsugar.get()), ats.get(), atd.get(), pat.get(), float(ataverage.get()), breathlessness.get(), float(indketle.get()), float(indkerdo.get()))
        except ValueError:
            showinfo("Помилка", "Введіть числа через точку")

    def hello(self):
        try:
            res = self.db.get_user_info(self.login)
            showinfo("Звіт", f"Ім'я: {res[0][0]}\n"
                             f"Вік: {res[0][1]}\n"
                             f"АП: {res[0][2]}\n"
                             f"Зріст: {res[0][3]}\n"
                             f"Вага: {res[0][4]}\n"
                             f"Група крові: {res[0][5]}\n"
                             f"Цукор крові: {res[0][6]}\n"
                             f"АТС: {res[0][7]}\n"
                             f"АТД: {res[0][8]}\n"
                             f"ПАТ: {res[0][9]}\n"
                             f"Атсер: {res[0][10]}\n"
                             f"Затримка дихання: {res[0][11]}\n"
                             f"Індекс Кетле: {res[0][12]}\n"
                             f"Індекс Кердо: {res[0][13]}\n")
        except IndexError:
            showinfo("Помилка", "Ваші дані відсутні")






    def start(self):
        self.main_window()
        self.window.mainloop()
