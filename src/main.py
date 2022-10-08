from datetime import datetime, date
import os

import pipeline.extract
from pipeline.utils import last_business_day, class_inputs, save_df_info
from pipeline.transform import decode_encode, string_to_df, clean_df
from pipeline.load import sql_insert,before_insert
from pipeline.log import log_everthing
import server.connections
import server.queries.remove_dup

def main():
    ### log start time
    starttime = datetime.now()

    ### inputs
    startDate       = last_business_day(date.today()).isoformat()
    endDate         = date.today().isoformat()
    reportId        = '500'

    api_key         = os.environ['api_key']
    secret          = os.environ['secret'] 
    server_name     = os.environ['server_name']
    database        = os.environ['database']
    table           = os.environ['table']

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






