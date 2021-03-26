import os
import psycopg2
import logging
from werkzeug.security import generate_password_hash, check_password_hash

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
        logging.error(e)
        return False


def get_messeges(username, unread=None):
    if unread:
        cur.execute(
            f"""select * from messages where unread = 't' and (sender = '{username}' or receiver = '{username}');""")
    else:
        cur.execute(f"""select * from messages where sender = '{username}' or receiver = '{username}';""")  #
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    elif len(rows) == 1:
        message_id_tup = '('+str(rows[0][0])+')'
    else:
        message_id_tup = tuple(row[0] for row in rows)
    update_unread_to_read(message_id_tup)
    return rows


def get_message(msg_id, username):
    try:
        cur.execute(f"""select * from messages where msg_id = {msg_id} and 
        (sender = '{username}' or receiver = '{username}');""")
        row = cur.fetchone()
        return row
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


def delete_message(msg_id, username):
    cur.execute(f"""delete from messages where msg_id = {msg_id} and 
        (sender = '{username}' or receiver = '{username}');""")
    conn.commit()


def update_unread_to_read(msg_id_tup):
    try:
        cur.execute(f"""update messages set unread = 'f' where msg_id in {msg_id_tup};""")
        conn.commit()
        return True
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


def create_user(username, password):
    try:
        hashed_password = generate_password_hash(password, 'sha256')
        cur.execute(f"""INSERT INTO users (username, password) VALUES('{username}', '{hashed_password}');""")
        conn.commit()
        return True
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


def check_user_credentials(username, password):
    try:
        cur.execute(f"""select * from users where username = '{username}';""")
        user = cur.fetchone()
        if user and check_password_hash(user[2], password):
            return True
        return False
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


