from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd
import xmltodict
import json
from datetime import datetime
import csv

# 현재 날짜 불러오기
todaymonth = datetime.today().strftime('%Y%m')
service_key = "%2FargzrCJK5%2BwZ0DhHr2rbJYbgS%2Bgrj9W2jtM45tBMXuSmZQkjpSezFTK4hUtq65ZuvcfgdpfjvKw1iqAfaDRaw%3D%3D"
#base_date = todaymonth
base_date = "202001"

#리스트 생성
price = []
year = []
dong = []
area = []
region_code = []
region_name = []

#csv파일 불러오기
f = open('refine_code.csv','r',encoding='utf-8')
rdr = csv.reader(f)

#정제된 법정동 코드를 for문을 통해 불러옴. 
for line in rdr:
    gu_code = line[1]
    region = line[2]
    print(gu_code)
    # 해당 구에 해당 달 거래내역 없을 수 있음. 따라서 try except구문 이용
    try:
        url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD='+gu_code+'&DEAL_YMD='+base_date+'&serviceKey='+service_key
        response = urlopen(url)
        results = response.read().decode("utf-8")
        result_to_json = xmltodict.parse(results)
        data = json.loads(json.dumps(result_to_json))
        val = data['response']['body']['items']['item']
        for i in val:
            price.append(i['거래금액'])
            year.append(i['년'])
            dong.append(i['법정동'])
            area.append(i['전용면적'])
            region_code.append(i['지역코드'])
            region_name.append(region)


    except:

        continue

f.close()

df= pd.DataFrame([price, year, dong, area, region_code, region_name]).T
df.columns=['price','year','dong','area','region_code','region_nmae']

for i in range(0,len(df)):
    df.at[i,'per_price']=int((df['price'][i]).replace(",",""))/float(df['area'][i])

print(df)


