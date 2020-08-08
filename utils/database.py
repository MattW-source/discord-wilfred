import sqlite3

def execute_query(table, query):
    conn = sqlite3.connect("/home/rsa-key-20190102/"+table)
    #conn = sqlite3.connect(table) #local debugging
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()
    conn.close()

def db_query(table, query):
    conn = sqlite3.connect("/home/rsa-key-20190102/"+table)
    #conn = sqlite3.connect(table) #local debugging
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    c.close()
    conn.close()
    return result
