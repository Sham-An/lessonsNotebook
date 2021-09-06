import psycopg2
import json
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def city_list_from_db():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        # password="",
        password=input("Пароль"),
        host="127.0.0.1",
        port="5432"
    )

    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT id, name,parent_Id from AVITO_city")

    rows = cur.fetchall()
    for row in rows:
        print("id =", row[0], " NAME =", row[1], "parent_Id =", row[2])
        #print("NAME =", row[1])

    print("Operation done successfully")
    con.close()

def city_from_js_to_db():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        # password="",
        password=input("Пароль"),
        host="127.0.0.1",
        port="5432"
    )

    print("Database opened successfully")
    cur = con.cursor()
    with open("json/avito_city.json",'r', encoding="utf-8") as file:
        data = json.load(file)
        print("Json opened")
    for item in data['data']:
        print(f"Сохраненный {item['id']} = {item['name']} регион {item['parent_Id']}")
        #id_reg = item['id']
        #name_reg = item['name']
        values = ({'id': item['id'], 'name': item['name'], 'parent_Id': item['parent_Id']})
        cur.execute(
            "INSERT INTO AVITO_city (id,NAME,parent_Id) VALUES (%(id)s,%(name)s,%(parent_Id)s)", values
        )
#        values = ({'id': 1, 'name': 'Vasya', 'age': 45})
#        cursor.execute("INSERT INTO tableName(id, name, age) VALUES (%(id)s,%(name)s,%(age)s)", values)
        con.commit()
        print("Record inserted successfully")


def create_city_db():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        # password="",
        password=input("Пароль"),
        host="127.0.0.1",
        port="5432"
    )

    print("Database opened successfully")
    cur = con.cursor()
    cur.execute('''CREATE TABLE AVITO_city
        (id INT PRIMARY KEY NOT NULL,
         NAME TEXT NOT NULL, parent_Id INT NOT NULL);''')

    print("Table created successfully")
    con.commit()
    con.close()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print_hi('PyCharm3')
    #create_city_db()
    #city_from_js_to_db()
    city_list_from_db()
