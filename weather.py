import streamlit as st
import pandas as pd
import numpy as np
import io
import requests
main = '/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69'
end = "?api-key=579b464db66ec23bdd000001f7f6f89696bc433048b33470cc2d86cd&format=csv&offset=0&limit=1000"
start = "https://api.data.gov.in/"
url = start+main+end
data = requests.get(url)

df = pd.read_csv(io.StringIO(data.text))
df.drop(['id','country','pollutant_unit'],axis=1,inplace=True)
state = st.sidebar.multiselect('select the state:-',
                       df['state'].unique())

city = df.query('state == @state')
city2 = st.sidebar.multiselect('select the city:-',
                       city['city'].unique())
station = df.query('city == @city2')
station2 = st.sidebar.multiselect('select the station:-',
                                 station['station'].unique())
dis = df.query('station == @station2')
pollutant = st.sidebar.multiselect('select the pollutant',df['pollutant_id'].unique())
pollutant2 = dis.query('pollutant_id == @pollutant')
dis2 = pollutant2[['station','pollutant_id','pollutant_avg']]
st.dataframe(dis2)
