def beaufort_scale(speed):
    if speed < 0:
        return "I don't fucking know"
    elif speed <= 0.3:
        return "Calm"
    elif speed <= 1.5:
        return "Light air"
    elif speed <= 3.3:
        return "Light breeze"
    elif speed <= 5.5:
        return "Gentle breeze"
    elif speed <= 7.9:
        return "Moderate breeze"
    elif speed <= 10.7:
        return "Fresh breeze"
    elif speed <= 13.8:
        return "Strong breeze"
    elif speed <= 17.1:
        return "Moderate gale"
    elif speed <= 20.7:
        return "Gale"
    elif speed <= 24.4:
        return "Strong gale"
    elif speed <= 28.4:
        return "Storm"
    elif speed <= 32.6:
        return "Violent storm"
    else:
        return "Hurricane force"

def pretty_weather(weather):
    weather = weather.lower()
    if weather == "light rain":
        return "Light rain"
    elif weather == "snow":
        return "Snow"
    elif weather == "light intensity drizzle":
        return "Light intensity drizzle"
    elif weather == "light snow":
        return "Light snow"
    elif weather == "broken clouds":
        return "Broken clouds"
    elif weather == "clear sky":
        return "Clear sky"
    elif weather == "haze":
        return "Haze"
    elif weather == "overcast clouds":
        return "Overcast clouds"
    elif weather == "mist":
        return "Mist"
    elif weather == "few clouds":
        return "Few clouds"
    elif weather == "scattered clouds":
        return "Scattered clouds"
    elif weather == "moderate rain":
        return "Moderate rain"
    elif weather == "shower rain":
        return "Shower rain"
    else:
        return weather.capitalize()