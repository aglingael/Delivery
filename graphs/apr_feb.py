import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext
import plotly.express as px
import numpy as np
import plotly.io as pio
from graphs import RUNNING_MODE, MODE

if RUNNING_MODE == MODE.DEVELOPMENT:
    from graphs import register_plot_for_embedding, df, df_addr, geojson_postal_aggr
if RUNNING_MODE == MODE.PRODUCTION:
    from graphs import register_plot_for_embedding

counts_feb = np.load("static/npy/counts_feb.npy", allow_pickle=True)
bins_feb = np.load("static/npy/bins_feb.npy", allow_pickle=True)
counts_apr = np.load("static/npy/counts_apr.npy", allow_pickle=True)
bins_apr = np.load("static/npy/bins_apr.npy", allow_pickle=True)
feb_bins_count_parcels = np.load("static/npy/feb_bins_count_parcels.npy", allow_pickle=True)
feb_bins_ratio = np.load("static/npy/feb_bins_ratio.npy", allow_pickle=True)
apr_bins_count_parcels = np.load("static/npy/apr_bins_count_parcels.npy", allow_pickle=True)
apr_bins_ratio = np.load("static/npy/apr_bins_ratio.npy", allow_pickle=True)
gap = 2
bins_names = pd.Series(bins_feb)
bins_names = (bins_names - gap).apply(int).apply(str) + "-" + (bins_names + gap).apply(int).apply(str)
n_week_days_apr = 21
n_week_days_feb = 20
counts_ratio = (n_week_days_feb / n_week_days_apr) * counts_apr / counts_feb
ratio_parcels_apr_feb = (n_week_days_feb / n_week_days_apr) * apr_bins_count_parcels / feb_bins_count_parcels

if RUNNING_MODE == MODE.DEVELOPMENT:
    df_ratio_aggr = pd.read_csv("static/csv/postalratio_aggr_avr_fev.csv", sep=',')
    df_ratio_aggr = pd.merge(df_ratio_aggr, df_addr)

    conf_weeks = np.load("static/npy/conf_weeks.npy", allow_pickle=True)
    num_week_new_clients = np.load("static/npy/num_week_new_clients.npy", allow_pickle=True)
    num_week_old_clients = np.load("static/npy/num_week_old_clients.npy", allow_pickle=True)
    num_visits_week_new_clients = np.load("static/npy/num_visits_week_new_clients.npy", allow_pickle=True)
    num_visits_week_old_clients = np.load("static/npy/num_visits_week_old_clients.npy", allow_pickle=True)

    df_ndays = df.groupby(['DELIVERY_DATE'])['TOT_VISITS'].sum().reset_index()
    df_ndays['BUSINESS_DAY'] = df_ndays['TOT_VISITS'].apply(lambda c: 1 if c > 100000 else 0)
    df_ndays = df_ndays.groupby(df_ndays['DELIVERY_DATE'].dt.to_period("M"))['BUSINESS_DAY'].sum().reset_index()

    df_month = df.groupby(['POSTAL_CODE2', df['DELIVERY_DATE'].dt.to_period("M")]).agg(
        {'TOT_VISITS': 'sum'}).reset_index()
    df_month = pd.merge(df_month, df_ndays)
    df_month['AVG_VISITS'] = df_month['TOT_VISITS'] / df_month['BUSINESS_DAY']
    df_month = pd.merge(df_month, df_addr)
    df_month['MUNICIPALITY2'] = df_month.apply(lambda x: x['MUNICIPALITY2'] + " (" + str(x['POSTAL_CODE2']) + ")",
                                               axis=1)
    df_month['AVG_VISITS'] = df_month['AVG_VISITS'] / df_month['N_ADDRESSES']
    df_month = df_month.sort_values(by=['DELIVERY_DATE', 'AVG_VISITS'], ascending=[False, True])
    df_month = df_month.loc[(df_month['DELIVERY_DATE'] == '2020-02') | (df_month['DELIVERY_DATE'] == '2020-04')]

    df_feb = df_month.loc[df_month['DELIVERY_DATE'] == '2020-02']
    df_apr = df_month.loc[df_month['DELIVERY_DATE'] == '2020-04']
    df_feb = df_feb.rename(columns={'AVG_VISITS': 'AVG_VISITS_FEB'}).drop(columns=['DELIVERY_DATE', 'TOT_VISITS', 'BUSINESS_DAY'])
    df_apr = df_apr.rename(columns={'AVG_VISITS': 'AVG_VISITS_APR'}).drop(columns=['DELIVERY_DATE', 'TOT_VISITS', 'BUSINESS_DAY'])
    df_cmp = pd.merge(df_feb, df_apr)


