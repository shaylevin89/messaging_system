from flask import Flask, request
import logging
import DB

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app = Flask(__name__)


@app.route('/')
def root():
    return DB.rows


"""
- Write message
- Get all messages for a specific user
- Get all unread messages for a specific user
- Read message (return one message)
- Delete message (as owner or as receiver)
"""

if __name__ == '__main__':
    app.run('0.0.0.0', 3489)
