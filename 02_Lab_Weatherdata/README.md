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

### Push forecast weather data to the Lab that uses SageMaker
code: weather_forecast_to_sagemaker.py
Lambda export: 


# 01\_Lab\_Flightdata/

## File Structure

### `/live`

- **Scripts**:
  - `01_GetLiveFlightData.py`
    - **Functionality**: Fetches live flight data from the API, checks for completeness, retries if necessary, and triggers `02_CopytoLake`. (Auto-triggered daily.)
    - **Lambda File**: `01_GetLiveFlightData-60921ca1-9128-42c0-b5c3-b158352a0e3d.zip`
  - `02_CopytoLake.py`
    - **Functionality**: Copies the data to the data lake.
    - **Lambda File**: `02_CopytoLake-3cb494c2-2954-48fb-b0bd-816c12253636.zip`

---

### `/historic`

- **Master Trigger**:
  - `01_Master_TriggerFunctions.py`
    - **Functionality**: Triggers sub-functions for each airport and month.
    - **Lambda File**: `01_Master_TriggerFunctions-c1f9de17-6e07-42e0-8ca2-cd76237d9483.zip`

- **Sub Function - Call API**:
  - `02_Sub_GetDataFromApi.py`
    - **Functionality**: Calls the API with required parameters (e.g., `iata_code`, `start_date`, `end_date`).
    - **Lambda File**: `02_Sub_GetDataFromApi-bc990f0b-3b39-4414-bc36-d871b55af458.zip`

- **Validation and Copy Scripts**:
  - `03_Q-Check_S3Bucket.py`
    - **Functionality**: Verifies if all days are present for each `iata` code in the S3 bucket.
    - **Lambda File**: `03_Q-Check_S3Bucket-5d962d01-4bd1-4bb2-a372-72ff687858cd.zip`

  - `04_Q-Check_GetTheMissingOnes.py`
    - **Functionality**: Retriggers `02_Sub_GetDataFromApi` to fetch any missing data.
    - **Lambda File**: `04_Q-Check_GetTheMissingOnes-cd47a82d-c129-4f12-90ec-1a50aeb09b06.zip`

  - `05_CopyData.py`
    - **Functionality**: Copies the retrieved data to the data lake.
    - **Lambda File**: `05_CopyData-91bedf27-7b1a-42af-bd37-764853227fc3.zip`

