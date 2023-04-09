import pandas as pd
import datetime


def week(date):
    return date.isocalendar()[1]


df_feb = pd.read_csv("../static/csv/data/fev-20.csv", parse_dates=['DELIVERY_DATE'])
df_mar = pd.read_csv("../static/csv/data/mar-20.csv", parse_dates=['DELIVERY_DATE'])
df_apr = pd.read_csv("../static/csv/data/avr-20.csv", parse_dates=['DELIVERY_DATE'])
df_may = pd.read_csv("../static/csv/data/mai-20.csv", parse_dates=['DELIVERY_DATE'])
df_jun = pd.read_csv("../static/csv/data/juin-20.csv", parse_dates=['DELIVERY_DATE'])
df_jul = pd.read_csv("../static/csv/data/juil-20.csv", parse_dates=['DELIVERY_DATE'])
df_aug = pd.read_csv("../static/csv/data/aout-20.csv", parse_dates=['DELIVERY_DATE'])
df_sep = pd.read_csv("../static/csv/data/sept-20.csv", parse_dates=['DELIVERY_DATE'])

df = pd.concat([df_feb, df_mar, df_apr, df_may, df_jun, df_jul, df_aug, df_sep])

# ignore location data
df = df.groupby(['DELIVERY_DATE']).agg({'BOX_ID': ['count'], 'CLASS': ['sum']}).reset_index()
df.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df.columns = df.columns.get_level_values(0)

df['WEEK'] = df['DELIVERY_DATE'].apply(lambda x: week(x))
df['HOUR'] = df['DELIVERY_DATE'].apply(lambda x: x.hour)

df = df.groupby([df['WEEK'], df['HOUR']]).agg({'TOT_VISITS': 'sum', 'TOT_SUCCESS': 'sum'}).reset_index()
df.to_csv("../static/csv/stats_week_hour.csv", index=False)
