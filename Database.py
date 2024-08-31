import sqlite3
import logging
from contextlib import closing

#set up logging, already done in the API.py but just to make sure it works.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherDatabase:
    def __init__(self, db_name='new_weather_data.db'):
        #initialize the database connection and create the weather table if it doesn't exist.
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        #create the weather table if it doesn't already exist.
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                cursor = conn.cursor()  #create the cursor within the context
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        state TEXT,
                        country TEXT NOT NULL,
                        temperature REAL,
                        feels_like REAL,
                        pressure REAL,
                        humidity REAL,
                        low REAL,
                        high REAL,
                        wind_speed REAL,
                        wind_deg REAL,
                        description TEXT,
                        category TEXT,
                        units TEXT,
                        rate_limiting_unique_lookups_remaining INTEGER,
                        rate_limiting_lookup_reset_window TEXT,
                        date_time TEXT NOT NULL
                    )
                ''')
                conn.commit()  #commit the changes to the database
                logging.info("Weather table created or verified successfully.")
                #handling database specific errors and any unexpected error
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while creating the table: {e}")

    def insert_weather_data(self, weather_info):
        #insert parsed weather data into the database.
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO weather (city, state, country, temperature, feels_like, pressure, humidity,
                                         low, high, wind_speed, wind_deg, description, category, units,
                                         rate_limiting_unique_lookups_remaining, rate_limiting_lookup_reset_window, date_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    weather_info['city'],
                    weather_info['state'],
                    weather_info['country'],
                    weather_info['temperature'],
                    weather_info['feels_like'],
                    weather_info['pressure'],
                    weather_info['humidity'],
                    weather_info['low'],
                    weather_info['high'],
                    weather_info['wind_speed'],
                    weather_info['wind_deg'],
                    weather_info['description'],
                    weather_info['category'],
                    weather_info['units'],
                    weather_info['rate_limiting_unique_lookups_remaining'],
                    weather_info['rate_limiting_lookup_reset_window'],
                    weather_info['date_time']
                ))
                conn.commit()  # Commit the insert operation
                logging.info(f"Weather data for {weather_info['city']} inserted successfully into the database.")

                #handling database specific errors and any unexpected error during the insertion


        except sqlite3.Error as e:
            logging.error(f"Error inserting data: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while inserting data: {e}")


        #close the database connection
    def close(self):
        pass
