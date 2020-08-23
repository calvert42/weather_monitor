import os
import weather_handler
import mail_bot
import time
import utils

# logging configuration
logger = utils.make_console_logger("Weather_Monitor")

# config
USER = os.environ.get('BOT_MAIL')
PASS = os.environ.get('BOT_GOOGLE_APP_PASS')
receiver = os.environ.get('MY_MAIL')
city = "Paris, France"
res_file = "data/result.json"
units = "metric"
api_key = os.environ.get('API_WEATHER')
part = "minutely,daily"
look_ahead = 5
total = 1
current_time = 0
run_time = 0
message = ""


class Weather_Monitor:
    def __init__(self):
        self = self

    @staticmethod
    def get_weather(city, part, units, api_key, res_file):
        lat, lon = utils.get_location_coordinates(city)
        owmap_request = utils.make_owmap_request(
            lat, lon, part, units, api_key)
        weather = utils.send_request(owmap_request)
        utils.save_json_file(weather, res_file)
        return weather

    @staticmethod
    def weather_is_changing(current, hour):
        if current != hour:
            state = f"Weather is changing to {hour}"
            logger.info(f"Weather change: {hour}")
            return state
        else:
            return None

    @staticmethod
    def temp_is_changing(current, hour):
        current = int(current)
        hour = int(hour)
        if current > hour:
            state = f"Temperature is dropping to from {current} to {hour}."
            logger.info("Temp dropping")
            return state
        elif hour > current:
            state = f"Temperature is rising from {current} to {hour}"
            logger.info("Temp rising")
            return state
        else:
            return None


if __name__ == "__main__":
    while current_time < total:
        current_time += 1
        m = Weather_Monitor()

        weather = m.get_weather(city, part, units, api_key, res_file)
        h = weather_handler.Weather_Handler(weather, look_ahead)

        current_weather = h.get_state(h.current)
        next_weather = h.get_state(h.hourly)

        if m.weather_is_changing(current_weather, next_weather):
            message += m.weather_is_changing(current_weather,
                                             next_weather) + "\n"

        current_temp = h.get_temperature(h.current)
        next_temp = h.get_temperature(h.hourly)

        if m.temp_is_changing(current_temp, next_temp):
            message += m.temp_is_changing(current_temp, next_temp) + "\n"

        if len(message) != 0:
            message += "I'm a bot :)"

            mb = mail_bot.Mail_Bot(USER, PASS)
            mb.send_mail(receiver, message)

        logger.info(f"Process ran {current_time} time(s)")
        time.sleep(run_time)
