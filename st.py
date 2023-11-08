import streamlit as st
from sql_connect import *
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import task1,task2,task5

Task = st.sidebar.selectbox("Select a Task", ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5",
                                           "Task 6", "Task 7", "Task 8", "Task 9", "Task 10"])


if Task == "Task 1":
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

elif Task == "Task 2":

    st.title('Bundle Subscriptions Dashboard')
 

    query = "SELECT bundle_id, bundle_name, COUNT(*) as bundle_count FROM bundles GROUP BY bundle_id, bundle_name"
    data = querry(query)
    columns = ['bundle_id', 'bundle_name', 'bundle_count']
    df_bundles = pd.DataFrame(data, columns=columns)


    query = "SELECT bundle_id, creation_date FROM bundles"
    user_data = querry(query)    

    time_interval = st.selectbox('Select Time Interval', ['Daily', 'Weekly', 'Monthly', 'Yearly'])

    if time_interval:
        subscription_counts = task2.calculate_subscription_counts(time_interval, user_data)
        st.subheader(f'Subscription Counts ({time_interval})')
        st.dataframe(subscription_counts)

    if not subscription_counts.empty:
        st.subheader(f'Subscription Counts Chart ({time_interval})')
        fig = px.line(subscription_counts, x=subscription_counts.index, y='bundle_id')
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Count')
        st.plotly_chart(fig)
        fig = px.pie(df_bundles, names='bundle_name', values='bundle_count', title='Bundle Distribution')
        st.plotly_chart(fig)
        
elif Task == "Task 3":
    query = """
        SELECT
        u.user_id AS User_ID, 
        u.age AS Age, 
        u.study_degree AS Study_Degree, 
        COUNT(ucc.user_id) AS Completed_Courses_Count,
        MAX(ucc.completion_date) AS Last_Completion_Date,
        ucc.course_degree AS Last_Completed_Course_Degree
    FROM users AS u 
    LEFT JOIN user_completed_courses AS ucc ON u.user_id = ucc.user_id
    WHERE u.10k_AI_initiative = 1  
    GROUP BY u.user_id  
    """

    user_data = querry(query)
    columns = ["User_ID", "Age", "Study_Degree", "Completed_Courses_Count", "Last_Completion_Date", "Last_Completed_Course_Degree"]

    user_df = pd.DataFrame(user_data, columns=columns)

    st.title('Users in the 10k AI Initiative')
    st.dataframe(user_df, use_container_width=True)

    selected_user = st.selectbox('Select a User', user_df['User_ID'])
    if not user_df.empty:
        user_info = user_df[user_df['User_ID'] == selected_user]
        st.subheader('User Information')
        st.write(f"User ID: {selected_user}")
        st.write(f"Age: {user_info['Age'].values[0]}")
        st.write(f"Study Degree: {user_info['Study_Degree'].values[0]}")
        st.write(f"Completed Courses Count: {user_info['Completed_Courses_Count'].values[0]}")
        st.subheader('Last Completed Course Information')
        st.write(f"Last Completion Date: {user_info['Last_Completion_Date'].values[0]}")
        st.write(f"Last Completed Course Degree: {user_info['Last_Completed_Course_Degree'].values[0]}")

elif Task == "Task 4":
    
    st.title('User Course Progress Dashboard')

    all_users = [str(user[0]) for user in querry("SELECT DISTINCT user_id FROM user_lesson_history")]

    selected_users = st.selectbox('Select Users', ['All Users'] + all_users, index=0)

    if selected_users == 'All Users':
        user_filter = ""  
    else:
        user_filter = f" AND u.user_id = {selected_users}"
    query_learning_courses = f"""
        SELECT u.user_id, COUNT(DISTINCT u.course_id) AS learning_courses   
        FROM user_lesson_history AS u
        WHERE 1 {user_filter}  
        GROUP BY u.user_id;
    """

    query_completed_courses = f"""
        SELECT u.user_id AS User_Id ,
                SUM(CASE WHEN ucc.completion_date BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() THEN 1 ELSE 0 END) AS completed_this_week,
                SUM(CASE WHEN ucc.completion_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW() THEN 1 ELSE 0 END) AS completed_this_month,
                SUM(CASE WHEN ucc.completion_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW() THEN 1 ELSE 0 END) AS completed_this_year
    FROM users AS u
    LEFT JOIN user_completed_courses AS ucc ON u.user_id = ucc.user_id
        WHERE 1 {user_filter}  
    GROUP BY u.user_id;
    """

    learning_courses_data = querry(query_learning_courses)
    completed_courses_data = querry(query_completed_courses)

    learning_courses_df = pd.DataFrame(learning_courses_data, columns=['user_id', 'learning_courses'])
    completed_courses_df = pd.DataFrame(completed_courses_data, columns=['user_id', 'completed_this_week', 'completed_this_month', 'completed_this_year'])

    st.subheader('Number of Currently Learning Courses')
    st.dataframe(learning_courses_df,hide_index=True, use_container_width=True)

    st.subheader('Number of Completed Courses')
    st.dataframe(completed_courses_df,hide_index=True, use_container_width=True)

