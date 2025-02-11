import csv
import psycopg2
from dotenv import load_dotenv
import os
import logging 

logging.basicConfig(
    level= logging.INFO,
    format = "%(asctime)s- %(levelname)s - %(message)s",
    handlers = [logging.FileHandler('log/uploadRDS.log'), logging.StreamHandler()] 
)

load_dotenv()

def uploadToRDS(processedFile):
    rdsHost = os.getenv("RDS_HOST")
    rdsPort = os.getenv("RDS_PORT")
    rdsDB = os.getenv("RDS_DB")
    rdsUser = os.getenv("RDS_USER")
    rdsPassword = os.getenv("RDS_PASSWORD")

    try: 
        logging.info("Connecting to RDS")
        connect = psycopg2.connect(
            host = rdsHost,
            port = rdsPort,
            dataBase = rdsDB,
            user = rdsUser,
            password = rdsPassword,
        )
        cursor = connect.cursor()
        
    except Exception as e:
        logging.error("Unexpected error: {e}")