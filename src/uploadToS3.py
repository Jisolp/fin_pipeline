import boto3
import logging 
import datetime 
# from fetchData import fetchData
import os
from dotenv import load_dotenv

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handler = [logging.FileHandler('app.log'),logging.StreamHandler()]
)
def uploadToS3(fileName, bucketName, objectName = None):
    s3Client = boto3.client('s3')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    if objectName is None:
        dataType = os.path.basename(os.path.dirname(fileName))
        objectName = f"{dataType}/{timestamp}"
    try:
        s3Client.upload_file(fileName,bucketName,objectName)
        logging.info(f"uploaded {fileName} to {bucketName}/{objectName}")
    except Exception as e:
        logging.info(f"Error uploading: {e}")


# if __name__ == '__main__':
#     API_KEY = os.getenv('API_KEY')
#     if not API_KEY:
#         logging.error("API key not found")
#         exit()
#     fetchData(API_KEY)
#     bucketName = 'fin-market-data'
#     rawData = os.path.join('data', 'raw', 'sp500_raw.csv')
#     processData = os.path.join('data','processed','sp500_processed.csv')
    
#     uploadToS3(rawData, bucketName)
#     uploadToS3(processData, bucketName)
