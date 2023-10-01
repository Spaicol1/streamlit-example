import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sample data (you can replace this with your own data)
df = pd.DataFrame({
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Provincia': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'Comune': ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
    'Fascia_Zona': ['Z1', 'Z2', 'Z3', 'Z1', 'Z2', 'Z3', 'Z1', 'Z2', 'Z3'],
    'Destinazione_Uso': ['D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D1', 'D2', 'D3'],
    'Valore_Mercato': [100, 110, 120, 90, 95, 100, 80, 85, 90],
    'Valore_Locazione': [80, 85, 90, 70, 75, 80, 60, 65, 70]
})

# Function to create the map
def create_map(df, selection):
    fig = px.scatter_geo(df, lat=[0], lon=[0], text=selection, scope="world")
    fig.update_geos(projection_type="natural earth")
    return fig

# Function to create the line chart
def create_line_chart(df, selection):
    fig = px.line(df, x='Year', y=selection, color='Fascia_Zona')
    return fig

# Sidebar for variable selection
st.sidebar.title("Variable Selection")

year = st.sidebar.slider("Select Year", min_value=df['Year'].min(), max_value=df['Year'].max())
provincia = st.sidebar.selectbox("Select Provincia", df['Provincia'].unique())
comune = st.sidebar.selectbox("Select Comune", df[df['Provincia'] == provincia]['Comune'].unique())
fascia_zona = st.sidebar.selectbox("Select Fascia/Zona", df[(df['Provincia'] == provincia) & (df['Comune'] == comune)]['Fascia_Zona'].unique())
destinazione_uso = st.sidebar.multiselect("Select Destinazione d'uso", df['Destinazione_Uso'].unique())

# Filter data based on selections
filtered_df = df[(df['Year'] == year) & (df['Provincia'] == provincia) & (df['Comune'] == comune) & (df['Fascia_Zona'] == fascia_zona) & (df['Destinazione_Uso'].isin(destinazione_uso))]

# Right side for displaying charts and legend
st.title("Real Estate Dashboard")

# Display map
st.write("Map Selection:")
st.write("You can customize the map display here.")
map_fig = create_map(filtered_df, 'Provincia')
st.plotly_chart(map_fig)

# Display line chart
st.write("Line Chart:")
if st.checkbox("Valore di Mercato $mq"):
    line_chart_fig = create_line_chart(filtered_df, 'Valore_Mercato')
    st.plotly_chart(line_chart_fig)

if st.checkbox("Valore Locazione $mq"):
    line_chart_fig = create_line_chart(filtered_df, 'Valore_Locazione')
    st.plotly_chart(line_chart_fig)

# Display legend
st.write("Legend:")
if st.checkbox("Show Legend"):
    legend_text = "\n".join([f"{fascia}: {filtered_df[filtered_df['Fascia_Zona'] == fascia]['Valore_Mercato'].mean():.2f}" for fascia in filtered_df['Fascia_Zona'].unique()])
    st.write(legend_text)