@register_plot_for_embedding("increase ratio aggr")
def postal_aggr_increase():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = px.choropleth_mapbox(geojson=geojson_postal_aggr,
                                   locations=df_ratio_aggr.POSTAL_CODE2,
                                   color=round(df_ratio_aggr.RATIO, 4), color_continuous_scale="magma_r",
                                   featureidkey="properties.aggr_PO",
                                   center={"lat": 50.521111, "lon": 4.668889},
                                   hover_name=round(df_ratio_aggr.RATIO, 4),
                                   hover_data=[df_ratio_aggr.MUNICIPALITY2],
                                   height=500,
                                   labels={
                                       "color": "Ratio",
                                       "locations": "CP2",
                                       "hover_data_0": "Municipality2"
                                   },
                                   mapbox_style="carto-positron", zoom=6.6)
        fig.update_geos(fitbounds="locations")
        fig.layout.coloraxis.colorbar.title = gettext("Ratio of parcels delivered in April over February")
        fig.layout.coloraxis.colorbar.titleside = "right"
        fig.layout.coloraxis.colorbar.ticks = "outside"
        fig.layout.coloraxis.colorbar.tickmode = "array"
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
        pio.write_json(fig, "static/figures/fig_apr_feb_1.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_apr_feb_1.json")
    return fig


@register_plot_for_embedding("number visit dist feb apr")
def hist_feb_apr():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=bins_feb, y=counts_feb, name="February", customdata=bins_names))
        fig.add_trace(go.Bar(x=bins_apr, y=counts_apr, name="April", customdata=bins_names))
        fig.update_traces(
            hovertemplate=gettext(gettext("#VISITS: [%{customdata}]<br>#ADDRESSES: %{y}"))
        )
        fig.update_layout(xaxis_title="Number of visits", yaxis_title="Number of addresses", yaxis_type="log",
                          margin=dict(l=0, r=0, t=5, b=0), height=500)
        pio.write_json(fig, "static/figures/fig_apr_feb_2.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_apr_feb_2.json")
    return fig


@register_plot_for_embedding("postal dot plot")
def postal_dot_plot():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = px.scatter(x=round(df_month.AVG_VISITS, 4), y=df_month.MUNICIPALITY2, color=df_month.DELIVERY_DATE,
                         labels={
                             "x": "Avg visits per adr",
                             "y": "Municipality2",
                             "color": "Month"
                         })
        fig.update_layout(height=1200, yaxis=dict(tickvals=df_month.MUNICIPALITY2))
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0),
                          xaxis_title="Average visits per address",
                          yaxis_title="Municipality2")
        pio.write_json(fig, "static/figures/fig_apr_feb_3.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_apr_feb_3.json")
    return fig


@register_plot_for_embedding("postal april vs february")
def postal_apr_feb():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = px.scatter(x=round(df_cmp.AVG_VISITS_FEB, 4), y=round(df_cmp.AVG_VISITS_APR, 4), color=df_cmp.MUNICIPALITY2,
                         labels={
                             "x": "Avg visits feb",
                             "y": "Avg visits apr",
                             "color": "Municipality2"
                         })
        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0),
                          xaxis_title="Average visits per address in February",
                          yaxis_title="Average visits per address in April")
        pio.write_json(fig, "static/figures/fig_apr_feb_4.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_apr_feb_4.json")
    return fig


