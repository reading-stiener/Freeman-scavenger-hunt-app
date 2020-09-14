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
    if user_table.query_user(username, password): 
        return False
    return user_table.add_user(username, password)

def handle_question(user, question, session):
    # pull the answer out
    ans_table = AnswerTable(**config)
    table_check = ans_table.read_answers(question)
    
    if table_check: 
        question_no, ans = table_check
    
        # saving ans in session. Not sure if this is a good idea 
        session['ans'] = ans

        # check if the user is on the right page
        game_table = GameTable(**config)
        score = game_table.check_score(user)
        
        # check if user is at the right spot.
        if question_no == score+1:
            return 'right_spot'
        elif question_no < score+1:
            return 'already_visited'
        else:    
            return 'wrong_spot'
    else: 
        return 'wrong spot'

def handle_answer(ans, user_ans, user):
    game_table = GameTable(**config)
    # check question_no and answer
    if str(ans).lower() == str(user_ans).lower():
        game_table.add_new_entry(user) 
        return True
    else:
        return False

def answer_count(user): 
    game_table = GameTable(**config)
    score = game_table.check_score(user)
    return score


# def ans2str(ans_count):
#     temp_lst = ['SQRF', 'CBRF', 'PLRF', 'BXRF', 'CSRF', 'TBRF', 'TFRF', 'CLRF', 'GMRF', 'GGRF']
#     return temp_lst[ans_count-1]

# def str2ans(q_str):
#     q_dict = { 
#         'SQRF' : 1,
#         'CBRF' : 2, 
#         'PLRF' : 3,
#         'BXRF' : 4,
#         'CSRF' : 5,
#         'TBRF' : 6,
#         'TFRF' : 7,
#         'CLRF' : 8,
#         'GMRF' : 9, 
#         'GGRF' : 10
#     } 


if __name__ == '__main__':
    request = { 
        'answer' : 1
    }
    question = 'one'
    user = 'Nik'
    print(handle_answer(request, question, user))
