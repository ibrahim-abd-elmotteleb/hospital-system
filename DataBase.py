import mysql.connector
from mysql.connector import Error


db_pw = '1234'

# connect to server


def create_server_connection(host_name, port, user_name, user_pass):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, port=port, user=user_name, passwd=user_pass)
        print("Mysql DataBase connection Successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# connect to database


def create_db_connection(host_name, user_name, user_pass, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_pass,
            database=db_name
        )
        print("SQL database connection succesful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query Succesful")
    except Error as err:
        print(f"Error: '{err}'")
    return cursor
