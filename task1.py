from sql_connect import *

def draw_daily(df):
    daily_activity = df.resample('D', on='registration_date').agg({'Pro':sum,'Subscribed': 'sum', 'Registered': 'sum'})
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(x=daily_activity.index, y=daily_activity['Subscribed'],
                                  mode='lines+markers', name='Subscribed'))
    fig_daily.add_trace(go.Scatter(x=daily_activity.index, y=daily_activity['Registered'],
                                  mode='lines+markers', name='Registered'))
    fig_daily.add_trace(go.Scatter(x=daily_activity.index, y=daily_activity['Pro'],
                                  mode='lines+markers', name='Pro'))
    fig_daily.update_layout(title='Daily Registered vs Subscribed Users',
                            xaxis_title='Date',
                            yaxis_title='Count')

    return daily_activity, fig_daily
def draw_weekly(df):
    weekly_activity = df.resample('W', on='registration_date').agg({'Pro':sum,'Subscribed': 'sum', 'Registered': 'sum'})
    weekly_activity = df.resample('W', on='registration_date').sum()
    weekly_activity['Week'] = weekly_activity.index.strftime('%Y-%m-%d')
    fig_weekly = px.bar(weekly_activity, x='Week', y=['Subscribed', 'Registered','Pro'],
                labels={'Subscribed': 'Subscribed', 'Registered': 'Registered','Pro':'Pro'},
                title='Weekly User Activity', height=400)
    fig_weekly.update_xaxes(type='category') 
    fig_weekly.update_yaxes(title_text='Count')
    return weekly_activity,fig_weekly

def draw_monthly(df):
    monthly_activity = df.resample('M', on='registration_date').sum()

    fig_monthly = px.bar(monthly_activity, x=monthly_activity.index.strftime('%Y-%m'), y=['Subscribed', 'Registered','Pro'],
                labels={'Subscribed': 'Subscribed', 'Registered': 'Registered','Pro':'Pro'},
                title='Monthly User Activity', height=400)
    fig_monthly.update_xaxes(title_text='Month')
    fig_monthly.update_yaxes(title_text='Count')
    return monthly_activity,fig_monthly

def draw_yearly(df):
    yearly_activity =  df.resample('Y', on='registration_date').sum()
    total_registered = yearly_activity['Registered'].sum()
    total_subscribed = yearly_activity['Subscribed'].sum()
    total_pro = yearly_activity['Pro'].sum()
    labels = ['Subscribed', 'Registered (Not Subscribed)','Pro Plan']
    values = [total_subscribed, total_registered,total_pro]
    fig_yearly = px.pie(names=labels, values=values,
                title='Overall User Activity (Subscribed vs. Registered)')
    return yearly_activity,fig_yearly


def task1():
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
        daily_activity,fig_daily = draw_daily(df)
        st.dataframe(daily_activity)
        st.plotly_chart(fig_daily)        
                
        st.subheader('Weekly User Activity')
        weekly_activity,fig_weekly = draw_weekly(df)
        st.dataframe(weekly_activity)
        st.subheader('Weekly User Activity')
        st.plotly_chart(fig_weekly)

        st.subheader('Monthly User Activity')
        monthly_activity,fig_monthly = draw_monthly(df)
        st.dataframe(monthly_activity)
        st.plotly_chart(fig_monthly)

        st.subheader('Yearly User Activity')
        yearly_activity,fig_yearly = draw_yearly(df)
        st.plotly_chart(fig_yearly)

    else:
        st.write("No data available for the selected month range.")

