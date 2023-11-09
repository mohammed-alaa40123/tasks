from sql_connect import *
import pandas as pd
def calculate_subscription_counts(time_interval, user_data):
    user_data_df = pd.DataFrame(user_data, columns=['bundle_id', 'creation_date'])
    user_data_df['creation_date'] = pd.to_datetime(user_data_df['creation_date'])
    if time_interval == 'Daily':
        subscription_counts = user_data_df.set_index('creation_date').resample('D').count()
    elif time_interval == 'Weekly':
        subscription_counts = user_data_df.set_index('creation_date').resample('W').count()
    elif time_interval == 'Monthly':
        subscription_counts = user_data_df.set_index('creation_date').resample('M').count()
    elif time_interval == 'Yearly':
        subscription_counts = user_data_df.set_index('creation_date').resample('Y').count()
    return subscription_counts


def task2():
    st.title('Bundle Subscriptions Dashboard')
    query = "SELECT bundle_id, bundle_name, COUNT(*) as bundle_count FROM bundles GROUP BY bundle_id, bundle_name"
    data = querry(query)
    columns = ['bundle_id', 'bundle_name', 'bundle_count']
    df_bundles = pd.DataFrame(data, columns=columns)


    query = "SELECT bundle_id, creation_date FROM bundles"
    user_data = querry(query)    

    time_interval = st.selectbox('Select Time Interval', ['Daily', 'Weekly', 'Monthly', 'Yearly'])

    if time_interval:
        subscription_counts = calculate_subscription_counts(time_interval, user_data)
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