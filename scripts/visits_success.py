import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

adr = pd.read_csv('../static/csv/addresses_count_per_postal_aggr.csv')
df_feb = pd.read_csv('../static/csv/data/fev-20.csv', parse_dates=['DELIVERY_DATE'])
df_feb['LOCATION'] = df_feb.BUILDING_ID.map(str) + '-' + df_feb.BOX_ID.map(str)

df_mar = pd.read_csv('../static/csv/data/mar-20.csv', parse_dates=['DELIVERY_DATE'])
df_mar['LOCATION'] = df_mar.BUILDING_ID.map(str) + '-' + df_mar.BOX_ID.map(str)

df_apr = pd.read_csv('../static/csv/data/avr-20.csv', parse_dates=['DELIVERY_DATE'])
df_apr['LOCATION'] = df_apr.BUILDING_ID.map(str) + '-' + df_apr.BOX_ID.map(str)

df_mai = pd.read_csv('../static/csv/data/mai-20.csv', parse_dates=['DELIVERY_DATE'])
df_mai['LOCATION'] = df_mai.BUILDING_ID.map(str) + '-' + df_mai.BOX_ID.map(str)

df_jun = pd.read_csv("../static/csv/data/juin-20.csv", parse_dates=['DELIVERY_DATE'])
df_jun['LOCATION'] = df_jun.BUILDING_ID.map(str) + '-' + df_jun.BOX_ID.map(str)

df_feb_addr = df_feb.groupby('LOCATION').agg({'CLASS': 'sum', 'BOX_ID': 'count'}).reset_index()
df_feb_addr.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_feb_addr['SUCCESS_RATE'] = 100 * df_feb_addr.TOT_SUCCESS / df_feb_addr.TOT_VISITS
df_feb_addr['MONTH'] = "FEB"
# df_feb_addr['DELIVERY_RATE'] = 100 * df_feb_addr.TOT_VISITS / df_feb_addr.TOT_VISITS.sum()

df_mar_addr = df_mar.groupby('LOCATION').agg({'CLASS': 'sum', 'BOX_ID': 'count'}).reset_index()
df_mar_addr.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_mar_addr['SUCCESS_RATE'] = 100 * df_mar_addr.TOT_SUCCESS / df_mar_addr.TOT_VISITS
df_mar_addr['MONTH'] = "MAR"

df_apr_addr = df_apr.groupby('LOCATION').agg({'CLASS': 'sum', 'BOX_ID': 'count'}).reset_index()
df_apr_addr.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_apr_addr['SUCCESS_RATE'] = 100 * df_apr_addr.TOT_SUCCESS / df_apr_addr.TOT_VISITS
df_apr_addr['MONTH'] = "APR"

df_may_addr = df_mai.groupby('LOCATION').agg({'CLASS': 'sum', 'BOX_ID': 'count'}).reset_index()
df_may_addr.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_may_addr['SUCCESS_RATE'] = 100 * df_may_addr.TOT_SUCCESS / df_may_addr.TOT_VISITS
df_may_addr['MONTH'] = "MAY"

df_jun_addr = df_jun.groupby('LOCATION').agg({'CLASS': 'sum', 'BOX_ID': 'count'}).reset_index()
df_jun_addr.rename(columns={"CLASS": "TOT_SUCCESS",  "BOX_ID": "TOT_VISITS"}, inplace=True)
df_jun_addr['SUCCESS_RATE'] = 100 * df_jun_addr.TOT_SUCCESS / df_jun_addr.TOT_VISITS
df_jun_addr['MONTH'] = "JUN"

df_visits_success = pd.concat([df_feb_addr[['TOT_VISITS', 'SUCCESS_RATE', 'MONTH']],
                               df_mar_addr[['TOT_VISITS', 'SUCCESS_RATE', 'MONTH']],
                               df_apr_addr[['TOT_VISITS', 'SUCCESS_RATE', 'MONTH']],
                               df_may_addr[['TOT_VISITS', 'SUCCESS_RATE', 'MONTH']],
                               df_jun_addr[['TOT_VISITS', 'SUCCESS_RATE', 'MONTH']]])
df_visits_success.to_csv('../static/csv/visits_success.csv', index=False)

ddf = df_feb_addr[df_feb_addr.TOT_VISITS <= 600]
fig = go.Figure()
fig.add_trace(
    px.scatter(
               x=ddf.TOT_VISITS,
               y=ddf.SUCCESS_RATE,
               animation_frame=ddf.MONTH).data[0])

# Disable the orca response timeout.
import plotly.io._orca
import retrying
unwrapped = plotly.io._orca.request_image_with_retrying.__wrapped__
wrapped = retrying.retry(wait_random_min=1000)(unwrapped)
plotly.io._orca.request_image_with_retrying = wrapped

fig.write_image("/Users/aglin/Desktop/vol2.png", width=900, height=500, scale=8)
