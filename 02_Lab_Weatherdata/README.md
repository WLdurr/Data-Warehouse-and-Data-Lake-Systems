

# 02\_Lab\_Weatherdata/

Author: Stefan Durrer

## File Structure

### `/wrangling`

- **Scripts**:
  - `weather_forecast_import.py`
    - **Functionality**: Fetches live weather data from the API, checks for completeness, transforms data and saves it to s3 bucket. This function is triggered every 3 hours.
    - **Lambda File**: `forecastimport-1c3babbc-fbc1-40f9-8c91-5a87ae27abeb.zip`
  - `historic_weather_import.py`
    - **Functionality**: Fetches historic weather data for entire 2024, checks for completeness and saves data to s3 bucket. This function was only executed once to get enough data for the model training.
    - **Lambda File**: `weatherimport-f176959c-6732-40f3-a462-5092f9a9b4d9.zip`

---


### `/copy`

- **Scripts**:
  - `weather_data_to_sagemaker.py`
    - **Functionality**: Copies the historic weather data to the Lab where sagemaker resides (Lab 03), such that the other student can access the data. This file was manually triggered whenever needed.
    - **Lambda File**: `copyhistoricweather-9de0cc8b-1756-4602-9860-30f0171cb11a.zip`
  - `weather_forecast_to_sagemaker.py`
    - **Functionality**: This file transfers forecast data to the sagemaker lab (Lab 03). This was used for testing and development. This function is inactive as of 08.01.2025.
    - **Lambda File**: `copyweatherforecast-cf9134ce-3bf4-44e6-a4fc-6e059e5f4d4c.zip`
  - `weather_historic_to_s3_rds.py`
    - **Functionality**: This file transfers data from one lab to another, where the data lake is (s3 to s3) (Lab 04). This is needed to not run into credit limitations. 
    - **Lambda File**: `weatherhistorictords-8644d030-4b17-4f70-9e56-d4a214be9791.zip`
  - `weather_forecast_to_s3_rds.py`
    - **Functionality**: This file transfers forecast data from one lab to another (triggered every 3 hours), where the data lake is (s3 to s3) (Lab 04). This is needed to not run into credit limitations. 
    - **Lambda File**: `weatehrforecasttords-2200c9ae-91e3-4485-9d58-8f833b29d7c4.zip`
  - `life_flight_to_s3_rds.py`
    - **Functionality**: From Lab 01, live aviation data is transferred to Lab 02, to avoid credit limitations. This function transfers the live aviation data to the data lake in Lab 04.
    - **Lambda File**: `flightlivetords-f77e9d7b-74fc-4e9a-abea-5b1980adc9cb.zip`
  - `historic_flight_to_s3_rds.py`
    - **Functionality**: From Lab 01, historic aviation data is transferred to Lab 02, to avoid credit limitations. This function transfers the historic aviation data to the data lake in Lab 04.
    - **Lambda File**: `historicflighttords-757300d8-71d7-4af5-8aab-4a98152e56fa.zip`

---

- `cloud9 lambda layer.txt`
  - **Functionality**: This text file contains all commands used in the AWS EC2 Cloud9 instance (Linux 2023 environment) that have been used to create the custom lambda layer for the scripts in the folder /wrangling.
  - **ANNOTATION**: The zip-file of the entire lambda layer needed for the data wrangling is 64MB. Github does not allow an Upload of files larger than 50MB. Upon request, a zipped file of the lambda layer can be provided. With the guide in `cloud9 lambda layer.txt` however, the creation of an identical layer should be possible. 











