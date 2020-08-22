import requests
import os
import logging
import weather_handler
import mail_bot
import json
from geopy.geocoders import Nominatim
import time
import utils

# logging configuration

logger = utils.make_console_logger("main")

USER = os.environ.get('BOT_MAIL')
PASS = os.environ.get('BOT_GOOGLE_APP_PASS')
receiver = os.environ.get('MY_MAIL')
city = "Paris, France"
res_file = "data/result.json"
units = "metric"
api_key = os.environ.get('API_WEATHER')
part = "minutely,daily"
look_ahead = 2
total = 4
current_time = 0
run_time = 60*60


def init(city, res_file, units, api_key, part):
    lat, lon = utils.get_location_coordinates(city)
    request_url = utils.make_api_request(lat, lon, part, units, api_key)
    weather = utils.send_request(request_url)
    utils.save_json_file(weather, res_file)
    weather = utils.open_json_file(res_file)
    logger.info("Initialisation succeeded")
    return weather


def main():

    weather = init(city, res_file, units, api_key, part)

    wh = weather_handler.Weather_Handler(weather)
    full_weather = wh.get_full_current_weather()
    next_full_weather = wh.get_full_hourly_weather((look_ahead - 1))
    current_weather = wh.get_weather_state(full_weather)
    next_weather = wh.get_weather_state(next_full_weather)
    weather_is_changing = wh.weather_is_changing(current_weather, next_weather)
    current_temp = wh.get_temperature(full_weather)
    next_temp = wh.get_temperature(next_full_weather)
    temp_is_changing = wh.temperature_is_changing(current_temp, next_temp)

    message = ""
    if weather_is_changing:
        message += weather_is_changing + "\n"

    if temp_is_changing:
        message += temp_is_changing + "\n"

    if len(message) != 0:
        message += "I'm a bot :)"

        mb = mail_bot.Mail_Bot(USER, PASS)
        mb.send_mail(receiver, message)


if __name__ == "__main__":
    while current_time < total:
        main()
        current_time += 1
        logger.info(f"Process ran {current_time} time(s)")
        time.sleep(run_time)
