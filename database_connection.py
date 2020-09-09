import mysql.connector

cnx = mysql.connector.connect(user='test-user', password='password',
                              host='localhost',
                              database='test_web_app')

cursor = cnx.cursor()
query = ("SELECT answers from answers "
         "WHERE questions = 1")

question = '1'

cursor.execute(query)

for answer in cursor: 
    print(answer)

cnx.close()