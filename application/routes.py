from flask import current_app as app


@app.route('/')
def say_hello():
    return "What have the Romans ever done for us?"
