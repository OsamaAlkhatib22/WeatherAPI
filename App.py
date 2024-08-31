from flask import Flask, render_template, request, redirect, url_for, flash
from API import WeatherAPI
from Database import WeatherDatabase

#initialize the Flask application
app = Flask(__name__)

#secret key needed for session management and flashing messages
app.secret_key = 'key_123'

#create instances of API and WeatherDatabase for API interaction and database storage
weather_api = WeatherAPI()
weather_db = WeatherDatabase(db_name='new_weather_data.db')


@app.route('/', methods=['GET', 'POST'])
def index():

    #handling both GET and POST requests.

    if request.method == 'POST':
        #retrieve form data entered by the user
        city = request.form.get('city')
        state = request.form.get('state', '').strip()  # State is optional, default to empty string if not provided
        country = request.form.get('country', '').strip() or 'US'  # Default to 'US' if no country is provided
        units = request.form.get('units', 'metric')  # Default units to 'metric' if not provided

        #validate inputs using the WeatherAPI validation method
        if not weather_api.validate_inputs(city, state, country, units):
            # If inputs are invalid, flash an error message and redirect back to the form
            flash("Invalid input parameters. Please correct them and try again.", "error")
            return redirect(url_for('index'))

        #fetch the weather data from the API
        data = weather_api.get_weather_data(city, state=state, country=country, units=units)

        #handle the case where the API returns an error or no data
        if not data:
            flash(
                "Failed to retrieve weather data. The city or country name might be incorrect, or the API is unreachable.",
                "error")
            return redirect(url_for('index'))

        #parse the fetched data to extract relevant weather information
        weather_info = weather_api.parse_weather_data(data)

        #handle errors during the parsing of the API data
        if not weather_info:
            flash("Failed to parse weather data. There might be an issue with the API response.", "error")
            return redirect(url_for('index'))

        #attempt to store the parsed weather data in the database
        try:
            weather_db.insert_weather_data(weather_info)
            flash(f"Weather data for {city}, {country} has been stored in the database.", "success")
            return render_template('result.html', weather_info=weather_info)
        except Exception as e:
            #handle any exceptions during the database insertion process
            flash(f"An error occurred while storing the data: {str(e)}", "error")
            return redirect(url_for('index'))

    #render the index.html template when the user accesses the form via GET
    return render_template('index.html')


#run the Flask app in debug mode for development purposes or you can run through the terminal first make sure your in the project directory path and type python app.py
if __name__ == '__main__':
    app.run(debug=True)
