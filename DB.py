import os
import psycopg2
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

DATABASE_URL = os.getenv('DATABASE_URL', "dbname=root user=root password=root")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


def insert_message(sender, receiver, subject, msg_data, created_at):
    try:
        cur.execute(f"""INSERT INTO messages (sender, receiver, subject, msg_data, created_at) 
        VALUES('{sender}', '{receiver}', '{subject}', '{msg_data}', '{created_at}');""")
        conn.commit()
        return True
    except Exception as e:
        cur.execute('rollback;')
        print(e)
        return False


