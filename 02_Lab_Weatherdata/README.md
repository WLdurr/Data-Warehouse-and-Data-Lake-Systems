### Structure

In this folder, all lambda functions and lambda layers for the Lab that handles weather data import and transfer to all other labs that require this data are listed.

### Extract weather forecast data from Open Meteo
code: 
Lambda export:

### Extract weather historical data from Open Meteo
code: 
Lambda export: 

### Push weather forecast to another s3 bucket (which handles RDS)
code: weather_forecast_to_s3_rds.py
Lambda export: 

### Push weather historic data to another s3 bucket (which handles RDS)
code: weather_historic_to_s3_rds.py
Lambda export:

### Push live flight data to another s3 bucket (which handles RDS)
code: life_flight_to_s3_rds.py
Lambda export: 

### Push historic flight data to another s3 bucket (which handles RDS)
code: historic_flight_to_s3_rds.py
Lambda export:

### Push historic weather data to the Lab that uses SageMaker
code: weather_data_to_sagemaker.py
Lambda export:

### Push forecast weather data to the Lab that uses SageMaker
code: weather_forecast_to_sagemaker.py
Lambda export: 


# 02\_Lab\_Weatherdata/

## File Structure

### `/wrangling`

- **Scripts**:
  - `weather_forecast_import.py`
    - **Functionality**: Fetches live weather data from the API, checks for completeness, transforms data and saves it to s3 bucket. This function is triggered every 3 hours.
    - **Lambda File**: ``
  - `historic_weather_import.py`
    - **Functionality**: Fetches historic weather data for entire 2024, checks for completeness and saves data to s3 bucket. This function was only executed once to get enough data for the model training.
    - **Lambda File**: ``

---


### `/copy`

- **Scripts**:
  - `weather_data_to_sagemaker.py`
    - **Functionality**: Copies the historic weather data to the Lab where sagemaker resides, such that the other student can access the data. This file was manually triggered whenever needed.
    - **Lambda File**: ``
  - `weather_forecast_to_sagemaker.py`
    - **Functionality**: This file transfers forecast data to the sagemaker lab. This was used for testing and development. This function is inactive as of 08.01.2025.
    - **Lambda File**: ``
  - `weather_historic_to_s3_rds.py`
    - **Functionality**: This file transfers data from one lab to another, where the data lake is (s3 to s3). This is needed to not run into credit limitations. 
    - **Lambda File**: ``
  - `weather_forecast_to_s3_rds.py`
    - **Functionality**: This file transfers forecast data from one lab to another (triggered every 3 hours), where the data lake is (s3 to s3). This is needed to not run into credit limitations. 
    - **Lambda File**: ``













