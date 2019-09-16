import requests, json, csv, os
import pandas as pd
from pprint import pprint
from datetime import datetime
from time import sleep

def get_data():
	# API Key
	api_key = os.environ["weather_api"]

	# Portland City ID (from openweathermap.org docs)
	city_id = "5746545"

	# URL
	url_address = "https://api.openweathermap.org/data/2.5/weather?id=" + city_id + "&APPID=" + api_key

	# make request
	response = requests.get(url_address)

	# convert json to dict
	all_data = response.json()

	return all_data

#x = get_data()
#pprint(x)


# format weather data for csv
def output_weather():
	# call get_data fcn
	d = get_data()
	# pull relevant fields from all_data, convert to preferred units
	main = d["main"]
	weather_cond = d["weather"]

	temperature = main["temp"]
	temperature = str(round(temperature - 273.15, 2))

	pressure = main["pressure"]
	pressure = str(round(pressure  * (0.75006),2))

	humidity = str(main["humidity"])

	weather_description = str(weather_cond[0]["description"])

	return temperature, pressure, humidity, weather_description

# create dated filename - will control when new file is created (at new month)
def create_filename():
	filepath = '/mnt/e/VirtualEnvs/data/'
	filename = filepath + "currentweather_" + str(datetime.now().year) + "_" + str(datetime.now().month) + ".csv"
	return filename

# create formatted timestamp for csv data
def create_timestamp():
	date = str(datetime.now().month) + "-" + str(datetime.now().day)
	time = str(datetime.now().hour) + ":" + str(datetime.now().minute)
	timestamp = (date, time)
	return timestamp

# open (or create) csv in append mode; add datapoint
def create_csv():
	filename = create_filename()

	with open(filename, 'a') as weatherfile:
		weatherwriter = csv.writer(weatherfile, delimiter = ',')

	# determine if csv is empty
	with open(filename, 'r') as weatherfile:
		try:
			empty = False
			readfile = pd.read_csv(weatherfile)
		except pd.errors.EmptyDataError:
			empty = True

	# add header to csv if blank (new month, new file)
	with open(filename, 'a') as weatherfile:
		weatherwriter = csv.writer(weatherfile, delimiter = ',')

		if empty == True:
			weatherwriter.writerow(['date', 'time', 'temp_degC', 'pressure_torr', 'humidity_pct', 'condition_text'])
		else:
			pass

		# add datapoint from output_weather fnc
		data_row = []
		data_row.extend(create_timestamp())
		data_row.extend(output_weather())

		weatherwriter.writerow(data_row)

if __name__ == "__main__":
	while True:
		create_csv()
		sleep(10*60)
