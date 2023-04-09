import pandas as pd

df_feb = pd.read_csv("../static/csv/data/30_parcels_feb.csv", parse_dates=['DELIVERY_DATE'])
df_mar = pd.read_csv("../static/csv/data/30_parcels_mar.csv", parse_dates=['DELIVERY_DATE'])
df_apr = pd.read_csv("../static/csv/data/30_parcels_apr.csv", parse_dates=['DELIVERY_DATE'])
df_may = pd.read_csv("../static/csv/data/30_parcels_may.csv", parse_dates=['DELIVERY_DATE'])
df_jun = pd.read_csv("../static/csv/data/30_parcels_jun.csv", parse_dates=['DELIVERY_DATE'])
df_jul = pd.read_csv("../static/csv/data/30_parcels_jul.csv", parse_dates=['DELIVERY_DATE'])
df_aug = pd.read_csv("../static/csv/data/30_parcels_aug.csv", parse_dates=['DELIVERY_DATE'])
df_sep = pd.read_csv("../static/csv/data/30_parcels_sep.csv", parse_dates=['DELIVERY_DATE'])

df = pd.concat([df_feb, df_mar, df_apr, df_may, df_jun, df_jul, df_aug, df_sep])

df_day = df.groupby([df.DELIVERY_DATE.dt.date, 'POSTAL_CODE']).agg({'CLASS': ['sum'], 'BOX_ID': ['count']}).reset_index()
df_day.columns = df_day.columns.get_level_values(0)
df_day.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_day.to_csv("../static/csv/30_parcels_dailycounts.csv", index=False)
