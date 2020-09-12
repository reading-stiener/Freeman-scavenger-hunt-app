#Nikesh, Md, Abi and John
#Sept 9 2020
#Scavenger Hunt webapp

#Importing Modules
from flask import Flask, render_template, redirect, url_for, request
from database_connection import AnswerTable, UserTable, GameTable
from game_logic import handle_answer

app = Flask(__name__)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Route for the handling the questions page for a user
@app.route('/question', methods=['GET', 'POST'])
def question(): 
    error = None
    if request.method == 'POST':
        ans = request.form['answer']
        question = request.args.get('question')
        user = request.args.get('user')
        handle_answer(ans, question, user)
        return ans
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