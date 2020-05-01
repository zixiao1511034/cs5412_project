import psycopg2

conn = psycopg2.connect(database="test_db", user="postgres", password="123456", host="127.0.0.1", port="5432")
print(conn)

cur = conn.cursor()
cur.execute("CREATE TABLE cow(ID integer, URL varchar);")

conn.commit()
conn.close