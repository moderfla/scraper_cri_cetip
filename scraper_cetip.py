import os
import requests
import base64
import pandas as pd
import io

headers = {
    # Requests sorts cookies= alphabetically
    # 'Cookie': f"dtCookie=v_4_srv_33_sn_5C4EA20842E4E7EB1C2D8401E36C4D92_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_0_app-3A6c080359c6da1713_1_app-3A2fa0c7805985f6bf_1_rcs-3Acss_0; dtLatC=18; rxVisitor=16551482089629L69FH8GEB0AI47QJ6PD8D6RA7UQ1DD3; dtPC=33{440751373_9h-vMSABCJCPTUPMQITCTKJATLVOFKKCGAQE-0e0;} rxvt=1655242553065|1655240751375; dtSa=-; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+14+2022+18%3A05%3A51+GMT-0300+(-03)&version=6.21.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0003%3A0%2CC0001%3A1%2CC0004%3A0%2CC0002%3A0&AwaitingReconsent=false; TS0171d45d=016e3b076f3cd8812680dc91c0076c70db0a161bbf38fef3270a5d016d564a401fbddb2239d517f772188a44a09c214220f8ddb0f6; BIGipServerpool_sistemaswebb3-balcao.b3.com.br_5443=2014602250.17173.0000; BIGipServerpool_sistemaswebb3-balcao.b3.com.br_5443_WAF=2855801866.64288.0000; TS01871345=011d592ce1c3fb53cf7e4eeb7cfb5b9eb8e323f089f6dcd4ccc10d99551d9d00b67de5c4a26e2da2e0b2493f52656b6621bbb959dd; rdtrk=%7B%22id%22%3A%22e116383d-8c8e-4821-be6d-b197daec92ba%22%7D; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3JlYXRlZF9hdCI6MTY1NTE1NzY2ODU0OX0=; TS0134a800=016e3b076f2982fabdf435cedd027378e0f9ca46fd7e0f5335aad7997fe520efb681fb0501fe616316ea67460306ded8505f44ff4c; visid_incap_2246223=Sry9mLcITaiPL9HAEi1lIJo5BWIAAAAAQUIPAAAAAAAOqYX+VPrTpI96v1QtBTZn",
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'sistemaswebb3-balcao.b3.com.br',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Referer': 'https://sistemaswebb3-balcao.b3.com.br/',
    'Connection': 'keep-alive',
}

response = requests.get('https://sistemaswebb3-balcao.b3.com.br/featuresCRIProxy/CriCall/GetDownload', headers=headers, verify=False)
tab = base64.b64decode(response.text).decode("ISO-8859-1")
cri = pd.read_csv(io.StringIO(tab), delimiter=";", encoding='ISO-8859-1', parse_dates=[8, 9, 10], infer_datetime_format= 'True', dayfirst='True', thousands=".", decimal=',')
cri.to_csv('emissoes_cri.csv', index=False)
