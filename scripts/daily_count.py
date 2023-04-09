import pandas as pd
from datetime import datetime

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %h:%m:%s')
df_feb = pd.read_csv("../static/csv/data/fev-20.csv", parse_dates=['DELIVERY_DATE'])
df_mar = pd.read_csv("../static/csv/data/mar-20.csv", parse_dates=['DELIVERY_DATE'])
df_apr = pd.read_csv("../static/csv/data/avr-20.csv", parse_dates=['DELIVERY_DATE'])
df_may = pd.read_csv("../static/csv/data/mai-20.csv", parse_dates=['DELIVERY_DATE'])
df_jun = pd.read_csv("../static/csv/data/juin-20.csv", parse_dates=['DELIVERY_DATE'])
df_jul = pd.read_csv("../static/csv/data/juil-20.csv", parse_dates=['DELIVERY_DATE'])
df_aug = pd.read_csv("../static/csv/data/aout-20.csv", parse_dates=['DELIVERY_DATE'])
df_sep = pd.read_csv("../static/csv/data/sept-20.csv", parse_dates=['DELIVERY_DATE'])

df = pd.concat([df_feb, df_mar, df_apr, df_may, df_jun, df_jul, df_aug, df_sep])

df_day = df.groupby([df.DELIVERY_DATE.dt.date, 'POSTAL_CODE']).agg({'CLASS': 'sum', 'BOX_ID': 'count'}).reset_index()
df_day.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_day.to_csv("../static/csv/dailycounts.csv", index=False)
