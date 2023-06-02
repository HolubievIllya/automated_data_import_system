from tkinter import *
from functools import partial
from tkinter.messagebox import showinfo
from db import FirstDb
import gspread
from oauth2client.service_account import ServiceAccountCredentials
s = FirstDb()



scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

creds = ServiceAccountCredentials.from_json_keyfile_name("data-project.json", scopes=scopes)
file = gspread.authorize(creds)
workbook = file.open("data_file")
sheet = workbook.sheet1
users = [i for i in sheet.get_all_records()]

class Test:
    tkWindow = Tk()
    tkWindow["bg"] = "#DDCE84"
    tkWindow.geometry("300x100+500+250")
    tkWindow.title("Вхід")
    db = FirstDb()
    log = False
    pas = False
    admin_rights = False
    login = ""

    def __init__(self):
        self.start()

    def start(self):
        usernameLabel = Label(self.tkWindow, text="Логін", bg="#DDCE84").grid(
            row=0, column=0
        )
        username = StringVar()
        usernameEntry = Entry(self.tkWindow, textvariable=username, bg="#DDCE84").grid(
            row=0, column=1
        )
        passwordLabel = Label(self.tkWindow, text="Пароль", bg="#DDCE84").grid(
            row=1, column=0
        )
        password = StringVar()
        passwordEntry = Entry(
            self.tkWindow, textvariable=password, show="*", bg="#DDCE84"
        ).grid(row=1, column=1)
        validateLogin = partial(self.validateLogin, username, password)
        loginButton = Button(
            self.tkWindow, text="Вхід", command=validateLogin, bg="#FFF9DB"
        ).grid(row=4, column=1)
        registButton = Button(
            self.tkWindow,
            text="Зареєструватися",
            command=self.regist_menu,
            bg="#FFF9DB",
        ).grid(row=5, column=1)
        self.tkWindow.mainloop()

    def regist_menu(self):
        win_reg = Toplevel(self.tkWindow)
        win_reg.wm_title("Реєстрація")
        win_reg["bg"] = "#DDCE84"
        usernameLabel = Label(win_reg, text="Введіть логін", bg="#DDCE84").grid(
            row=0, column=0
        )
        username = StringVar()
        usernameEntry = Entry(win_reg, textvariable=username, bg="#DDCE84").grid(
            row=0, column=1
        )
        passwordLabel = Label(win_reg, text="Введіть пароль", bg="#DDCE84").grid(
            row=1, column=0
        )
        password = StringVar()
        passwordEntry = Entry(
            win_reg, textvariable=password, show="*", bg="#DDCE84"
        ).grid(row=1, column=1)
        passwordLabel2 = Label(
            win_reg, text="Введіть пароль ще раз", bg="#DDCE84"
        ).grid(row=2, column=0)
        password2 = StringVar()
        passwordEntry2 = Entry(
            win_reg, textvariable=password2, show="*", bg="#DDCE84"
        ).grid(row=2, column=1)
        validateReg = partial(self.validateReg, username, password, password2)
        loginButton = Button(
            win_reg, text="Зареєструватися", command=validateReg, bg="#FFF9DB"
        ).grid(row=4, column=1)

    def validateReg(self, username, password, password2):
        if self.db.check_if_excists_login(username.get()):
            showinfo("Помилка", "Такий користувач вже існує")
        elif password.get() != password2.get():
            showinfo("Помилка", "Паролі не співпадають")
        else:
            self.db.insert_new_user(username.get(), password.get())
            showinfo(
                "Успішна реєстрація",
                f"Вітаю, {username.get()}, ви успішно зареєструвались!",
            )

    def validateLogin(self, username, password):
        if self.db.check_if_excists_login(username.get()):
            if self.db.check_if_excists_password(password.get()):
                self.tkWindow.destroy()
                self.log = True
                self.pas = True
                self.admin_rights = False
                self.login = username.get()
                print(self.login, self.log, self.pas)
            else:
                showinfo("Помилка", "Ви ввели некоректний пароль")
        elif self.db.check_if_exists_login_adm(username.get()):
            if self.db.check_if_exists_password_adm(password.get()):
                self.tkWindow.destroy()
                self.log = True
                self.pas = True
                self.admin_rights = True
            else:
                showinfo("Помилка", "Ви ввели некоректний пароль")
        else:
            showinfo("Помилка", "Ви ввели некоректний логін")


b = Test()
if b.log and b.pas and b.admin_rights:
    from chernovik import Prog
    if len(users) != 0:
        for i in users:
            s.insert_user(i["Введіть ім'я"], i['Введіть вік'], i['Введіть АП'], i['Введіть зріст'], i['Введіть вагу'], i['Введіть групу крові'], i['Введіть цукор крові'], i['Введіть АТС'], i['Введіть АТД'], i['Введіть ПАТ'], i['Введіть Атсер'], i['Введіть затримку дихання'], i['Введіть індекс Кетле'], i['Введіть індекс Кердо'])
            sheet.delete_row(2)
    else:
        print("nothing")
    p = Prog()
elif b.log and b.pas and not b.admin_rights:
    from chernovik_user import Users
    u = Users(b.login)


