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
        df = pd.read_csv(rawData)

        #cleaning data - checking for missing columns (alert only)
        cols = ['1. open','2. high','3. low','4. close','5. volume']
        logging.info("checking for misisng colums...")
        for col in cols:
            if col not in df.columns:
                logging.error(f"column {col} not found in the data")
                return 
            
        #cleaning data - checking for missing values and dropping the rows 
        logging.info("checking for missing values...")
        missingVal = df.isnull().sum()
        logging.info(f"missing values:\n {missingVal}")
        cleanDf = df.dropna()

        #standardizing format - dates
        if '1. date' in cleanDf.columns:
            logging.info("Standardizing date format...")
            cleanDf.index = pd.to_datetime(cleanDf.index,error = 'coerce')
            cleanDf = cleanDf.dropna(subset=['date'])

        #standardizing format - converting number values to numeric 
        cols = ['1. open','2. high','3. low','4. close','5. volume']
        for col in cols:
            if col in cleanDf.columns:
                logging.info(f"standardizing {col} numeric format")
                cleanDf[col] = pd.to_numeric(cleanDf[col], errors = 'coerce')
                cleanDf = cleanDf.dropna(subset=[col])
        
        #validate data - check for neg price cols 
        logging.info(f"Checking for negative prices...")
        cols = ['1. open','2. high','3. low','4. close','5. volume']
        for col in cols:
            if col in cleanDf.columns:
                cleanDf = cleanDf[cleanDf[col] >= 0]
        
        #validate data - volume outlier 
        logging.info("Checking for outliers in volume...")
        if '5. volume' in cleanDf.columns:
            vol99th = cleanDf['5. volume'].quantile(.99)
            cleanDf = cleanDf[cleanDf['5. volume'] <= vol99th]

        #save data
        os.makedirs(os.path.join('data','processed'), exist_ok=True)
        df.to_csv(os.path.join('data','processed','sp500_processed.csv'))
        logging.info('data processed and saved')
    except Exception as e:
        logging.error(f"Error occured: {e}")
    
# if __name__ == "__main__":
#     # File paths
#     raw_data_path = "data/raw/sp500_raw.csv"  # Path to the raw data CSV
#     cleaned_data_path = "data/processed/sp500_processed.csv"  # Where to save the cleaned data

#     # Run the data processing function
#     processData(raw_data_path, cleaned_data_path)
