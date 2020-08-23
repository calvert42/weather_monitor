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
        # weather data will be collected for this location
        self.location = config['location']
        # where the weather data will be stored
        self.res_file = config['result_file']
        # units for temperature, by defaults Celsius
        self.units = config['units']
        # keep only a part of the data, by default current/hourly weather
        self.part = config['part']
        # this sets the time period to be evaluated, by default 1h
        self.look_ahead = config['look_ahead']
        # number of time the bot is supposed to send updates
        self.total = config['total']
        # how long should the bot wait between runs
        self.run_time = config['run_time']
        # current update number
        self.current_process = 0
        # empty message for initialisation
        self.message = ""

    def get_weather(self):
        # get the location coordinates and sends a request to OWM api
        # returns a dic containing the weather data
        lat, lon = utils.get_location_coordinates(self.location)
        owmap_request = utils.make_owmap_request(
            lat, lon, self.part, self.units, self.api_key)
        weather = utils.send_request(owmap_request)
        utils.save_json_file(weather, self.res_file)
        return weather

    @staticmethod
    # check wether the weather will be changing during the time period
    def weather_is_changing(current_w, next_w):
        if current_w != next_w:
            state = f"Weather is changing to {next_w}"
            logger.info(f"Weather change: {next_w}")
            return state
        else:
            return None

    @staticmethod
    # check wether the temperature will be changing during the time period
    def temp_is_changing(current_t, next_t):
        current_t = int(current_t)
        next_t = int(next_t)
        if current_t > next_t:
            state = f"Temperature is dropping to {current_t} from {next_t}."
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
    # initialise the monitor
    m = Weather_Monitor(config)
    while m.current_process < m.total:

        # get the weather data and send them to a handler
        weather = m.get_weather()
        h = weather_handler.Weather_Handler(weather, m.look_ahead)

        # check wether the weather will be changing
        # and update the monitor's response
        current_weather = h.get_state(h.current)
        next_weather = h.get_state(h.hourly)
        weather_change = m.weather_is_changing(
            current_weather, next_weather)
        if weather_change:
            m.message += weather_change + "\n"

        # check wether the temperature will be changing
        # and update the monitor's response
        current_temp = h.get_temperature(h.current)
        next_temp = h.get_temperature(h.hourly)
        temp_change = m.temp_is_changing(current_temp, next_temp)
        if temp_change:
            m.message += temp_change + "\n"

        # check wether the message is empty and sends the update
        # to the receiver
        if len(m.message) != 0:
            m.message += f'This will happen in {m.look_ahead} hour(s).\n'
            logger.info(f"Will send {m.message}")
            mb = mail_bot.Mail_Bot()
            mb.send_mail(m.receiver, m.message)
        m.message = ""
        m.current_process += 1

        logger.info(f"Process ran {m.current_process} time(s)")
        time.sleep(m.run_time)
