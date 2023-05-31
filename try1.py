import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

#st.set_option('server.maxUploadSize', 500 * 1024 * 1024)
st.set_page_config(page_title="pixel challenge",page_icon=":bar_chart:",layout="wide")

df = pd.read_csv('output1.csv')
#print(df)
#adding the year column  
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])
df['YEAR'] = df['CRASH DATE'].dt.year

df['CRASH TIME'] = pd.to_datetime(df['CRASH TIME'], format='%H:%M', errors='coerce').dt.time
df['CRASH DATETIME'] = df['CRASH DATE'].astype(str) + ' ' + df['CRASH TIME'].astype(str)
df['CRASH DATETIME'] = pd.to_datetime(df['CRASH DATETIME'], format='%Y-%m-%d %H:%M:%S')
#print(df['CRASH DATETIME'])

##########
print(df)