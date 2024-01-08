from sqlite3 import Connection

conn = Connection("data.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS locations(id TEXT, name TEXT, phone TEXT, about TEXT, latitude TEXT, longitude TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS users(id TEXT, login TEXT, parol TEXT)""")
conn.commit()
conn.close()

def add_location(id, name, phone, about, latitude, longitude):
    conn = Connection("data.db")
    c = conn.cursor()
    c.execute(
        f"""INSERT INTO locations VALUES ("{id}", "{name}", "{phone}", "{about}", "{latitude}", "{longitude}")"""
    )
    conn.commit()
    conn.close()

def add_user(id, login, parol):
    conn = Connection("data.db")
    c = conn.cursor()
    c.execute(
        f"""INSERT INTO users VALUES ("{id}", "{login}", "{parol}")"""
    )
    conn.commit()
    conn.close()

def set_admin(id, login, parol):
    conn = Connection("data.db")
    c = conn.cursor()
    c.execute(
        f"""UPDATE users SET login="{login}", parol="{parol}" WHERE id="{id}" """
    )
    conn.commit()
    conn.close()



def get_location(id):
    conn = Connection("data.db")
    c = conn.cursor()
    data = c.execute(
        f"""SELECT * FROM locations WHERE id="{id}" """
    ).fetchone()
    conn.commit()
    conn.close()
    return {
        "id": data[0],
        "name": data[1],
        "phone": data[2],
        "about": data[3],
        "latitude": data[4],
        "longitude": data[5],
    } if data else False

def get_user(id):
    conn = Connection("data.db")
    c = conn.cursor()
    data = c.execute(
        f"""SELECT * FROM users WHERE id="{id}" """
    ).fetchone()
    conn.commit()
    conn.close()
    return {
        "id": data[0],
        "login": data[1],
        "parol": data[2],
    } if data else False

def remove_location(id):
    conn = Connection("data.db")
    c = conn.cursor()
    flag = True
    zakaz = c.execute(f"""SELECT * FROM locations WHERE id="{id}" """).fetchall()
    if zakaz:
        c.execute(
            f"""DELETE FROM locations WHERE id="{id}" """
        )
    else:
        flag = False
    conn.commit()
    conn.close()
    return flag
