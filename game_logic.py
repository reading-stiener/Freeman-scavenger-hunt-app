from database_connection import UserTable, GameTable, AnswerTable 

config = {
    'user': 'test-user',
    'password': 'password',
    'host': 'localhost',
    'database': 'test_web_app',
    #'port': '18159'
} 

def handle_login(username, password): 
    user_table = UserTable(**config)
    return user_table.query_user(username, password)

def handle_signups(username, password):
    user_table = UserTable(**config)
    game_table = GameTable(**config)
    game_table.add_new_entry(username)
    return user_table.add_user(username, password)

def handle_question(user, question, session):
    # pull the answer out
    ans_table = AnswerTable(**config)
    question_no, ans = ans_table.read_answers(question)
    
    # saving ans in session. Not sure if this is a good idea 
    session['ans'] = ans

    # check if the user is on the right page
    game_table = GameTable(**config)
    score = game_table.check_score(user)
    
    # check if user is at the right spot
    if question_no == score+1:
        return True
    else:
        return False

def handle_answer(ans, user_ans, user):
    game_table = GameTable(**config)
    # check question_no and answer
    if str(ans).lower() == str(user_ans).lower():
        game_table.add_new_entry(user) 
        return True
    else:
        return False

if __name__ == '__main__':
    request = { 
        'answer' : 1
    }
    question = 'one'
    user = 'NIk'
    print(handle_answer(request, question, user))
