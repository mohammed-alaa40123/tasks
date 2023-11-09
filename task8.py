from sql_connect import *

def task8():
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
