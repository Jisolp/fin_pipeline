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

def createDB(connect, dbName):
    cursor = connect.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (dbName,))
    if cursor.fetchone():
        logging.info(f"Database {dbName} already exists")
    else:
        cursor.execute(f"CREATE DATABASE {dbName};")
        connect.commit()
        logging.info(f"Database {dbName} created")

#creates table if it doesn't exist 
def createTable(cursor,tableName):
    makeCreateTable = f"""
    CREATE TABLE IF NOT EXISTS {tableName} (
        id SERIAL PRIMARY KEY, 
        date DATE, 
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        volume NUMERIC
    );
    """
    cursor.execute(makeCreateTable)
    logging.info(f"Table {tableName} exists")

#uploads the processed data to RDS
def uploadToRDS(processedFile):
    rdsHost = os.getenv("RDS_HOST")
    rdsPort = os.getenv("RDS_PORT")
    rdsUser = os.getenv("RDS_USER")
    rdsPassword = os.getenv("RDS_PASSWORD")
    rdsDB = "fin_db"

    connect, cursor = None, None

    try: 
        logging.info("Connecting to RDS")
        connect = psycopg2.connect(
            host = rdsHost,
            port = rdsPort,
            dbname = "postgres",
            user = rdsUser,
            password = rdsPassword,
        )
        connect.set_session(autocommit=True) 
        cursor = connect.cursor()
        createDB(connect,rdsDB)
        logging.info(f"Connected to {rdsDB}")
        connect.close()
        cursor.close()

        #reconnect with the db name
        connect = psycopg2.connect(
            host = rdsHost,
            port = rdsPort,
            dbname = rdsDB,
            user = rdsUser,
            password = rdsPassword,
        )
        cursor = connect.cursor()

        table_name = "financial_table"
        createTable(cursor,table_name)

        with open(processedFile, mode = 'r') as csvFile:
            reader = csv.reader(csvFile)
            header = next(reader)

            insertQuery = f"INSERT INTO {table_name}({', '.join(header)}) VALUES ({', '.join(['%s'] * len(header))})"

            logging.info(f"SQL insert query prepared: {insertQuery}")

            for row in reader: 
                cursor.execute(insertQuery, row)
        connect.commit()
        logging.info(f"Data from {processedFile} loaded to RDS table {table_name}")


    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    finally:
        if connect:
            cursor.close()
            connect.close()
            logging.info("RDS connection closed")

# if __name__ == '__main__':
#     processedFile = "data/processed/sp500_processed.csv"
#     uploadToRDS(processedFile)