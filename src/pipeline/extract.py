from dataclasses import dataclass
import requests, json
from requests.structures import CaseInsensitiveDict

@dataclass
class api():
    key:str
    secret:str
    reportId:str
    start:str
    end:str
    fileName:str        = 'test_3.csv'
    saveAsFile:str      = 'FALSE'
    includeHeaders:str  = 'TRUE'
    baseurl:str         = 'https://api-c52.nice-incontact.com/incontactapi'
    download_path:str   = 'services/v23.0/report-jobs/datadownload'
    
    def access_token(self):
        url = "https://na1.nice-incontact.com/authentication/v1/token/access-key"
        headers = {'Content-Type': 'application/json'}
        payload = f"""{{
                    "accessKeyId":"{self.key}",
                    "accessKeySecret":"{self.secret}"
                    }}"""
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        return data["access_token"]
    
    def url(self):
        return f"{self.baseurl}/{self.download_path}/{self.reportId}?startDate={self.start}&endDate={self.end}&saveAsFile={self.saveAsFile}&includeHeaders={self.includeHeaders}" 

    def headers(self):
        header_param = CaseInsensitiveDict()
        header_param['Authorization'] = f"bearer {self.access_token()}"
        header_param['Content-Type']  = 'application/x-www-form-urlencoded'
        header_param['Accept']        = 'application/json, text/javascript, */*'
        return header_param

    def payload(self):
            return {
            'reportId'  : self.reportId,
            'fileName'  : self.fileName,
            'startDate' : self.start,
            'endDate'   : self.end,
            'saveAsFile': self.saveAsFile,
            'includeHeaders' : self.includeHeaders
            }

    def request_report(self):
        # Make http post request
        response = requests.post(self.url(), headers=self.headers(), data=self.payload())
        return response
        