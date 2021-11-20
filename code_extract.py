import pandas as pd
import numpy as np

df = pd.read_csv(r"code_data.txt", sep='\t')

#폐지된 시군구 삭제
df = df[df.폐지여부 != '폐지']
#동면읍 삭제
df = df[df.법정동코드 % 100000 == 0]

#특별시 광역시 도 등 잘라줘야함. 
df = df[df.법정동코드 % 100000000 != 0]

#구가 존재하는 시일 경우 시를 삭제해줘야 함.
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