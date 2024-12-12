### Structure

In this folder, all lambda functions and lambda layers for the Lab that handles weather data import and transfer to all other labs that require this data are listed.

### Extract weather forecast data from Open Meteo
code: weather_forecast_import.py
Lambda export:

### Extract weather historical data from Open Meteo
code: historic_weather_import.py
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

