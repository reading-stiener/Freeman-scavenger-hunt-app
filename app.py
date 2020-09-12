#Nikesh, Md, Abi and John
#Sept 9 2020
#Scavenger Hunt webapp

#Importing Modules
from flask import Flask, render_template, redirect, url_for, request, session
from markupsafe import escape
from database_connection import AnswerTable, UserTable, GameTable
from game_logic import handle_answer, handle_login, handle_signups
from datetime import timedelta

# Set the secret key to some random bytes. Keep this really secret!
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=20)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in.'

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        session.permanent = True
        if handle_login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# Route for the handling the questions page for a user
@app.route('/question', methods=['GET', 'POST'])
def question(): 
    error = None
    if request.method == 'POST':
        ans = request.form['answer']
        question = request.args.get('question')
        user = request.args.get('user')
        return handle_answer(ans, question, user)
    return render_template('question.html', error=error)

if __name__ == '__main__':
    config = {
        'user': 'test-user',
        'password': 'password',
        'host': 'localhost',
        'database': 'test_web_app',
        #'port': '18159'
    } 
    ans_schema = AnswerTable(**config)
    q_ans ={ 
        'one' : 1,
        'two' : 2, 
        'three' : 3,
        'four' : 4
    }
    ans_schema.create_table(**q_ans)
    game_table = GameTable(**config)
    game_table.create_table()
    user_table = UserTable(**config)
    user_table.create_table()
    app.run(debug=True)