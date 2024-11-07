import pandas as pd
import locale

ratings_df = pd.read_csv('sw_karlsruhe_ratings_verivox.csv')

def get_rating_ratio_labels_and_data():
    df_pie_chart = ratings_df.groupby(['rts_title'])['rts_title'].count().reset_index(name='count_ratings')
    return {'labels': df_pie_chart.rts_title.to_list(), 'data': df_pie_chart.count_ratings.to_list()}

'''
    is_asc --> True: returns df with ascending order of date col
    is_asc --> Fale: returns df descending order of date col  
    is_last_13_month --> True: returns df of last 13 month
    is_last_13_month --> False: returns df with all rows
'''

def get_ratings_per_month(is_asc):
    # set date to german format
    locale.setlocale(locale.LC_TIME, 'de_DE.utf8')
    # group by month
    ratings_per_month_df = ratings_df.groupby(['rts_date_of_change'])['rts_date_of_change'].count().reset_index(name='count_ratings')
    # convert string representation of date to datetime (datatype)
    ratings_per_month_df['date'] = pd.to_datetime(ratings_per_month_df['rts_date_of_change'], format='%B %Y')
    # add missing months
    date_range = pd.date_range(start=ratings_per_month_df['date'].min(), end=ratings_per_month_df['date'].max(), freq='MS')
    ratings_per_month_df = ratings_per_month_df.set_index('date').reindex(date_range).rename_axis('date').reset_index()
    # change NaN to string representation of date or NaN to 0 (depending on col)
    ratings_per_month_df['count_ratings'] = ratings_per_month_df['count_ratings'].fillna(0).astype(int)
    ratings_per_month_df['rts_date_of_change'] = ratings_per_month_df['rts_date_of_change'].fillna(ratings_per_month_df['date'].dt.strftime('%B %Y'))
    
    ratings_per_month_df = ratings_per_month_df.sort_values(by='date', ascending=is_asc)
    return ratings_per_month_df

def get_last_13_month():
    df = get_ratings_per_month(False).head(13).sort_values(by='date', ascending=True)
    return {'labels': df.rts_date_of_change.to_list(), 'data': df.count_ratings.to_list()}

def get_kpi_values():
    locale.setlocale(locale.LC_TIME, 'de_DE.utf8')
    # group by month
    mean_score_price_df = ratings_df[ratings_df['rts_scoring_price'] != 0].groupby(['rts_date_of_change'])['rts_scoring_price'].mean().reset_index(name='mean_score_price')
    mean_score_service_df = ratings_df[ratings_df['rts_scoring_service'] != 0].groupby(['rts_date_of_change'])['rts_scoring_service'].mean().reset_index(name='mean_score_service')
    mean_score_provider_change_df = ratings_df[ratings_df['rts_scoring_provider_change'] != 0].groupby(['rts_date_of_change'])['rts_scoring_provider_change'].mean().reset_index(name='mean_score_provider_change')
    number_of_ratings_per_month_df = ratings_df.groupby(['rts_date_of_change'])['rts_date_of_change'].count().reset_index(name='count_ratings')

    kpis_per_month_df =  mean_score_price_df.merge(mean_score_service_df, on='rts_date_of_change', how='outer') \
                                            .merge(mean_score_provider_change_df, on='rts_date_of_change', how='outer') \
                                            .merge(number_of_ratings_per_month_df, on='rts_date_of_change', how='outer')

    # convert string representation of date to datetime (datatype)
    kpis_per_month_df['date'] = pd.to_datetime(kpis_per_month_df['rts_date_of_change'], format='%B %Y')
    # add missing months
    date_range = pd.date_range(start=kpis_per_month_df['date'].min(), end=kpis_per_month_df['date'].max(), freq='MS')
    kpis_per_month_df = kpis_per_month_df.set_index('date').reindex(date_range).rename_axis('date').reset_index()
    kpis_per_month_df['mean_score_price'] = kpis_per_month_df['mean_score_price'].fillna(0).astype(int)
    kpis_per_month_df['mean_score_service'] = kpis_per_month_df['mean_score_service'].fillna(0).astype(int)
    kpis_per_month_df['mean_score_provider_change'] = kpis_per_month_df['mean_score_provider_change'].fillna(0).astype(int)
    kpis_per_month_df['count_ratings'] = kpis_per_month_df['count_ratings'].fillna(0).astype(int)
    kpis_per_month_df['rts_date_of_change'] = kpis_per_month_df['rts_date_of_change'].fillna(kpis_per_month_df['date'].dt.strftime('%B %Y'))
    
    kpis_per_month_df = kpis_per_month_df.tail(2)

    kpis_data = {'price': kpis_per_month_df.mean_score_price.to_list(),
                 'service': kpis_per_month_df.mean_score_service.to_list(),
                 'provider_change': kpis_per_month_df.mean_score_provider_change.to_list(),
                 'count_ratings': kpis_per_month_df.count_ratings.to_list(),
                 'dates': kpis_per_month_df.rts_date_of_change.to_list()}
    
    return kpis_data

def get_recommendation_ratio():
    good_recommendation_df = ratings_df[ratings_df['rts_title'].str.contains('Kunde würde wieder zu diesem Anbieter wechseln.', na=False)]
    good_recommendation_df = (
        good_recommendation_df.groupby(['rts_date_of_change'])
        .size()
        .reset_index(name='count_good_ratings')
    )
    
    nmb_ratings_df = get_ratings_per_month(is_asc=True)
    recommendation_ratio_df = nmb_ratings_df.merge(good_recommendation_df, on='rts_date_of_change', how='left', suffixes=('_left', '_right'))
    recommendation_ratio_df['count_good_ratings'] = recommendation_ratio_df['count_good_ratings'].fillna(0).astype(int)
    recommendation_ratio_df['recommendation_ratio'] = (recommendation_ratio_df['count_good_ratings'] / recommendation_ratio_df['count_ratings']).fillna(0).round(2)
    recommendation_ratio_df['target_ratio'] = 0.75
    
    return  {'ratio_data': recommendation_ratio_df['recommendation_ratio'].to_list(), 
             'target_data': recommendation_ratio_df['target_ratio'].to_list(), 
             'labels': recommendation_ratio_df['rts_date_of_change'].to_list()}