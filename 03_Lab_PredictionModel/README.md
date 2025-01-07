# 03_Lab_PredictionModel/

Author: ankudat

## File Structure

### `/model`

- **Scripts**:
  - `1_transform_weather_data.py`
    - **Functionality**: Transforms weather data by tasks such as recoding airport codes into numeric values.
    - **Lambda File**: `transformweatherdata-9320ce95-6319-4106-985f-50be63716fa7.zip`
  - `2_send_to_sagemaker_lab.py`
    - **Functionality**: Transfers transformed data to the Sagemaker lab for predictions.
    - **Lambda File**: `sendtosagemakerlab-b72df576-f1e3-43aa-8957-3ddd08c0ebb3.zip`
  - `3_make_prediction_delay.py`
    - **Functionality**: Calls the machine learning model endpoint to make predictions based on input data.
    - **Lambda File**: `makepredictiondelay-690d4014-83fc-49b1-8a8a-cdc8455dfa87.zip`
  - `4_send_to_data_exchange_lab.py`
    - **Functionality**: Sends prediction data back to the data lab for storage and further analysis.
    - **Lambda File**: `sendprediction-46156be5-0e90-4095-bb2f-58119a67665e.zip`
  - `5_send_to_stefans_lab.py`
    - **Functionality**: Transfers processed data from the data lab to Stefan's lab.
    - **Lambda File**: `sendtostefans_lab-62229e34-d9e5-4308-9716-205b6a5278b6.zip`

---

### `/historic_data`

- **Scripts**:
  - `1_create_flight_summary.py`
    - **Functionality**: Calculates average flight delays by airport and date to produce a summarized dataset.
  - `2_transform_weather_data.py`
    - **Functionality**: Transforms weather data (e.g., recoding airport codes into numeric values).
  - `3_merge_flight_weather.py`
    - **Functionality**: Combines flight and weather data into a final dataset used for model training.
