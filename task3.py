from sql_connect import *

def task3():
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
