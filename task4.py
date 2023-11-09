from sql_connect import *

def task4():
    st.title('User Course Progress Dashboard')

    all_users = [str(user[0]) for user in querry("SELECT DISTINCT user_id FROM users")]

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
