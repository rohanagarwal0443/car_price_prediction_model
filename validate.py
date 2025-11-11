import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yash0443",
    database="mini_project"
)

if conn.is_connected():
    cursor=conn.cursor()
    def login(data:tuple):
        try:
            q="select * from users_login where email=%s and password=%s"
            cursor.execute(q,data)
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(e)
    
    def singup(data:tuple):
        try:
            sub_data=data[1:3]
            if login(sub_data)==False:
                q="insert into users_login (name,email,password,phone) values (%s,%s,%s,%s)"
                cursor.execute(q,data)
                conn.commit()
                if cursor.rowcount>0:
                    return True
            else:
                return False
        except Exception as e:
            print(e)
            