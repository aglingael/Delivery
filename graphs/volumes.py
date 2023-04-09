import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext
import plotly.express as px
import plotly.io as pio
from graphs import RUNNING_MODE, MODE

if RUNNING_MODE == MODE.DEVELOPMENT:
    from graphs import register_plot_for_embedding, df_count, geojson_postal_aggr, df_week, LAST_WEEK_DAY  # , LAST_VALID_WEEK, df_addr
if RUNNING_MODE == MODE.PRODUCTION:
    from graphs import register_plot_for_embedding, LAST_WEEK_DAY


if RUNNING_MODE == MODE.DEVELOPMENT:
    df1 = pd.read_csv("static/csv/30_parcels_dailycounts.csv", parse_dates=['DELIVERY_DATE'], sep=',')
    df1['WEEK'] = df1.DELIVERY_DATE.dt.weekofyear
    df1['POSTAL_CODE2'] = df1.POSTAL_CODE // 100

    # df_30_week = df1.groupby([df1.WEEK, df1.POSTAL_CODE2]).agg({'TOT_VISITS': 'sum', 'TOT_SUCCESS': 'sum'}).reset_index()
    # df_30_week["SUCCESS_RATE"] = df_30_week.TOT_SUCCESS / df_30_week.TOT_VISITS
    # df_30_week = df_30_week.loc[(df_30_week.WEEK >= 6) & (df_30_week.WEEK <= LAST_VALID_WEEK)]
    # df_30_week = df_30_week.merge(df_addr, left_on='POSTAL_CODE2', right_on='POSTAL_CODE2')
    # df_30_week['VISITS_PER_ADDRESS'] = df_30_week.TOT_VISITS / df_30_week.N_ADDRESSES
    # df_30_week = pd.read_csv("static/csv/30_parcels_volume_aggr.csv")


@register_plot_for_embedding("volume")
def daily_volume():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        min_y = ((df_count.TOT_VISITS.min()//1000) - 15) * 1000
        max_y = ((df_count.TOT_VISITS.max()//1000) + 15) * 1000
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_count.DELIVERY_DATE, y=df_count.TOT_VISITS, mode="lines+markers"
                      # labels={
                      #     "x": "Date",
                      #     "y": "#Visits"
                      # }
                                 ))
        fig.add_annotation(
            x="2020-03-18",
            y=200000,
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
            y1=500000,
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
            y=200000,
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
            y1=500000,
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
            y=200000,
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
            y=200000,
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
            y=200000,
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
        fig.update_layout(xaxis_title="Delivery date", yaxis_title="Number of visits", margin=dict(l=0, r=0, t=5, b=0),
                          yaxis_range=[min_y, max_y], xaxis_range=["2020-02-03", LAST_WEEK_DAY], height=500)
        pio.write_json(fig, "static/figures/fig_volumes_1.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_volumes_1.json")
        # fig.write_image("/Users/aglin/Desktop/vol1.png", width=900, height=500, scale=8)
    return fig


@register_plot_for_embedding("visits per address")
def weekly_visits_per_address_map():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = px.choropleth_mapbox(geojson=geojson_postal_aggr,
                                   locations=df_week.POSTAL_CODE2,
                                   color=df_week.VISITS_PER_ADDRESS, color_continuous_scale="magma_r",
                                   range_color=(0, 0.4),
                                   animation_frame=df_week.WEEK, animation_group=df_week.POSTAL_CODE2,
                                   featureidkey="properties.aggr_PO",
                                   center={"lat": 50.521111, "lon": 4.668889},
                                   hover_name=df_week.VISITS_PER_ADDRESS,
                                   hover_data=[df_week.TOT_VISITS, df_week.MUNICIPALITY2],
                                   height=600,
                                   labels={
                                       "animation_frame": "Week",
                                       "color": "#Visits per adr",
                                       "locations": "CP2",
                                       "hover_data_0": "#Visits",
                                       "hover_data_1": "Municipality2"
                                   },
                                   mapbox_style="carto-positron", zoom=6.6)
        fig.update_geos(fitbounds="locations")
        fig.layout.coloraxis.colorbar.title = gettext("Number of visits per adress")
        fig.layout.coloraxis.colorbar.titleside = "right"
        fig.layout.coloraxis.colorbar.ticks = "outside"
        fig.layout.coloraxis.colorbar.tickmode = "array"
        fig.update_traces(
            hovertemplate=gettext(gettext("CP2: %{location}(%{customdata[1]})<br>"
                                          "#Visits per adr: %{z:.4f}<br>"
                                          "#Visits: %{customdata[0]}"))
        )
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
        pio.write_json(fig, "static/figures/fig_volumes_2.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_volumes_2.json")
    return fig
