import pandas as pd
import mysql.connector
import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px

# Define MySQL database connection parameters
config = {
    'user': 'root',
    'port':'3306',
    'password': '',
    'host': 'localhost',  # or the MySQL server's hostname or IP address
    'database': 'electropi',
}
st.title('User Registration and Subscription Dashboard')

# Sidebar to select date range
st.sidebar.header('Select Date Range')
start_date = st.sidebar.date_input('Start Date', datetime.now() - timedelta(days=365))
end_date = st.sidebar.date_input('End Date', datetime.now())

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Query to fetch user registration and subscription data
    query = f"""
        SELECT registration_date, Subscribed
        FROM users
        WHERE registration_date BETWEEN '{start_date}' AND '{end_date}'
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Convert the data to a DataFrame
    user_data = []
    for row in data:
        registration_date, subscribed = row
        user_data.append({'registration_date': registration_date, 'Subscribed': subscribed})

    df = pd.DataFrame(user_data)
except mysql.connector.Error as err:
    st.error(f"Error: {err}")
finally:
    cursor.close()
    connection.close()
if not df.empty:
    # Daily registration and subscription count
    st.subheader('Daily User Activity')
    df["Registered"] = 1
    daily_activity = df.groupby('registration_date').agg({'Subscribed': 'sum', 'Registered': 'count'})
    st.dataframe(daily_activity)


    fig = px.line(daily_activity, x=daily_activity.index, y=['Subscribed'],
                 labels={'Subscribed': 'Registered'},
                 title='Daily Registered Users')

    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Count')
    st.plotly_chart(fig)
    
    # Weekly registration and subscription count
    st.subheader('Weekly User Activity')
    weekly_activity = df.resample('W', on='registration_date').agg({'Subscribed': 'sum', 'Registered': 'count'})
    st.dataframe(weekly_activity)



    st.subheader('Weekly User Activity (Plotly Bar Chart)')


    # Define a function to resample data for weekly activity
    def resample_weekly(df):
        df_weekly = df.resample('W', on='registration_date').sum()
        df_weekly['Week'] = df_weekly.index.strftime('%Y-%m-%d')
        return df_weekly

    # Resample the data for weekly activity
    weekly_activity = resample_weekly(df)
    # Create a Plotly bar chart
    fig = px.bar(weekly_activity, x='Week', y=['Subscribed', 'Registered'],
                labels={'Subscribed': 'Subscribed', 'Registered': 'Registered'},
                title='Weekly User Activity', height=400)

    fig.update_xaxes(type='category')  # To ensure the 'Week' column is treated as categorical data
    fig.update_yaxes(title_text='Count')

    st.plotly_chart(fig)




    # Monthly registration and subscription count
    st.subheader('Monthly User Activity')
    # Resample the data for monthly activity
    monthly_activity = df.resample('M', on='registration_date').sum()

    # Create the Plotly bar chart
    fig = px.bar(monthly_activity, x=monthly_activity.index.strftime('%Y-%m'), y=['Subscribed', 'Registered'],
                labels={'Subscribed': 'Subscribed', 'Registered': 'Registered'},
                title='Monthly User Activity', height=400)
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Count')

    st.plotly_chart(fig)


    # Yearly registration and subscription count
    st.subheader('Yearly User Activity')
    yearly_activity =  df.resample('Y', on='registration_date').sum()
    total_registered = yearly_activity['Registered'].sum()

    # Calculate the total number of subscribed users
    total_subscribed = yearly_activity['Subscribed'].sum()

    # Calculate the number of registered but not subscribed users
    registered_not_subscribed = total_registered - total_subscribed

    # Create a Pie Chart to visualize the distribution
    labels = ['Subscribed', 'Registered (Not Subscribed)']
    values = [total_subscribed, registered_not_subscribed]

    fig = px.pie(names=labels, values=values,
                 title='Overall User Activity (Subscribed vs. Registered)')

    st.plotly_chart(fig)



else:
    st.write("No data available for the selected month range.")


