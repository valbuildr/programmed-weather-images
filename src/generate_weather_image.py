from PIL import Image, ImageDraw, ImageFont
from random import choice
from requests import get
from discord import File

api_key = open("./weather_token.txt", "r").read()


icons = {
    "day": {
        "Sunny": "wi-day-sunny",
        "Partly cloudy": "wi-day-cloudy",
        "Cloudy": "wi-cloud",
        "Overcast": "wi-cloud",
        "Mist": "wi-sprinkle",
        "Patchy rain possible": "wi-day-rain",
        "Patchy snow possible": "wi-day-snow",
        "Patchy sleet possible": "wi-day-sleet",
        "Patchy freezing drizzle possible": "wi-rain-mix",
        "Thundery outbreaks possible": "wi-day-lightning",
        "Blowing snow": "wi-snow-wind",
        "Blizzard": "wi-snow-wind",
        "Fog": "wi-fog",
        "Freezing fog": "wi-fog",
        "Patchy light drizzle": "wi-rain",
        "Light drizzle": "wi-rain",
        "Freezing drizzle": "wi-rain-mix",
        "Heavy freezing drizzle": "wi-rain-mix",
        "Patchy light rain": "wi-day-rain",
        "Light rain": "wi-rain",
        "Moderate rain at times": "wi-day-rain",
        "Moderate rain": "wi-rain",
        "Heavy rain at times": "wi-day-rain",
        "Heavy rain": "wi-rain",
        "Light freezing rain": "wi-rain-mix",
        "Moderate or heavy freezing rain": "wi-rain-mix",
        "Light sleet": "wi-sleet",
        "Moderate or heavy sleet": "wi-sleet",
        "Patchy light snow": "wi-day-snow",
        "Light snow": "wi-snow",
        "Patchy moderate snow": "wi-day-snow",
        "Moderate snow": "wi-snow",
        "Patchy heavy snow": "wi-day-snow",
        "Heavy snow": "wi-snow",
        "Ice pellets": "wi-hail",
        "Light rain shower": "wi-day-showers",
        "Moderate or heavy rain shower": "wi-day-rain",
        "Torrential rain shower": "wi-day-rain",
        "Light sleet showers": "wi-day-sleet",
        "Moderate or heavy sleet showers": "wi-day-sleet",
        "Light snow showers": "wi-day-snow",
        "Moderate or heavy snow showers": "wi-day-snow",
        "Light showers of ice pellets": "wi-day-hail",
        "Moderate or heavy showers of ice pellets": "wi-day-hail",
        "Patchy light rain with thunder": "wi-day-lightning",
        "Moderate or heavy rain with thunder": "wi-lightning",
        "Patchy light snow with thunder": "wi-day-snow-thunderstorm",
        "Moderate or heavy snow with thunder": "wi-lightning",
    },
    "night": {
        "Clear": "wi-night-clear",
        "Partly cloudy": "wi-night-cloudy",
        "Cloudy": "wi-cloud",
        "Overcast": "wi-cloud",
        "Mist": "wi-sprinkle",
        "Patchy rain possible": "wi-night-rain",
        "Patchy snow possible": "wi-night-snow",
        "Patchy sleet possible": "wi-night-sleet",
        "Patchy freezing drizzle possible": "wi-rain-mix",
        "Thundery outbreaks possible": "wi-night-lightning",
        "Blowing snow": "wi-snow-wind",
        "Blizzard": "wi-snow-wind",
        "Fog": "wi-fog",
        "Freezing fog": "wi-fog",
        "Patchy light drizzle": "wi-rain",
        "Light drizzle": "wi-rain",
        "Freezing drizzle": "wi-rain-mix",
        "Heavy freezing drizzle": "wi-rain-mix",
        "Patchy light rain": "wi-night-rain",
        "Light rain": "wi-rain",
        "Moderate rain at times": "wi-night-rain",
        "Moderate rain": "wi-rain",
        "Heavy rain at times": "wi-night-rain",
        "Heavy rain": "wi-rain",
        "Light freezing rain": "wi-rain-mix",
        "Moderate or heavy freezing rain": "wi-rain-mix",
        "Light sleet": "wi-sleet",
        "Moderate or heavy sleet": "wi-sleet",
        "Patchy light snow": "wi-night-snow",
        "Light snow": "wi-snow",
        "Patchy moderate snow": "wi-night-snow",
        "Moderate snow": "wi-snow",
        "Patchy heavy snow": "wi-night-snow",
        "Heavy snow": "wi-snow",
        "Ice pellets": "wi-hail",
        "Light rain shower": "wi-night-showers",
        "Moderate or heavy rain shower": "wi-night-rain",
        "Torrential rain shower": "wi-night-rain",
        "Light sleet showers": "wi-night-sleet",
        "Moderate or heavy sleet showers": "wi-night-sleet",
        "Light snow showers": "wi-night-snow",
        "Moderate or heavy snow showers": "wi-night-snow",
        "Light showers of ice pellets": "wi-night-hail",
        "Moderate or heavy showers of ice pellets": "wi-night-hail",
        "Patchy light rain with thunder": "wi-night-lightning",
        "Moderate or heavy rain with thunder": "wi-lightning",
        "Patchy light snow with thunder": "wi-night-snow-thunderstorm",
        "Moderate or heavy snow with thunder": "wi-lightning",
    }
}


