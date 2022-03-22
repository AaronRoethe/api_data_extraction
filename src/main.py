"""
Created on Thu Dec  2 11:23:19 2021
Created on Thu Aug  5 13:45:36 2021
@author: RGotety

Updated on Fri Mar 18
@author: Aaron Roethe
"""

###Generates a custom report via post request

#Import required packages
from datetime import datetime, date

from pipeline.config import api_keys
from pipeline.utils import last_business_day
from pipeline.extract import get_access_token, request_report
from pipeline.transform import decode_encode, string_to_df, clean_df
from pipeline.load import sql_engine, load_MSSQL

def main():
    ### log start time
    starttime = datetime.now()
    print(starttime)
    # report_500 = api(api_key,secret,reportId,startDate,endDate)

    ### inputs
    api_key, secret = api_keys()
    startDate       = last_business_day(date.today()).isoformat()
    endDate         = date.today().isoformat()
    reportId        = '500'
    server          = 'EUS1PCFSNAPDB01'
    database        = 'DWWorking'
    table           = 'api_nic_agentbyday'
    
    ### pipeline
    ## Generate Access token
    accessToken = get_access_token(api_key, secret)
    ## Post request
    #generate info as base64
    #Define parameters for request
    api_requested_data = request_report(
        accessToken, startDate, endDate, reportId=reportId)
    ## clean requested data
    str_data    = decode_encode(api_requested_data)
    df          = string_to_df(str_data)
    load        = clean_df(df)
    print(load)
    ## load into server
    # engine = sql_engine(server, database)
    # load_MSSQL(engine, load, table_name=table)

    print("Time to Complete:",datetime.now() - starttime)

if __name__ == "__main__":
    main()






