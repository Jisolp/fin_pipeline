# Financial Data Pipeline

This project is a pipeline for fetching, processing, and uploading financial data to AWS services including S3 and RDS. It automates the process of gathering financial data from Alpha Vantage, processing it, and storing it in AWS services for further analysis and visualization with AWS QuickSight.

## Tech Stack

The following technologies were used in this project:

- **Python**: The main programming language for scripting and data manipulation.
- **AWS S3 (Simple Storage Service)**: For storing raw and processed financial data.
- **AWS RDS (Relational Database Service)**: For storing processed data in a PostgreSQL database.
- **Alpha Vantage API**: Used to fetch daily stock data for S&P 500.
- **Pandas**: For data manipulation and processing.
- **Logging**: Python's logging module is used to log different actions and errors in the pipeline.

## Overview

This project automates the process of:
1. Fetching raw financial data from the Alpha Vantage API.
2. Processing and cleaning the raw data.
3. Uploading the processed data to AWS S3.
4. Storing the processed data in a PostgreSQL database in AWS RDS.
5. The data is available for analysis in AWS QuickSight for further visualization.

## Setup Instructions

### 1. Installing 

- Python 3.x installed
- AWS CLI configured with appropriate permissions
- API Key from Alpha Vantage
- Install the required libraries: request, pandas, python-dotenv
, boto3


### 2. Create your .env file 
```bash
API_KEY=your_alpha_vantage_api_key
RDS_HOST=your_rds_endpoint
RDS_PORT=5432
RDS_USER=your_rds_user
RDS_PASSWORD=your_rds_password
```

### 3. Create S3, Set up RDS instance 
RDS database and table will be created 

### 4. Run main.py

### 5. Set up QuickSight 
In AWS QuickSight, several key visualizations and metrics were analyzed:

**Open vs Close:** A large difference between the open and close prices might indicate significant market movement, highlighting potential trading opportunities.

**High vs Low:** The volatility of the stock. A smaller range between high and low prices indicates a more stable market.
Volume: Volume data can show major news or events that have affected the stock prices. Analyzing this can help identify key events driving stock movement.

### 6. Set up CloudWatch 
For this project, the following metrics are monitored:

#### S3 Monitoring
**Number of Objects:** Tracks the number of objects in your S3 bucket to ensure it is within expected limits.

**Bucket Size (Bytes):** Monitors the total size of the S3 bucket. This helps track storage usage and manage costs.
#### RDS Monitoring
**CPUUtilization:** Monitors the percentage of CPU being utilized by the RDS instance. High CPU usage may indicate inefficient database queries or the need for more compute resources. 

**FreeStorageSpace:** Tracks the amount of storage available for the RDS instance. Low free space can indicate that you need to scale the database or clean up unused data. 

#### QuickSight Monitoring
**Visual Error Count:** Tracks errors within QuickSight visualizations, ensuring that all data visualizations are functioning correctly.

## Next Step
**Machine Learning Model:** In the future, I plan to implement my own machine learning model for stock price prediction and compare its performance with the forecasts generated by QuickSight. 

**AWS Lambda:** I am also interested in automating the pipeline using AWS Lambda. However, as AWS Lambda incurs additional costs, I am considering a more cost-effective solution. Once I have a more sustainable budget, I will incorporate Lambda to run the pipeline on a scheduled basis or trigger it based on specific events.