import pandas as pd
from datetime import datetime
import numpy as np
import math

df_feb = pd.read_csv("../static/csv/data/fev-20.csv", parse_dates=['DELIVERY_DATE'])
df_mar = pd.read_csv("../static/csv/data/mar-20.csv", parse_dates=['DELIVERY_DATE'])
df_apr = pd.read_csv("../static/csv/data/avr-20.csv", parse_dates=['DELIVERY_DATE'])

for i, df in enumerate([df_feb, df_mar, df_apr]):
    df_group = df.groupby(['POSTAL_CODE','MUNICIPALITY'])['DELIVERY_DATE'].count().reset_index(name="COUNT")
    name = ["fev.csv", "mar.csv", "avr.csv"]
    df_group.to_csv("../static/csv/postal_count/" + name[i], index=False)

for i, df in enumerate([df_feb, df_mar, df_apr]):
    df['POSTAL_CODE2'] = df['POSTAL_CODE'].apply(lambda c: math.floor(int(c)/100))
    df_group = df.groupby(['POSTAL_CODE2'])['DELIVERY_DATE'].count().reset_index(name="COUNT")
    name = ["fev.csv", "mar.csv", "avr.csv"]
    df_group.to_csv("../static/csv/postal_count_aggr/" + name[i], index=False)
