import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext
import plotly.express as px
import numpy as np
import plotly.io as pio
from plotly.subplots import make_subplots
from graphs import RUNNING_MODE, MODE

if RUNNING_MODE == MODE.DEVELOPMENT:
    from graphs import register_plot_for_embedding, geojson_postal_aggr, LAST_VALID_WEEK
if RUNNING_MODE == MODE.PRODUCTION:
    from graphs import register_plot_for_embedding, LAST_VALID_WEEK


if RUNNING_MODE == MODE.DEVELOPMENT:
    conf_weeks = np.load("static/npy/conf_weeks.npy", allow_pickle=True)
    num_week_new_clients = np.load("static/npy/num_week_new_clients.npy", allow_pickle=True)
    num_week_old_clients = np.load("static/npy/num_week_old_clients.npy", allow_pickle=True)
    num_visits_week_new_clients = np.load("static/npy/num_visits_week_new_clients.npy", allow_pickle=True)
    num_visits_week_old_clients = np.load("static/npy/num_visits_week_old_clients.npy", allow_pickle=True)
    cum_week_new_clients = np.load("static/npy/cum_week_new_clients.npy", allow_pickle=True)
    cum_week_old_clients = np.load("static/npy/cum_week_old_clients.npy", allow_pickle=True)
    num_week_new_ex_clients = np.load("static/npy/num_week_new_ex_clients.npy", allow_pickle=True)
    num_week_old_ex_clients = np.load("static/npy/num_week_old_ex_clients.npy", allow_pickle=True)

    df_new_agg = pd.read_csv('static/csv/new_clients_weeks_postal_aggr.csv')
    df_new_agg = df_new_agg[(df_new_agg.WEEK > 9) & (df_new_agg.WEEK <= LAST_VALID_WEEK)]


@register_plot_for_embedding("new clients weeks")
def new_clients_weeks_percent_visits():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = go.Figure()
        fig.add_annotation(
            x=12.35,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=12.5,
            y0=0,
            x1=12.5,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="LightSalmon",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=18.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=19,
            y0=0,
            x1=19,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="CadetBlue",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=19.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=20,
            y0=0,
            x1=20,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="PaleTurquoise",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=20.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=21,
            y0=0,
            x1=21,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="PaleTurquoise",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=23.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=24,
            y0=0,
            x1=24,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="PaleTurquoise",
            # layer="below",
            # line_width=2,
        )
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=num_visits_week_new_clients[1:],
            name='New customers',
            mode='lines',
            customdata=num_visits_week_new_clients[1:],
            line=dict(width=0.5, color='rgb(131, 90, 241)'),
            stackgroup='one',  # define stack group
            groupnorm='percent'
        ))
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=num_visits_week_old_clients[1:],
            name='Old customers',
            mode='lines',
            customdata=num_visits_week_old_clients[1:],
            line=dict(width=0.5, color='rgb(111, 231, 219)'),
            stackgroup='one'
        ))
        fig.update_layout(yaxis_range=(0, 100), xaxis_title="Weeks", yaxis_title="Percentage of visits",
                          xaxis_range=[10, LAST_VALID_WEEK], margin=dict(l=0, r=0, t=5, b=0))
        fig.update_traces(hovertemplate=gettext("Week: %{x}<br>% visits: %{y:.2f}<br># visits: %{customdata}<extra></extra>"))
        pio.write_json(fig, "static/figures/fig_nc_1.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_nc_1.json")
    return fig


