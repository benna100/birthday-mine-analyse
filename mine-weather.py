from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select
import urllib
import urllib2
import time
import json
from datetime import timedelta, date, datetime

weather_storage = {}

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(1996, 7, 1)
end_date = datetime.now().date()

def mine_city_weather(city_name, airport_name, filename_to_save):
    with open(filename_to_save) as data_file:    
        weather_storage = json.load(data_file)
    
    for single_date in daterange(start_date, end_date):
        dict_key = single_date.strftime("%Y-%m-%d")

        year = single_date.strftime("%Y")
        month = single_date.strftime("%m")
        day = single_date.strftime("%d")
        if(dict_key not in weather_storage.keys()):
            print dict_key

            soup = Soup(urllib2.urlopen('https://www.wunderground.com/history/airport/' + airport_name + '/' + year + '/' + month + '/' + day + '/DailyHistory.html?req_city=' + city_name + '&req_statename=Denmark'))
            tekst = str(select(soup, '#observations_details'))
            column_counter = 0
            weather_conditions = []
            for column in select(soup, '#obsTable tbody tr'):
                #print column.text.split(';')[-1]
                time_clock = column.text.split(';')[0].split(' ')[0].split(':')[0]
                time_clock = int(time_clock)
                am_pm = column.text.split(';')[0].split(' ')[1]
                if('AM' in am_pm):
                    am_pm = 'AM'
                else:
                    am_pm = 'PM'

                if(am_pm == 'AM' and time_clock > 6 and time_clock != 12):
                    weather_conditions.append(column.text.split(';')[-1])
                elif(am_pm == 'PM' and time_clock <= 10):
                    weather_conditions.append(column.text.split(';')[-1])
                #if(column_counter % 13 == 12):
                    #print '-------------------'
                #    print column.text
                #    weather_conditions.append(column.text)
                    #print '-------------------'
                #column_counter += 1

            weather_storage[dict_key] = weather_conditions

            time.sleep(1)
            with open(filename_to_save, 'w') as outfile:
                json.dump(weather_storage, outfile)

mine_city_weather('Copenhagen', 'EKCH', 'weather_storage_copenhagen.json')
mine_city_weather('Arhus', 'EKAH', 'weather_storage_aarhus.json')
mine_city_weather('Odense', 'EKOD', 'weather_storage_odense.json')
mine_city_weather('Aalborg', 'EKYT', 'weather_storage_aalborg.json')