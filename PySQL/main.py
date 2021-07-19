import psycopg2
import json
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def region_from_js_to_db():
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
    with open("json/avito_region.json") as file:
        data = json.load(file)
    for item in data['data']:
        print(f"Сохраненный {item['id']} = {item['name']}")
        id_reg = item['id']
        name_reg = item['name']

        cur.execute(
            "INSERT INTO AVITO_REGION (id,NAME) VALUES (id_reg, name_reg)"
        )

        con.commit()
        print("Record inserted successfully")


def create_region_db():
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
    cur.execute('''CREATE TABLE AVITO_REGION
        (id INT PRIMARY KEY NOT NULL,
         NAME TEXT NOT NULL);''')

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
    #create_region_db()
    region_from_js_to_db()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
