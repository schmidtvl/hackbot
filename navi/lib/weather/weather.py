import urllib, json

def calc_windchill(T,V):
    ve = V ** 0.16
    c1 = 13.12
    c2 = 0.6215 * T
    c3 = 11.37 * ve
    c4 = 0.3965 * T * ve

    return int(round(c1 + c2 - c3 + c4))

def get(location):
    if location and location == "help":
        return ( "Looks up the current weather for anywhere you'd like. "
        "Defaults to Winnipeg (ex. !weather Berlin, Germany)"
        )
    if not location:
        location = "winnipeg"
    key = "16942d985928497a9c7cabb4b3b924ec"
    url = "http://api.openweathermap.org/data/2.5/weather?q={loc}&units=metric&appid={key}"

    try:
        response = urllib.urlopen(url.format(loc=location,key=key))
    except:
        return (
            "Sorry! The weather service is currently unavailable, "
            "but https://www.google.ca/search?q={location}+weather"
        ).format(location=location)

    weather = json.loads(response.read())

    if weather['cod'] == 200:
        temp = weather['main']['temp']
        temp_with_windchill = None
        wind_speed = weather['wind']['speed']
        windchill_message = ""

        if  temp < 0 and  wind_speed >= 5:
            temp_with_windchill = calc_windchill(temp, wind_speed)

        if temp_with_windchill:
            windchill_message = " but feels like {temp_with_windchill}C".format(temp_with_windchill=temp_with_windchill)

        return (
            "{location}, {country} currently: "
            "{temp}C{windchill_message} with {desc}, {detail}"
        ).format(
            location=weather['name'],
            country=weather['sys']['country'],
            temp=weather['main']['temp'],
            desc=weather['weather'][0]['main'],
            detail=weather['weather'][0]['description'],
            windchill_message=windchill_message
        )
    else:
        return (
            '''I can't find the weather for "{location}".'''
        ).format(location=location)
