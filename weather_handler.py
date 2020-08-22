import utils

# logging configuration
logger = utils.make_console_logger("weather_handler")


class Weather_Handler:
    def __init__(self, weather_data):
        self.weather_data = weather_data
        logger.info("Full weather data loaded")

    def get_full_current_weather(self):
        current = self.weather_data['current']
        logger.info("Current weather data loaded")
        return current

    def get_full_hourly_weather(self, i):
        hourly = self.weather_data['hourly'][i]
        logger.info(f"+{i+1} hourly weather data loaded")
        return hourly

    def get_weather_state(self, full_weather):
        weather_state = full_weather['weather'][0]['main']
        logger.info(f"Weather state: {weather_state}")
        return weather_state

    def get_weather_description(self, full_weather):
        description = full_weather['weather'][0]['description']
        logger.info(f"Weather description: {description}")
        return description

    def get_temperature(self, full_weather):
        temperature = full_weather['temp']
        logger.info(f"Temperature: {temperature} dC")
        return temperature

    @staticmethod
    def weather_is_changing(current, hour):
        if current != hour:
            state = f"Weather is changing to {hour}"
            logger.info(f"Weather change: {hour}")
            return state
        else:
            return None

    @staticmethod
    def temperature_is_changing(current, hour):
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
