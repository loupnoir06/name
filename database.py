import sqlite3
from utils import *

def connection():
    return sqlite3.connect('dbt.db')


def create_table_tovarlar():
    con = connection()
    cur = con.cursor()
    cur.execute("""
        create table if not exists tovarlar(
                id integer not null primary key autoincrement,
                tovarlar varchar(30),
                tovarlar_soni int,
                narxlar varchar(30)
        )
    """)
    con.commit()
    con.close()


def delete_tovar(table, tovar):
    con = connection()
    cur = con.cursor()
    cur.execute(f"""
        delete from {table} where `tovarlar`='{tovar}'
    """)
    con.commit()


def create_table_user():
    con = connection()
    cur = con.cursor()
    cur.execute("""
        create table if not exists user(
                id integer not null primary key autoincrement,
                first_name varchar(30),
                last_name varchar(30),
                birth_day date,
                email varchar(50),
                is_active boolean default false,
                username varchar(30),
                password varchar(150),
                admin boolean default false
        )
    """)
    con.commit()
    con.close()


def add_user(data: dict):
    con = connection()
    cur = con.cursor()
    hashed_password = hash_password(data['password'])
    data['password'] = hashed_password
    query = """
        insert into user(
        first_name,
        last_name,
        birth_day,
        email,
        is_active,
        username,
        password
        ) values
        (?, ?, ?, ?, ?, ?, ?)
    """
    values = tuple(data.values())
    cur.execute(query, values)
    con.commit()
    con.close()


def add_tovar(data: dict):
    con = connection()
    cur = con.cursor()
    query = """
        insert into tovarlar(
        tovarlar,
        tovarlar_soni,
        narxlar
        ) values
        (?, ?, ?)
    """
    values = tuple(data.values())
    cur.execute(query, values)
    con.commit()
    con.close()


def user_is_exist(field, value):
    query = f"""
        select count(id) from user
        where {field}=?
    """
    value = (value,)
    con = connection()
    cur = con.cursor()
    cur.execute(query, value)
    return cur.fetchone()[0]


def update(table, part, new_data, username):
    con = connection()
    cur = con.cursor()
    cur.execute(f"""
        update {table}
        set {part}='{new_data}'
        where `username`='{username}'
    """)
    con.commit()


def update_price(table, new_data, tovar):
    con = connection()
    cur = con.cursor()
    cur.execute(f"""
        update {table}
        set narxlar='{new_data}'
        where `tovarlar`='{tovar}'
    """)
    con.commit()


def update_count(table, new_data, tovar):
    con = connection()
    cur = con.cursor()
    cur.execute(f"""
        update {table}
        set tovarlar_soni='{new_data}'
        where `tovarlar`='{tovar}'
    """)
    con.commit()


def login(username: str, password: str):
    con = connection()
    cur = con.cursor()
    hashed_password = hash_password(password)
    query = """
        select * from user
        where username=? and password=?
    """
    value = (username, hashed_password)
    cur.execute(query, value)
    return bool(cur.fetchone())

def admin_panel(username, password):
    a=login(username, password)
    if a:
        con=connection()
        cur=con.cursor()
        cur.execute("""
        select * from user
        """)
        rows = cur.fetchall()
        arr=[]
        for row in rows:
            arr.append(row)
        
        for i in arr:
            print(i)
            if i[6]==username:
                b=i[8]
        
        if b:
            print("Admin paneliga xush kelibsiz!")
            n=input("""
        1.Tovar qo'shish
        2.Narxni o'zgartirish
        3.Tovar o'chirish
        4.Admin qo'shish
        5.Admin o'chirish
        0.Chiqish
        Tanlang: """)
            if n=='1':
                tovar=input("Tovarni kiriting: ")
                digit=input('Tovar sonini kiriting: ')
                price=input("Tovar narxini kiriting: ")
                data = dict(
                    tovarlar=tovar,
                    tovarlar_soni=digit,
                    narxlar=price,
                )
                add_tovar(data)
                print("Muvaffaqiyatli qo'shildi!")

            elif n=='2':
                tovar=input("Tovarni kiriting: ")
                new_price=input("Yangi narxni kiriting: ")
                update_price('tovarlar', new_price, tovar)
                print("Narx o'zgartirildi!")

            elif n=='3':
                tovar=input("Tovarni kiriting: ")
                y_or_n=input("Tovarni rostan o'chirvoqchimisiz(HA->y, YO'Q->n): ")
                if y_or_n=='y':
                    delete_tovar('tovarlar', tovar)
                    print("Muvaffaqiyatli o'chirildi!")

            elif n=='4':
                username1=input("Username kiriting: ")
                update('user', 'admin', True, username1)
                print("Admin qo'shildi!")

            elif n=='5':
                username1=input("Username kiriting: ")
                update('user', 'admin', False, username1)
                print("Admin o'chirildi!")
