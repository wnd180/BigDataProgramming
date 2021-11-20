import pandas as pd
import numpy as np

df = pd.read_csv(r"code_data.txt", sep='\t')

#폐지된 시군구 삭제
df = df[df.폐지여부 != '폐지']
#동면읍 삭제
df = df[df.법정동코드 % 100000 == 0]

df.to_csv('refine_code.csv')