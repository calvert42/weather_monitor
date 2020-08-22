import logging
import json
import requests
from geopy.geocoders import Nominatim

# initialise utils logging
logger_utils = logging.getLogger(__name__)
logger_utils.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger_utils.addHandler(console_handler)


def make_console_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def make_file_logger(name, file):
    logger = make_console_logger(name)
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(logging.CRITICAL)
    file_handler.setFormatter
    logger.addHandler(file_handler)
    return logger


def make_api_request(lat, lon, part, units, api_key):
    base = "https://api.openweathermap.org/data/2.5/onecall?"
    full = base+"lat="+str(lat)+"&lon="+str(lon)+"&exclude=" + \
        part+"&units="+units+"&appid="+api_key
    logger_utils.info(f"Requesting at: {full}")
    return full


def send_request(req):
    r = requests.get(req)
    if r.ok:
        logger_utils.info("Request successful :)")
        weather = r.json()
        return weather
    else:
        logger_utils("Request failed :(")


def open_json_file(file):
    with open(file, "r") as f:
        data = json.load(f)
        logger_utils.info("Data loaded from json successfully")
    return data


def save_json_file(weather, file):
    with open(file, "w") as f:
        json.dump(weather, f)
        logger_utils.info("Jason file written")


def get_location_coordinates(location):
    geolocator = Nominatim(user_agent="Weather Monitor")
    location = geolocator.geocode(location)
    logger_utils.info(f"Fetched coordinates for {location}")
    return location.latitude, location.longitude
