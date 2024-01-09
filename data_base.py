import sqlite3
import os


def checking_table():
    if not os.path.exists('data_base_local.db'):
        con = sqlite3.connect('data_base_local.db')
        cursor = con.cursor()

        cursor.execute("""CREATE TABLE location
                        (id INTEGER,
                        name TEXT,
                        lat REAL, 
                        lon REAL)
                    """)
        con.commit()
        con.close()
        print('[!] Таблица создалась успешно!')


def write_to_table(id, lat, lon, name):
    checking_table()

    con = sqlite3.connect('data_base_local.db')
    cursor = con.cursor()
    info = cursor.execute('SELECT * FROM location WHERE id=?', (id, )).fetchone()
    #Если запрос вернул 0 строк, то...
    params = (id, name, lat, lon)
    try:
        if len(info) == 0: 
            cursor.execute(f"INSERT INTO location VALUES (?, ?, ?, ?)", params)

            con.commit()
            cursor.close()
            print('[!] Запись прошла успешно!')
    except:
        cursor.execute(f"INSERT INTO location VALUES (?, ?, ?, ?)", params)

        con.commit()
        cursor.close()
        print('[!] Запись прошла успешно!')

    
def read_to_table(id_users):
    checking_table()

    con = sqlite3.connect('data_base_local.db')
    cursor = con.cursor()
    info = cursor.execute('SELECT * FROM location WHERE id=?', (id_users, )).fetchone()
    try:
        if len(info) > 0: 
            id, lat, lon = cursor.execute('SELECT * FROM location WHERE id=?', (id_users, )).fetchone()
            lat = str(lat)
            lon = str(lon)
            del id
            con.commit()
            cursor.close()
            print('Пользователь есть!')
            return lat, lon
        else:
            lat = '45.009548'
            lon = '39.09996'
            con.commit()
            cursor.close()
            print('Пользователя нет!')
            return lat, lon
        
    except:
        print('Пользователя нет!')
        lat = '45.009548'
        lon = '39.09996'
        con.commit()
        cursor.close()
        return lat, lon
        

def main():
    write_to_table()
    read_to_table()
    

if __name__ == '__main__':
    main()