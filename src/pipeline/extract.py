from dataclasses import dataclass
from urllib import response
import requests, json
from requests.structures import CaseInsensitiveDict

def get_access_token(api_key:str, secret:str):
    url = "https://na1.nice-incontact.com/authentication/v1/token/access-key"

    payload = f"""{{
                "accessKeyId":"{api_key}",
                "accessKeySecret":"{secret}"
                }}"""

    headers = {
    'Content-Type': 'application/json'
    }
    #Generate response
    response = requests.request("POST", url, headers=headers, data = payload)
    data = json.loads(response.text) #load to json 
    return data["access_token"]

def request_report(accessToken, start, end, reportId, fileName='test_3.csv',saveAsFile='false',includeHeaders='true'):
    BASEURL = 'https://api-c52.nice-incontact.com/incontactapi'
    # Define parameters in payload
    payload={
    'reportId'  : reportId,
    'fileName'  : fileName,
    'startDate' : start,
    'endDate'   : end,
    'saveAsFile': saveAsFile,
    'includeHeaders' : includeHeaders
    }

    #add required headers
    header_param = CaseInsensitiveDict()
    header_param['Authorization'] = f"bearer {accessToken}"
    header_param['Content-Type']  = 'application/x-www-form-urlencoded'
    header_param['Accept']        = 'application/json, text/javascript, */*'

    # Make http post request
    download_path = 'services/v23.0/report-jobs/datadownload'
    url = f"{BASEURL}/{download_path}/{reportId}?startDate={start}&endDate={end}&saveAsFile={saveAsFile}&includeHeaders={includeHeaders}" 
    response = requests.post(url, headers=header_param, data=payload)
    #Check response codes
    print(response.status_code, response.reason)
    # #Cast response to json
    return response.json()
