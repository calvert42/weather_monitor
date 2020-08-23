import os
import weather_handler
import mail_bot
import time
import utils

# logging configuration
logger = utils.make_console_logger("Weather_Monitor")


class Weather_Monitor:
    def __init__(self, config):
        self.api_key = os.environ.get('API_WEATHER')
        self.receiver = os.environ.get('MY_MAIL')
        self.city = config['city']
        self.res_file = config['res_file']
        self.units = config['units']
        self.part = config['part']
        self.look_ahead = config['look_ahead']
        self.total = config['total']
        self.current_process = config['current_process']
        self.run_time = config['run_time']
        self.message = ""

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
    config = utils.open_json_file("config.json")
    m = Weather_Monitor(config)
    while m.current_process < m.total:
        m.current_process += 1

        weather = m.get_weather(m.city, m.part, m.units, m.api_key, m.res_file)
        h = weather_handler.Weather_Handler(weather, m.look_ahead)

        current_weather = h.get_state(h.current)
        next_weather = h.get_state(h.hourly)
        weather_change = m.weather_is_changing(
            current_weather, next_weather)
        if weather_change:
            m.message += weather_change + "\n"

        current_temp = h.get_temperature(h.current)
        next_temp = h.get_temperature(h.hourly)
        temp_change = m.temp_is_changing(current_temp, next_temp)
        if temp_change:
            m.message += temp_change + "\n"

        if len(m.message) != 0:
            mb = mail_bot.Mail_Bot()
            mb.send_mail(m.receiver, m.message)

        logger.info(f"Process ran {m.current_process} time(s)")
        time.sleep(m.run_time)