@register_plot_for_embedding("new clients weeks")
def new_clients_weeks_percent_address():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = go.Figure()
        fig.add_annotation(
            x=12.35,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=12.5,
            y0=0,
            x1=12.5,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="LightSalmon",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=18.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=19,
            y0=0,
            x1=19,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="CadetBlue",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=19.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=20,
            y0=0,
            x1=20,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="PaleTurquoise",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=20.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=21,
            y0=0,
            x1=21,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="PaleTurquoise",
            # layer="below",
            # line_width=2,
        )
        fig.add_annotation(
            x=23.85,
            y=30,
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
            type="line",
            xref="x",
            yref="y",
            x0=24,
            y0=0,
            x1=24,
            y1=100,
            line=dict(
                color="#000000",
                width=2,
                dash="dashdot"
            ),
            # fillcolor="PaleTurquoise",
            # layer="below",
            # line_width=2,
        )
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=num_week_new_clients[1:],
            name='New customers',
            mode='lines',
            customdata=num_week_new_clients[1:],
            line=dict(width=0.5, color='rgb(131, 90, 241)'),
            stackgroup='one',  # define stack group
            groupnorm='percent'
        ))
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=num_week_old_clients[1:],
            name='Old customers',
            mode='lines',
            customdata=num_week_old_clients[1:],
            line=dict(width=0.5, color='rgb(111, 231, 219)'),
            stackgroup='one'
        ))
        fig.update_layout(yaxis_range=(0, 100), xaxis_title="Weeks", yaxis_title="Percentage of addresses",
                          xaxis_range=[10, LAST_VALID_WEEK], margin=dict(l=0, r=0, t=5, b=0))
        fig.update_traces(hovertemplate=gettext("Week: %{x}<br>% addresses: %{y:.2f}<br># addresses: %{customdata}<extra></extra>"))
        pio.write_json(fig, "static/figures/fig_nc_2.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_nc_2.json")
    return fig


@register_plot_for_embedding("cumulative new clients weeks")
def cum_clients_weeks_address():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        max_height = 2500000
        fig = go.Figure()
        fig.add_annotation(
            x=12.5,
            y=500000,
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
            x0=12.5,
            y0=0,
            x1=19,
            y1=max_height,
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
            x=19,
            y=500000,
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
            x0=19,
            y0=0,
            x1=20,
            y1=max_height,
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
            x=20,
            y=500000,
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
            x0=20,
            y0=0,
            x1=21,
            y1=max_height,
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
            x=21,
            y=500000,
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
            x0=21,
            y0=0,
            x1=24,
            y1=max_height,
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
            x=24,
            y=500000,
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
            x0=24,
            y0=0,
            x1=26,
            y1=max_height,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="Green",
            opacity=0.3,
            layer="below",
            line_width=0,
        )
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=cum_week_new_clients[1:],
            name='New customers',
            mode='lines+markers',
            customdata=cum_week_new_clients[1:],
            line=dict(width=1.5),
            # stackgroup='two',  # define stack group
        ))
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=cum_week_old_clients[1:],
            name='Old customers',
            mode='lines+markers',
            customdata=cum_week_old_clients[1:],
            line=dict(width=1.5),
            # stackgroup='one'
        ))
        fig.update_layout(xaxis_title="Weeks", yaxis_title="Number of addresses", margin=dict(l=0, r=0, t=5, b=0),
                          xaxis_range=[10, LAST_VALID_WEEK], yaxis_range=[min(min(cum_week_old_clients[1:]), min(cum_week_new_clients[1:]))-100000,
                                                             max(max(cum_week_old_clients[1:]), max(cum_week_new_clients[1:]))+100000])
        fig.update_traces(hovertemplate=gettext("Week: %{x}<br>#addresses: %{y}<extra></extra>"))
        pio.write_json(fig, "static/figures/fig_nc_3.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_nc_3.json")
    return fig


