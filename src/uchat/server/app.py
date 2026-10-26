import redis
from flask import Flask, request, make_response
import random
import secrets


app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379, decode_responses=True)

def chat_key(client1, client2):
    sorted_clients = sorted([client1, client2])
    client_string = ':'.join(sorted_clients)
    return f"chat:{client_string}"

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    username = request.form.get('username')
    password = request.form.get('password')    
    token = secrets.token_hex(16)
    cache.set(f"client:{username}:token", token)

    response = make_response('SUCCESS')
    response.set_cookie('token', token, httponly=True)
    response.set_cookie('username', username)
    return response


@app.route('/handle', methods=['GET', 'POST'])
def handle_request():
    target = request.form.get('target')
    username = request.form.get('username')
    message = request.form.get('message')
    token = request.cookies.get('token')

    formatted_message = f"{username}: {message}"

    if cache.get(f"client:{username}:token") == token:
        key = chat_key(username, target)
        cache.rpush(key, formatted_message)
        return make_response(cache.lrange(key, 0, -1))
    else:
        response = make_response('Invalid Token')
        return response

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5500)