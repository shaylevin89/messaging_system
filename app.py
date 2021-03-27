from flask import Flask, request, jsonify
import logging
import DB
import secure
from Message import Message
from functools import wraps
import jwt
import datetime
import os

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app = Flask(__name__)
app.config['secret'] = os.getenv('JWT_SECRET')


def get_messages_id(messages):
    if len(messages) == 0:
        return False
    elif len(messages) == 1:
        messages_id_tup = '(' + str(messages[0]['msg_id']) + ')'
    else:
        messages_id_tup = tuple(message['msg_id'] for message in messages)
    return messages_id_tup


@app.route('/register', methods=['POST'])
def register():
    credentials = request.get_json(force=True)
    if 'username' not in credentials or 'password' not in credentials:
        return {"error": "Credentials missing"}, 400
    hashed_password = secure.hash_generate(credentials['password'])
    if DB.create_user(credentials['username'], hashed_password):
        return {"message": "User created"}, 201
    return {"error": "Username not available"}, 400


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {"error": "Missing fields"}, 400
    db_user = DB.get_user(auth.username)
    db_user_password = db_user['password']
    if not secure.login_check(db_user_password, auth.password):
        return {"error": "Authentication failed"}, 400
    token = jwt.encode({'username': auth.username,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('JWT_EXP', 20)))},
                       app.config['secret'], 'HS256')
    return jsonify({'token': token})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Auth-token' in request.headers:
            token = request.headers['Auth-token']
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['secret'], 'HS256')
            username = data['username']
        except Exception as e:
            logging.error(e)
            return jsonify({'error': 'Token is invalid, please login'}), 401
        return f(username, *args, **kwargs)
    return decorated


@app.route("/message", methods=['POST'])
@token_required
def write_message(username):
    try:
        request_body = request.get_json(force=True)
    except Exception as e:
        logging.error(e)
        return {"error": "Wrong message format. only JSON accepted"}, 400
    message = Message(request_body, username)
    if message.ready_to_DB():
        if DB.insert_message(message):
            return {"message": "Message created"}, 201
        else:
            return {"error": "Message did not insert"}, 400
    return {"error": "Wrong message data"}, 400


@app.route("/message/<msg_id>", methods=['GET'])
@token_required
def read_message(username, msg_id):
    if msg_id.isdigit():
        db_message = DB.get_message(msg_id, username)
        if db_message:
            msg_id_tup = '(' + str(msg_id) + ')'
            DB.update_messages_as_read(msg_id_tup, username)
            json_message = Message(db_message, username).to_json()
            return jsonify({'message': json_message}), 200
        return {"error": "Msg_id not available"}, 400
    return {"error": "Msg_id not valid"}, 400


@app.route("/unread_messages", methods=['GET'])
@app.route("/messages", methods=['GET'])
@token_required
def read_messages(username):
    path = request.path
    unread = False
    if path == '/unread_messages':
        unread = True
    db_messages = DB.get_messages(username, unread)
    if db_messages:
        msg_id_tup = get_messages_id(db_messages)
        DB.update_messages_as_read(msg_id_tup, username)
        json_messages_array = []
        for db_message in db_messages:
            message = Message(db_message, username).to_json()
            json_messages_array.append(message)
        return jsonify({'messages': json_messages_array}), 200
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
