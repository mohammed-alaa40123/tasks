import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def draw_daily(df):
    daily_activity = df.resample('D', on='registration_date').agg({'Subscribed': 'sum', 'Registered': 'sum'})
    print(daily_activity.head(10))
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(x=daily_activity.index, y=daily_activity['Subscribed'],
                                  mode='lines+markers', name='Subscribed'))
    fig_daily.add_trace(go.Scatter(x=daily_activity.index, y=daily_activity['Registered'],
                                  mode='lines+markers', name='Registered'))
    fig_daily.update_layout(title='Daily Registered vs Subscribed Users',
                            xaxis_title='Date',
                            yaxis_title='Count')

    return daily_activity, fig_daily
def draw_weekly(df):
    weekly_activity = df.resample('W', on='registration_date').agg({'Subscribed': 'sum', 'Registered': 'sum'})
    weekly_activity = df.resample('W', on='registration_date').sum()
    weekly_activity['Week'] = weekly_activity.index.strftime('%Y-%m-%d')
    fig_weekly = px.bar(weekly_activity, x='Week', y=['Subscribed', 'Registered'],
                labels={'Subscribed': 'Subscribed', 'Registered': 'Registered'},
                title='Weekly User Activity', height=400)
    fig_weekly.update_xaxes(type='category') 
    fig_weekly.update_yaxes(title_text='Count')
    return weekly_activity,fig_weekly

def draw_monthly(df):
    monthly_activity = df.resample('M', on='registration_date').sum()

    fig_monthly = px.bar(monthly_activity, x=monthly_activity.index.strftime('%Y-%m'), y=['Subscribed', 'Registered'],
                labels={'Subscribed': 'Subscribed', 'Registered': 'Registered'},
                title='Monthly User Activity', height=400)
    fig_monthly.update_xaxes(title_text='Month')
    fig_monthly.update_yaxes(title_text='Count')
    return monthly_activity,fig_monthly

def draw_yearly(df):
    yearly_activity =  df.resample('Y', on='registration_date').sum()
    total_registered = yearly_activity['Registered'].sum()
    total_subscribed = yearly_activity['Subscribed'].sum()
    labels = ['Subscribed', 'Registered (Not Subscribed)']
    values = [total_subscribed, total_registered]
    fig_yearly = px.pie(names=labels, values=values,
                title='Overall User Activity (Subscribed vs. Registered)')
    return yearly_activity,fig_yearly