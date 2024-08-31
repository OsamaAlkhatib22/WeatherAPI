from API import WeatherAPI
from Database import WeatherDatabase


def main():
    #  the parameters for the API request
    city = 'Dubai'  #required field, the city for which you want to fetch weather data
    state = ''  #optional field, only 2 letters needed, needed only if the country is 'US' , leave it empty if you dont want to include it ''.
    country = 'AE'  #country code, 'US' if none specified, only 2 letters needed.
    units = 'standard'  #valid options are 'metric', 'standard', 'imperial'; default is 'metric', anything else not excepted.

    #create an instance of WeatherAPI to handle API interactions
    weather_api = WeatherAPI()

    #validate inputs before making the API request
    if not weather_api.validate_inputs(city, state, country, units):
        print("Invalid input parameters. Please correct them and try again.")
        return  #exit the function if validation fails

    #create an instance of WeatherDatabase to handle database operations
    weather_db = WeatherDatabase(db_name='new_weather_data.db')

    #fetching the weather data using the API
    data = weather_api.get_weather_data(city, state=state, country=country, units=units)

    #parse the JSON data received from the API
    weather_info = weather_api.parse_weather_data(data)

    if weather_info:
        #insert the parsed data into the database

        weather_db.insert_weather_data(weather_info)
        print(f"Weather data for {city} has been stored in the database.")

    #close the database connection
    weather_db.close()


if __name__ == '__main__':
    main()