elif Task == "Task 5":
    st.title("User Information Dashboard")
    user_id = st.text_input("Enter User ID:")
    if user_id:
        user_query = f"SELECT * FROM users WHERE user_id = {user_id}"
        user_data = querry(user_query)
        if user_data:
            bundle_query = f"SELECT * FROM bundles WHERE user_id = {user_id}"

            current_learning_courses_query = f"""
            SELECT
                ulh.user_id AS User_ID,
                COUNT(DISTINCT ulh.course_id) AS Learning_Courses_Count,
                GROUP_CONCAT(DISTINCT c.title) AS Learning_Courses_Titles
            FROM user_lesson_history AS ulh
            JOIN courses AS c ON ulh.course_id = c.course_id
            WHERE ulh.count > 0
                AND ulh.user_id = {user_id}
                AND ulh.last_viewed = (SELECT MAX(last_viewed) FROM user_lesson_history WHERE user_id = ulh.user_id)
            GROUP BY ulh.user_id;
            """

            completed_courses_query = f"""
                SELECT c.course_id, c.title, u.course_degree, u.completion_date
                FROM user_completed_courses u
                JOIN courses c ON u.course_id = c.course_id
                WHERE u.user_id = {user_id}
            """
            completed_capstone_query = f"""
                SELECT c.course_id, c.title,u.chapter_id,u.lesson_id,u.course_id, u.degree, u.evaluation_date
                FROM capstone_evaluation_history u
                JOIN courses c ON u.course_id = c.course_id
                WHERE u.user_id = {user_id}
            """        
            bundle_data = querry(bundle_query)
            current_learning_courses_data = querry(current_learning_courses_query)
            completed_courses_data = querry(completed_courses_query)
            capstone_data = querry(completed_capstone_query)

            st.subheader("User Details")
            st.write(f"User ID: {user_data[0][0]}")
            st.write(f"Age: {user_data[0][8]}")
            if user_data[0][7] == "m":
                st.write(f"Gender: Male")
            else: 
                st.write(f"Gender: Female")
            if user_data[0][1]:
                st.write(f"Subscribed: Yes")
            else:
                st.write(f"Subscribed: No")
            st.write(f"Level: {user_data[0][6]}")
            
            if  bundle_data:
                st.subheader("User Bundles")
                for bundle in  bundle_data:
                    st.write(f"Bundle Name: {bundle[1]}")
            else: st.write("User has no bundles")
        
            if  current_learning_courses_data:
                st.subheader("Currntly Courses learning")
                for course in  current_learning_courses_data:
                    st.write(f"Number of currently learning courses: {course[1]}")
                    st.write(f"Course Name: {course[2]}")
                    st.write("---")
            else: st.write("User has no current courses")
            
            if  completed_courses_data:
                st.subheader("Completed Courses")
                for course in  completed_courses_data:
                    st.write(f"Course Name: {course[1]}")
                    st.write(f"Degree: {course[2]}")
                    st.write("---")
            else: st.write("User has no completed courses")
            
            if  capstone_data:
                st.subheader("Completed Capstones")
                for capstone in  capstone_data:
                    st.write(f"Capstone ID: {capstone[2]}")
                    st.write(f"Course Name: {capstone[1]}")
                    st.write(f"Degree: {capstone[5]}")
                    st.write(f"Evaluation Date: {capstone[6]}")
                    if capstone[5]>50:
                        st.write(f"Passed: Yes")
                    else:
                        st.write(f"Passed: No")
                    st.write("---")
            else: st.write("User has no Capstones")
                    
        else:
            st.write("User not found. Please enter a valid User ID.")

elif Task == "Task 6":
    admins_query = "SELECT admin_id FROM admins"
    admin_ids = querry(admins_query)
    admin_id_list = [admin[0] for admin in admin_ids]
    today = datetime.now().date()
    this_week_start = today - timedelta(days=today.weekday())
    this_month_start = today.replace(day=1)
    st.title('Capstone Admin Evaluation Counts')
    total_query = f"""
        SELECT 
            SUM(CASE WHEN evaluation_date = '{today}' THEN 1 ELSE 0 END) AS total_today_count,
            SUM(CASE WHEN evaluation_date >= '{this_week_start}' THEN 1 ELSE 0 END) AS total_this_week_count,
            SUM(CASE WHEN evaluation_date >= '{this_month_start}' THEN 1 ELSE 0 END) AS total_this_month_count
        FROM capstone_evaluation_history
        """
        
    total_evaluation_data = querry1(total_query)

    if total_evaluation_data is not None:
        st.subheader('Total Evaluation Counts for All Admins')
        total_today_count, total_this_week_count, total_this_month_count = total_evaluation_data 
        st.markdown(f"**Total Today's Evaluation Count for All Admins:** {total_today_count}")
        st.markdown(f"**Total This Week's Evaluation Count for All Admins:** {total_this_week_count}")
        st.markdown(f"**Total This Month's Evaluation Count for All Admins:** {total_this_month_count}")
    st.write("---")
    selected_admin = st.selectbox('Select Admin (1 to 13)', admin_id_list)


    query = f"""
        SELECT 
            SUM(CASE WHEN evaluation_date = '{today}' THEN 1 ELSE 0 END) AS today_count,
            SUM(CASE WHEN evaluation_date >= '{this_week_start}' THEN 1 ELSE 0 END) AS this_week_count,
            SUM(CASE WHEN evaluation_date >= '{this_month_start}' THEN 1 ELSE 0 END) AS this_month_count
        FROM capstone_evaluation_history
        WHERE admin_id = {selected_admin}
    """

    evaluation_data = querry1(query)

    if evaluation_data is not None:
        st.subheader('Evaluation Counts')
        today_count, this_week_count, this_month_count = evaluation_data 

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

