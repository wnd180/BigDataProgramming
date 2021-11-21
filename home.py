from urllib.request import urlopen
import pandas as pd
import xmltodict
import json
from datetime import datetime
import csv

#새로운 시가 발생했을때 증가율 불러오기 고민

def get_code():
    #새로운 시가 발생했을 때는?
    # -> API로 코드 불러오기
    #매달 불러올 때 확인해야되는데 제공해주는 API가 한개뿐. 따라서 beautifulsoup selenium모듈 이용해 txt파일 저장하는 크롤링 개발 예정..
    #txt파일 인코딩 다르기 때문에 저장된 파일 인코딩 바꿔주고 그래야 할듯.
    #h로 끝나는거 쓰자.!
    print('a')

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

#공정한 집값 계산을 위해 면적당 가격을 구함.
for i in range(0,len(df)):
    df.at[i,'per_price']=int((df['price'][i]).replace(",",""))/float(df['area'][i])

print(df)

#트래픽 초과 오류 발생..
#어떻게 해결해야 할까..
#계속 불러오면서 csv에 추가. 오류 발생하면 중단. 처음 데이터 셋만 잘 갖다 붙이면 될듯.
