import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from sklearn.neighbors import KernelDensity
import folium
import pydeck as pdk

#st.set_option('server.maxUploadSize', 500 * 1024 * 1024)
st.set_page_config(page_title="pixel challenge",page_icon=":bar_chart:",layout="wide")
@st.experimental_singleton
def inject_css(file_path):
    with open(file_path, 'r') as f:
        css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Call the inject_css function with the path to your CSS file
inject_css('styles.css')
@st.cache_data
def load_data():
    # Load the data from a file or database
    data = pd.read_csv('outputupdated2.csv')
    
    return data

# Load and read the data
df = load_data()

@st.cache_data
def load_data1():
    # Load the data from a file or database
    data = pd.read_csv('contri1.csv')
    
    return data

# Load and read the data
df1 = load_data()
# df = pd.read_csv('output1.csv')
#print(df)
#adding the year column  
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])
df['YEAR'] = df['CRASH DATE'].dt.year

df['CRASH TIME'] = pd.to_datetime(df['CRASH TIME'], format='%H:%M', errors='coerce').dt.time
df['CRASH DATETIME'] = df['CRASH DATE'].astype(str) + ' ' + df['CRASH TIME'].astype(str)
df['CRASH DATETIME'] = pd.to_datetime(df['CRASH DATETIME'], format='%Y-%m-%d %H:%M:%S')

###
#########
@st.cache_data
def generate_bar_graph(df, selected_boroughs, selected_years):
    # Filter the data for multiple collision cases
    multiple_collision_data = df[df['Check Multiple Collision'] == 'Yes']

    # Filter the data based on selected boroughs and years
    filtered_data = multiple_collision_data[
        (multiple_collision_data['BOROUGH'].isin(selected_boroughs)) &
        (multiple_collision_data['YEAR'].isin(selected_years))
    ]

    # Group the data by borough and year and calculate the collision count
    grouped_data = filtered_data.groupby(['BOROUGH', 'YEAR']).size().reset_index(name='Collision Count')

    # Create a color map for each selected borough
    color_map = {borough: f"rgb({i * 30},{i * 30},{i * 30})" for i, borough in enumerate(selected_boroughs)}

    # Add a color column based on the selected boroughs
    grouped_data['Color'] = grouped_data['BOROUGH'].map(color_map)

    # Create a bar graph using Plotly Express
    fig = px.bar(grouped_data, x='YEAR', y='Collision Count', color='BOROUGH',
                 title='Collision Count by Year for Selected Borough(s)',
                 labels={'YEAR': 'Year', 'Collision Count': 'Collision Count'})

    # Update the legend title
    fig.update_layout(legend_title_text='Borough')

    return fig

# Get unique boroughs and years
unique_boroughs = df['BOROUGH'].unique()
unique_years = df['YEAR'].unique()

# Create multiselect boxes for filtering
selected_boroughs = st.multiselect('Select Borough(s)', unique_boroughs, default=unique_boroughs)
selected_years = st.multiselect('Select Year(s)', unique_years, default=unique_years)

# Generate or retrieve the cached bar graph
fig = generate_bar_graph(df, selected_boroughs, selected_years)

# Display the bar graph using Streamlit
st.plotly_chart(fig)
###############import streamlit as st


@st.cache_data
def filter_data(df, selected_boroughs, selected_years):
    return df[(df['BOROUGH'].isin(selected_boroughs)) & (df['YEAR'].isin(selected_years))]

selected_boroughs = st.multiselect('Select Boroughs', df['BOROUGH'].unique(), default=df['BOROUGH'].unique())
selected_years = st.multiselect('Select Years', df['YEAR'].unique(), default=df['YEAR'].unique())

filtered_data = filter_data(df, selected_boroughs, selected_years)

# Categories
categories = ['Cars and Sedans', 'Trucks and Pick-ups', 'Emergency Vehicles', 'Commercial Vehicles']

# Initialize color map for boroughs
color_map = {borough: px.colors.qualitative.Plotly[i] for i, borough in enumerate(selected_boroughs)}

# Calculate the number of accidents per category for each borough
data = []
text_values = []
for borough in selected_boroughs:
    borough_data = []
    borough_text = []
    for category in categories:
        category_data = filtered_data[(filtered_data['BOROUGH'] == borough) & (filtered_data[category] == True)]
        num_accidents = len(category_data)
        borough_data.append(num_accidents)
        borough_text.append(f"{num_accidents}")
    data.append(borough_data)
    text_values.append(borough_text)

# Create the stacked bar graph
bar_graphs = []
for i, borough in enumerate(selected_boroughs):
    bar_graph = go.Bar(name=borough, x=categories, y=data[i], text=text_values[i], textposition='auto',
                       marker_color=color_map[borough])
    bar_graphs.append(bar_graph)

# Set the layout for the graph
layout = go.Layout(
    title='Accidents by Category and Borough',
    xaxis=dict(title='Category'),
    yaxis=dict(title='Number of Accidents'),
    barmode='stack',
)

# Create the figure
fig = go.Figure(data=bar_graphs, layout=layout)

# Display the chart using Streamlit
st.plotly_chart(fig)



##############
# Filter the data based on selected boroughs
@st.cache_data
def filter_data(df, selected_boroughs1):
    return df[df['BOROUGH'].isin(selected_boroughs1)]

selected_boroughs1 = st.multiselect('Select Boroughs to comapre', df['BOROUGH'].unique(), default=df['BOROUGH'].unique())

filtered_data = filter_data(df, selected_boroughs1)

# Extract hour from CRASH DATETIME
filtered_data['HOUR'] = pd.to_datetime(filtered_data['CRASH DATETIME']).dt.hour

# Group the data by hour and calculate the collision count
grouped_data = filtered_data.groupby('HOUR').size().reset_index(name='Collision Count')

# Create a line graph using Plotly Express
fig = px.line(grouped_data, x='HOUR', y='Collision Count', title='Accidents Variation by Time of Day')

# Set the layout for the graph
fig.update_layout(
    xaxis=dict(title='Hour of the Day'),
    yaxis=dict(title='Number of Accidents'),
)

# Display the line graph using Streamlit
st.plotly_chart(fig)




#####
st.markdown('[Go to App A](http://localhost:8501)') 