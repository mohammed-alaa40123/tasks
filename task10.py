from sql_connect import *

def task10():
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