def get_season(data):
    month = data["location"]["localtime"].split("-")[1]

    if month == "03" or month == "04" or month == "05":
        return "Spring"
    elif month == "06" or month == "07" or month == "08":
        return "Summer"
    elif month == "09" or month == "10" or month == "11":
        return "Fall"
    elif month == "12" or month == "01" or month == "02":
        return "Winter"
    else:
        raise Exception("Unexpected month")

def create_4_by_3(save_to: str, imperial: bool = True, location: str = "10001"):
    # api
    r = get(
        "http://api.weatherapi.com/v1/current.json",
        params={
            "key": api_key,
            "q": location,
            "aqi": "no"
        },
        headers={
            "Accept": "application/json"
        }
    )

    data = r.json()

    if r.status_code == 400 and r.json()["error"]["code"] == 1006:
        raise Exception("No matching location found.")
    elif r.status_code == 400:
        raise Exception("An error ocurred.")

    # season
    season = get_season(data)

    # background
    c = choice(["1", "2", "3"])
    img = Image.open(f"./assets/bg/cut/4-3/{season}{c}.png")

    # transparent elements
    img2 = Image.open("./reference/4-3/template-4_3.png")

    # text and icons
    img3 = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img3)

    # city name
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Bold.ttf", 38)
    draw.text((51, 59), data["location"]["name"], font=font, anchor="lt", align="left")

    # clock
    font = ImageFont.truetype("./assets/fonts/JetBrainsMono-Bold.ttf", 38)
    draw.text((860, 59), data["location"]["localtime"].split(" ")[1], font=font, anchor="lt", align="left")

    # now text
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 21)
    draw.text((63, 158), "Now", font=font, anchor="lt", align="left")

    # circle
    draw.ellipse((63, 271, 288, 496), (54, 54, 54, 255))

    # condition icon
    t = "night"
    if data["current"]["is_day"] == 1:
        t = "day"
    icon = icons[t][data["current"]["condition"]["text"]]
    iconImg = Image.open(f"./assets/icons/4-3/{icon}.png")
    img3.paste(iconImg, (106, 295), iconImg)

    # temperature text
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Bold.ttf", 46)
    if imperial:
        draw.text((176, 439), str(round(data["current"]["temp_f"])), font=font, anchor="mt", align="center")
    else:
        draw.text((176, 439), str(round(data["current"]["temp_c"])), font=font, anchor="mt", align="center")

    # condition text
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Bold.ttf", 46)
    draw.text((325, 220), data["current"]["condition"]["text"], font=font, anchor="lt", align="left")

    # winds
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 288), "Winds", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    if imperial:
        draw.text((513, 288), f"{str(round(data["current"]["wind_mph"]))} mph {data["current"]["wind_dir"]}", font=font, anchor="lt", align="left")
    else:
        draw.text((513, 288), f"{str(round(data["current"]["wind_kph"]))} kph {data["current"]["wind_dir"]}", font=font, anchor="lt", align="left")
    
    # humidity
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 327), "Humidity", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    draw.text((513, 327), f"{data["current"]["humidity"]}%", font=font, anchor="lt", align="left")

    # feels like
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 366), "Feels like", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    if imperial:
        draw.text((513, 366), f"{str(round(data["current"]["feelslike_f"]))}°", font=font, anchor="lt", align="left")
    else:
        draw.text((513, 366), f"{str(round(data["current"]["feelslike_c"]))}°", font=font, anchor="lt", align="left")

    # dewpoint
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 405), "Dewpoint", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    if imperial:
        draw.text((513, 405), f"{str(round(data["current"]["dewpoint_f"]))}°", font=font, anchor="lt", align="left")
    else:
        draw.text((513, 405), f"{str(round(data["current"]["dewpoint_c"]))}°", font=font, anchor="lt", align="left")

    # visibility
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 444), "Visibility", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    if imperial:
        draw.text((513, 444), f"{data["current"]["vis_miles"]} mi", font=font, anchor="lt", align="left")
    else:
        draw.text((513, 444), f"{data["current"]["vis_km"]} km", font=font, anchor="lt", align="left")
    
    # uv
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 483), "UV", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    draw.text((513, 483), f"{round(data["current"]["uv"])}", font=font, anchor="lt", align="left")

    # pressure
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 36)
    draw.text((325, 522), "Pressure", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 36)
    if imperial:
        draw.text((513, 522), f"{data["current"]["pressure_in"]} in", font=font, anchor="lt", align="left")
    else:
        draw.text((513, 522), f"{data["current"]["pressure_mb"]} mb", font=font, anchor="lt", align="left")

    # credit and disclaimer
    font = ImageFont.truetype("./assets/fonts/JetBrainsMono-Italic.ttf", 15)

    disclaimer = ""
    if imperial:
        disclaimer = "All temperatures are in Fahrenheit unless otherwise noted."
    else:
        disclaimer = "All temperatures are in Celsius unless otherwise noted."
    
    credit = ""
    if season == "Fall":
        if c == "1":
            credit = "Photo by Pixabay via Pexels."
        elif c == "2":
            credit = "Photo by Chait Goli via Pexels."
        elif c == "3":
            credit = "Photo by Craig Adderley via Pexels."
    elif season == "Spring":
        if c == "1":
            credit = "Photo by Pixabay via Pexels."
        elif c == "2":
            credit = "Photo by David Bartus via Pexels."
        elif c == "3":
            credit = "Photo by Abby Chung via Pexels."
    elif season == "Summer":
        if c == "1":
            credit = "Photo by Aleksandar Pasaric via Pexels."
        elif c == "2":
            credit = "Photo by Pixabay via Pexels."
        elif c == "3":
            credit = "Photo by Roberto Nickson via Pexels."
    elif season == "Winter":
        if c == "1":
            credit = "Photo by Riccardo via Pexels."
        elif c == "2":
            credit = "Photo by Stefan Stefancik via Pexels."
        elif c == "3":
            credit = "Photo by Marek Piwnicki via Pexels."

    draw.text((38, 664), f"{disclaimer}\nData provided by weatherapi.com.\n{credit}", font=font, align="left", stroke_fill=(0, 0, 0), stroke_width=1)


    # overlay transparent elements
    img = Image.alpha_composite(img, img2)
    img = Image.alpha_composite(img, img3)

    # save image
    img.save(save_to, "png")

    return File(save_to)

