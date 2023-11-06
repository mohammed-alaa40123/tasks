import streamlit as st
from sql_connect import *
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
Task = st.sidebar.selectbox("Select a Task", ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5",
                                           "Task 6", "Task 7", "Task 8", "Task 9", "Task 10"])


if Task == "Task 1":
    import task1
    st.title('User Registration and Subscription Dashboard')
    st.sidebar.header('Select Date Range')
    start_date = st.sidebar.date_input('Start Date', datetime.now() - timedelta(days=365))
    end_date = st.sidebar.date_input('End Date', datetime.now())

    query = f"""
        SELECT registration_date, Subscribed
        FROM users
        WHERE registration_date BETWEEN '{start_date}' AND '{end_date}'
    """
    
    data = querry(query)
    user_data = []
    for row in data:
        registration_date, subscribed = row
        user_data.append({'registration_date': registration_date, 'Subscribed': subscribed})

    df = pd.DataFrame(user_data)

    df["Registered"] = df.apply(lambda x: 1 if x["Subscribed"] == 0 else 0, axis=1)
    df["Pro"] = df.apply(lambda x: 1 if x["Subscribed"] == 2 else 0, axis=1)
    if not df.empty:
        
        st.subheader('Daily User Activity')
        daily_activity,fig_daily = task1.draw_daily(df)
        st.dataframe(daily_activity)
        st.plotly_chart(fig_daily)        
                
        st.subheader('Weekly User Activity')
        weekly_activity,fig_weekly = task1.draw_weekly(df)
        st.dataframe(weekly_activity)
        st.subheader('Weekly User Activity')
        st.plotly_chart(fig_weekly)

        st.subheader('Monthly User Activity')
        monthly_activity,fig_monthly = task1.draw_monthly(df)
        st.dataframe(monthly_activity)
        st.plotly_chart(fig_monthly)

        st.subheader('Yearly User Activity')
        yearly_activity,fig_yearly = task1.draw_yearly(df)
        st.plotly_chart(fig_yearly)

    else:
        st.write("No data available for the selected month range.")

elif Task == "Task 6":
    st.title('Capstone Admin Evaluation Counts')
    today = datetime.now().date()
    this_week_start = today - timedelta(days=today.weekday())
    this_month_start = today.replace(day=1)
    selected_admin = st.selectbox('Select Admin (1 to 13)', list(range(1, 14)))

    # Query to count capstones evaluated for today, this week, and this month
    query = f"""
        SELECT 
            SUM(CASE WHEN evaluation_date = '{today}' THEN 1 ELSE 0 END) AS today_count,
            SUM(CASE WHEN evaluation_date >= '{this_week_start}' THEN 1 ELSE 0 END) AS this_week_count,
            SUM(CASE WHEN evaluation_date >= '{this_month_start}' THEN 1 ELSE 0 END) AS this_month_count
        FROM capstone_evaluation_history
        WHERE admin_id = {selected_admin}
    """

    # Execute the query and fetch a single row
    evaluation_data = querry1(query)

    # Display evaluation counts in cards
    if evaluation_data is not None:
        st.subheader('Evaluation Counts')
        today_count, this_week_count, this_month_count = evaluation_data  # Fetch a single row

        st.markdown(f"**Today's Evaluation Count:** {today_count}")
        st.markdown(f"**This Week's Evaluation Count:** {this_week_count}")
        st.markdown(f"**This Month's Evaluation Count:** {this_month_count}")
   
elif Task == "Task 7":
    st.title('Capstone Evaluation History Dashboard')
    username = st.text_input('Enter Username')

    if username:
        query = f"""
            SELECT c.course_id, c.title, ce.degree, ce.evaluation_date
            FROM capstone_evaluation_history ce
            JOIN courses c ON ce.course_id = c.course_id
            WHERE ce.user_id = '{username}'
        """
        data = querry(query)

        if not data:
            st.warning(f"No capstone evaluation history found for user: {username}")
        else:
            eval_history = pd.DataFrame(data, columns=['Course ID', 'Course Title', 'Degree', 'Evaluation Date'])
            st.subheader(f'Evaluation History for User: {username}')
            st.dataframe(eval_history)
