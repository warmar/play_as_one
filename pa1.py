from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, jsonify

app = Flask(__name__)
from flask_socketio import SocketIO, emit
from json import loads, dumps

socketio = SocketIO(app)
mode = get_mode()
user_count = 0
users = {}
democracy = []


@app.route("/")
def hello():
    render_template('index.html')


if __name__ == "__main__":
    app.run()
    socketio.run(app)


@socketio.on('test')
def handle_test():
    emit('test')


@socketio.on('initialize')
def handle_initialize():
    emit("initialize", {'input_type': get_input_mode()}, {'mode': mode})


@socketio.on("add user")
def handle_add_user(json):
    global user_count
    user_count += 1
    user = loads(json)
    users[user['username']] = {'input_count': 0}


@socketio.on('on disconnect')
def handle_disconnect(json):
    global user_count
    user_count -= 1
    user = loads(json)
    users.pop(user['username'])


@socketio.on("sendInput")
def handle_input(json):
    user_input = loads(json)
    users[input['username']]['input_count'] += 1
    if (mode == 'chaos'):
        handle_chaos(user_input)
    elif (mode == 'democracy'):
        handle_democracy(user_input)


def handle_chaos(user_input):
    execute_input(user_input)


def handle_democracy(user_input):
    global democracy
    for demo_input in democracy:
        if demo_input[0] == user_input['input']:
            demo_input[1] +=1
            break
    democracy.append((user_input['input'], 1))

def execute_democracy():
    most_votes = ""
    most_count = 0
    for input in democracy:
        if input > most_count:
            most_votes = input
