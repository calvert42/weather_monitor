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
    def weather_is_changing(current_w, next_w):
        if current_w != next_w:
            state = f"Weather is changing to {next_w}"
            logger.info(f"Weather change: {next_w}")
            return state
        else:
            return None

    @staticmethod
    def temp_is_changing(current_t, next_t):
        current_t = int(current_t)
        next_t = int(next_t)
        if current_t > next_t:
            state = f"Temperature is dropping to from {current_t} to {next_t}."
            logger.info("Temp dropping")
            return state
        elif next_t > current_t:
            state = f"Temperature is rising from {current_t} to {next_t}"
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
        weather_change = m.weather_is_changing(current_weather, next_weather)
        if weather_change:
            message += weather_change + "\n"

        current_temp = h.get_temperature(h.current)
        next_temp = h.get_temperature(h.hourly)
        temp_change = m.temp_is_changing(current_temp, next_temp)
        if temp_change:
            message += temp_change + "\n"

        if len(message) != 0:
            mb = mail_bot.Mail_Bot(USER, PASS)
            mb.send_mail(receiver, message)

        logger.info(f"Process ran {current_time} time(s)")
        time.sleep(run_time)
