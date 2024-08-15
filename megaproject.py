import os
import json
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import random
import re
from tkinter import messagebox
from datetime import datetime

inf_users = {}
current_user = None
show_password_state = False

style = Style("sandstone")

transactions_file = "transactions.json"

def load_transactions(user_login):
    try:
        with open(f"{user_login}_transactions.json", 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_transaction(user_login, transaction):
    transactions = load_transactions(user_login)
    transactions.append(transaction)
    with open(f"{user_login}_transactions.json", 'w') as file:
        json.dump(transactions, file, indent=4)


admin_list = ["YlyGod"]

def load_data():
    global inf_users
    try:
        with open("users.json", "r") as f:
            inf_users = json.load(f)
    except FileNotFoundError:
        inf_users = {}

    for admin in admin_list:
        if admin not in inf_users:
            inf_users[admin] = {
                "password": "@2348ZW@LGFD",
                "balance": 0,
                "own_code": localCode(),
                "cards": [],
                "name": "Ilia",
                "surname": "Shkedov",
                "age": 17,
                "is_admin": True
            }
    save_data()

def save_data():
    with open("users.json", "w") as file:
        json.dump(inf_users, file, indent=4)

def toggle_password(entry, button):
    global show_password_state
    if show_password_state:
        entry.config(show='*')
        button.config(text='Показать пароль')
    else:
        entry.config(show='')
        button.config(text='  Скрыть пароль  ')
    show_password_state = not show_password_state


def is_valid_pasword(pasword):
    global entry_password
    if len(str(pasword)) < 5: return False
    else: return True

def is_valid_username(username):
    if re.search(r'[а-яА-Я]', username):
        return False
    if re.search(r'[!@#$%^&*()\[\];\'",./?`]', username):
        return False
    if ' ' in username:
        return False
    return True


def show_register_page():
    global entry_login, entry_password, lb_register_status, bt_register, bt_toggle_password, entry_name, entry_surname, entry_age

    clear_frame()

    labLogin = ttk.Label(root, text='Введите логин', width=50)
    labLogin.place(x=225, y=20)
    entry_login = ttk.Entry(root, width=65)
    entry_login.place(x=80, y=60)

    labPassword = ttk.Label(root, text='Введите пароль')
    labPassword.place(x=225, y=100)
    entry_password = ttk.Entry(root, width=65, show='*')
    entry_password.place(x=80, y=140)

    labName = ttk.Label(root, text='Введите имя')
    labName.place(x=225, y=180)
    entry_name = ttk.Entry(root, width=65)
    entry_name.place(x=80, y=220)

    labSurname = ttk.Label(root, text='Введите фамилию')
    labSurname.place(x=225, y=260)
    entry_surname = ttk.Entry(root, width=65)
    entry_surname.place(x=80, y=300)

    labAge = ttk.Label(root, text='Введите возраст')
    labAge.place(x=225, y=340)
    entry_age = ttk.Entry(root, width=65)
    entry_age.place(x=80, y=380)

    bt_toggle_password = ttk.Button(root, text='Показать пароль',
                                    command=lambda: toggle_password(entry_password, bt_toggle_password))
    bt_toggle_password.place(x=340, y=420)

    bt_register = ttk.Button(root, text='Зарегистрироваться')
    bt_register.place(x=80, y=420)

    lb_register_status = ttk.Label(root, text='Вы еще не зарегистрированы', width=50)
    lb_register_status.place(x=150, y=470)

    bt_to_auth = ttk.Button(root, text='Уже зарегистрированы? Авторизоваться', command=show_login_page, width=43)
    bt_to_auth.place(x=80, y=500)

    bt_register.bind('<Button-1>', registration)


def show_login_page():
    global entry_login_auth, entry_password_auth, lb_auth_status, bt_login, bt_toggle_password_auth
    clear_frame()
    labAuthLogin = ttk.Label(root, text='Введите логин', width=50)
    labAuthLogin.place(x=170, y=20)
    entry_login_auth = ttk.Entry(root, width=50)
    entry_login_auth.place(x=80, y=60)
    labAuthPassword = ttk.Label(root, text='Введите пароль')
    labAuthPassword.place(x=170, y=100)
    entry_password_auth = ttk.Entry(root, width=50, show='*')
    entry_password_auth.place(x=80, y=140)
    bt_toggle_password_auth = ttk.Button(root, text='Показать пароль',
                                         command=lambda: toggle_password(entry_password_auth, bt_toggle_password_auth))
    bt_toggle_password_auth.place(x=250, y=185)
    bt_login = ttk.Button(root, text='Авторизоваться')
    bt_login.place(x=80, y=185)
    lb_auth_status = ttk.Label(root, text='', width=50)
    lb_auth_status.place(x=130, y=230)
    bt_to_register = ttk.Button(root, text='Еще не зарегистрированы? Регистрация', command=show_register_page)
    bt_to_register.place(x=80, y=260)
    bt_login.bind('<Button-1>', authorize)

def show_Hello_page():
    global lb_profile
    clear_frame()
    if current_user and current_user.get("login") in inf_users:
        lb_profile = ttk.Label(root, text=f'Добро пожаловать, {current_user["login"]}!', width=50)
        lb_profile.place(x=185, y=20)
        root.after(2000, show_profile_page)
    else:
        lb_profile = ttk.Label(root, text='Ошибка: Пользователь не авторизован или данные не найдены!', width=50)
        lb_profile.place(x=185, y=20)

def show_profile_page():
    global lb_profile, lb_balance, bt_logout, bt_add_money, bt_transfer, lb_own_code, bt_edit_profile, bt_view_cards

    clear_frame()

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    sidebar = Frame(main_frame, bg='#333', width=200)
    sidebar.pack(fill=Y, side=LEFT)

    content_frame = Frame(main_frame, bg='#fff')
    content_frame.pack(fill=BOTH, expand=True)

    profile_pic = Label(sidebar, text='[Profile Pic]', bg='#333', fg='#fff')
    profile_pic.pack(pady=10)

    profile_name = Label(sidebar, text=f'{current_user["login"]}', bg='#333', fg='#fff', font=('Arial', 14))
    profile_name.pack(pady=5)

    profile_status = Label(sidebar, text='Профиль', bg='#333', fg='#fff', cursor="hand2")
    profile_status.pack(pady=5)
    profile_status.bind("<Button-1>", lambda e: show_edit_profile_page())

    cards_label = Label(sidebar, text='Карты', bg='#333', fg='#fff', cursor="hand2")
    cards_label.pack(pady=5)
    cards_label.bind("<Button-1>", lambda e: show_cards_list(content_frame))

    transfer_label = Label(sidebar, text='Перевод средств', bg='#333', fg='#fff', cursor="hand2")
    transfer_label.pack(pady=5)
    transfer_label.bind("<Button-1>", lambda e: show_transfer_page())

    transactions_label = Label(sidebar, text='История переводов', bg='#333', fg='#fff', cursor="hand2")
    transactions_label.pack(pady=5)
    transactions_label.bind("<Button-1>", lambda e: show_transactions_page())

    if current_user.get("is_admin", False):
        print("администратор")
        admin_label = Label(sidebar, text='Админ панель', bg='#333', fg='#fff', cursor="hand2")
        admin_label.pack(pady=5)
        admin_label.bind("<Button-1>", lambda e: show_admin_panel())
    else:
        print("не администратор")

    welcome_label = Label(content_frame, text=f'Добро пожаловать, {current_user["login"]}!', bg='#fff', fg='#333', font=('Arial', 18))
    welcome_label.pack(pady=20)

    lb_balance = Label(content_frame, text=f'Ваш баланс: {round(inf_users[current_user["login"]]["balance"],2)} рублей', bg='#fff', fg='#333', font=('Arial', 14))
    lb_balance.pack(pady=10)

    bt_add_money = Button(content_frame, text='Пополнить баланс', command=add_money, bg='#4CAF50', fg='#fff', padx=20, pady=10)
    bt_add_money.pack(pady=10)

    bt_logout = Button(content_frame, text='Выйти', command=show_login_page, bg='#f44336', fg='#fff', padx=20, pady=10)
    bt_logout.pack(pady=10)

def show_transfer_page():
    global entry_transfer_amount, entry_transfer_code, entry_transfer_phone, transfer_method_var

    transfer_window = Toplevel(root)
    transfer_window.title("Перевод средств")
    transfer_window.geometry("600x400")

    label_font = ('Helvetica', 12)
    entry_font = ('Bahnschrift SemiLight', 12)

    transfer_method_var = StringVar(value="code")

    lbl_method = Label(transfer_window, text="Выберите метод перевода:", font=label_font)
    lbl_method.place(x=50, y=20)
    rb_code = Radiobutton(transfer_window, text="По личному коду", variable=transfer_method_var, value="code", font=label_font)
    rb_code.place(x=50, y=50)
    rb_phone = Radiobutton(transfer_window, text="По номеру телефона", variable=transfer_method_var, value="phone", font=label_font)
    rb_phone.place(x=50, y=80)

    lbl_amount = Label(transfer_window, text="Сумма:", font=label_font)
    lbl_amount.place(x=15, y=120)
    entry_transfer_amount = Entry(transfer_window, font=entry_font)
    entry_transfer_amount.place(x=150, y=120)

    lbl_code = Label(transfer_window, text="Личный код:", font=label_font)
    lbl_code.place(x=15, y=160)
    entry_transfer_code = Entry(transfer_window, font=entry_font)
    entry_transfer_code.place(x=150, y=160)

    lbl_phone = Label(transfer_window, text="Номер телефона:", font=label_font)
    lbl_phone.place(x=15, y=200)
    entry_transfer_phone = Entry(transfer_window, font=entry_font)
    entry_transfer_phone.place(x=150, y=200)

    bt_transfer = Button(transfer_window, text="Перевести", command=transfer_funds, font=label_font)
    bt_transfer.place(x=250, y=300)

def show_transactions_page():
    transactions_window = Toplevel(root)
    transactions_window.title("История переводов")
    transactions_window.geometry("600x400")

    if current_user and current_user.get("login") in inf_users:
        user_login = current_user["login"]
        transactions = load_transactions(user_login)
        listbox = Listbox(transactions_window, width=80, height=20)
        listbox.pack(pady=20)

        for transaction in transactions:
            sender = transaction.get("sender", "Неизвестный отправитель")
            sender_code = transaction.get("sender_code", "Неизвестный код")
            recipient = transaction.get("recipient", "Неизвестный получатель")
            recipient_code = transaction.get("recipient_code", "Неизвестный код")
            amount = transaction.get("amount", "Неизвестная сумма")
            date = transaction.get("date", "Неизвестная дата")
            listbox.insert(END, f"{date} - {sender} ({sender_code}) -> {recipient} ({recipient_code}): {amount} рублей")

    close_button = Button(transactions_window, text="Закрыть", command=transactions_window.destroy)
    close_button.pack(pady=10)


def show_message(title, message):
    message_box = Toplevel(root)
    message_box.title(title)
    Label(message_box, text=message, padx=20, pady=20).pack()
    Button(message_box, text="OK", command=message_box.destroy).pack(pady=10)


def show_cards_list(parent_frame):

    label_font = ('Helvetica', 20)

    cards_window = Toplevel(root)
    cards_window.title("Список карт")
    cards_window.geometry("400x300")

    Label(cards_window,text='Пока в разработке',font=label_font).place(x=200,y=150)

    for card in inf_users[current_user["login"]].get("cards", []):
        card_label = Label(cards_window, text=f'{card["type"]}\nБаланс: {card["balance"]} ₽', bg='#444', fg='#fff', padx=10, pady=5)
        card_label.pack(fill=X, pady=2)

def show_edit_profile_page():
    global entry_name, entry_surname, entry_age, lbl_own_code

    edit_window = Toplevel(root)
    edit_window.title("Редактировать профиль")
    edit_window.geometry("600x400")

    user_data = inf_users[current_user["login"]]

    label_font = ('Helvetica', 12)
    entry_font = ('Bahnschrift SemiLight', 12)

    lbl_name = Label(edit_window, text="Имя:", font=label_font)
    lbl_name.place(x=50, y=25)
    entry_name = Entry(edit_window, font=entry_font)
    entry_name.place(x=140, y=25)
    entry_name.insert(0, user_data.get("name", ""))

    lbl_surname = Label(edit_window, text="Фамилия:", font=label_font)
    lbl_surname.place(x=50, y=55)
    entry_surname = Entry(edit_window, font=entry_font)
    entry_surname.place(x=140, y=55)
    entry_surname.insert(0, user_data.get("surname", ""))

    lbl_age = Label(edit_window, text='Возраст:', font=label_font)
    lbl_age.place(x=50, y=85)
    entry_age = Entry(edit_window, font=entry_font)
    entry_age.place(x=140, y=85)
    entry_age.insert(0, user_data.get("age", ""))

    bt_save = Button(edit_window, text="Сохранить", command=save_profile_data, width=10, font=label_font)
    bt_save.place(x=200, y=300)


    lbl_own_code = Label(edit_window,text=f'Ваш личный код: {user_data.get("own_code", "")}', font=label_font)
    lbl_own_code.bind('<Button-1>', lambda e: copy_own_code())
    lbl_own_code.place(x=20,y=200)

def copy_own_code():
    code = lbl_own_code.cget("text").split(": ")[1]
    if code:
        root.clipboard_clear()
        root.clipboard_append(code)
        root.update()
        messagebox.showinfo("Информация", "Личный код скопирован!")


def transfer_funds():
    amount = entry_transfer_amount.get()
    method = transfer_method_var.get()
    if not amount:
        show_message("Ошибка", "Введите сумму перевода")
        return

    try:
        amount = float(amount)
    except ValueError:
        show_message("Ошибка", "Сумма должна быть числом")
        return

    if amount <= 0:
        show_message("Ошибка", "Сумма должна быть положительной")
        return

    if current_user and current_user.get("login") in inf_users:
        if inf_users[current_user["login"]]["balance"] < amount:
            show_message("Ошибка", "Недостаточно средств")
            return

        recipient = None
        if method == "code":
            code = entry_transfer_code.get()
            for user, data in inf_users.items():
                if data.get("own_code") == code:
                    recipient = user
                    break
            if not recipient:
                show_message("Ошибка", "Неверный личный код")
                return
        elif method == "phone":
            phone = entry_transfer_phone.get()
            for user, data in inf_users.items():
                if data.get("phone") == phone:
                    recipient = user
                    break
            if not recipient:
                show_message("Ошибка", "Неверный номер телефона")
                return

        inf_users[current_user["login"]]["balance"] -= amount
        inf_users[recipient]["balance"] += amount
        save_data()

        transaction_for_sender = {
            "sender": current_user["login"],
            "sender_code": inf_users[current_user["login"]]["own_code"],
            "recipient": recipient,
            "recipient_code": inf_users[recipient]["own_code"],
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        transaction_for_recipient = {
            "sender": current_user["login"],
            "sender_code": inf_users[current_user["login"]]["own_code"],
            "recipient": recipient,
            "recipient_code": inf_users[recipient]["own_code"],
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_transaction(current_user["login"], transaction_for_sender)
        save_transaction(recipient, transaction_for_recipient)

        show_message("Успех", "Перевод успешно выполнен")
        show_profile_page()
    else:
        show_message("Ошибка", "Пользователь не найден")


def save_profile_data():
    if current_user and current_user.get("login") in inf_users:
        name = entry_name.get()
        surname = entry_surname.get()
        age = entry_age.get()

        inf_users[current_user["login"]]["name"] = name
        inf_users[current_user["login"]]["surname"] = surname
        inf_users[current_user["login"]]["age"] = age
        save_data()
    else:
        show_message("Ошибка", "Пользователь не найден")

def add_money():
    global lb_balance
    if current_user and current_user.get("login") in inf_users:
        inf_users[current_user["login"]]["balance"] += 100
        current_user["balance"] = inf_users[current_user["login"]]["balance"]
        lb_balance.config(text=f'Ваш баланс: {current_user["balance"]} рублей')
        save_data()
    else:
        show_message("Ошибка", "Пользователь не найден")

def localCode():
    all_symbols = [
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
        'v', 'b', 'n', 'm',
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C',
        'V', 'B', 'N', 'M',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    while True:
        code = ''.join(random.choice(all_symbols) for _ in range(20))
        if not any(user.get("own_code") == code for user in inf_users.values()):
            return code


def registration(event):
    global entry_login, entry_password, lb_register_status, inf_users, entry_name, entry_surname, entry_age

    log = entry_login.get()
    pas = entry_password.get()
    name = entry_name.get()
    surname = entry_surname.get()
    age = entry_age.get()

    if not is_valid_username(log):
        lb_register_status.config(text='Логин или пароль содержат запрещенные символы')
        return
    if not is_valid_pasword(pas):
        lb_register_status.config(text='Пароль должен содержать минимум 5 символов')
        return

    if not (log and pas and name and surname and age):
        lb_register_status.config(text='Заполните все поля')
        return

    if log in inf_users:
        lb_register_status.config(text='Логин занят')
        return

    try:
        age = int(age)
    except ValueError:
        lb_register_status.config(text='Возраст должен быть числом')
        return

    inf_users[log] = {
        "password": pas,
        "balance": 0,
        "own_code": localCode(),
        "cards": [],
        "name": name,
        "surname": surname,
        "age": age,
        "is_admin": False
    }
    save_data()
    lb_register_status.config(text='Регистрация успешна')
    root.after(1500, show_login_page)


def authorize(event):
    global entry_login_auth, entry_password_auth, lb_auth_status, inf_users, current_user
    log = entry_login_auth.get()
    pas = entry_password_auth.get()

    if not (log and pas):
        lb_auth_status.config(text='Введите логин и пароль')
        return

    user = inf_users.get(log)
    if not user or user["password"] != pas:
        lb_auth_status.config(text='Неверный логин или пароль')
        return

    current_user = {
        "login": log,
        "balance": user["balance"],
        "is_admin": user.get("is_admin", False)
    }

    print(f"Авторизован")
    show_Hello_page()

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()



# ----------------------------------------------------------------------
#Реализация админ панели



def create_admin_account():
    global entry_login_admin, entry_password_admin, lb_admin_status

    log = entry_login_admin.get()
    pas = entry_password_admin.get()

    if not is_valid_username(log):
        lb_admin_status.config(text='Логин содержит недопустимые символы')
        return

    if not is_valid_pasword(pas):
        lb_admin_status.config(text='Пароль должен содержать минимум 5 символов')
        return

    if log in inf_users:
        lb_admin_status.config(text='Логин занят')
        return

    inf_users[log] = {
        "password": pas,
        "balance": 0,
        "own_code": localCode(),
        "cards": [],
        "name": "Admin",
        "surname": "User",
        "age": 0,
        "is_admin": True
    }
    save_data()
    lb_admin_status.config(text='Администратор успешно создан')
    root.after(1500, show_admin_panel)

def show_admin_panel():
    global admin_frame, entry_login_admin, entry_password_admin, lb_admin_status

    label_font = ('Helvetica', 13)

    clear_frame()

    admin_frame = Frame(root)
    admin_frame.pack(fill=BOTH, expand=True)

    user_list_frame = Frame(admin_frame)
    user_list_frame.place(x=20, y=20)

    user_list = Listbox(user_list_frame, width=50, height=20)
    user_list.pack(side=LEFT, fill=Y)

    scrollbar = Scrollbar(user_list_frame)
    scrollbar.pack(side=LEFT, fill=Y)

    user_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=user_list.yview)

    for user in inf_users.keys():
        user_list.insert(END, user)

    user_list.bind("<<ListboxSelect>>", show_user_details)

    btn_delete_user = Button(admin_frame, text="Удалить пользователя", command=lambda: delete_user(user_list), font=label_font)
    btn_delete_user.place(x=20, y=400)

    btn_add_admin = Button(admin_frame, text="Назначить администратором", command=lambda: add_admin(user_list), font=label_font)
    btn_add_admin.place(x=220, y=400)

    btn_back = Button(admin_frame, text="Назад", command=show_profile_page, font=label_font)
    btn_back.place(x=470, y=400)

    admin_controls_frame = Frame(admin_frame)
    admin_controls_frame.place(x=400, y=20)

    lbl_create_admin = Label(admin_controls_frame, text="Создать нового администратора", font=label_font)
    lbl_create_admin.pack(anchor="w", pady=5)

    lbl_login = Label(admin_controls_frame, text="Логин:", font=label_font)
    lbl_login.pack(anchor="w", pady=5)

    entry_login_admin = Entry(admin_controls_frame)
    entry_login_admin.pack(pady=5)

    lbl_password = Label(admin_controls_frame, text="Пароль:", font=label_font)
    lbl_password.pack(anchor="w", pady=5)

    entry_password_admin = Entry(admin_controls_frame, show='*')
    entry_password_admin.pack(pady=5)

    lb_admin_status = Label(admin_controls_frame, text='', fg='red')
    lb_admin_status.pack(pady=5)

    btn_create_admin = Button(admin_controls_frame, text="Создать", command=create_admin_account)
    btn_create_admin.pack(pady=10)


def show_user_details(event):

    selection = event.widget.curselection()

    if selection:
        index = selection[0]
        user_login = event.widget.get(index)

        user_details = Toplevel(root)
        user_details.title(f"Профиль пользователя: {user_login}")
        user_details.geometry("300x300")

        user_info = inf_users.get(user_login)

        if user_info:
            Label(user_details, text=f"Логин: {user_login}").pack()
            Label(user_details, text=f"Баланс: {user_info['balance']} рублей").pack()
            Label(user_details, text=f"Код: {user_info['own_code']}").pack()
            Label(user_details, text=f"Карты: {len(user_info['cards'])}").pack()
            Label(user_details, text=f"Имя: {user_info.get('name', 'Не указано')}").pack()
            Label(user_details, text=f"Фамилия: {user_info.get('surname', 'Не указано')}").pack()
            Label(user_details, text=f"Возраст: {user_info.get('age', 'Не указано')}").pack()
            Label(user_details, text=f"Пароль: {user_info.get('password','Не указано')}").pack()

def delete_user(user_list):
    selection = user_list.curselection()
    if selection:
        index = selection[0]
        user_login = user_list.get(index)

        if user_login in inf_users:
            del inf_users[user_login]
            save_data()
            user_list.delete(index)
            messagebox.showinfo("Успех", "Пользователь успешно удален")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")
    else:
        messagebox.showerror("Ошибка", "Выберите пользователя для удаления")

def add_admin(user_list):
    selection = user_list.curselection()
    if selection:
        index = selection[0]
        user_login = user_list.get(index)

        if user_login in inf_users:
            inf_users[user_login]['is_admin'] = True
            save_data()
            messagebox.showinfo("Успех", "Пользователь успешно назначен администратором")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")
    else:
        messagebox.showerror("Ошибка", "Выберите пользователя для назначения администратором")


root = Style().master
root.geometry('800x600')
root.title('Уникальная банковская система')

style.configure('TButton', padding=6, font=('Helvetica', 12))
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12))

load_data()
show_login_page()


root.mainloop()