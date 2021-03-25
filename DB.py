import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL', "dbname=root user=root password=root")
print(DATABASE_URL)
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# conn = psycopg2.connect("dbname=root user=root password=root", sslmode='require')
cur = conn.cursor()

users = cur.execute("SELECT password FROM users")
rows = cur.fetchall()
# print(rows)