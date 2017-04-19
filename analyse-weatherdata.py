import json
import operator

def analyse_city_data(city_name):
    weather_dates = {}
    with open('weather_storage_' + city_name + '.json') as data_file:
        weather_dates = json.load(data_file)
    most_typical_weather_conditions = {}
    for weather_date_key in weather_dates.keys():
        weather_condition_counter = {}
        weather_conditions = weather_dates[weather_date_key]
        # set not sunshine as default
        sun = False
        if(len(weather_conditions) != 0):
            for weather_condition in weather_conditions:
                # if just one appearance of sunshine count the day as sunshine
                if(weather_condition == 'Clear'):
                    sun = True
            most_typical_weather_conditions[weather_date_key] = sun
    with open('most_typical_weather_conditions_' + city_name + '.json', 'w') as outfile:
        json.dump(most_typical_weather_conditions, outfile)

analyse_city_data('copenhagen')
analyse_city_data('aarhus')
analyse_city_data('odense')
analyse_city_data('aalborg')