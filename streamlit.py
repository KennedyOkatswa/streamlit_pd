import streamlit as st
import pandas as pd
import numpy as np

from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import os
import folium
from folium.plugins import HeatMap
from folium.features import Choropleth
import json
from plotly.subplots import make_subplots
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

# Data
column_names = ['timestamp', 'ip_address', 'req_method', 'path', 'status_code', 'country', 'home', 'language', 'navigation', 'content', 'content2', 'content3', 'Date', 'Time']

web_server_logs = pd.read_csv('Final_web_logs.csv')

# Geo data
geo_data='world-countries.geojson',

with open('world-countries.geojson') as response:
    geo = json.load(response)


# Setting the logo 
left_logo, middle_logo, right_logo = st.columns([1, 6, 1])

with left_logo:
    st.text(' ')

with middle_logo:
    logo_image = Image.open('FUN.png').resize((600, 200))
    st.image(logo_image)
with right_logo:
    st.text(' ')

st.markdown("<h1 style='text-align: center; color: grey;'>2023 FunOlympic Games</h1>", unsafe_allow_html=True)


web_server_logs['Date'] = pd.to_datetime(web_server_logs['Date'])
web_server_logs['Time'] = pd.to_datetime(web_server_logs['Time'])
web_server_logs['Time'] = web_server_logs['Time'].dt.strftime('%H:%M')

web_server_logs['Month'] = pd.DatetimeIndex(web_server_logs['Date']).month
web_server_logs['Year'] = pd.DatetimeIndex(web_server_logs['Date']).year

st.markdown("<h2 style='text-align: center; color: black;'>-------------------------------------------------------------------------------</h2>", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: black;'>Analysis of Sports</h1>", unsafe_allow_html=True)


# ---------SIDEBAR ----------------
st.sidebar.header("Please Filter Here: ")
sport = st.sidebar.multiselect(
    "Select the Sport:",
    options= web_server_logs.loc[(web_server_logs['Navigation'] == "sports")]['Content'].unique(),
    default= web_server_logs.loc[(web_server_logs['Navigation'] == "sports")]['Content'].unique()

)

web_logs_selection = web_server_logs.query(
    "Content == @sport"
)



col1, col2, col3 = st.columns([4, 1, 4])

with col1:

    top_foll_spo = web_server_logs.loc[(web_server_logs['Navigation'] == "sports")]['Content']
    top_foll_spo_freq = top_foll_spo.value_counts().sort_values(ascending=False)

    top_followed =  top_foll_spo_freq[0]

    st.subheader("Most accessed Sport")
    st.text(f"{top_foll_spo_freq.index[0]} : {top_foll_spo_freq.values[0]}")
    
    st.markdown("<h4 style='text-align: center;'>Accessed Sport by Top 10 countries</h4>", unsafe_allow_html=True)
    sports_cont = web_logs_selection.loc[(web_logs_selection['Navigation'] == "sports")]['country']
    sports_freq = sports_cont.value_counts()[:10]
    chart = st.bar_chart(sports_freq, width=10, height=0)

    for i, val in enumerate(sports_freq.values):
        plt.text(i, val+1, str(val), ha='center', fontweight='bold')

with col2:
    st.text(" ")
with col3:

    st.subheader("Least accessed Sport")
    st.text(f"{top_foll_spo_freq.index[-1]} : {top_foll_spo_freq.values[-1]}")
    
    st.markdown("<h4 style='text-align: center;'>Accessed Sport by Month</h4>", unsafe_allow_html=True)

    sports_month23 = web_logs_selection.loc[(web_logs_selection['Navigation'] == "sports") & (web_logs_selection['Year'] == 2023) ]['Month']
    sports_month_freq23 = sports_month23.value_counts()

    sports_month22 = web_logs_selection.loc[(web_logs_selection['Navigation'] == "sports") & (web_logs_selection['Year'] == 2022) ]['Month']
    sports_month_freq22 = sports_month22.value_counts()

    st.line_chart(sports_month_freq23)
    st.line_chart(sports_month_freq22)

#############################################################################################

left_column3, middle_column3, right_column3 = st.columns([1, 5, 1])

with left_column3:
    st.text(' ')

with middle_column3:
    st.markdown("<h3 style='text-align: center; color: black;'>Accessibility of Sports around the world</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>How user accessed Sports around the world</h4>", unsafe_allow_html=True)


    sports_country = web_server_logs.loc[(web_server_logs['Navigation'] == "sports")]['country']
    sports_country_freq = sports_country.value_counts()

    world_map = folium.Map(location=[0, 0], zoom_start=2)  

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geo,
        locations= sports_country_freq.index,
        featureidkey='properties.name',
        z=sports_country_freq.values,
        colorscale="sunsetdark",
        marker_opacity=0.5,
        marker_line_width=0
        )
    )

    fig.update_layout(
        mapbox_style= "carto-positron",
        mapbox_zoom=6.6,
        mapbox_center={"lat": 46.8, "lon": 8.2},
        width=800,
        height=600
        )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
with right_column3:
    st.text(" ")

####################################################################################################################
st.markdown("<h1 style='text-align: center; color: black;'>Analysis of Live Events</h1>", unsafe_allow_html=True)


left_column2, right_column2 = st.columns([1, 1])
# define the parameters of the filter



