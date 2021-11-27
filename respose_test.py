from urllib.request import urlopen
import pandas as pd
import xmltodict
import json
from datetime import datetime

pd.set_option('display.max_rows', None) ## 모든 열을 출력한다.

#인증키1
#1qjOjsNCCQP1Tt8rugK42qmJZb13HczJl4MWvHcD86GI54UNOUC%2FnANu1FKC28EJ3nxtie5a7wE6L%2FDHeJ5%2BLQ%3D%3D
#인증키2
#%2FargzrCJK5%2BwZ0DhHr2rbJYbgS%2Bgrj9W2jtM45tBMXuSmZQkjpSezFTK4hUtq65ZuvcfgdpfjvKw1iqAfaDRaw%3D%3D

# 현재 날짜 불러오기
todaymonth = datetime.today().strftime('%Y%m')
service_key = "VL2jOrZ6duirXHCSKvgN%2Fu1ORHdZeM35it9vO8awdiXAJGiz3rjFrNEKPoEHOABVTEymHMa4kjT0ow94NC4WLQ%3D%3D"

# 해당 월 거래내역 불러오기.
base_date = "201304"
gu_code = '50130' #테스트 할 법정동 코드 확인
# 폐지된 곳: 소사구 41197

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

    df.to_csv('3.csv',encoding='utf-8-sig')