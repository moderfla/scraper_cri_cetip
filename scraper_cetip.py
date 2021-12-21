import requests
from   bs4 import BeautifulSoup
import pandas as pd
import io
import os

url    = 'https://www2.cetip.com.br/TitulosCRI'
s = requests.Session()
r = s.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
viewstate  = soup.find('input', {'id': '__VIEWSTATE'})['value']
validation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']
r2 = s.post(url, data={ 
            '__VIEWSTATE'      : viewstate,
            '__EVENTVALIDATION': validation,
            'txtDtEmissao':"01/01/0001", 
            'btExportarCSV': "Exportar para CSV"
        })

CRI = pd.read_csv(io.BytesIO(r2.content), delimiter=";", encoding='ISO-8859-1', parse_dates=[7, 8, 9], infer_datetime_format= 'True', dayfirst='True', thousands=".", decimal=',')

CRI.to_csv('emissoes_cri.csv', index='False')
