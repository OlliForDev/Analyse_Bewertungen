from flask import Flask, render_template
from data_handling import get_rating_ratio_labels_and_data, get_kpi_values, get_last_13_month, get_recommendation_ratio

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/dashboard-analyse-bewertungen')
def dashboard_analyse_bewertungen():

    return render_template('dashboard.html', 
                           bar_last_13_month_labels=get_last_13_month()['labels'], 
                           bar_last_13_month_data=get_last_13_month()['data'],
                           pie_rating_ratio_labels=get_rating_ratio_labels_and_data()['labels'],
                           pie_rating_ratio_data=get_rating_ratio_labels_and_data()['data'],
                           price=get_kpi_values()['price'],
                           service=get_kpi_values()['service'],
                           provider_change=get_kpi_values()['provider_change'],
                           count_ratings=get_kpi_values()['count_ratings'],
                           latest_month=get_kpi_values()['dates'][1],
                           ratio_per_month_data=get_recommendation_ratio()['ratio_data'],
                           target_per_month_data=get_recommendation_ratio()['target_data'],
                           ratio_per_month_labels=get_recommendation_ratio()['labels']
                           )

if __name__ == '__main__':
    app.run(debug=True)