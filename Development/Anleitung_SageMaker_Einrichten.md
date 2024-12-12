# Amazon SageMaker

- This service can assume the `LabRole` IAM role.
- You can create SageMaker Notebook instances.
  - Supported notebook instance types: medium, large, and xlarge only.
  - GPU instance types are not supported.
  - Maximum SageMaker Notebooks: 2
  - Maximum SageMaker Apps: 2

## To create a SageMaker domain:
1. Choose **Domains** and then choose **Create domain**.
2. Choose **Set up for organizations** and choose **Set up**.
   - **Step 1**: Domain details
     - For *How would you describe the domain*, give the domain a name.
   - **Step 2**: Users and ML Activities
     - For *How do you want to access studio*, choose *Login through IAM*.
     - Leave *Who will use SageMaker* blank.
     - For *What ML activities users will perform*, choose *Use an existing role*.
     - Set the Default execution role to `LabRole`.
   - **Step 3**: Applications
     - For *StageMaker Studio*, choose *SageMaker Studio - New*.
     - In the **Canvas** panel, choose *Configure Canvas*.
     - In the **Time series forecasting configuration** panel towards the bottom, either disable the feature or, if you leave it enabled, choose *Use an existing role* and choose `LabRole`.
     - In the **Canvas Ready-to-use models configuration** panel, choose *Use an existing execution role*. Set the *Execution role name* to *Use an existing execution role*. Set the *Custom IAM role ARN* to the ARN of `LabRole`.  
       **Tip**: You can find the ARN for `LabRole` in the IAM console. It will be in the format `arn:aws:iam::ACCOUNT-ID:role/LabRole` where `ACCOUNT-ID` is your actual AWS account ID.
   - **Step 4**: Network
     - Choose either *VPC only* or *Public internet access*. Select an existing VPC and one or more existing subnets.  
       **Tip**: For a simpler notebook access configuration, users often find it helpful to choose *Public internet access* and to specify at least two subnets.
   - **Step 5**: Accept the default storage settings and choose **Next**.
   - **Step 6**: In the *Review and create* screen, choose **Submit**.
3. Wait for the domain to be created. It typically takes 5 to 8 minutes to complete. Refresh the browser tab occasionally to know when it has completed.

## To create a SageMaker user profile:
1. In the list of SageMaker domains, choose the name link of the domain you created.
2. In the **User profiles** tab, choose **Add user**.
3. In **General settings**, for *Execution role*, choose `LabRole` and then choose **Next**.
4. In **Step 2**, choose **Next**.
5. In **Step 3**, choose **Next**.
6. In **Step 4**:
   - In the **Canvas Ready-to-use models configuration** panel:
     - Choose *Use an existing execution role*. Set the *Execution role name* to *Enter a custom IAM role ARN*. Set the *Custom IAM role ARN* to the ARN of `LabRole`.  
       **Tip**: You can find the ARN for `LabRole` in the IAM console. It will be in the format `arn:aws:iam::ACCOUNT-ID:role/LabRole` where `ACCOUNT-ID` is your actual AWS account ID.
     - Turn off *Enable time series forecasting*.
     - Choose **Submit**.

## Notes:
- There is limited support for SageMaker Studio features. Some SageMaker JumpStart projects require more access permissions than can be granted in Learner Labs.
  - To use SageMaker Studio, first create a SageMaker domain and user profile (steps documented above).
  - Once you have a domain and user profile, choose **Studio**. Then, from the **Applications** list in the top left corner, choose an application.
    - For example, choose **JupyterLab** and then choose **Create JupyterLab space**. Give the space a name and choose **Create space**. Then choose **Run space**. Wait for the JupyterLab space to start, then choose **Open JupyterLab**. Once in the JupyterLab UI, you can launch a notebook, console, or other type of resource.
  - If you have a running studio space, it will appear as a running *App* in the SageMaker Studio console.

- There is limited support for SageMaker Canvas features. Many SageMaker Canvas models (including many Ready-to-use models) are not supported in Learner Labs. For example, if a model is "powered by" an AWS service that is not supported in Learner Labs, the model will not run in Learner Labs.
  - To use SageMaker Canvas, first create a SageMaker domain and user profile (see the steps above).
  - Once you have a domain and user profile, from the **User profiles** list, in the row with the profile you want to use, choose **Launch > Canvas**. The SageMaker Canvas console appears.

## Tips to preserve your budget:
- Choose the **SageMaker dashboard** link to view recent activity, including running jobs, models, or instances. Stop or delete anything that is running and that you no longer need.
- When your session ends, the lab environment may place running SageMaker notebook instances into a 'stopped' state. Stopped SageMaker notebook instances will not be automatically restarted when you start a new session.
- When using SageMaker Canvas or SageMaker Studio, log out of the session when you are done working with it. Consider deleting SageMaker Canvas and SageMaker Studio apps that are no longer needed.
