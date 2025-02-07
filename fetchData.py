import requests
import pandas as pd 
import os 
import datetime as datetime
import logging 
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level= logging.INFO,
    format = "%(asctime)s- %(levelname)s - %(message)s",
    handlers = [logging.FileHandler('app.log'), logging.StreamHandler()] 
)

def fetchData(apikey, function = 'TIME_SERIES_DAILY', symbol='SPY'):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}'
    logging.info(f"Initalizaing request to {url}")
    print(f"Initalizaing request to {url}")
    try:
        response = requests.get(url)
        logging.info(f"API reponse status code: {response.status_code} at {datetime.datetime.now()}")

        if response.status_code == 200:
            data = response.json()

            if 'Time Series (Daily)' in data:
                df = pd.DataFrame.from_dict(data['Time Series (Daily)'],orient = 'index')
                df = df.apply(pd.to_numeric)
                df.index = pd.to_datetime(df.index)

                #save data to csv 
                os.makedirs(os.path.join('data','raw'), exist_ok=True)
                df.to_csv(os.path.join('data','raw','sp500_raw.csv'))

                logging.info('data fetched and saved')
            else:
                logging.error(f"Error in getting data: {data.get('Error Message')}")
        else:
            logging.error(f"Failed at getting API request. Status Code: {response.status_code}")

    except requests.RequestException as e:
        logging.error(f"Request error:{e}")
    except Exception as e:
        logging.error(f"Unexpected error:{e}")
    
# if __name__ == '__main__':
#     API_KEY = os.getenv('API_KEY')
#     if not API_KEY:
#         logging.error("API key not found")
#         exit()
#     fetchData(API_KEY)


