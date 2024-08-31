# WeatherAPI Project

## Getting Started

### 1. Download and Install Python
- Download the latest version of Python from the official [Python website](https://www.python.org/downloads/).
- During installation, make sure to remember the installation path of Python. It’s recommended to create a dedicated folder on your system for Python, such as `C:\Python\` or `D:\Python\`, and install Python there.

### 2. Install PyCharm
- Download and install [PyCharm](https://www.jetbrains.com/pycharm/download/) for your development environment.
- After installation, open PyCharm and create a new project or open the `WeatherAPI` project.
- Set the Python interpreter to the Python installation path you specified earlier. This can be done in `Settings` > `Project: WeatherAPI` > `Python Interpreter`.

### 3. Set Up the Database (Optional)
- If you need to view or manage the database, you can download [DB Browser for SQLite](https://sqlitebrowser.org/).
- Open DB Browser and navigate to the project directory.
- Select the `new_weather_data.db` file to open the database.
- Browse the tables, particularly the `weather` table, to view the stored weather data.

### 4. Install Project Dependencies
- The project dependencies are listed in the `requirements.txt` file that has been committed to the repository.
- To install the required dependencies, open your terminal and navigate to the project directory.
- Run the following command to install all the dependencies:

```bash
pip install -r requirements.txt
