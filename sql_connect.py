# Here are all the libraries used in the tasks

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
config = {
    'user': 'root',
    'port':'3306',
    'password': '',
    'host': 'localhost', 
    # Just change the name of the database 
    'database': 'electropi2',
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
    data = cursor.fetchone()  
    cursor.close()
    connection.close()
    return data