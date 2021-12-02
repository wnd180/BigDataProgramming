from urllib.request import urlopen
import pandas as pd
import xmltodict
import json
from datetime import datetime
import csv
from selenium import webdriver
import zipfile
import os
import glob

# to-do-list
# 새로운 시가 발생했을때 증가율 불러오기 고민하기

def check_month():
    print("한달마다 실행되도록 구현")
    #schedule 이용하자
    # 2021/12/01일때 2021년 11월 자료 불러오도록.

def new_year_Check():
    print("202201 일경우 2012년 파일 delete 해주세요")
# 새 해일경우 (ex 2022년 1월), 2012년 데이터 다 지우고 새로 merge 해도 될듯.

# 매달 시군구가 생기거나 폐지 될 수 있기 때문에 매달 crawling 통해 check해서 새로운 txt파일 받아옴
def crawling():

    #새로운 시가 발생했을 때는?
    # -> 편입된 상위 시 소속으로 변경됌
    # -> API로 코드 불러오기
    # 매달 불러올 때 확인해야되는데 제공해주는 API가 한개뿐. 따라서 beautifulsoup selenium모듈 이용해 txt파일 저장하는 크롤링 개발 예정..

    # 기존 zip파일 존재할 경우 삭제해주기
    if os.path.isfile('~/Downloads/법정동코드 전체자료.zip'):
        os.remove('~/Downloads/법정동코드 전체자료.zip')
        
    driver = webdriver.Chrome('~/Downloads/chromedriver')
    driver.get('https://www.code.go.kr/stdcode/regCodeL.do')
    driver.implicitly_wait(10) # 페이지 전체 로딩 기다림.

    # 법정동코드 전체 다운로드 버튼을 눌러주자.
    driver.find_element_by_xpath('//*[@id="contents"]/form/table/tbody/tr[2]/td/div/div/a[2]').click()

    # 파일 존재할 때 까지 크롬창 기다리기
    while 1:
        if os.path.isfile('/Users/kwonseongjung/Downloads/법정동코드 전체자료.zip'):
            driver.close()
            break


def zip_to_txt():
    # txt파일 인코딩 다르기 때문에 저장된 파일 인코딩 바꿔주고 그래야 할듯.
    # https://www.code.go.kr/stdcode/regCodeL.do
    # 1. 압축해제
    # 2. txt파일 꺼내기
    # 3. 인코딩 형태 변환하기 -> cp949쓰면 될듯.

    #현재 디렉토리로 압축해제
    zipfile.ZipFile('/Users/kwonseongjung/Downloads/법정동코드 전체자료.zip').extractall(os.getcwd())

    # rename
    file_oldname = os.path.join(os.getcwd(), "╣²┴ñ╡┐─┌╡σ └ⁿ├╝└┌╖ß.txt")
    file_newname_newfile = os.path.join(os.getcwd(), "code_data.txt")

    os.rename(file_oldname, file_newname_newfile)

def code_extract():

    df = pd.read_csv(r"./code_data.txt", sep='\t', encoding='cp949')

    # 폐지된 시군구 삭제 뺴줘야되나..? 없으면 try except로 빠져나갈텐데..흠 모르겠네 ㅎㅎ;
    # -> 변경된 시군구로 출력되기 때문에 그럴 필요 x
    # 구 존재하는 시 코드 받으면 정상적으로 출력되나 확인할 것.
    # -> 출력 x 구가 포함된 시 일경우 상위 시로 출력하면 에러발생

    # 동 코드 받으면 정상적으로 response하나 확인할 것.
    # 동은 굳이 건드릴 필요 없을듯 상위 시에서 법정동 코드로 받아오는거라(다시 check)
    # 폐지된 시군구 폐지되기 전 날짜로 response되나 확인할 것.(check 필요)

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

    df.to_csv('./refine_code.csv')

#매달 api 불러오는 함수입니다.

def call_api(service_key, base_date):

    # 현재 날짜 불러오기
    todaymonth = datetime.today().strftime('%Y%m')
    # base_date = todaymonth
    # service_key = "1qjOjsNCCQP1Tt8rugK42qmJZb13HczJl4MWvHcD86GI54UNOUC%2FnANu1FKC28EJ3nxtie5a7wE6L%2FDHeJ5%2BLQ%3D%3D"

    # 리스트 생성
    price = []
    year = []
    dong = []
    area = []
    region_code = []
    region_name = []

    # csv파일 불러오기
    f = open('./refine_code.csv','r',encoding='utf-8')
    rdr = csv.reader(f)
    
    #헤더 제거하고 진행해야 여러개 파일 뽑을 때 딱 들어 맞음. 250* 4= 1000 인증키당 4달씩 한번에 뽑을 수 있음.
    next(rdr)

    # 정제된 법정동 코드를 for문을 통해 불러옴. 
    for line in rdr:
        gu_code = line[1]
        region = line[2]
        print(gu_code)

        try:
            # 해당 구에 해당 달 거래내역 없을 수 있음. 따라서 try except구문 이용
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

    df.to_csv('./data/'+base_date+'.csv',encoding='utf-8-sig')

def merge_csv():
    print("csv파일 merge해서 저장해줄게요")
    csv_path = "./data/"
    merge_path = "./merge.csv"

    file_list = glob.glob(csv_path+'*') #merge 파일 확인
    with open(merge_path,'w') as f:
        for i,file in enumerate(file_list):
            if i== 0:
                with open(file,'r') as f2:
                    while True:
                        line = f2.readline()

                        if not line:
                            break
                        f.write(line)

            else:
                with open(file,'r') as f2:
                    n = 0
                    while True:
                        line = f2.readline()
                        if n != 0:
                            f.write(line)
                        if not line:
                            break
                        n+=1
                
# 맨 처음 data 수집을 위한 코드 입니다.
def collect_data():
    
    base_year = '2017'
    base_month = 1
    keylist = ['1qjOjsNCCQP1Tt8rugK42qmJZb13HczJl4MWvHcD86GI54UNOUC%2FnANu1FKC28EJ3nxtie5a7wE6L%2FDHeJ5%2BLQ%3D%3D',
    '%2FargzrCJK5%2BwZ0DhHr2rbJYbgS%2Bgrj9W2jtM45tBMXuSmZQkjpSezFTK4hUtq65ZuvcfgdpfjvKw1iqAfaDRaw%3D%3D',
    'VL2jOrZ6duirXHCSKvgN%2Fu1ORHdZeM35it9vO8awdiXAJGiz3rjFrNEKPoEHOABVTEymHMa4kjT0ow94NC4WLQ%3D%3D']

    for service_key in keylist:

        for month in range(base_month,base_month+4):

            if month<10:
                base_date = base_year+'0'+str(month)
            else:
                base_date = base_year+str(month)

            call_api(service_key, base_date)

        base_month += 4

def main():
    crawling()
    zip_to_txt()
    code_extract()
    call_api()

collect_data()