# TODO: 16:9
def create_16_by_9(save_to: str, imperial: bool = True, location: str = "10001"):
    # api
    r = get(
        "http://api.weatherapi.com/v1/current.json",
        params={
            "key": api_key,
            "q": location,
            "aqi": "no"
        },
        headers={
            "Accept": "application/json"
        }
    )

    data = r.json()

    if r.status_code == 400 and r.json()["error"]["code"] == 1006:
        raise Exception("No matching location found.")
    elif r.status_code == 400:
        raise Exception("An error ocurred.")
    
    # season
    season = get_season(data)

    # background
    c = choice(["1", "2", "3"])
    img = Image.open(f"./assets/bg/cut/16-9/{season}{c}.png")

    # transparent elements
    img2 = Image.open("./reference/16-9/template-16_9.png")

    # text and icons
    img3 = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img3)

    # city name
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Bold.ttf", 53)
    draw.text((312, 83), data["location"]["name"], font=font, anchor="lt", align="left")

    # clock
    font = ImageFont.truetype("./assets/fonts/JetBrainsMono-Bold.ttf", 53)
    draw.text((1450, 83), data["location"]["localtime"].split(" ")[1], font=font, anchor="lt", align="left")

    # now text
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 30)
    draw.text((329, 222), "Now", font=font, anchor="lt", align="left")

    # circle
    draw.ellipse((329, 381, 645, 698), (54, 54, 54, 255))

    # condition icon
    t = "night"
    if data["current"]["is_day"] == 1:
        t = "day"
    icon = icons[t][data["current"]["condition"]["text"]]
    iconImg = Image.open(f"./assets/icons/16-9/{icon}.png")
    img3.paste(iconImg, (399, 435), iconImg)

    # temperature text
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Bold.ttf", 64)
    if imperial:
        draw.text((487, 603), str(round(data["current"]["temp_f"])), font=font, anchor="mt", align="center")
    else:
        draw.text((487, 603), str(round(data["current"]["temp_c"])), font=font, anchor="mt", align="center")

    # condition text
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Bold.ttf", 64)
    draw.text((697, 309), data["current"]["condition"]["text"], font=font, anchor="lt", align="left")

    # winds
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 405), "Winds", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    if imperial:
        draw.text((961, 405), f"{str(round(data["current"]["wind_mph"]))} mph {data["current"]["wind_dir"]}", font=font, anchor="lt", align="left")
    else:
        draw.text((961, 405), f"{str(round(data["current"]["wind_kph"]))} kph {data["current"]["wind_dir"]}", font=font, anchor="lt", align="left")
    
    # humidity
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 459), "Humidity", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    draw.text((961, 459), f"{data["current"]["humidity"]}%", font=font, anchor="lt", align="left")

    # feels like
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 514), "Feels like", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    if imperial:
        draw.text((961, 514), f"{str(round(data["current"]["feelslike_f"]))}°", font=font, anchor="lt", align="left")
    else:
        draw.text((961, 514), f"{str(round(data["current"]["feelslike_c"]))}°", font=font, anchor="lt", align="left")
    
    # dewpoint
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 568), "Dewpoint", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    if imperial:
        draw.text((961, 568), f"{str(round(data["current"]["dewpoint_f"]))}°", font=font, anchor="lt", align="left")
    else:
        draw.text((961, 568), f"{str(round(data["current"]["dewpoint_c"]))}°", font=font, anchor="lt", align="left")
    
    # visibility
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 622), "Visibility", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    if imperial:
        draw.text((961, 622), f"{data["current"]["vis_miles"]} mi", font=font, anchor="lt", align="left")
    else:
        draw.text((961, 622), f"{data["current"]["vis_km"]} km", font=font, anchor="lt", align="left")
    
    # uv
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 676), "UV", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    draw.text((961, 676), f"{round(data["current"]["uv"])}", font=font, anchor="lt", align="left")

    # pressure
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-SemiBold.ttf", 51)
    draw.text((697, 731), "Pressure", font=font, anchor="lt", align="left")
    font = ImageFont.truetype("./assets/fonts/InstrumentSans-Regular.ttf", 51)
    if imperial:
        draw.text((961, 731), f"{data["current"]["pressure_in"]} in", font=font, anchor="lt", align="left")
    else:
        draw.text((961, 731), f"{data["current"]["pressure_mb"]} mb", font=font, anchor="lt", align="left")
    
    # credit and disclaimer
    font = ImageFont.truetype("./assets/fonts/JetBrainsMono-Italic.ttf", 21)

    disclaimer = ""
    if imperial:
        disclaimer = "All temperatures are in Fahrenheit unless otherwise noted."
    else:
        disclaimer = "All temperatures are in Celsius unless otherwise noted."
    
    credit = ""
    if season == "Fall":
        if c == "1":
            credit = "Photo by Pixabay via Pexels."
        elif c == "2":
            credit = "Photo by Chait Goli via Pexels."
        elif c == "3":
            credit = "Photo by Craig Adderley via Pexels."
    elif season == "Spring":
        if c == "1":
            credit = "Photo by Pixabay via Pexels."
        elif c == "2":
            credit = "Photo by David Bartus via Pexels."
        elif c == "3":
            credit = "Photo by Abby Chung via Pexels."
    elif season == "Summer":
        if c == "1":
            credit = "Photo by Aleksandar Pasaric via Pexels."
        elif c == "2":
            credit = "Photo by Pixabay via Pexels."
        elif c == "3":
            credit = "Photo by Roberto Nickson via Pexels."
    elif season == "Winter":
        if c == "1":
            credit = "Photo by Riccardo via Pexels."
        elif c == "2":
            credit = "Photo by Stefan Stefancik via Pexels."
        elif c == "3":
            credit = "Photo by Marek Piwnicki via Pexels."
    
    draw.text((293, 935), f"{disclaimer}\nData provided by weatherapi.com.\n{credit}", font=font, align="left", stroke_fill=(0, 0, 0), stroke_width=1)


    # overlay transparent elements
    img = Image.alpha_composite(img, img2)
    img = Image.alpha_composite(img, img3)

    # save image
    img.save(save_to, "png")

    return File(save_to)