with left_column2:
    sports_month_suc = web_server_logs['Date']
    sports_month_suc_freq = sports_month_suc.dt.month_name().value_counts()
    months = sports_month_suc_freq.index



    month = left_column2.selectbox("Choose Month", months)

    sports_events200 = web_server_logs.loc[(web_server_logs['Navigation'] == "sport-events") & (web_server_logs['Date'].dt.month_name() == month ) & (web_server_logs['status_code'] == 200)]['Content']
    sports_events200_freq = sports_events200.value_counts()

    sports_events204 = web_server_logs.loc[(web_server_logs['Navigation'] == "sport-events") & (web_server_logs['Date'].dt.month_name() == month ) & (web_server_logs['status_code'] == 204)]['Content']
    sports_events204_freq = sports_events204.value_counts()
    st.markdown("<h4 style='text-align: center;'>Live events' that managed to display</h4>", unsafe_allow_html=True)

    fig1, ax1 = plt.subplots()
    ax1.pie(sports_events200_freq.values, labels= sports_events200_freq.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)


    st.markdown("<h4 style='text-align: center;'>Live events' that were not found</h4>", unsafe_allow_html=True)

    fig2, ax2 = plt.subplots()
    ax2.pie(sports_events204_freq.values, labels= sports_events204_freq.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)



with right_column2:

    countries = web_server_logs['country'].unique()
    month = right_column2.selectbox("Choose Countries", countries)

    events_countries = web_server_logs.loc[(web_server_logs['Navigation'] == "sport-events") & (web_server_logs['country'] == month)]['Content']
    events_countries_freq = events_countries.value_counts()

    fig4 = go.Figure()
    fig4.add_trace(
        go.Bar(
            y=events_countries_freq.index,
            x=events_countries_freq.values,
            hovertemplate= "%{x:.2f}",
            orientation='h',
            text = events_countries_freq.values
        ),
    )
    fig4.update_layout(barmode="stack")
    fig4.update_layout(
    
    plot_bgcolor="#f9e5e5",
    width=800,
    height=600,
    title="Watched Live Event Content"
    )
    st.plotly_chart(fig4)

###############################################################################################################################################################
st.markdown("<h1 style='text-align: center; color: black;'>Analysis of Searches</h1>", unsafe_allow_html=True)

left_column4, middle_column4, right_column4 = st.columns([1,5, 1])



with left_column4:
    st.text(' ')

with middle_column4:

    cont = middle_column4.selectbox("Choose Months", months)
    search = web_server_logs.loc[(web_server_logs['Navigation'] == "search") & (web_server_logs['Date'].dt.month_name() == cont )]['Content2']
    search_freq = search.value_counts()

    fig5= go.Figure()
    fig5.add_trace(
        go.Bar(
            y=search_freq.index,
            x=search_freq.values,
            orientation= 'h',
            text= search_freq.values
        ),
    )
    fig5.update_layout(barmode="stack")

    fig5.update_layout(
    
    plot_bgcolor="#f9e5e5",
    width=800,
    height=600,
    title="Searched Content"
    )
    st.plotly_chart(fig5)

with right_column4:
    st.text(" ")


###############################################################################################################################################################
st.markdown("<h1 style='text-align: center; color: black;'>Analysis of Videos</h1>", unsafe_allow_html=True)



right_column5, mid_column5, left_column5 = st.columns([5, 1, 5])

with right_column5:
    suc_videos = web_server_logs.loc[(web_server_logs['Navigation'] == "video") & (web_server_logs['status_code'] == 200)]['Content']
    suc_videos_freq = suc_videos.value_counts()
    st.markdown("<h4 style='text-align: center;'>Successfully played videos</h4>", unsafe_allow_html=True)


    fig5, ax5 = plt.subplots()
    ax5.pie(suc_videos_freq.values, labels= suc_videos_freq.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax5.axis('equal')
    st.pyplot(fig5  )

with left_column5:
    countries5 = web_server_logs['country'].unique()
    country_filter = left_column5.selectbox("Choose Location", countries5)

    notfound_videos = web_server_logs.loc[(web_server_logs['Navigation'] == "video") & (web_server_logs['country'] == country_filter)]['Content']
    notfound_videos_freq = notfound_videos.value_counts()
    videosByMonth = st.bar_chart(notfound_videos_freq, width=10, height=0)

    for i, val in enumerate(notfound_videos_freq.values):
        plt.text(i, val+1, str(val), ha='center', fontweight='bold')



###############################################################################################################################################################
st.markdown("<h1 style='text-align: center; color: black;'>Analysis of Athletes</h1>", unsafe_allow_html=True)
left_column6, mid_column6, right_column6 = st.columns([2, 5, 2])

with mid_column6:
    st.markdown("<h4 style='text-align: center;'>Viewed Athletes</h4>", unsafe_allow_html=True)


    athletes = web_server_logs.loc[(web_server_logs['Navigation'] == "athletes")]['Content']
    athletes_freq = athletes.value_counts()
    athletes = st.bar_chart(athletes_freq, width=10, height=0)

    for i, val in enumerate(athletes_freq.values):
        plt.text(i, val+1, str(val), ha='center', fontweight='bold')

left_column7, mid_column7, right_column7 = st.columns([5, 2, 5])


left_column7.download_button("Download CSV File", data='world-countries.geojson', file_name ="Web server logs", mime = 'text/csv')

if right_column7.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=web_server_logs)
    #st.table(data=df)





















