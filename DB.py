import os
import psycopg2.extras
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

DATABASE_URL = os.getenv('DATABASE_URL', "dbname=root user=root password=root")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def insert_message(message):
    try:
        cur.execute(f"""INSERT INTO messages (sender, receiver, subject, msg_data, created_at, unread) 
                        VALUES('{message.sender}', 
                               '{message.receiver}', 
                               '{message.subject}', 
                               '{message.msg_data}', 
                               '{message.created_at}',
                               '{message.unread}');""")
        conn.commit()
        return True
    except Exception as e:
        cur.execute('rollback;')
        logging.error(e)
        return False


def get_messages(username, unread):
    if unread:
        cur.execute(
            f"""select * from messages where unread = 't' and (sender = '{username}' or receiver = '{username}');""")
    else:
        cur.execute(f"""select * from messages where sender = '{username}' or receiver = '{username}';""")  #
    messages = cur.fetchall()
    return messages


def get_message(msg_id, username):
    try:
        cur.execute(f"""select * from messages where msg_id = {msg_id} and 
        (sender = '{username}' or receiver = '{username}');""")
        message = cur.fetchone()
        return message
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


def delete_message(msg_id, username):
    cur.execute(f"""delete from messages where msg_id = {msg_id} and 
        (sender = '{username}' or receiver = '{username}');""")
    conn.commit()


def update_messages_as_read(msg_id_tup, username):
    try:
        cur.execute(f"""update messages set unread = 'f' where msg_id in {msg_id_tup} and 
        (sender = '{username}' or receiver = '{username}');""")
        conn.commit()
        return True
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


def create_user(username, hashed_password):
    try:
        cur.execute(f"""INSERT INTO users (username, password) VALUES('{username}', '{hashed_password}');""")
        conn.commit()
        return True
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


def get_user(username):
    try:
        cur.execute(f"""select * from users where username = '{username}';""")
        user = cur.fetchone()
        return user
    except Exception as e:
        logging.error(e)
        cur.execute('rollback;')
        return False


