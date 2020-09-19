#Nikesh, Md, Abi and John
#Sept 9 2020
#Scavenger Hunt webapp

#Importing Modules
from flask import Flask, render_template, redirect, url_for, request, session
from database_connection import AnswerTable, UserTable, GameTable
from game_logic import handle_question, handle_answer, handle_login, handle_signups, answer_count
from datetime import timedelta

# Set the secret key to some random bytes. Keep this really secret!
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=20)

@app.route('/')
def index():
    if 'username' in session:
        session['answer_count'] = answer_count(session['username'])
        return render_template(
            'index.html', 
            username=session['username'], 
            ans_count=session['answer_count'],
        )
    return render_template('index.html', username=None)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        session.permanent = True
        if handle_login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    return render_template('login.html', action='sign in')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        session.permanent = True
        if handle_signups(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    return render_template('login.html', action='sign up')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# Route for the handling the questions page for a user
@app.route('/question', methods=['GET', 'POST'])
def question():
    q_string = request.args.get('question', None)
    user = session.get('username', None)
    if not user: 
        return render_template('index.html', username=None)
    check = handle_question(user, q_string, session)
    if check == 'right_spot':
        if request.method == 'POST':
            user_ans = request.form['answer']
            ans = session['ans']
            if handle_answer(ans, user_ans, user):
                if session.get('answer_count', None): 
                    session['answer_count'] +=1
                if session['answer_count'] == 10: 
                    return redirect(url_for('final'))
                return redirect(url_for('response', response='correct'))
            else: 
                return redirect(url_for('response', response='wrong'))
        else: 
            return render_template('question.html', num = q_string)
    elif check == 'already_visited': 
        if request.method == 'POST': 
            return redirect(url_for('visited'))
        else: 
            return render_template('question.html', num = q_string)
    else:        
        return redirect(url_for('response', response='lost'))

# Route for already visited
@app.route('/visited')
def visited():
    return render_template('visited.html')

# Route for response
@app.route('/response')
def response():
    response = request.args.get('response', None)
    return render_template('response.html', response=response)

@app.route('/final')
def final():
    return render_template('final.html')


# Route for hints
@app.route('/hint')
def hint():
    q_solved = session.get('answer_count', None)
    return render_template('hint.html', question=q_solved+1)

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
        'SQRF' : 'Kylie Jenner',
        'CBRF' : 'White Claw', 
        'PLRF' : 'Billie Eilish',
        'BXRF' : 'X Æ A-123',
        'CSRF' : 'Shakira',
        'TBRF' : 'water',
        'TFRF' : 6,
        'CLRF' : 'Iron Man',
        'GMRF' : 'Rami Malek',
        'GGRF' : 3
    }
    ans_schema.create_table(**q_ans)
    game_table = GameTable(**config)
    game_table.create_table()
    user_table = UserTable(**config)
    user_table.create_table()
    app.run()