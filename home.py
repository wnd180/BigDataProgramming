from urllib.request import urlopen
import pandas as pd
import xmltodict
import json
from datetime import datetime
import csv
from selenium import webdriver
from time import sleep

# 새로운 시가 발생했을때 증가율 불러오기 고민
# 나중에 생각하기

def crawling():

    #새로운 시가 발생했을 때는?
    # -> 편입된 상위 시 소속으로 변경됌

    # -> API로 코드 불러오기
    # 매달 불러올 때 확인해야되는데 제공해주는 API가 한개뿐. 따라서 beautifulsoup selenium모듈 이용해 txt파일 저장하는 크롤링 개발 예정..
    # txt파일 인코딩 다르기 때문에 저장된 파일 인코딩 바꿔주고 그래야 할듯.
    # https://www.code.go.kr/stdcode/regCodeL.do

    # 압축파일 불러올 떄는 h로 끝나는거 쓰자.!
    # https://www.mois.go.kr/frt/bbs/type001/commonSelectBoardList.do?bbsId=BBSMSTR_000000000052

    # 매달 시군구가 생기거나 폐지 될 수 있기 때문에 매번 check해서 새로운 txt파일 받아옴
    driver = webdriver.Chrome('/Users/kwonseongjung/Downloads/chromedriver')
    driver.implicitly_wait(3) # 페이지 전체 로딩 기다림.
    driver.get('https://www.code.go.kr/stdcode/regCodeL.do')

    # 법정동코드 전체 다운로드 버튼을 눌러주자.
    driver.find_element_by_xpath('//*[@id="contents"]/form/table/tbody/tr[2]/td/div/div/a[2]').click()

    sleep(3) # 3초간 기다림

    # 크롬창 닫기
    driver.close()

def zip_to_txt():
    # 1. 압축해제
    # 2. txt파일 꺼내기
    # 3. csv파일로 변환하기
    print("hello world")

def txt_to_csv():

    df = pd.read_csv(r"code_data.txt", sep='\t')

    # 폐지된 시군구 삭제 뺴줘야되나..? 없으면 try except로 빠져나갈텐데..흠 모르겠네 ㅎㅎ;
    # -> 변경된 시군구로 출력되기 때문에 그럴 필요 x

    # 동 코드 받으면 정상적으로 response하나 확인할 것.
    # 동은 굳이 건드릴 필요 없을듯 상위 시에서 법정동 코드로 받아오는거라

    # 구 존재하는 시 코드 받으면 정상적으로 출력되나 확인할 것.
    # -> 출력 x 구가 포함된 시 일경우 상위 시로 출력하면 에러발생

    # 폐지된 시군구 폐지되기 전 날짜로 response되나 확인할 것.

    #폐지인 곳 삭제
    df = df[df.폐지여부 != '폐지']

    #동면읍 삭제
    df = df[df.법정동코드 % 100000 == 0]

    #특별시 광역시 도 등 잘라줘야함. 
    df = df[df.법정동코드 % 100000000 != 0]

    # 구가 존재하는 시일 경우 시를 삭제해줘야 함.
    # 알고리즘 다시 짜자.

    # 얘도 try except 구문으로 풀려나지 않을까? 다시 해보자.
    # -> 에러로 넘어가면 됌 굳이 없애줄 필요 x
    # -> 트래픽 제한 때문에 일단은 이거라도 줄여야겠다.

    df = df[df.법정동명 != '경기도 수원시']
    df = df[df.법정동명 != '경기도 성남시']
    df = df[df.법정동명 != '경기도 안양시']
    df = df[df.법정동명 != '경기도 안산시']
    df = df[df.법정동명 != '경기도 고양시']
    df = df[df.법정동명 != '경기도 용인시']
    df = df[df.법정동명 != '충청북도 청주시']
    df = df[df.법정동명 != '충청남도 천안시']
    df = df[df.법정동명 != '전라북도 전주시']
    df = df[df.법정동명 != '경상북도 포항시']
    df = df[df.법정동명 != '경상남도 창원시']

    #법정동 코드 str 타입 변환
    df.법정동코드 = df.법정동코드.astype(str)

    #API를 불러오기 위한 법정동 코드 앞선 5자리만 필요
    df['법정동코드'] = df['법정동코드'].str.slice(start=0, stop=5) #인덱스 사이 값 반환

    #index 초기화
    df.reset_index(inplace = True, drop = True)

    df.to_csv('refine_code.csv')

# 현재 날짜 불러오기
todaymonth = datetime.today().strftime('%Y%m')
service_key = "%2FargzrCJK5%2BwZ0DhHr2rbJYbgS%2Bgrj9W2jtM45tBMXuSmZQkjpSezFTK4hUtq65ZuvcfgdpfjvKw1iqAfaDRaw%3D%3D"
# base_date = todaymonth
base_date = "202001"

# 리스트 생성
price = []
year = []
dong = []
area = []
region_code = []
region_name = []

# csv파일 불러오기
f = open('refine_code.csv','r',encoding='utf-8')
rdr = csv.reader(f)

# 정제된 법정동 코드를 for문을 통해 불러옴. 
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

# 공정한 집값 계산을 위해 면적당 가격을 구함.
for i in range(0,len(df)):
    df.at[i,'per_price']=int((df['price'][i]).replace(",",""))/float(df['area'][i])

print(df)

# for 문 도중 트래픽 초과 오류 발생..
# 어떻게 해결해야 할까..
# 계속 불러오면서 csv에 축적. 오류 발생하면 중단. 처음 데이터 셋만 잘 갖다 붙이면 될듯.
# 한달마다 반복
