import utils.values as value # Contains DB Values
import mysql.connector

def execute_query(query):
    conn = mysql.connector.connect(
           host = value.db_host,
           user = value.db_user,
           password = value.db_password,
           database = value.db_database)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()
    conn.close()

def db_query(query):
    conn = mysql.connector.connect(
           host = value.db_host,
           user = value.db_user,
           password = value.db_password,
           database = value.db_database)
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    c.close()
    conn.close()
    return result