@register_plot_for_embedding("ratio n_address april vs february")
def ratio_nadr_apr_feb():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = go.Figure()
        fig.add_shape(
            # Line reference to the axes
            type="line",
            xref="x",
            yref="y",
            x0="0",
            y0=1,
            x1=bins_feb[-1] + gap,
            y1=1,
            line=dict(
                color="#000000",
                width=0.6,
            ),
            # layer="below"
        )
        fig.add_trace(go.Bar(x=bins_feb, y=counts_ratio,
                             customdata=pd.DataFrame(list(zip(counts_apr, counts_feb, bins_names, apr_bins_ratio)))))
        fig.update_layout(xaxis_title="Number of parcels", yaxis_title="Ratio #addresses April over February",
                          margin=dict(l=0, r=0, t=5, b=0), height=500)
        fig.update_traces(
            hovertemplate="#VISITS: [%{customdata[2]}]<br>"
                          "Addresses ratio: %{y:.4f}<br>"
                          "%April visits: %{customdata[3]:.3f}%<br>"
                          "#April addresses: %{customdata[0]}<br>"
                          "#February addresses: %{customdata[1]}"
                          "<extra></extra>")
        pio.write_json(fig, "static/figures/fig_apr_feb_5.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_apr_feb_5.json")
    return fig


@register_plot_for_embedding("ratio n_visits april vs february")
def ratio_nvisits_apr_feb():
    color_scale_values = [0, 10, 100, 1000, 10000, 100000, 1000000, 4000000]
    color_scale_real_values = [0] + list(map(np.log, color_scale_values[1:]))
    color_scale_labels = ["1", "10", "100", "1K", "10K", "100K", "1M", "4M"]
    fig = go.Figure()
    fig.add_shape(
        # Line reference to the axes
        type="line",
        xref="x",
        yref="y",
        x0="0",
        y0=1,
        x1=bins_feb[-1] + gap,
        y1=1,
        line=dict(
            color="#000000",
            width=0.6,
        ),
        # layer="below"
    )
    fig.add_trace(go.Bar(
        x=bins_feb,
        y=ratio_parcels_apr_feb,
        marker=dict(
            color=np.log(apr_bins_count_parcels),
            colorbar=dict(title='Number of visits<br>in April',
                          tickvals=color_scale_real_values,
                          ticktext=color_scale_labels),
            colorscale="magma_r"
        ),
        customdata=pd.DataFrame(list(zip(apr_bins_count_parcels, feb_bins_count_parcels, bins_names, apr_bins_ratio)))
    ))
    # fig.add_trace(go.Scatter(x=[0, bins_feb[-1]], y=[1, 1], mode='lines', marker=dict(color="#000000"), showlegend=False, line=dict(width=1)))
    fig.update_layout(xaxis_title="Number of parcels", yaxis_title="Ratio #visits April over February",
                      margin=dict(l=0, r=0, t=5, b=0), height=500, showlegend=False)
    fig.update_traces(
        hovertemplate="#VISITS: [%{customdata[2]}]<br>"
                      "Visits ratio: %{y:.4f}<br>"
                      "%April visits: %{customdata[3]:.3f}%<br>"
                      "#April visits: %{customdata[0]}<br>"
                      "#February visits: %{customdata[1]}"
                      "<extra></extra>")
    pio.write_json(fig, "static/figures/fig_apr_feb_6.json")
    # fig = pio.read_json("static/figures/fig_apr_feb_6.json")
    return fig


@register_plot_for_embedding("april parcels distribution")
def apr_parcels_dist():
    fig = None
    if RUNNING_MODE == MODE.DEVELOPMENT:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=bins_feb,
            y=apr_bins_ratio,
            marker=dict(
                color=ratio_parcels_apr_feb,
                colorbar=dict(title='Ratio #visits<br>April over February'),
                colorscale="magma_r"
            ),
            customdata=pd.DataFrame(
                list(zip(apr_bins_count_parcels, feb_bins_count_parcels, bins_names, ratio_parcels_apr_feb)))
        ))
        fig.update_layout(xaxis_title="Number of parcels", yaxis_title="Percentage of April visits",
                          margin=dict(l=0, r=0, t=5, b=0), height=500)
        fig.update_traces(
            hovertemplate="#VISITS: [%{customdata[2]}]<br>"
                          "%April visits: %{y:.3f}%<br>"
                          "Ratio: %{customdata[3]:.4f}<br>"
                          "#April visits: %{customdata[0]}<br>"
                          "#February visits: %{customdata[1]}"
                          "<extra></extra>")
        pio.write_json(fig, "static/figures/fig_apr_feb_7.json")
    if RUNNING_MODE == MODE.PRODUCTION:
        fig = pio.read_json("static/figures/fig_apr_feb_7.json")
    return fig
