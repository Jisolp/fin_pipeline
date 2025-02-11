import os 
import pandas as pd 
import logging

logging.basicConfig(
    level= logging.INFO,
    format = "%(asctime)s- %(levelname)s - %(message)s",
    handlers = [logging.FileHandler('cleanData.log'), logging.StreamHandler()] 
)
def processData(rawData, cleanedData):
    try: 
        logging.info(f'loading {rawData}...')
        df = pd.read_csv(rawData, index_col = None)
        df.columns = ["date", "open", "high", "low", "close", "volume"]

        #cleaning data - checking for missing columns (alert only)
        cols = ["open", "high", "low", "close", "volume"]
        logging.info("Checking for misisng colums...")
        for col in cols:
            if col not in df.columns:
                logging.error(f"Column {col} not found in the data")
                return 
            
        #cleaning data - checking for missing values and dropping the rows 
        logging.info("Checking for missing values...")
        missingVal = df.isnull().sum()
        logging.info(f"Missing values:\n {missingVal}")
        cleanDf = df.dropna()

        #standardizing format - dates
        if '1. date' in cleanDf.columns:
            logging.info("Standardizing date format...")
            cleanDf['date'] = pd.to_datetime(cleanDf.index,error = 'coerce')
            cleanDf['date'] = cleanDf.dropna(subset=['date'])

        #standardizing format - converting number values to numeric 
        cols = ["open", "high", "low", "close", "volume"]
        for col in cols:
            if col in cleanDf.columns:
                logging.info(f"Standardizing {col} numeric format")
                cleanDf[col] = pd.to_numeric(cleanDf[col], errors = 'coerce')
                cleanDf = cleanDf.dropna(subset=[col])
        
        #validate data - check for neg price cols 
        logging.info(f"Checking for negative prices...")
        cols = ["open", "high", "low", "close", "volume"]
        for col in cols:
            if col in cleanDf.columns:
                cleanDf = cleanDf[cleanDf[col] >= 0]
        
        #validate data - volume outlier 
        logging.info("Checking for outliers in volume...")
        if 'volume' in cleanDf.columns:
            vol99th = cleanDf['volume'].quantile(.99)
            cleanDf = cleanDf[cleanDf['volume'] <= vol99th]

        #save data
        os.makedirs(os.path.join('data','processed'), exist_ok=True)
        df.to_csv(os.path.join('data','processed','sp500_processed.csv'),index=False)
        logging.info('data processed and saved')
    except Exception as e:
        logging.error(f"Error occured: {e}")
    
# if __name__ == "__main__":
#     # File paths
#     raw_data_path = "data/raw/sp500_raw.csv"  # Path to the raw data CSV
#     cleaned_data_path = "data/processed/sp500_processed.csv"  # Where to save the cleaned data

#     # Run the data processing function
#     processData(raw_data_path, cleaned_data_path)
