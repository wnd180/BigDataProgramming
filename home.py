from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
from os import sep
import pandas as pd
import xmltodict
import json
from datetime import datetime

# 현재 날짜 불러오기
todaymonth = datetime.today().strftime('%Y%m')
service_key = "%2FargzrCJK5%2BwZ0DhHr2rbJYbgS%2Bgrj9W2jtM45tBMXuSmZQkjpSezFTK4hUtq65ZuvcfgdpfjvKw1iqAfaDRaw%3D%3D"
#base_date = todaymonth
base_date = "202001"
gu_code = '41110' ## 법정동 코드 5자리라면, 구 단위로 데이터를 확보하는 것. 11215 = 광진구
url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD='+gu_code+'&DEAL_YMD='+base_date+'&serviceKey='+service_key
response = urlopen(url)
results = response.read().decode("utf-8")
result_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(result_to_json))
print(data)

val = data['response']['body']['items']['item']

price = []
year = []
dong = []
area = []
region_code = []

for i in val:
    price.append(i['거래금액'])
    year.append(i['년'])
    dong.append(i['법정동'])
    area.append(i['전용면적'])
    region_code.append(i['지역코드'])

df= pd.DataFrame([price, year, dong, area, region_code]).T
df.columns=['price','year','dong','area','region_code']

for i in range(0,len(df)):
    df.at[i,'per_price']=int((df['price'][i]).replace(",",""))/float(df['area'][i])

print(df)


