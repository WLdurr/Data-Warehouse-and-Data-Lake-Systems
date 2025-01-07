

# 02\_Lab\_Weatherdata/

Author: Stefan Durrer

## File Structure

- **Scripts**:
  - `live_flight_to_rds.py`
    - **Functionality**: Transforms live aviation data. Loads data into flight_info table in RDS. Checks for unique constraints in RDS (combination of flight_number, airport_iata_code and scheduled_departure_timestamp) and updates if this flight is already present. Inserts if not.
    - **Lambda File**: `drsliveflight-444abf56-77cf-4dc6-b5d4-1e21a1878ec7.zip`
  - `sagemaker_output_to_rds.py`
    - **Functionality**: Loads data from prediciton model into the corresponding table in the RDS.
    - **Lambda File**: `dwlrdsmodeloutput-08400da9-0b99-4228-871b-a42edc0e0b01.zip`
  - `weather_forecast_to_rds.py`
    - **Functionality**: Transforms forecast data (timestamp conversion) ans loads data into the forecast_weather table in the RDS. Checks for duplicates. Updates each existing unique entry and inserts if not already present. Unique constraint is a combination of airport_iata_code and timestamp. 
    - **Lambda File**: `rdsforecastweather-f5a610a4-17f9-4836-821f-563abd82a566.zip`

---

- **Additional Material**:
  - `rds_lambda_layer.zip`
    - **Functionality**: Zipped lambda layer that is needed for all lambda functions responsible for the data transfer from data lake (s3 buckets) to the data warehouse PostgresRDS.
  - `Cloud9 lambda layer.txt`
    - **Functionality**: Cloud 9 Console code for the lambda layer creation in Amazon Linux 2023 environment









