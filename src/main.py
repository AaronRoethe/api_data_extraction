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

import pipeline.extract
from pipeline.utils import last_business_day, class_inputs, save_df_info
from pipeline.transform import decode_encode, string_to_df, clean_df
from pipeline.load import sql_insert,before_insert
from pipeline.log import log_everthing
import server.config
import server.connections
import server.queries.remove_dup

def main():
    ### log start time
    starttime = datetime.now()

    ### inputs
    api_key, secret = server.config.api_keys()
    startDate       = last_business_day(date.today()).isoformat()
    endDate         = date.today().isoformat()
    reportId        = '500'
    # server          = 'EUS1PCFSNAPDB01'
    server_name     = 'EUS1QCFSNAPDB01'
    database        = 'DWWorking'
    table           = 'api_nic_agentbyday'

    ### call api class    
    report_500 = pipeline.extract.api(
        api_key, secret, reportId, startDate, endDate)
    ### collect & log inputs
    log_everthing("INPUTS",class_inputs(report_500))
    ### api requested data
    response = report_500.request_report()
    log_everthing("STATUS_CODE", (response.status_code, response.reason))

    ## clean requested data
    str_data = decode_encode(response.json())
    log_everthing("READABLE", str_data.readable())

    df = string_to_df(str_data)
    # log_everthing("DF_INFO: {save_df_info(df)}")

    load = clean_df(df)
    # log_everthing(f"CLEAN DF_INFO: {save_df_info(load)}")
    print(load)
    # load into server
    dwworking   = server.connections.MSSQL(server_name, database)
    dw_engine   = dwworking.create_engine()
    remove_dup  = server.queries.remove_dup.sql(endDate)
    before_insert(dw_engine, remove_dup)
    sql_insert(dw_engine, table, load)
    log_everthing("COMPLETED", datetime.now() - starttime)

if __name__ == "__main__":
    main()






