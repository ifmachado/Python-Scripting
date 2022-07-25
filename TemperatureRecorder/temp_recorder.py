# !/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
# code above makes this file an executable to make scheduling with Crontab easier.



import datetime
import pygal
import requests
from pygal.style import LightSolarizedStyle

from WeatherDatabase import *

# new Database class object that will create a new database called "weather".
# path had to be hardcoded due to script scheduling with Crontab.
db = WeatherDatabase("//Users//ingridmachado//Documents//ComputerScienceCourse//Scripting//pythonProject2//"
                     "Assignment2// weather.db")

# creates a table inside temperatures database called "weather".
# Columns in the database will be city, time  and temperature.
table_name = "temperatures"
db.add_table(table_name, "(city TEXT, date DATETIME, temperature INT)")

# nested dict to hold information necessary to create dynamic urls needed to use for API requests.
cities = {
    "Rio de Janeiro": {"country": "BR", "lat": 0, "lon": 0},
    "Sao Paulo": {"country": "BR", "lat": 0, "lon": 0},
    "Tokyo": {"country": "JP", "lat": 0, "lon": 0},
    "London": {"country": "GB", "lat": 0, "lon": 0},
    "The Hague": {"country": "NL", "lat": 0, "lon": 0}
}

# API key needed for API authentication
API_key = "2467454e38ec39f571d5dce96f19fbe1"

# dict to hold city name and temp from api
temperatures = {}

# get all the lat and lon values needed to use the weather api from another part of the openweathermap API.
for key, value in cities.items():
    # looping through the cities dict, we will have all the values needed to create a url for each city
    url = 'http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit={limit}&appid={key}'.format(city=key,
                                                                                                             country=
                                                                                                             value[
                                                                                                                 "country"],
                                                                                                             limit=1,
                                                                                                             key=API_key)
    # get data from url
    data = requests.get(url)

    # parse into json format
    parsed_data = data.json()

    # parsed data is a 1 value list with a dict inside, therefore get the value on index 0 in each list (the dict
    # with all info). Then get the value referring to "lon" and "lat" keys from the API dict that has been returned.
    # Finally, add the obtained lon and lat values to cities dict under the city key, under "lon" and "lat" keys.
    cities[key]["lon"] = parsed_data[0]["lon"]
    cities[key]["lat"] = parsed_data[0]["lat"]

# from openweatermap API, get the current temperature values
for key, value in cities.items():
    # looping through the cities dict, we will have all the values needed to create a url for each city.
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}'.format(lat=value["lat"],
                                                                                                   lon=value["lon"],
                                                                                                   key=API_key)
    # get data from url
    data = requests.get(url)

    # parse into json format
    parsed_data = data.json()

    # the keys from cities dict will also be keys in the temperatures dict,
    # therefore it was store in "city" var for code clarity.
    city = key

    # convert the temperatures from kelvin to celsius
    converted_temp = round(parsed_data["main"]["temp"] - 273.15)

    # add key value pair to temperatures dict, where key is the city and value is the converted temperature
    temperatures[city] = converted_temp

# get current date from python's datetime library
current_date = datetime.date.today()

# VISUALIZATION - PART 1 (non-automated script):

# print table with city, date and value extracted from API.

# print table header
print("_________________________________________________________")
print("     city       |      date      |      temperature      ")
print("_________________________________________________________")

# loop through the temperatures dict to get city and temperature values
for key, value in temperatures.items():
    # for table formatting, number of spaces between city name and
    # vertical bar will be determined by length of city name.
        print(key + ((" ")*(15-len(key))) + " |   " + str(current_date) + "   |         " + str(value))

print("_________________________________________________________")



# Bar chart for temperatures in 1 day.
# For multiple dates(automated script), the bar chart was getting confusing, so I changed to a line chart.
bar_chart = pygal.Bar()

# bar chart title
bar_chart.title = ('Temperatures on ' + str(current_date))

# loop through temperatures dict to get key,value pairs.
for key, value in temperatures.items():
    # add a line to the chart where reference is the key in dict (city), and value is current temperature.
    bar_chart.add(key, value)

# render chart o svg file "temperature_bars
bar_chart.render_to_file('temperature_bars.svg')

# output to console success message
print("chart created successfully")



# PART 2 - MULTIPLE DATES AND AUTOMATION


# for each key:value pair in the temperatures dictionary, call the WeatherDatabase add_info function
for key, value in temperatures.items():
    # the function will add the city, temperature and current date values to the database, if they don't already exist.
    db.add_info(key, current_date, value)

# dict to hold city and temperature data extracted from DB
temps_per_city = {}

# set to hold the date extracted from DB
dates = set()


# loop through keys only from cities dict
for key in cities.keys():
    # calling WeatherDatabase method to get the info stored in database for each city.
    # in this case, we only want to get 1 result per city per date, where the line has the highest temperature value.
    temps = db.get_info(table="temperatures", primary_col="city", value=key, secondary_col="date",
                        max_col="temperature", group="date")

    # list to hold all temperatures
    temps_list = []

    # value returned from db and store on temps will be a nested list.
    # Therefore a for loop will be needed to get information based on index.
    for i in range(len(temps)):
        # in each list returned from DB, city value will be the first, as it's passed to get_info as primary col.
        city = temps[i][0]

        # date is the second, as it's passed to get_info as secondary col.
        date = temps[i][1]

        # temperature is the third, as it's passed to get_info as max col.
        temperature = temps[i][2]

        # add date value to dates set.
        dates.add(date)

        # append temperature values to temp_list list
        temps_list.append(temperature)

    # store key:value pair in temps_per_city dict, where the key is the city
    # and the value is a list of temperatures for that city obtained from the DB.
    temps_per_city[key] = temps_list

# sort date values in dates.
sorted_dates = sorted(dates)


# VISUALIZATION PART 2 (AUTOMATED SCRIPT)
# This chart will show the highest temperature recorded per city per date.

# create a line chart with pygal's pre-built LightColorizedStyle style and 20degree x label rotation.
line_chart = pygal.Line(interpolate='cubic', style=LightSolarizedStyle, x_label_rotation=20)

# chart title
line_chart.title = 'Temperatures around the world'

# label on the x axis will the dates in the dates set.
line_chart.x_labels = sorted_dates

# loop through temps_per_city key,value pairs.
for key, value in temps_per_city.items():
    # add a line to the chart where reference value is the key in dict (city),
    # and value is the list of temperatures.
    line_chart.add(key, value)

# render chart to svg file called temperature_lines
# path had to be hardcoded due to script scheduling with Crontab.
line_chart.render_to_file("//Users//ingridmachado//Documents//ComputerScienceCourse//Scripting//pythonProject2//"
                          "Assignment2//temperature_lines.svg")

# print success message
print("chart updated successfully")

# close database
db.close_database()
