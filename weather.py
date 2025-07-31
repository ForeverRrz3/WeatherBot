from math import *
from requests import *



def weather_town_one_day(town:str):


    params = {"q": town,
            "appid":"API KEY",
            "units":"metric",
            "lang":"ru"}
    url = f"https://api.openweathermap.org/data/2.5/weather"
    response = get(url, params=params).json()
    
    weather = response["main"]
    feels, temp, sky  = ceil(weather["feels_like"]),ceil(weather["temp"]),response["weather"][0]["description"]
    
    return f"Температура ощущается как {"+"+str(feels) if feels>=0 else "-"+str(feels)}, реальная - {"+"+str(temp) if temp>=0 else "-"+str(temp)}. Погода - {sky}"

def weather_days(town:str):
    params = {"q": town,
            "appid":"API KEY",
            "units":"metric",
            "lang":"ru"}
    

    url = f"http://api.openweathermap.org/data/2.5/forecast"
    response = get(url,params=params)
    data = response.json()

    back = []
    for i in data["list"]:
        if "12:00:00" in i["dt_txt"]:
            feels, temp = ceil(i["main"]["feels_like"]), ceil(i["main"]["temp"])
            sky = i["weather"][0]["description"]
            back.append(f"- {i["dt_txt"]} температура ощущается как {"+"+str(feels) if feels>=0 else "-"+str(feels)}, реальная - {"+"+str(temp) if temp>=0 else "-"+str(temp)}. Погода - {sky}\n")
    return back


