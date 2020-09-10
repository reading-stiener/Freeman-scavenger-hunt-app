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

    def create_table(self):
        # leaving this out because we can manually set this up before hand 
        pass

    def read_answers(self, question_num):
        cursor = self.cnx.cursor()
        query = 'SELECT answers from answers WHERE questions = %s'
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
        


if __name__ == '__main__':
    config = {
        'user': 'test-user',
        'password': 'password',
        'host': 'localhost',
        'database': 'test_web_app'
    } 
    ans_schema = AnswerTable(**config)
    ans_schema.read_answers('1')
    game_table = GameTable(**config)