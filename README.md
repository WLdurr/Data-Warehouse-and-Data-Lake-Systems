![Header](ReadmeFiles/Header.png)

# WEATHER BASED DELAY PREDICTION IN AVIATION​

In this project, we set up a data warehouse and data lake system using AWS in the scope of the HSLU M.Sc. in Applied Information and Data Science course. 
The scope is about extracting historical weather and aviation data, training a model which predicts cancellations based on extreme weather events and using this model 
to predict future delays based on airport locations.

## Dashboards
### For each Airport
1. [AMS Amsterdam](https://oliverheisel.grafana.net/public-dashboards/54b39863f0eb4728bfd2971c83a85efb)
2. [CDG Paris](https://oliverheisel.grafana.net/public-dashboards/3e02d6593eb842d7b25438a810b91791)
3. [FRA Frankfurt](https://oliverheisel.grafana.net/public-dashboards/22d72ad0730147e9a34cb91847123919)
4. [LHR London](https://oliverheisel.grafana.net/public-dashboards/026355ddb94649589cef73c6a34f1c07)
5. [ZRH Zürich](https://oliverheisel.grafana.net/public-dashboards/6014e6bbbce04360831691730bf5ee5f)

### Statistics
[Flight Stats](https://oliverheisel.grafana.net/public-dashboards/9ff89ab776034694aa3f512bd5d97d76)

## Architecture
The scripts for each lab can be found in their respective folders. The representation deviates from the actual Lambda function and script, as adjustments were necessary due to the limitations of the labs.

![Architecture Diagram](ReadmeFiles/Architecture2.png)

## How to Import and Run AWS Lambda Functions

To set up the system, follow these sequential steps. This guide will help you import and execute Lambda scripts in your AWS environment.

### Prerequisites
1. Start by downloading all the necessary files from this repository. Each Lambda script is located in one of the following folders:
   - **01_Lab_Flightdata**
   - **02_Lab_Weatherdata**
   - **03_Lab_PredictionModel**
   - **04_Lab_DataLake_DataWarehouse**

   Each folder contains **multiple scripts**. The structure of the scripts and their intended purpose can be found within each folder. It is essential to proceed sequentially through the folders and scripts to set up the system correctly.

### Steps to Import and Run a Lambda Function
1. **Log in to AWS**:
   - Navigate to the **Lambda Console** in your AWS Management Console.

2. **Create a New Lambda Function**:
   - Click on the **"Create Function"** button.
   - Select **"Author from scratch"** and give your function a meaningful name.
   - Choose the **runtime environment** that matches your Lambda script (e.g., Python, Node.js, etc.).

3. **Import the Lambda Script**:
   - In the newly created Lambda function, click on the **"Actions"** button in the upper-right corner.
   - Select **"Import function"** from the dropdown menu.

4. **Upload the Script**:
   - In the import dialog, choose the **ZIP file** of the Lambda function you want to run. Each folder contains ZIP files for the individual scripts. Select the one you want to execute.

5. **Review and Save**:
   - Ensure that all the settings (runtime, permissions, etc.) are correctly configured.
   - Click **"Save"** to import the Lambda function successfully.

6. **Test the Lambda Function**:
   - Navigate to the **Test** tab in the Lambda console.
   - Create a test event and populate it with any required parameters for the function.
   - Click **"Test"** to execute the Lambda function.

7. **Repeat for Other Scripts**:
   - Repeat the steps above for each Lambda script in the repository, ensuring they are executed in the correct sequence:
     1. **01_Lab_Flightdata**: Complete all scripts in this folder first.
     2. **02_Lab_Weatherdata**: Proceed to the scripts in this folder.
     3. **03_Lab_PredictionModel**: Configure services using the scripts in this folder.
     4. **04_Lab_DataLake_DataWarehouse**: Finalize the setup with the scripts in this folder.

### Important Notes
- Each folder contains **multiple scripts** designed for a specific part of the setup process. Review the structure and purpose of the scripts in each folder before proceeding.
- Execute the scripts **sequentially** within each folder to ensure proper configuration.
- Ensure that the necessary **IAM roles and permissions** are assigned to each Lambda function for it to run properly.
- This guide solely explains the successful setup of the lambda functions as we developed them. Make sure to set up additional required services, such as s3, SageMaker and Amazon RDS

By following these steps, you can import and run all Lambda scripts successfully to set up your system.

Happy coding!
