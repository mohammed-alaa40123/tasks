from sql_connect import *
def task6():
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