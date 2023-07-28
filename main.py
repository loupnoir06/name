from database import *
from email_configuration import *


def login_register():
    n=input("1.Kirish \n2.Ro'yhatdan o'tish \nTanlang: ")

    if n.lower()=='admin':
        username=input("Username: ")
        password=input("Password: ")
        admin_panel(username, password)

    if n=='1':
        username=input("Username: ")
        password=input("Password: ")
        a=login(username, password)
        if a:
            n=input("1.Tovar xarid qilish (+): ")

            if n=='+':
                con=connection()
                cur=con.cursor()
                cur.execute("""
                select * from tovarlar
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

                tovar=input("Nima xarid qilmoqchisiz: ")

                con=connection()
                cur=con.cursor()
                cur.execute("""
                select * from tovarlar
                """)
                rows = cur.fetchall()
                arr=[]
                for row in rows:
                    arr.append(row)

                for i in arr:
                    if i[1]==tovar:
                        print(i)

                cur.execute("""
                select * from tovarlar
                """)
                rows = cur.fetchall()
                arr=[]
                for row in rows:
                    arr.append(row)
                for i in arr:
                    if i[1]==tovar:
                        a=i[2]
                
                buy=int(input(f"Nechta xarid qilasiz? {tovar} soni {a}ta: "))

                update_count('tovarlar', a-buy, tovar)

                print("Tovarni muvaffaqiyatli xarid qildingiz: ")


    elif n=='2':
        first_name=input("Ismingiz: ")
        last_name=input("Familyangiz: ")
        birth_day=input("Tug'ilgan (yil-oy-kun): ")
        email=input("Emailingiz: ")

        if user_is_exist('email', email):
            s=False
            while s!=True:
                if user_is_exist('email', email):
                    email=input("Email avval ishlatilgan! Qayta kiriting: ")
                else:
                    s=True

        code=generate_code()
        send_mail(email, code)

        active_code=input("Emailingizga borgan kodni kiriting: ")

        if active_code==code:
            is_active=True
        else:
            s=False
            while s!=True:
                active_code=input("Xato! Qayta kiriting: ")
                if active_code==code:
                    s=True
            is_active=True

        username=input("Yangi username: ")

        if user_is_exist('username', username):
            s=False
            while s!=True:
                if user_is_exist('username', username):
                    username=input("Username avval ishlatilgan! Qayta kiriting: ")
                else:
                    s=True

        password=input("Yangi parol kiriting: ")
        password2=input("Parolni tasdiqlash uchun qayta tering: ")

        if password!=password2:
            s=False
            while s!=True:
                password=input("Birinchi parolga to'g'ri kelmadi! Qayta kiriting: ")
                password2=input("Parolni tasdiqlash uchun qayta tering: ")
                if password2==password:
                    s=True

        data = dict(
            first_name=first_name,
            last_name=last_name,
            birth_day=birth_day,
            email=email,
            is_active=is_active,
            username=username,
            password=password
        )
        add_user(data)
        print("Muvaffaqiyatli ro'yhatdan o'tdingiz!")


login_register()