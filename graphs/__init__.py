import geopandas
import pandas as pd
import os.path
from enum import Enum
from datetime import date, timedelta


class MODE(Enum):
    DEVELOPMENT = 1
    PRODUCTION = 2


registered_plots = {}

if os.path.exists("static/csv/last_plots.csv"):
    __plots = pd.read_csv("static/csv/last_plots.csv").set_index("name")
else:
    __plots = pd.DataFrame(columns=["name", "link_html", "link_image"]).set_index("name")


def get_start_end_dates(year, week):
    d = date(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6), d + dlt + timedelta(days=4)


# RUNNING_MODE = MODE.DEVELOPMENT  # uncomment this line before editing
RUNNING_MODE = MODE.PRODUCTION  # uncomment this line before pushing

LAST_VALID_WEEK = 39
LAST_WEEK_DAY = get_start_end_dates(2020, LAST_VALID_WEEK)[2].__str__()
LAST_WEEKEND_DAY = get_start_end_dates(2020, LAST_VALID_WEEK)[2].__str__()

if RUNNING_MODE == MODE.DEVELOPMENT:
    df = pd.read_csv("static/csv/dailycounts.csv", parse_dates=['DELIVERY_DATE'])
    df['WEEK'] = df.DELIVERY_DATE.dt.weekofyear
    df['POSTAL_CODE2'] = df.POSTAL_CODE // 100

    df_addr = pd.read_csv("static/csv/addresses_count_per_postal_aggr.csv", sep=',')
    df_week = df.groupby([df.WEEK, df.POSTAL_CODE2]).agg({'TOT_VISITS': 'sum', 'TOT_SUCCESS': 'sum'}).reset_index()
    df_week["SUCCESS_RATE"] = df_week.TOT_SUCCESS / df_week.TOT_VISITS
    df_week = df_week[(df_week.WEEK >= 6) & (df_week.WEEK <= LAST_VALID_WEEK)]
    df_week = df_week.merge(df_addr, left_on='POSTAL_CODE2', right_on='POSTAL_CODE2')
    df_week['VISITS_PER_ADDRESS'] = df_week.TOT_VISITS / df_week.N_ADDRESSES

    df_count = df.groupby([df.DELIVERY_DATE]).agg({'TOT_VISITS': 'sum', 'TOT_SUCCESS': 'sum'}).reset_index()
    df_count = df_count[df_count.TOT_VISITS > 50000]
    df_count["SUCCESS_RATE"] = df_count.TOT_SUCCESS / df_count.TOT_VISITS
    df_count.index = df_count['DELIVERY_DATE']
    df_count = df_count[df_count.index <= LAST_WEEK_DAY]
    df_count = df_count[df_count.index.dayofweek < 5]

    geojson_postal = geopandas.read_file('static/json/postal_codes.geojson')
    geojson_postal_aggr = geopandas.read_file('static/json/postal_codes_aggr.geojson')


def register_plot_for_embedding(name):
    def inside(f):
        f.name = name
        f.get_html_link = lambda: __plots.loc[name].link_html
        f.get_image_link = lambda: __plots.loc[name].link_image
        registered_plots[name] = f
        return f
    return inside
