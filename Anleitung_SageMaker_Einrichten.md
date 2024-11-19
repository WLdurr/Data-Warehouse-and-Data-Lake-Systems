# Amazon SageMaker Setup Guide

Source: https://awsacademy.instructure.com/courses/94424/modules/items/8706643

## Overview
Amazon SageMaker allows users to create and manage machine learning models and applications. This guide covers basic steps to set up SageMaker Notebook instances, domains, and user profiles in a controlled environment.

---

## SageMaker Permissions and Roles
- This service assumes the **LabRole** IAM role.
- Maximum limits:
  - **SageMaker Notebooks**: 2
  - **SageMaker Apps**: 2
- Supported notebook instance types:
  - `medium`, `large`, and `xlarge`
  - **GPU instance types** are not supported.

---

## Creating a SageMaker Notebook Instance
1. Navigate to the **SageMaker console**.
2. Choose **Notebook Instances** and click **Create notebook instance**.
3. Select one of the supported instance types: `medium`, `large`, or `xlarge`.
4. Assign the **LabRole** IAM role to the notebook instance.
5. Click **Create notebook instance**.

---

## Creating a SageMaker Domain
1. Go to the **Domains** section in the SageMaker console.
2. Click **Create domain**.
3. Choose **Set up for organizations** and then click **Set up**.

### Step-by-Step Configuration
1. **Step 1: Domain details**
   - Give the domain a name.
2. **Step 2: Users and ML Activities**
   - Select **Login through IAM** for accessing Studio.
   - Leave **Who will use SageMaker** blank.
   - For **ML activities**, choose **Use an existing role** and set the **Default execution role** to **LabRole**.
3. **Step 3: Applications**
   - Select **SageMaker Studio - New**.
   - Configure **Canvas** settings as needed.
     - For time series forecasting, either disable the feature or set to use an existing role.
   - Set the **Custom IAM role ARN** for **Canvas Ready-to-use models** to the **ARN of LabRole**.
4. **Step 4: Network**
   - Choose **VPC only** or **Public internet access**.
   - Select an existing VPC and at least two subnets.
5. **Step 5: Storage Settings**
   - Accept the default storage settings.
6. **Step 6: Review and Create**
   - Click **Submit**.

> Note: Domain creation may take 5-8 minutes.

---

## Creating a SageMaker User Profile
1. Navigate to the list of **SageMaker domains** and select the domain name.
2. In the **User profiles** tab, click **Add user**.
3. In **General settings**, set the **Execution role** to **LabRole** and click **Next**.
4. Proceed through **Steps 2** and **3** by clicking **Next**.
5. **Step 4 Configuration**:
   - For **Canvas Ready-to-use models**, set **Execution role name** to enter a custom IAM role ARN and provide the **LabRole** ARN.
   - Disable **Time series forecasting**.
6. Click **Submit**.

---

## Using SageMaker Studio and Canvas
### SageMaker Studio
1. Create a **SageMaker domain** and **user profile** as described above.
2. Choose **Studio** from the **Applications list** and select an application (e.g., **JupyterLab**).
3. Create and run a **JupyterLab space** to launch notebooks, consoles, or other resources.

### SageMaker Canvas
1. Create a **SageMaker domain** and **user profile**.
2. From the **User profiles** list, select the desired profile and click **Launch > Canvas**.

> Note: Some SageMaker Canvas models, especially those requiring services unsupported by **Learner Labs**, may not be available.

---

## Budget Preservation Tips
- Use the **SageMaker dashboard** to view recent activities and stop/delete unused instances.
- SageMaker notebook instances in a **stopped** state will not automatically restart when starting a new session.
- Log out from **SageMaker Studio** and **Canvas** when done.
- Consider deleting unused **SageMaker apps** to conserve resources.

---

For more information, visit the [AWS Documentation](https://aws.amazon.com/sagemaker/).
