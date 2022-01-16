
import sqlite3

# def init_db_with_tg_id(telegram_id):
#     try:
#         sqlite_connection = sqlite3.connect('database.db')
#         cursor = sqlite_connection.cursor()
#         print("Подключен к SQLite")

#         sqlite_insert = """INSERT INTO users()
#                               VALUES ();"""

#         data_tuple = []
#         cursor.execute(sqlite_insert, data_tuple)
#         sqlite_connection.commit()
#         print("Переменные Python успешно вставлены в таблицу sqlitedb_developers")

#         cursor.close()

#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#     finally:
#         if sqlite_connection:
#             sqlite_connection.close()
#             print("Соединение с SQLite закрыто")



def insert_teleram_id(telegram_id):
    try:
        sqlite_connection = sqlite3.connect('database.db')
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
            return cursor.lastrowid 

insert_teleram_id(222)
