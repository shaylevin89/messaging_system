import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# conn = psycopg2.connect("dbname=root user=root password=root")
cur = conn.cursor()

users = cur.execute("SELECT password FROM users")
rows = cur.fetchall()
# print(rows)