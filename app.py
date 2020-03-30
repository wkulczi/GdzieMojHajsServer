from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hey now you're an all star"


if __name__ == '__main__':
    app.run()
