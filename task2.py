import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
def calculate_subscription_counts(time_interval, user_data):
    user_data_df = pd.DataFrame(user_data, columns=['bundle_id', 'creation_date'])
    user_data_df['creation_date'] = pd.to_datetime(user_data_df['creation_date'])
    # user_data_df['creation_date'] = 
    if time_interval == 'Daily':
        subscription_counts = user_data_df.set_index('creation_date').resample('D').count()
    elif time_interval == 'Weekly':
        subscription_counts = user_data_df.set_index('creation_date').resample('W').count()
    elif time_interval == 'Monthly':
        subscription_counts = user_data_df.set_index('creation_date').resample('M').count()
    elif time_interval == 'Yearly':
        subscription_counts = user_data_df.set_index('creation_date').resample('Y').count()
    
    return subscription_counts
