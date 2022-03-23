import pandas as pd
import base64
import base64
from io import StringIO

def decode_encode(api_request:str) -> str:
    ##Check keys in the JSON
    # key_list = list(output.keys()) 

    #extract file column from 'output' dict
    raw = api_request["file"]
    #decode file value from base64 and convert to string
    raw_string = base64.b64decode(raw)
    #convert raw_string to utf-8 str
    utf_8 = str(raw_string, 'utf-8')
    #wrap in StrinIO to convert to df
    cleaned = StringIO(utf_8)
    return cleaned

def string_to_df(string:str) -> pd.DataFrame():
    #In case of bad data, write to flatfile
    try:
        df = pd.read_csv(string)
    except:
        print('check bad data')
        with open(f"data/bad_data/{endDate}.csv", "w") as csv:
            csv.writer(string)
        df = pd.read_csv(f'data/bad_data/{endDate}.csv',delimiter=",", encoding='utf-8')
    return df

def clean_df(df:pd.DataFrame() ) -> pd.DataFrame():
    df.dropna(axis='rows', how='all',inplace=True)
    ####Bug ALERT : MUST COMPLETE THE BELOW STEP TO FILL NAS!!!!!!
    ####replace na values with 0 to be able to coerce to ssms
    #   df.dropna(subset=['Contact_ID'], inplace=True)
    df = df.fillna(0)
    # convert date fromat
    df['start_date'] = pd.to_datetime(df['start_date']) 
    return df