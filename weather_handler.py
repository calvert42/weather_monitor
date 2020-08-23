import utils

# logging configuration
logger = utils.make_console_logger("weather_handler")


class Weather_Handler:
    def __init__(self, weather_data, i):
        self.weather_data = weather_data
        self.current = weather_data['current']
        self.hourly = weather_data['hourly'][i-1]
        logger.info("Full weather data loaded")

    @staticmethod
    def get_state(full_info):
        weather_state = full_info['weather'][0]['main']
        logger.info(f"Weather state: {weather_state}")
        return weather_state

    @staticmethod
    def get_description(full_info):
        description = full_info['weather'][0]['description']
        logger.info(f"Weather description: {description}")
        return description

    @staticmethod
    def get_temperature(full_info):
        temperature = full_info['temp']
        logger.info(f"Temperature: {temperature} dC")
        return temperature
