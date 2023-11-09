from sql_connect import *
def task9():
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
