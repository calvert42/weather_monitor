import utils

# logging configuration
logger = utils.make_console_logger("weather_handler")


class Weather_Handler:
    def __init__(self, weather_data, i):
        # contains the full weather data
        self.weather_data = weather_data
        # contains the full current weather data
        self.current = weather_data['current']
        # contains the hourly data with the look ahead
        # specified by the monitor, by default 1h
        self.hourly = weather_data['hourly'][i-1]
        logger.info("Full weather data loaded")

    @staticmethod
    # gets the coarse description of the weather
    def get_state(full_info):
        weather_state = full_info['weather'][0]['main']
        logger.info(f"Weather state: {weather_state}")
        return weather_state

    @staticmethod
    # gets the more detailled description of the weather
    def get_description(full_info):
        description = full_info['weather'][0]['description']
        logger.info(f"Weather description: {description}")
        return description

    @staticmethod
    # gets the temperature
    def get_temperature(full_info):
        temperature = full_info['temp']
        logger.info(f"Temperature: {temperature} dC")
        return temperature