elif Task == "Task 8":
    st.title('Coupon Usage Dashboard')

    query = """
            SELECT coupon_id AS ID, copon_code AS Code, exp_date AS Expiry_date, max_users AS Max_Users, disount_rate AS Discount
            FROM copons 
        """
    coupon_data = querry(query)
    filter_options = ["All Coupons", "Expire Soon", "High Discount"]

    # Filter selection
    filter_selection = st.selectbox("Select a filter:", filter_options)

    # Filter by coupon code
    coupon_codes = [row[1] for row in coupon_data]  
    selected_code = st.selectbox("Select a coupon code:", ["All Codes"] + coupon_codes)

    if filter_selection == "Expire Soon":
        today = datetime.today()
        expiration_threshold = today + timedelta(days=7)
        filtered_coupon_data = [row for row in coupon_data if row[2] < expiration_threshold]
    elif filter_selection == "High Discount":
        filtered_coupon_data = [row for row in coupon_data if row[4] > 0.9]
    else:
        filtered_coupon_data = coupon_data  

    if selected_code != "All Codes":
        filtered_coupon_data = [row for row in filtered_coupon_data if row[1] == selected_code]

    if filtered_coupon_data:
        st.subheader('Filtered Coupon Data')
        
        for row in filtered_coupon_data:
            coupon_id, coupon_code, exp_date, max_users, discount_rate = row
            st.write(f"**Coupon ID:** {coupon_id}")
            st.write(f"**Coupon Code:** {coupon_code}")
            st.write(f"**Expiry Date:** {exp_date}")
            st.write(f"**Max Users:** {max_users}")
            st.write(f"**Discount Rate:** {discount_rate}")
            st.write('---')  

elif Task == "Task 9":
    st.title('User Data Dashboard')
    st.sidebar.title('Filters')
    min_age, max_age = st.sidebar.slider("Age Range", 0, 100, (0, 100))
    study_degree = st.sidebar.selectbox("Study Degree", ["All", "Student", "Graduated"])
    
    query = f"""
        SELECT age, study_degree, COUNT(*) AS user_count
        FROM users
        WHERE age >= {min_age} AND age <= {max_age}
        AND (study_degree = '{study_degree}' OR '{study_degree}' = 'All')
        GROUP BY age, study_degree
    """
    user_data = querry(query)
    if user_data:
        user_df = pd.DataFrame(user_data, columns=['Age', 'Study Degree', 'User Count']) 
        st.subheader('User Data')
        st.dataframe(user_df,  hide_index=True, use_container_width=True)
        study_degree_counts = user_df['Study Degree'].value_counts()
        
        fig_pie = px.pie(study_degree_counts, names=study_degree_counts.index, values=study_degree_counts.values, title='Study Degree Distribution')
        st.plotly_chart(fig_pie)
        
        age_bar = px.bar(user_df, x='Age', y='User Count', title='User Age Distribution')
        st.plotly_chart(age_bar)

elif Task == "Task 10":
    st.title("Employment Grant Dashboard")

    employment_grant_query = """
        SELECT ueg.user_id, ueg.status, ueg.application_date
        FROM users_employment_grant ueg
        LEFT JOIN users_employment_grant_actions uega ON ueg.user_id = uega.user_id
        ORDER BY ueg.user_id
    """
    employment_grant_data = querry(employment_grant_query)

    st.subheader("All Users and Their Employment Grant Status and History")
    st.dataframe(pd.DataFrame(employment_grant_data,columns=["user_id","status","application_date"]),hide_index=True)

    grant_status_query = """
        SELECT status, COUNT(user_id) AS user_count
        FROM users_employment_grant
        GROUP BY status
    """
    grant_status_data = querry(grant_status_query)

    st.subheader("Number of Users in Each Employment Grant Status")
    st.dataframe(pd.DataFrame(grant_status_data,columns=["Status","Count"]),hide_index=True)
    fig = px.pie(grant_status_data, values=1, names=0, title="Employment Grant Status Distribution")
    st.plotly_chart(fig)
