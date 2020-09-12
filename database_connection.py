import mysql.connector
from mysql.connector import errorcode

class AnswerTable:
    def __init__(self, **config):
        self.config = config
        try:  
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def create_table(self, **q_answers):
        # leaving this out because we can manually set this up before hand 
        DB_NAME = self.config['database']
        TABLE = (
            'CREATE TABLE answer_table ('
            '   question_no int NOT NULL AUTO_INCREMENT PRIMARY KEY,'
            '   question varchar(256) NOT NULL,'
            '   answer varchar(256) NOT NULL'
            ')'
        )
        conn = self.cnx;
        cursor = conn.cursor(buffered=True)
        try: 
            cursor.execute( 
                'CREATE DATABASE {}'.format(DB_NAME)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

        table_description = TABLE
        try:
            print("Creating table {}: ".format('answer_table'), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        insert_query = (
            'INSERT INTO answer_table (question, answer)'
            'values (%s, %s)'
        )
        data = [(key, value) for key, value in q_answers.items()]
        cursor.executemany(insert_query, data)
        conn.commit()
        cursor.close()

    def read_answers(self, question_num):
        cursor = self.cnx.cursor()
        query = 'SELECT answer from answer_table WHERE question = %s'
        question = (question_num,)
        cursor.execute(query, question)
        for answer in cursor: 
            print(answer)

class GameTable:
    def __init__(self, **config):
        self.config = config
        try:  
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.create_table()

    def create_table(self):
        DB_NAME = self.config['database']
        TABLE = (
            "CREATE TABLE game_table ("
            "   id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
            "   username varchar(20) NOT NULL,"
            "   correct_ans int"
            ")"
        )
        cursor = self.cnx.cursor()
        try: 
            cursor.execute( 
                'CREATE DATABASE {}'.format(DB_NAME)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

        table_description = TABLE
        try:
            print("Creating table {}: ".format('game_table'), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()

    def add_new_entry(self, username):
        '''
            add to answers if user entry exists
        '''
        conn = self.cnx
        cursor = conn.cursor(buffered=True)
        check_query = (
            'SELECT correct_ans FROM game_table WHERE '
            'username = %s'
        )
        data =  (username,)
        cursor.execute(check_query, data)
        check = cursor.fetchall()
        if check:
            # Updating a row
            ans = check[0][0] + 1
            update_query = (
                'UPDATE game_table SET correct_ans = %s '
                'WHERE username = %s'
            )
            data = (ans, username)
            cursor.execute(update_query, data)
            conn.commit()
        else:
            # Inserting a new row
            insert_query = (
                'INSERT INTO game_table (username, correct_ans) '
                'VALUES (%s, %s)'
            )
            data = (username, 1)
            cursor.execute(insert_query, data)
            conn.commit()
        
class UserTable:
    def __init__(self, **config):
        self.config = config
        try:  
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.create_table()

    def create_table(self):
        DB_NAME = self.config['database']
        TABLE = (
            "CREATE TABLE user_table ("
            "   user_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
            "   username varchar(20) NOT NULL,"
            "   password varchar(256) NOT NULL"
            ")"
        )
        cursor = self.cnx.cursor(buffered=True)
        try: 
            cursor.execute( 
                'CREATE DATABASE {}'.format(DB_NAME)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

        table_description = TABLE
        try:
            print("Creating table {}: ".format('user_table'), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()
    
    def query_user(self, username, password):
        conn = self.cnx 
        cursor = conn.cursor()
        query = (
            'SELECT user_id FROM user_table '
            'WHERE username = %s and password = %s'
        )
        user_data = (username, password)
        cursor.execute(query, user_data)
        user_id = cursor.fetchall()    
        if user_id:
            cursor.close()
            return user_id[0]
        else:
            insert_query = (
                'INSERT INTO user_table (username, password) '
                'VALUES (%s, %s)'
            )
            cursor.execute(insert_query, user_data)
            conn.commit()
        cursor.execute(query, user_data)
        user_id = cursor.fetchall()
        cursor.close()
        return user_id[0]
        
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
    ans_schema.read_answers('1')
    game_table = GameTable(**config)
    user_table = UserTable(**config)
    print(user_table.query_user('Nikesh15', '9807'))
    game_table.add_new_entry('Abi')
    #game_table.add_new_entry('Abi')
    game_table.add_new_entry('Nikesh')