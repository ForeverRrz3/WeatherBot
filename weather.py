from time import *
from translate import *
from math import *
from bs4 import BeautifulSoup
from requests import *

def lat_lon_town(name:str):
    t = Translator(from_lang="ru",to_lang="en")
    town = t.translate(name)
    print(town)
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={name}&limit=5&appid=01c132b3eb49bd5fc9483e858314c928"
    response = get(url).json()[0]

    lat = response["lat"]
    lon = response["lon"]



    return lat,lon

def weather_town_one_day(town:str):
    lat,lon = lat_lon_town(town)
    t = Translator(to_lang="ru",from_lang="en")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={town}&appid=01c132b3eb49bd5fc9483e858314c928&units=metric"
    response = get(url).json()
    print(response)
    weather = response["main"]
    feels, temp  = ceil(weather["feels_like"]),ceil(weather["temp"])
    sky = t.translate(response["weather"][0]["description"])
    return f"Температура ощущается как {"+"+str(feels) if feels>=0 else "-"+str(feels)}, реальная - {"+"+str(temp) if temp>=0 else "-"+str(temp)}. Погода - {sky}"

def weather_days(town:str):
    t = Translator(to_lang="ru",from_lang="en")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={town}&appid=01c132b3eb49bd5fc9483e858314c928&units=metric&lang=ru"
    response = get(url)
    data = response.json()
    back = []
    for i in data["list"]:
        if "12:00:00" in i["dt_txt"]:
            feels, temp = ceil(i["main"]["feels_like"]), ceil(i["main"]["temp"])
            sky = i["weather"][0]["description"]
            back.append(f"- {i["dt_txt"]} температура ощущается как {"+"+str(feels) if feels>=0 else "-"+str(feels)}, реальная - {"+"+str(temp) if temp>=0 else "-"+str(temp)}. Погода - {sky}\n")
    return back

# 01c132b3eb49bd5fc9483e858314c928


