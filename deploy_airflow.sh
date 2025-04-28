#!/bin/bash

set -e
echo "🚀 Starting Airflow setup..."

# 1. Install dependencies
sudo apt update
sudo apt install -y software-properties-common

# 2. Add deadsnakes PPA for Python 3.8
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# 3. Install Python 3.8 and required packages
sudo apt install -y python3.8 python3.8-venv python3.8-distutils python3.8-dev

# 4. Set up virtual environment
python3.8 -m venv ~/airflow-env
source ~/airflow-env/bin/activate

# 5. Install Google Cloud SDK if not present
if ! command -v gcloud &> /dev/null; then
  echo "📦 Installing Google Cloud SDK..."
  sudo apt install -y apt-transport-https ca-certificates gnupg
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" |
    sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |
    sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
  sudo apt update && sudo apt install -y google-cloud-sdk
fi

# 6. Authenticate with GCP
echo "🔐 Authenticating with GCP..."
gcloud auth application-default login --no-launch-browser

# 7. (Optional) Set GCP project
gcloud config set project double-genius-456516-g6

# 8. Install Airflow with GCP extras
AIRFLOW_VERSION=2.7.3
PYTHON_VERSION=3.8
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install --upgrade pip
pip install "apache-airflow[gcp]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
export AIRFLOW__CORE__LOAD_EXAMPLES=False


# 9. Start Airflow
nohup airflow standalone > airflow.log &

# 10. Wait for Airflow to start
sleep 30

# 11. Deploy your DAG
mkdir -p ~/airflow/dags
echo "📄 Copying your DAG file to Airflow DAGs directory..."
cp ./create_table_dag.py ~/airflow/dags/

echo "✅ Airflow setup complete! Access it on http://localhost:8080"
