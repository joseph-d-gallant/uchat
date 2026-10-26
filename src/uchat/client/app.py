from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import random
import time
import requests.cookies


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    token = request.cookies.get('token', default=None)
    if token:
        return render_template('main.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)

    data = {
        'username' : username,
        'password' : password,
    }

    response = requests.post('http://server:5500/connect', data=data)
    token = response.cookies.get('token')
    username = response.cookies.get('username')
    
    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', token, httponly=True)
    response.set_cookie('username', username)
    
    return response

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    message = request.form.get('message')
    reciever = request.args.get('to')
    token = request.cookies.get('token')
    username = request.cookies.get('username')

    cookies = {
        'token' : token, 
    }

    data = {
        'target' : reciever,
        'username' : username,
        'message' : message
    }

    response = requests.post('http://server:5500/handle', data=data, cookies=cookies)
    raw_data = response.text
    clean_data = raw_data.strip()[1:-1].replace('"', '')

    strings = clean_data.split(',')

    messages = []
    for message in strings:
        split = message.strip().split(":", 1)
        if len(split) == 2:
            messages.append([split[0].strip(), split[1].strip()])


    stringBuilder = ""
    for element in messages:
        if element[0] == username:
            stringBuilder += '<div class="outgoing-message">' + '<h1 class="message-content">{}</h1></div>'.format(element[1])  
        else:
            stringBuilder += '<div class="incoming-message">' + '<h1 class="message-content">{}</h1></div>'.format(element[1])
    
    print(stringBuilder)

    return render_template('main.html', messages=stringBuilder)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5005)