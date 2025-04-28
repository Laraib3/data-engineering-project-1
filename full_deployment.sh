#!/bin/bash

set -e
echo "🚀 Starting Full Deployment Script..."

# 1. Upload local file to GCP Bucket
echo "📤 Uploading local file to GCP bucket..."
python3 local_to_gcp_bucket.py

# 2. Fancy Countdown Timer for 10 minutes (600 seconds)
echo "⏳ Waiting 10 minutes to ensure file upload completes..."
SECONDS_LEFT=600

while [ $SECONDS_LEFT -gt 0 ]; do
    MINS=$((SECONDS_LEFT / 60))
    SECS=$((SECONDS_LEFT % 60))
    printf "\r⏳ Time left: %02d:%02d" $MINS $SECS
    sleep 1
    SECONDS_LEFT=$((SECONDS_LEFT - 1))
done
echo -e "\n✅ Wait complete!"

# 3. Fix line endings on deploy_airflow.sh
echo "🧼 Fixing line endings on deploy_airflow.sh..."
sudo apt update && sudo apt install -y dos2unix
dos2unix deploy_airflow.sh

# 4. Make deploy_airflow.sh executable
chmod +x deploy_airflow.sh

# 5. Run deploy_airflow.sh
echo "🚀 Running Airflow deployment script..."
./deploy_airflow.sh

echo "✅ Full Deployment Complete!"
