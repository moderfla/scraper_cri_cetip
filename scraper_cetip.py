import os
import requests
import base64
import pandas as pd
import io

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Host': 'sistemaswebb3-balcao.b3.com.br',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Referer': 'https://sistemaswebb3-balcao.b3.com.br/',
    'Connection': 'keep-alive',
}

response = requests.get('https://sistemaswebb3-balcao.b3.com.br/featuresCRIProxy/CriCall/GetDownload', headers=headers, verify=False)
tab = base64.b64decode(response.text).decode("ISO-8859-1")
cri = pd.read_csv(io.StringIO(tab), delimiter=";", encoding='ISO-8859-1', parse_dates=[8, 9, 10], infer_datetime_format= 'True', dayfirst='True', thousands=".", decimal=',')
cri.drop(cri.columns[[12]], axis=1).to_csv('emissoes_cri.csv', index=False)
