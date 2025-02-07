import os 
import pandas as pd 
import logging

logging.basicConfig(
    level = logging.INFO,
    format = '%{asctime}s - %{levelname}s - %{message}s',
    handler = [logging.FileHandler('cleanData.log'),logging.StreamHandler()]
)
def processData(rawData, cleanedData):
    logging.info(f'loading {rawData}')
    df = pd.read_csv(rawData)

    #missing values