from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd
import xmltodict
import json
from datetime import datetime

# 처음 작성된 20200120부터 현재 날짜 까지 불러오도록 한다.
todaydate = datetime.today().strftime('%Y%m%d')

#API파싱
key='%2FargzrCJK5%2BwZ0DhHr2rbJYbgS%2Bgrj9W2jtM45tBMXuSmZQkjpSezFTK4hUtq65ZuvcfgdpfjvKw1iqAfaDRaw%3D%3D'
url = f'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={key}&'
queryParams = urlencode({ quote_plus('pageNo') : 1, 
                        quote_plus('numOfRows') : 10,
                        quote_plus('startCreateDt') : '20200120',
                        quote_plus('endCreateDt') : todaydate})
url2 = url + queryParams
response = urlopen(url2)

# print(type(response)) # HTTPSresponse 
results = response.read().decode("utf-8")

# xml을 JSON형식으로 전환
results_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(results_to_json))

# {'accDefRate': '1.5093139972', 'accExamCnt': '4269316', 'accExamCompCnt': '4092389', 'careCnt': '17897', 
# 'clearCnt': '42953', 'createDt': '2021-01-01 09:36:53.691',                              'deathCnt': '917', 'decideCnt': '61767', 
# 'examCnt': '176927', 'resutlNegCnt': '4030622', 'seq': '372', 
# 'stateDt': '20210101', 'stateTime': '00:00', 'updateDt': '2021-01-03 10:35:39.056'}

corona=data['response']['body']['items']['item']
#Date, Cnt list로 불러오기 
Date=[]
Cnt=[]

for i in corona:
    Date.append(i['stateDt'])  #'stateDt': '20200801'
    Cnt.append(i['decideCnt'])  # decideCnt': '14336'   누적확진자

df=pd.DataFrame([Date,Cnt]).T
df.columns=['날짜','누적확진자'] 
#날짜순으로 정렬
df=df.sort_values(by='날짜', ascending=True)

#index 날짜 오래된 순으로 초기화
df.reset_index(inplace = True, drop = True)
print(df)

df.at[0,'일일확진자']=df['누적확진자'][0]#첫번째 값을 계산할 땐 전날값이 없으므로(0이므로) 오늘값이 증가량임
for i in range(1,len(df)):
    df.at[i,'일일확진자']=int(df['누적확진자'][i])-int(df['누적확진자'][i-1]) #오늘값-전날값=증가량

print(df)


df.to_csv('daily.csv',encoding='utf-8-sig')

#주간확진자로 묶어볼까요

weeklen = len(df)//7*7
print(weeklen)
#|ㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡ|ㅡㅡㅡ|
#|ㅡ주차ㅡ|ㅡ주간확진자ㅡ|증가율|
#|ㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡ|ㅡㅡㅡ|
#|몇월몇주차|        |1.111|
#|ㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡ|
#|ㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡ|
#|ㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡ|
#|ㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡ|


week_df = pd.DataFrame(columns=['주차','주간확진자','증가율'])

for i in range(0,(weeklen//7)):
    if i == 0:
        week_df.loc[i] = [str(i+1)+'주차', 
                        int(df.at[6,'누적확진자'])
                        # ,int(df.at[6,'누적확진자'])
                        ,0]

    else:
        week_df.loc[i] = [str(i+1)+'주차', 
                int(df.at[i*7+6,'누적확진자'])-int(df.at[i*7-1,'누적확진자']),
                0]

week_df.to_csv('weekly.csv',encoding='utf-8-sig')
print(week_df)
