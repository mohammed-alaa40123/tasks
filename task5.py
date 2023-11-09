from sql_connect import *

def task5():
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
