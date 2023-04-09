import pandas as pd


df = pd.read_csv("../static/csv/dailycounts.csv", parse_dates=['DELIVERY_DATE'])
df['POSTAL_CODE2'] = df['POSTAL_CODE'].apply(lambda c: c//100)

n_addresses = pd.read_csv("../static/csv/addresses_count_per_postal.csv")

df_all = pd.merge(df, n_addresses)
df_all['TOT_SUCCESS'] = df_all['TOT_SUCCESS'] / df_all['N_ADDRESSES']
df_all['TOT_VISITS'] = df_all['TOT_VISITS'] / df_all['N_ADDRESSES']
df_all = df_all.rename(columns={"TOT_SUCCESS": "AVG_SUCCESS_BY_ADDRESS", "TOT_VISITS": "AVG_VISITS_BY_ADDRESS"})
df_all.groupby(['POSTAL_CODE'])['AVG_VISITS_BY_ADDRESS'].sum()
df_all.to_csv("../static/csv/dailyavgs_norm_by_n_address.csv", index=False)
