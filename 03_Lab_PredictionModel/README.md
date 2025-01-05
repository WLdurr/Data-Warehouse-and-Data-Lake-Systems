This folder contains all the code necessary for generating training data and making predictions in AWS. Below is the structure and description of each file:

## Folder Structure

### `historic_data`

#### `1_transform_weather_data.py`
- **Description**: Transforms weather data by performing tasks such as recoding airport codes into numeric values.

#### `2_send_to_sagemaker_lab.py`
- **Description**: Sends transformed data to the SageMaker lab environment from the data lab.

#### `3_make_prediction_delay.py`
- **Description**: Calls the endpoint of the trained model to make predictions.

#### `4_send_to_data_exchange_lab.py`
- **Description**: Sends prediction data back to the data lab for further processing.

#### `5_send_to_stefans_lab.py`
- **Description**: Transfers data from the data lab to Stefan’s lab environment.
