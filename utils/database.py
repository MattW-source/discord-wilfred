import values
import mysql.connector

def execute_query(query):
    conn = mysql.connector.connect(
           host = db_host,
           user = db_user,
           password = db_password,
           database = db_database)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()
    conn.close()

def db_query(query):
    conn = mysql.connector.connect(
           host = db_host,
           user = db_user,
           password = db_password,
           database = db_database)
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    c.close()
    conn.close()
    return result
