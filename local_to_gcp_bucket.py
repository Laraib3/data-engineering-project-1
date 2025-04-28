import os
import time
import datetime
from google.cloud import storage
import pytz


# === CONFIGURATION ===
WATCH_FOLDER = "/mnt/c/Users/Laraib/Data-Engineering-Project-1"
BUCKET_NAME = "data-engineering-project-11"
DESTINATION_PREFIX = "uploads"

# Initialize GCS client
storage_client = storage.Client()

# Get today's date string
def today_date_str():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d")

# Check if file is readable (not locked)
def is_file_ready(filepath):
    try:
        with open(filepath, "rb"):
            return True
    except (PermissionError, OSError):
        return False

# Upload file to GCS
def upload_to_gcs(local_file_path):
    filename = os.path.basename(local_file_path)
    blob_path = f"{DESTINATION_PREFIX}/{filename}"
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_path)

    if is_file_ready(local_file_path):
        blob.upload_from_filename(local_file_path)
        print(f"✅ Uploaded: {local_file_path} → gs://{BUCKET_NAME}/{blob_path}")
    else:
        print(f"❌ File not ready: {local_file_path}")

# Upload existing files only
def upload_existing_files():
    print("🔎 Scanning existing files...")
    print(today_date_str())
    for file in os.listdir(WATCH_FOLDER):
        if file.endswith(".csv") and today_date_str() in file:
            full_path = os.path.join(WATCH_FOLDER, file)
            print(f"📄 Found existing file: {file}")
            upload_to_gcs(full_path)

if __name__ == "__main__":
    upload_existing_files()
    print("✅ All files uploaded! Exiting...")
