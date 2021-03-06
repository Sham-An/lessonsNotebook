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
cur.execute("UPDATE STUDENT set AGE = 20 where ADMISSION = 3420")
con.commit()

print("Total updated rows:", cur.rowcount)
cur.execute("SELECT admission, age, name, course, department from STUDENT")

rows = cur.fetchall()
for row in rows:
   print("ADMISSION =", row[0])
   print("NAME =", row[1])
   print("AGE =", row[2])
   print("COURSE =", row[2])
   print("DEPARTMENT =", row[3], "\n")

print("Operation done successfully")
con.close()

