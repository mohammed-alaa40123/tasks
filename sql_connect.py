import mysql.connector
import pandas as pd
config = {
    'user': 'root',
    'port':'3306',
    'password': '',
    'host': 'localhost', 
    'database': 'electropi',
}
def querry(query):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def querry1(query):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchone()  # Fetch a single row
    cursor.close()
    connection.close()
    return data