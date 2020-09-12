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
    return user_table.add_user(user_name, password)

def handle_answer(ans, question, user):
    user_ans = ans
    # pull the answer out
    ans_table = AnswerTable(**config)
    question_no, ans = ans_table.read_answers(question)

    print('q ', question_no)
    # check if the user is on the right page
    game_table = GameTable(**config)
    score = game_table.check_score(user)
   
    # check question_no and answer
    if question_no == score+1 and str(ans).lower() == str(user_ans).lower():
        game_table.add_new_entry(user) 
        return "Awesome! You got it! On to the next one"
    elif question_no != score+1: 
        return "You're at the wrong spot. Think harder!"
    elif str(ans).lower() != str(user_ans).lower():
        return "Wrong answer. Try again"
    else:
        return "You're clearly lost."
if __name__ == '__main__':
    request = { 
        'answer' : 1
    }
    question = 'one'
    user = 'NIk'
    print(handle_answer(request, question, user))
