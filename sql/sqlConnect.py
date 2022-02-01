
import sqlite3

def insert_teleram_id(telegram_id , db_path = 'sql/database.db' ):
    try:
        sqlite_connection = sqlite3.connect(db_path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert = """INSERT INTO users(telegram_id)
                              VALUES (?);"""

        data_tuple = [telegram_id]
        cursor.execute(sqlite_insert, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу sqlitedb_developers")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            # return cursor.lastrowid 



def insert_data(id , data , data_type,db_path = 'sql/database.db' ):
    try:
        sqlite_connection = sqlite3.connect(db_path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert = f"""UPDATE users SET {data_type} = ? WHERE telegram_id = ?"""

        data_tuple = [data, id]
        cursor.execute(sqlite_insert, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу sqlitedb_developers")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            return cursor.lastrowid 
        
def clean_data(id ,db_path = 'sql/database.db' ):
    try:
        sqlite_connection = sqlite3.connect(db_path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert = f"""DELETE FROM users WHERE telegram_id = ?"""

        data_tuple = [id]
        cursor.execute(sqlite_insert, data_tuple)
        sqlite_connection.commit()
        print(f"Таблица очищена от  пользователя {id}")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            # return cursor.lastrowid 
            

def state_check(id , data , db_path = 'sql/database.db' ):
    try:
        sqlite_connection = sqlite3.connect(db_path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert = f"""SELECT {data} FROM users WHERE telegram_id = ?"""

        data_tuple = [id]
        cursor.execute(sqlite_insert, data_tuple)
        records = cursor.fetchone()
        print(f"Переменная получена {id}")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            return records
            

# def get_developer_info(id):
#     try:
#         sqlite_connection = sqlite3.connect('sqlite_python.db')
#         cursor = sqlite_connection.cursor()
#         print("Подключен к SQLite")

#         sql_select_query = """select * from sqlitedb_developers where id = ?"""
#         cursor.execute(sql_select_query, (id,))
#         records = cursor.fetchall()
#         print("Вывод ID ", id)
#         for row in records:
#             print("ID:", row[0])
#             print("Имя:", row[1])
#             print("Почта:", row[2])
#             print("Добавлен:", row[3])
#             print("Зарплата:", row[4], end="\n\n")

#         cursor.close()

#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#     finally:
#         if sqlite_connection:
#             sqlite_connection.close()
#             print("Соединение с SQLite закрыто")

# a = processor_check(420010587, 'database.db')   
# print(type(a[0]))
            
