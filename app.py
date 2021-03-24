from flask import Flask, request
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run('0.0.0.0', 3489)
