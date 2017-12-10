from flask import Flask, render_template, request, redirect, url_for, json, jsonify
import datetime
import requests
import logging
 
# Create app
app = Flask(__name__)
 
 
@app.route('/', methods=['GET'])
def index():
    return 'Hello world!'
 
 
@app.route('/stuff/<message>', methods=['GET'])
def url_param_example(message):
    return render_template('message.html', message=message)
 
 
@app.route('/temp', methods=['GET'])
def template_example():
    return render_template('a_temp.html', adj='Awesome',
                           things=['Flask', 'Python'],
                           date=datetime.datetime.now().strftime('%m/%d/%Y'))
 
 
@app.route('/child', methods=['GET'])
def template_child():
    return render_template('extends.html')
 
 
@app.route('/submit', methods=['GET', 'POST'])
def submit_page():
    if request.method == 'POST':
        msg = '{} was POST-ed'.format(request.form['submit'])
    else:
        msg = request.args.get('submit')
    return redirect((url_for('log', msg=msg, mode='debug')))
 
 
@app.route('/log/<msg>/<mode>')
def log(msg, mode):
    app.logger.debug(msg)
    return('LEVEL:{}\nLogged: {}'.format(mode, msg))
 
 
@app.route('/json', methods=['GET', 'POST'])
def json_endpoint():
    if request.method == 'POST':
        extracted = json.loads(request.form['data'])
        return 'key: {}\nlength: {}'.format(extracted.keys(), len(extracted))
    else:
        obj = {'data': [True, ['a list', 'of strings'], {'null': None}]}
        return jsonify(obj)
 
@app.route('/board', methods=['GET', 'POST'])
def message_board():
    if request.method == 'POST':
        username = request.form['usr']
        message = request.form['msg']
        with open("mb.txt", 'a') as f:
            f.write("{} says: {} \t [{}]\n".format(username, message, datetime.datetime.now().strftime('%m/%d/%Y')))
    with open("mb.txt", 'r') as f:
        return f.read()
 
def test_request_data():
    data = {'submit': 'some post data'}
    params = {'submit': 'some get params'}
    url = 'http://127.0.0.1:5000/submit'
    requests.get(url, params=params)
    requests.post(url, data=data)

def test_message_board(message="hello", usr="sharry"):
    data = {'usr' : usr, 'msg' : msg}
    url = 'http://127.0.0.1:5000/board'
    requests.post(url, data=data)

 
def test_json():
    data = {'some numbers': [1, 2.5]}
    url = 'http://127.0.0.1:5000/json'
    r = requests.get(url)
    r.text
    r.json()
    r = requests.post(url, data={'data': json.dumps(data)})
    print(r.text)
 
 
def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.run()
 
if __name__ == '__main__':
    main()