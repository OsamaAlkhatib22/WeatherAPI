import requests
import logging
from datetime import datetime

#logging set up
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class WeatherAPI:
    #class to interact with the API to fetch and parse weather data.

    def __init__(self):
        #initialize the API with the URL.
        self.base_url = "https://weather.talkpython.fm/api/weather"
        logging.info("WeatherAPI initialized.")

    def validate_inputs(self, city, state, country, units):
        """
        validate the inputs before making the API request.
        ensuring  country code is 2 letters, state is 2 letters (only for US), and units are valid.
        and if there is nothing wrong return true.
        """
        if country and len(country) != 2:
            logging.error("Country code must be exactly 2 letters.")
            return False

        if state and (len(state) != 2 or (country and country.upper() != 'US')):
            logging.error("State code must be 2 letters and is only required when country is US.")
            return False

        if units not in {'metric', 'standard', 'imperial'}:
            logging.error("Invalid units specified. Valid options are 'metric', 'standard', 'imperial'.")
            return False

        return True

    def get_weather_data(self, city, state=None, country=None, units='metric'):
        """
        request weather data for a specific city.
        handling the construction of the request and error handling.
        """
        # inputs
        if not self.validate_inputs(city, state, country, units):
            return None

        try:
            # Construct the request parameters
            params = {
                'city': city,
                'units': units
            }
            if state:
                params['state'] = state
            if country:
                params['country'] = country.upper()

            #API request
            logging.info(f"Requesting weather data for {city}, {country}.")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            logging.info(f"Weather data for {city} received successfully.")
            return response.json()
        except requests.exceptions.HTTPError as http_err:

            #handle specific  errors, like a 404 for an unknown city
            if response.status_code == 404:
                logging.error(f"City name '{city}' might be incorrect or not found in the database.")
            else:
                logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            #handle general request exceptions
            logging.error(f"Error fetching weather data: {req_err}")
        except Exception as e:
            #handle unexpected errors
            logging.error(f"An unexpected error occurred: {e}")
        return None

    def parse_weather_data(self, data):

        #parse the JSON response from the weather API to extract relevant weather information.

        if not data:
            logging.warning("No data to parse.")
            return None

        try:
            #extract and organize weather data into a dictionary
            weather_info = {
                'city': data['location']['city'],
                'state': data['location'].get('state', 'N/A'),
                'country': data['location'].get('country', 'N/A'),
                'temperature': data['forecast']['temp'],
                'feels_like': data['forecast']['feels_like'],
                'pressure': data['forecast']['pressure'],
                'humidity': data['forecast']['humidity'],
                'low': data['forecast']['low'],
                'high': data['forecast']['high'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind']['deg'],
                'description': data['weather']['description'],
                'category': data['weather']['category'],
                'units': data['units'],
                'rate_limiting_unique_lookups_remaining': data['rate_limiting']['unique_lookups_remaining'],
                'rate_limiting_lookup_reset_window': data['rate_limiting']['lookup_reset_window'],
                'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #current date and time
            }
            logging.info(f"Weather data parsed successfully for {weather_info['city']}.")
            return weather_info

        #handling JSON response and any unexpected errors during parsing

        except KeyError as e:
            logging.error(f"Key error while parsing data: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred during parsing: {e}")
            return None
