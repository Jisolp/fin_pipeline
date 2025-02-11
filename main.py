from src.fetchData import fetchData
from src.processData import processData
from src.uploadToS3 import uploadToS3
from src.uploadToRDS import uploadToRDS
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log/main.log"), logging.StreamHandler()],
)

if __name__ == '__main__':
    try:
        API_KEY = os.getenv('API_KEY')
        if not API_KEY:
            logging.error("API key not found")
            exit()

        fetchData(API_KEY)

        rawData = os.path.join('data', 'raw', 'sp500_raw.csv')
        cleanData = os.path.join('data','processed','sp500_processed.csv')
        processData(rawData, cleanData)

        bucketName = 'fin-market-data'
        uploadToS3(rawData, bucketName)
        uploadToS3(cleanData, bucketName)

        uploadToRDS(cleanData)
        logging.info("All tasks completed successfully.")

    except Exception as e:
        logging.error(f"Error in processing: {e}")
