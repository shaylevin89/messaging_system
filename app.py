from flask import Flask, request, jsonify
import logging
import DB

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    return ''


@app.route('/login', methods=['POST'])
def login():
    return ''


@app.route('/logout', methods=['POST'])
def logout():
    return ''
"""
- Write message  V
- Get all messages for a specific user
- Get all unread messages for a specific user
- Read message (return one message)
- Delete message (as owner or as receiver)
"""


@app.route("/message", methods=['POST'])
def write_message():
    try:
        msg = request.get_json(force=True)
        # TODO get sender name or just validate
        if DB.insert_message(
                msg.get('sender'), msg.get('receiver'), msg.get('subject'), msg.get('msg_data'), msg.get('created_at')):
            return {"message": "Message created"}, 200
        else:
            return {"error": "Wrong message keys or values"}, 400
    except Exception as e:
        logging.error(e)
        return {"error": "Wrong message format. only JSON accepted"}, 400


if __name__ == '__main__':
    app.run('0.0.0.0', 3489)
