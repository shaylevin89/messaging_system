from flask import Flask, request, jsonify
import logging
import DB
from functools import wraps
import jwt
import datetime

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app = Flask(__name__)
app.config['secret'] = 'shaylevin'


class Message:
    def __init__(self, row_message):
        self.row_message = row_message
        self.json_message = dict(msg_id=None, sender=None, receiver=None, subject=None, msg_data=None, created_at=None)

    def to_json_message(self):
        self.json_message['msg_id'] = self.row_message[0]
        self.json_message['sender'] = self.row_message[1]
        self.json_message['receiver'] = self.row_message[2]
        self.json_message['subject'] = self.row_message[3]
        self.json_message['msg_data'] = self.row_message[4]
        self.json_message['created_at'] = self.row_message[5]
        return self.json_message


@app.route('/register', methods=['POST'])
def register():
    credentials = request.get_json(force=True)
    if 'username' not in credentials or 'password' not in credentials:
        return {"error": "Credentials missing"}, 400
    if DB.create_user(credentials['username'], credentials['password']):
        return {"message": "User created"}, 200
    return {"error": "Username not available"}


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {"error": "Authentication required"}, 400
    if not DB.check_user_credentials(auth.username, auth.password):
        return {"error": "Authentication failed"}, 400
    token = jwt.encode({'username': auth.username,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
                       app.config['secret'], 'HS256')
    return jsonify({'token': token})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Auth-token' in request.headers:
            token = request.headers['Auth-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['secret'], 'HS256')
            username = data['username']
        except Exception as e:
            logging.error(e)
            return jsonify({'message': 'Token is invalid, please login'}), 401
        return f(username, *args, **kwargs)
    return decorated


@app.route("/message", methods=['POST'])
@token_required
def write_message(username):
    try:
        msg = request.get_json(force=True)
        if DB.insert_message(
                username, msg.get('receiver'), msg.get('subject'), msg.get('msg_data'), msg.get('created_at')):
            return {"message": "Message created"}, 201
        else:
            return {"error": "Wrong message keys or values"}, 400
    except Exception as e:
        logging.error(e)
        return {"error": "Wrong message format. only JSON accepted"}, 400


@app.route("/message/<msg_id>", methods=['GET'])
@token_required
def read_message(username, msg_id):
    if msg_id.isdigit():
        row_message = DB.get_message(msg_id, username)
        if row_message:
            json_message = Message(row_message).to_json_message()
            return jsonify({'message': json_message}), 200
        return {"error": "Msg_id not found"}, 400
    return {"error": "Msg_id not valid"}, 400


@app.route("/unread_messages", methods=['GET'])
@app.route("/messages", methods=['GET'])
@token_required
def read_messages(username):
    path = request.path
    unread = None
    if path == '/unread_messages':
        unread = True
    messages = DB.get_messeges(username, unread)
    if messages:
        json_messages = []
        for message in messages:
            json_messages.append(Message(message).to_json_message())
        return jsonify({'messages': json_messages}), 200
    if unread:
        return {"message": "No unread messages for current user"}, 200
    return {"message": "No messages for current user"}, 200


@app.route('/message/<msg_id>', methods=['DELETE'])
@token_required
def delete_message(username, msg_id):
    if msg_id.isdigit():
        DB.delete_message(msg_id, username)
        return {"message": f"Message {msg_id} no longer exist"}, 200
    return {"error": "Msg_id not valid"}, 400


if __name__ == '__main__':
    app.run('0.0.0.0', 3489)
