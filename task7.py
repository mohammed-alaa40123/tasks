from sql_connect import *

def task7():
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