This folder contains all the code necessary for generating training data and making predictions in AWS. Below is the folder structure with a brief description of each file.

---

## Folder Structure

### **model**

Files related to preprocessing and managing data in the data lab.

- **`1_transform_weather_data.py`**  
  Transforms weather data by tasks like recoding airport codes into numeric values.

- **`2_send_to_sagemaker_lab.py`**  
  Transfers transformed data to the Sagemaker lab for prediction.

- **`3_make_prediction_delay.py`**  
  Calls the machine learning model endpoint to make predictions based on input data.

- **`4_send_to_data_exchange_lab.py`**  
  Sends prediction data back to the data lab for storage.

- **`5_send_to_stefans_lab.py`**  
  Transfers data from the data lab to Stefan's lab.

---

### **historic_data**

Files related to generating summarized datasets and preparing data for training.

- **`1_create_flight_summary.py`**  
  Calculates average flight delays by airport and date, producing a summarized dataset.

- **`2_transform_weather_data.py`**  
  Transforms weather data, e.g. recoding airport codes into numeric values.

- **`3_merge_flight_weather.py`**  
  Combines flight data with weather data to create the final dataset used for model training.
  
---
