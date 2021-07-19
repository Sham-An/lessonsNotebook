import psycopg2
#From URL https://dev-gang.ru/article/rabota-s-postgresql-v-python-xn8721sq0g/
con = psycopg2.connect(
  database="postgres",
  user="postgres",
  #password="",
  password=input("Пароль"),
  host="127.0.0.1",
  port="5432"
)

print("Database opened successfully")
cur = con.cursor()
#cur.execute('''CREATE TABLE STUDENT
#     (ADMISSION INT PRIMARY KEY NOT NULL,
#      NAME TEXT NOT NULL,
#      AGE INT NOT NULL,
#      COURSE CHAR(50),
#      DEPARTMENT CHAR(50));''')
#
# print("Table created successfully")
# con.commit()
# con.close()

cur.execute(
  "INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3446, 'John2', 19, 'Computer Science', 'ICT')"
)

con.commit()
print("Record inserted successfully")

# con.close()
#
# con = psycopg2.connect(
#    database="postgres",
#    user="postgres",
#    password="Kaliakakya",
#    host="127.0.0.1",
#    port="5432"
# )

print("Database opened 2 successfully")

cur = con.cursor()
cur.execute(
   "INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3419, 'Abel', 17, 'Computer Science', 'ICT')"
)
cur.execute(
  "INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3421, 'Joel', 17, 'Computer Science', 'ICT')"
)
cur.execute(
  "INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3422, 'Antony', 19, 'Electrical Engineering', 'Engineering')"
)
cur.execute(
  "INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3423, 'Alice', 18, 'Information Technology', 'ICT')"
)

con.commit()
print("Records inserted successfully")

con.close()