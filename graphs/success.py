import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext
import plotly.express as px
import plotly.io as pio
from graphs import RUNNING_MODE, MODE

if RUNNING_MODE == MODE.DEVELOPMENT:
    from graphs import register_plot_for_embedding, df_count, geojson_postal_aggr, LAST_VALID_WEEK, df_week, LAST_WEEK_DAY
if RUNNING_MODE == MODE.PRODUCTION:
    from graphs import register_plot_for_embedding, LAST_WEEK_DAY


if RUNNING_MODE == MODE.DEVELOPMENT:
    df_week_hour = pd.read_csv("static/csv/stats_week_hour.csv", sep=',')
    df_week_hour = df_week_hour.loc[(df_week_hour['WEEK'] >= 6) & (df_week_hour['WEEK'] <= LAST_VALID_WEEK)]
    df_week_hour = df_week_hour.loc[(df_week_hour['HOUR'] >= 8) & (df_week_hour['HOUR'] <= 15)]
    df_week_hour['TOT_SUCCESS'] = df_week_hour['TOT_SUCCESS'] / df_week_hour['TOT_VISITS']
    df_week_hour.rename(columns={"TOT_SUCCESS": "SUCCESS_RATE"}, inplace=True)

    df_30_success = pd.read_csv("static/csv/30_parcels_dailycounts.csv", parse_dates=['DELIVERY_DATE'])
    df_30_success = df_30_success.groupby([df_30_success.DELIVERY_DATE]).agg({'TOT_VISITS': 'sum', 'TOT_SUCCESS': "sum"}).reset_index()
    df_30_success = df_30_success[df_30_success.TOT_VISITS > 50000]
    df_30_success["SUCCESS_RATE"] = df_30_success.TOT_SUCCESS / df_30_success.TOT_VISITS
    df_30_success.index = df_30_success.DELIVERY_DATE
    df_30_success = df_30_success[df_30_success.index <= LAST_WEEK_DAY]
    df_30_success = df_30_success[df_30_success.index.dayofweek < 5]