@register_plot_for_embedding("exclusive new clients weeks")
def ex_clients_weeks_address():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        # fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_annotation(
            x=12.5,
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
            x0=12.5,
            y0=0,
            x1=19,
            y1=600000,
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
            x=19,
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
            x0=19,
            y0=0,
            x1=20,
            y1=600000,
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
            x=20,
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
            x0=20,
            y0=0,
            x1=21,
            y1=600000,
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
            x=21,
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
            x0=21,
            y0=0,
            x1=24,
            y1=600000,
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
            x=24,
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
            x0=24,
            y0=0,
            x1=26,
            y1=600000,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=3,
            # ),
            fillcolor="Green",
            opacity=0.3,
            layer="below",
            line_width=0,
        )
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=num_week_new_ex_clients[1:],
            name='Week new customers',
            mode='lines+markers',
            customdata=num_week_new_ex_clients[1:],
            line=dict(width=1.5),
            # stackgroup='two',  # define stack group
        ), secondary_y=False, )
        fig.add_trace(go.Scatter(
            x=conf_weeks[1:],
            y=num_week_new_clients[1:],
            name='All new customers<br>parcels',
            mode='lines+markers',
            customdata=num_week_new_clients[1:],
            line=dict(width=1.5),
            # stackgroup='two',  # define stack group
        ), secondary_y=True, )
        fig.update_traces(hovertemplate=gettext("Week: %{x}<br># addresses: %{y}<extra></extra>"))
        fig.update_yaxes(title_text="Number of week new customers", secondary_y=False,
                         range=[min(min(num_week_new_ex_clients[1:]), min(num_week_new_clients[1:])) - 5000,
                                max(max(num_week_new_ex_clients[1:]), max(num_week_new_clients[1:])) + 10000]
                         )
        fig.update_yaxes(title_text="Number of parcels of all new customers", secondary_y=True,
                         range=[min(min(num_week_new_ex_clients[1:]), min(num_week_new_clients[1:])) - 5000,
                                max(max(num_week_new_ex_clients[1:]), max(num_week_new_clients[1:])) + 10000]
                         )
        fig.update_layout(xaxis_title="Weeks", margin=dict(l=0, r=0, t=5, b=0),
                          xaxis_range=[10, LAST_VALID_WEEK],
                          # yaxis_range=[min(min(num_week_new_ex_clients[1:]), min(num_week_new_clients[1:]))-5000,
                          #              max(max(num_week_new_ex_clients[1:]), max(num_week_new_clients[1:]))+10000]
                          )

        # fig.add_trace(go.Scatter(
        #     x=conf_weeks[1:],
        #     y=num_week_new_ex_clients[1:],
        #     name='New customers',
        #     mode='lines+markers',
        #     customdata=num_week_new_ex_clients[1:],
        #     line=dict(width=1.5),
        #     # stackgroup='two',  # define stack group
        # ))
        # fig.update_layout(xaxis_title="Weeks", yaxis_title="Number of addresses", margin=dict(l=0, r=0, t=5, b=0),
        #                   xaxis_range=[10, LAST_VALID_WEEK], yaxis_range=[min(num_week_new_ex_clients[1:])-5000, max(num_week_new_ex_clients[1:])+10000])
        # fig.update_traces(hovertemplate=gettext("Week: %{x}<br># addresses: %{y}<extra></extra>"))
        pio.write_json(fig, "static/figures/fig_nc_4.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_nc_4.json")
    return fig


@register_plot_for_embedding("normalized_new_clients_distribution")
def norm_new_clients_dist():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = px.choropleth_mapbox(geojson=geojson_postal_aggr,
                                   locations=df_new_agg.POSTAL_CODE2,
                                   color=df_new_agg.NORM_NEW, color_continuous_scale="magma_r",
                                   animation_frame=df_new_agg.WEEK, animation_group=df_new_agg.POSTAL_CODE2,
                                   featureidkey="properties.aggr_PO",
                                   center={"lat": 50.521111, "lon": 4.668889},
                                   hover_name=df_new_agg.NORM_NEW,
                                   hover_data=[df_new_agg.MUNICIPALITY2],
                                   height=600,
                                   labels={
                                       "animation_frame": "Week",
                                       "color": "#New clients per addr",
                                       "locations": "CP2",
                                       "hover_data_0": "Municipality2"
                                   },
                                   mapbox_style="carto-positron", zoom=6.6)
        fig.update_geos(fitbounds="locations")
        fig.layout.coloraxis.colorbar.title = gettext("#New clients per address")
        fig.layout.coloraxis.colorbar.titleside = "right"
        fig.layout.coloraxis.colorbar.ticks = "outside"
        fig.layout.coloraxis.colorbar.tickmode = "array"
        fig.update_traces(
            hovertemplate=gettext(gettext("CP2: %{location}(%{customdata[0]})<br>"
                                          "#New clients per address: %{z:.4f}"))
        )
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
        pio.write_json(fig, "static/figures/fig_nc_5.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_nc_5.json")
    return fig
