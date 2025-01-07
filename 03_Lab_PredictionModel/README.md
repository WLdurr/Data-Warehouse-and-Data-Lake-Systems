# 03_Lab_PredictionModel/

Author: ankudat

## File Structure

### `/model`

- **Scripts**:
  - `1_transform_weather_data.py`
    - **Functionality**: Transforms weather data by tasks such as recoding airport codes into numeric values.
  - `2_send_to_sagemaker_lab.py`
    - **Functionality**: Transfers transformed data to the Sagemaker lab for predictions.
  - `3_make_prediction_delay.py`
    - **Functionality**: Calls the machine learning model endpoint to make predictions based on input data.
  - `4_send_to_data_exchange_lab.py`
    - **Functionality**: Sends prediction data back to the data lab for storage and further analysis.
  - `5_send_to_stefans_lab.py`
    - **Functionality**: Transfers processed data from the data lab to Stefan's lab.

---

### `/historic_data`

- **Scripts**:
  - `1_create_flight_summary.py`
    - **Functionality**: Calculates average flight delays by airport and date to produce a summarized dataset.
  - `2_transform_weather_data.py`
    - **Functionality**: Transforms weather data (e.g., recoding airport codes into numeric values).
  - `3_merge_flight_weather.py`
    - **Functionality**: Combines flight and weather data into a final dataset used for model training.
