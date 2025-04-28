# Data Engineering Project: Dynamic Data Pipeline with Airflow and BigQuery

## Overview
This project implements a dynamic data pipeline using Apache Airflow, Google Cloud Storage (GCS), and BigQuery. The pipeline performs the following tasks:
1. Uploads CSV files from a local directory to a GCS bucket.
2. Loads the CSV data into BigQuery.
3. Creates country-specific tables and views based on the data.
4. Provides a reporting layer for countries with specific health data.

Additionally, the project integrates with **Power BI** for visualizing the data via dynamically created views in BigQuery.

The project uses a set of Bash and Python scripts to automate these tasks.




## Project Description
This project automates the ETL pipeline for health data:
1. **Upload CSV Files**: Local CSV files are uploaded to Google Cloud Storage.
2. **Load Data into BigQuery**: The data is loaded into BigQuery from GCS.
3. **Dynamic Table Creation**: The pipeline extracts unique country names from the data and creates country-specific tables and views in BigQuery.
4. **Health Data Reporting**: A Power BI dashboard connects to the BigQuery views to visualize health data for countries.


## Project Structure

- **`full_deployment.sh`**: A Bash script that automates the full deployment process, including uploading files to GCS and setting up Airflow.
- **`deploy_airflow.sh`**: A Bash script that installs Apache Airflow, sets up the environment, and deploys the Airflow DAG.
- **`create_table_dag.py`**: The Airflow DAG script that defines the data pipeline for uploading data to BigQuery, creating country-specific tables, and generating views based on the data.
- **`local_to_gcp_bucket.py`**: A Python script that uploads CSV files from a local directory to GCS.


## Technologies Used
- **Apache Airflow**: Orchestrates the ETL pipeline.
- **Google Cloud Platform (GCP)**: Includes GCS for file storage and BigQuery for data processing.
- **Python**: Used for scripting and task management.
- **Power BI**: For reporting and data visualization.
- **Google Cloud SDK**: For interacting with Google Cloud services.

## Prerequisites

Before running the project, ensure that you have the following prerequisites set up:

### 1. Google Cloud Platform (GCP) Account
- You need a GCP account with access to **Google Cloud Storage (GCS)** and **BigQuery**.

### 2. Python 3.x
- Ensure that **Python 3.x** is installed on your system.

### 3. Apache Airflow
- **Apache Airflow** should be installed or ready to be deployed.

### 4. Google Cloud SDK
- Ensure you have **Google Cloud SDK** installed and authenticated on your machine.

```bash
gcloud auth application-default login
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-directory>
```

### 2. Install Dependencies

- **Create a Virtual Environment**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Install Required Python Packages**:
  ```bash
  pip install -r requirements.txt
  ```

- **Ensure Google Cloud SDK is Installed**:
  Follow the instructions here: https://cloud.google.com/sdk/docs/install

- **Authenticate with Google Cloud**:
  ```bash
  gcloud auth application-default login
  ```

- **Set Your GCP Project** (if necessary):
  ```bash
  gcloud config set project <your-project-id>
  ```



## Running the Project

To run the entire data pipeline, execute the `full_deployment.sh` script. This script automates the entire process, including uploading files, setting up Airflow, and executing the data pipeline.

### 1. Run the Deployment Script

```bash
bash full_deployment.sh
```

### What Happens When You Run `full_deployment.sh`

The `full_deployment.sh` script handles the entire deployment process automatically. Here’s a step-by-step breakdown of what happens when you run the script:

#### **1. Upload Local Files to GCS**
- The script runs the `local_to_gcp_bucket.py` script, which uploads CSV files from the local directory to the GCS bucket specified in the script. It looks for files that match the current date and uploads them to the `uploads` folder in the bucket.

#### **2. Wait for Upload to Complete**
- The script waits for 10 minutes to ensure that the file upload to GCS completes before continuing to the next steps.

#### **3. Fix Line Endings for `deploy_airflow.sh`**
- The script uses the `dos2unix` utility to fix any line ending issues with the `deploy_airflow.sh` script, ensuring that it works properly on Linux-based systems.

#### **4. Set Permissions for `deploy_airflow.sh`**
- The script ensures that the `deploy_airflow.sh` script is executable by changing its file permissions.

#### **5. Deploy Airflow and Set Up DAG**
- The script runs `deploy_airflow.sh`, which installs Apache Airflow, sets up a virtual environment, and deploys the Airflow DAG (`create_table_dag.py`).
  - **Airflow** is configured to run as a standalone service.
  - The script installs necessary dependencies (including Google Cloud SDK).
  - The DAG is deployed to the Airflow instance.

#### **6. Run the DAG**
- The Airflow DAG (`create_table_dag.py`) is responsible for:
  - Loading data from GCS into BigQuery.
  - Creating country-specific tables and views in BigQuery based on the uploaded data.
  - The DAG will automatically trigger when the file upload completes and will start processing the data.



## Airflow UI

Once the deployment completes, you can access the Airflow UI at:

```
http://localhost:8080
```

Here, you can monitor the status of your DAG, view logs, and manually trigger the DAG if needed.


## Troubleshooting

### 1. **Airflow Setup Issues**
- If Airflow is not starting properly, check the logs in the `airflow.log` file or visit the Airflow UI at `http://localhost:8080`.

### 2. **CSV File Not Uploading to GCS**
- Ensure that the local directory path and GCS bucket path are correctly configured in `local_to_gcp_bucket.py`.

### 3. **Permission Issues**
- Make sure that the GCP service account or user running the scripts has the necessary permissions for accessing GCS and BigQuery.


## License

This project is licensed under the MIT License.
