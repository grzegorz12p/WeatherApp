from django.shortcuts import render
import json
import requests
from datetime import datetime


def index(request):
    if request.method == 'POST':
        city = request.POST['city_name']
        try:
            current_weather_api = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
                city) + "&appid=50737126b843bf219db538152e2f4206"
            current_weather_response = requests.get(current_weather_api)
            current_weather_data_api = json.loads(current_weather_response.text)
            five_days_weather_api = "http://api.openweathermap.org/data/2.5/forecast?q=" + str(
                city) + "&appid=4247b26da6522ed8f74af54dfc0da192"
            five_days_weather_response = requests.get(five_days_weather_api)
            five_days_weather_data_api = json.loads(five_days_weather_response.text)
            sunrise_time = datetime.fromtimestamp(current_weather_data_api['sys']['sunrise'])
            sunset_time =datetime.fromtimestamp(current_weather_data_api['sys']['sunset'])

            current_day = {
                "city": str(city).capitalize(),
                "country_code": str(current_weather_data_api['sys']['country']),
                "icon": str(current_weather_data_api['weather'][0]['icon']),
                "sunrise_time": sunrise_time.strftime('%I:%M %p'),
                "sunset_time": sunset_time.strftime('%I:%M %p'),
                "coordinate_lon": str(current_weather_data_api['coord']['lon']),
                "coordinate_lat": str(current_weather_data_api['coord']['lat']),
                "temp": str(int(current_weather_data_api['main']['temp']) - 273) + " C",
                "wind": str(current_weather_data_api['wind']['speed']) + " m/s",
                "cloudiness": str(current_weather_data_api['clouds']['all']) + " %",
                "pressure": str(current_weather_data_api['main']['pressure']) + " hPa",
                "humidity": str(current_weather_data_api['main']['humidity']) + " %",
            }
            five_days_weather_list = {}
            today_date = int(datetime.today().strftime('%d'))
            j = 0
            for i in range(0, five_days_weather_data_api['cnt']):
                date_json = five_days_weather_data_api['list'][i]['dt_txt']
                date = datetime.strptime(date_json, '%Y-%m-%d %H:%M:%S')
                if not(int(date.strftime('%d')) == today_date):
                    five_days_weather_list[j] = {}
                    five_days_weather_list[j]['day'] = date.strftime('%A')
                    five_days_weather_list[j]['date'] = date.strftime('%d.%m.%Y')
                    five_days_weather_list[j]['time'] = date.strftime('%I:%M')
                    five_days_weather_list[j]['temp'] = str(
                        int(five_days_weather_data_api['list'][i]['main']['temp']) - 273) + " C"
                    five_days_weather_list[j]['pressure'] = str(
                        five_days_weather_data_api['list'][i]['main']['pressure']) + " hPa"
                    five_days_weather_list[j]['icon'] = str(
                        five_days_weather_data_api['list'][i]['weather'][0]['icon'])
                    today_date += 1
                    j += 1
                else:
                    pass
            data = {
                'current_day': current_day,
                'five_days_list': five_days_weather_list
            }
            print(data)
        except KeyError:
            data = {'current_day': ""}
    else:
        data = {}
    return render(request, "main/index.html", data)