@register_plot_for_embedding("success")
def daily_success():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        min_y = min(df_count.SUCCESS_RATE.min(), df_30_success.SUCCESS_RATE.min())*100 - 0.3
        max_y = max(df_count.SUCCESS_RATE.max(), df_30_success.SUCCESS_RATE.max())*100 + 0.3
        fig = go.Figure()
        fig.add_annotation(
            x="2020-03-18",
            y=86,
            xref="x",
            yref="y",
            text="<b>Beginning of confinement</b>",
            align='center',
            showarrow=False,
            font=dict(size=16),
            yanchor='bottom',
            textangle=270
        )
        fig.add_shape(
            # Line reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0="2020-03-18",
            y0=0,
            x1="2020-05-04",
            y1=100,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
        fig.add_annotation(
            x="2020-05-04",
            y=86,
            xref="x",
            yref="y",
            text="<b>Phase 1A of deconfinement</b>",
            align='center',
            showarrow=False,
            font=dict(size=16),
            yanchor='bottom',
            textangle=270
        )
        fig.add_shape(
            # Line reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0="2020-05-04",
            y0=0,
            x1="2020-05-11",
            y1=100,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="CadetBlue",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
        fig.add_annotation(
            x="2020-05-11",
            y=86,
            xref="x",
            yref="y",
            text="<b>Phase 1B of deconfinement</b>",
            align='center',
            showarrow=False,
            font=dict(size=16),
            yanchor='bottom',
            textangle=270
        )
        fig.add_shape(
            # Line reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0="2020-05-11",
            y0=0,
            x1="2020-05-18",
            y1=500000,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="PaleTurquoise",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
        fig.add_annotation(
            x="2020-05-18",
            y=86,
            xref="x",
            yref="y",
            text="<b>Phase 2 of deconfinement</b>",
            align='center',
            showarrow=False,
            font=dict(size=16),
            yanchor='bottom',
            textangle=270
        )
        fig.add_shape(
            # Line reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0="2020-05-18",
            y0=0,
            x1="2020-06-08",
            y1=500000,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="Yellow",
            opacity=0.2,
            layer="below",
            line_width=0,
        )
        fig.add_annotation(
            x="2020-06-08",
            y=86,
            xref="x",
            yref="y",
            text="<b>Phase 3 of deconfinement</b>",
            align='center',
            showarrow=False,
            font=dict(size=16),
            yanchor='bottom',
            textangle=270
        )
        fig.add_shape(
            # Line reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0="2020-06-08",
            y0=0,
            x1="2020-07-01",
            y1=500000,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="Green",
            opacity=0.3,
            layer="below",
            line_width=0,
        )
        fig.add_trace(go.Scatter(x=df_count.DELIVERY_DATE, y=round(df_count.SUCCESS_RATE * 100, 2),
                                 mode='lines',
                                 name='all customers'))
        fig.add_trace(go.Scatter(x=df_30_success.DELIVERY_DATE, y=round(df_30_success.SUCCESS_RATE * 100, 2),
                                 mode='lines',
                                 name='less frequent<br>customers'))
        fig.update_layout(xaxis_title="Delivery date", yaxis_title="Success rate in %",
                          yaxis_range=[min_y, max_y], xaxis_range=["2020-02-03", LAST_WEEK_DAY],
                          margin=dict(l=0, r=0, t=5, b=0), height=500)
        fig.update_traces(hovertemplate=gettext(gettext("Date: %{x}<br>Success rate: %{y:.2f}%")))
        pio.write_json(fig, "static/figures/fig_success_1.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_success_1.json")
    return fig


@register_plot_for_embedding("success map week")
def success_map_week_year_slider():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = px.choropleth_mapbox(geojson=geojson_postal_aggr,
                                   locations=df_week.POSTAL_CODE2,
                                   color=round(df_week.SUCCESS_RATE*100, 2), color_continuous_scale="magma_r",
                                   range_color=(85, 100),
                                   animation_frame=df_week.WEEK, animation_group=df_week.POSTAL_CODE2,
                                   featureidkey="properties.aggr_PO",
                                   center={"lat": 50.521111, "lon": 4.668889},
                                   hover_name=round(df_week.SUCCESS_RATE*100, 2),
                                   hover_data=[df_week.TOT_VISITS, df_week.MUNICIPALITY2],
                                   height=600,
                                   labels={
                                       "animation_frame": "Week",
                                       "color": "%Success rate",
                                       "locations": "CP2",
                                       "hover_data_0": "#Visits",
                                       "hover_data_1": "Municipality2"
                                   },
                                   mapbox_style="carto-positron", zoom=6.6)
        fig.update_geos(fitbounds="locations")
        fig.layout.coloraxis.colorbar.title = gettext("Success rate in %")
        fig.layout.coloraxis.colorbar.titleside = "right"
        fig.layout.coloraxis.colorbar.ticks = "outside"
        fig.layout.coloraxis.colorbar.tickmode = "array"
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
        pio.write_json(fig, "static/figures/fig_success_2.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_success_2.json")
    return fig


@register_plot_for_embedding("success rates by hour and week")
def success_by_hour_and_week_slider():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        min_y = df_week_hour.SUCCESS_RATE.min()*100 - 0.3
        max_y = df_week_hour.SUCCESS_RATE.max()*100 + 0.3
        fig = px.bar(x=df_week_hour.HOUR, y=round(df_week_hour.SUCCESS_RATE*100, 2), color=df_week_hour.TOT_VISITS,
                     animation_frame=df_week_hour.WEEK, range_y=[min_y, max_y], color_continuous_scale="magma_r",
                     labels={
                         "animation_frame": "Week",
                         "color": "#Visits",
                         "x": "Hour",
                         "y": "%Success rate"
                     },
                     height=500,
                     range_color=(100000, 450000))
        fig.layout.coloraxis.colorbar.title = gettext("Number of parcels")
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0), xaxis_title="Delivery hour", yaxis_title="Success rate in %")
        pio.write_json(fig, "static/figures/fig_success_3.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_success_3.json")
    return fig


@register_plot_for_embedding("success and volume by postal")
def success_volume_by_postal_slider():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        min_y = df_week.VISITS_PER_ADDRESS.min() - 0.03
        max_y = df_week.VISITS_PER_ADDRESS.max() + 0.03
        min_x = df_week.SUCCESS_RATE.min()*100 - 0.3
        max_x = df_week.SUCCESS_RATE.max()*100 + 0.3
        fig = px.scatter(x=round(df_week.SUCCESS_RATE*100, 2), y=df_week.VISITS_PER_ADDRESS, animation_frame=df_week.WEEK,
                         size=df_week.TOT_VISITS, color=df_week.MUNICIPALITY2, hover_name=df_week.MUNICIPALITY2, range_x=[min_x, max_x],
                         hover_data=[df_week.POSTAL_CODE2],
                         labels={
                             "animation_frame": "Week",
                             "color": "Municipality2",
                             "x": "%Success rate",
                             "y": "Avg visits per address",
                             "size": "#Visits",
                             "hover_data_0": "CP2"
                         },
                         height=500,
                         range_y=[min_y, max_y], log_y=False)
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0), xaxis_title="Success rate in %", yaxis_title="Average visits per address")
        pio.write_json(fig, "static/figures/fig_success_4.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_success_4.json")
    return fig