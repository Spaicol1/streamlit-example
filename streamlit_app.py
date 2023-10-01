import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import plotly.express as px

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

# Title
st.title("Italian Provinces Map and Real Estate Dashboard")

# Create a Folium map
m = folium.Map(location=[41.9028, 12.4964], zoom_start=6)

# Add GeoJSON data with choropleth
folium.Choropleth(
    geo_data="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/italy.geojson",
    name="choropleth",
    data=None,  # You can assign province-specific data here if needed
    columns=None,
    key_on="feature.properties.name",
    fill_color="YlGnBu",  # You can use different color schemes
    fill_opacity=0.7,
    line_opacity=0.2,
).add_to(m)

# Display the Folium map using streamlit_folium
sf.folium_static(m)

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
st.write("Real Estate Dashboard")

# Display map
st.write("Map Selection:")
st.write("You can customize the map display here.")
# Create map using Streamlit elements or external libraries

# Display line chart
st.write("Line Chart:")
if st.checkbox("Valore di Mercato $mq"):
    # Create line chart for "Valore di Mercato $mq"
    fig_mercato = px.line(filtered_df, x='Year', y='Valore_Mercato', color='Destinazione_Uso', title="Valore di Mercato $mq")
    st.plotly_chart(fig_mercato)

if st.checkbox("Valore Locazione $mq"):
    # Create line chart for "Valore Locazione $mq"
    fig_locazione = px.line(filtered_df, x='Year', y='Valore_Locazione', color='Destinazione_Uso', title="Valore Locazione $mq")
    st.plotly_chart(fig_locazione)

# Display legend
st.write("Legend:")
if st.checkbox("Show Legend"):
    # Display the legend
    legend_text = "\n".join([f"{uso}: {filtered_df[filtered_df['Destinazione_Uso'] == uso]['Valore_Mercato'].mean():.2f}" for uso in filtered_df['Destinazione_Uso'].unique()])
    st.write(legend_text)

# You can customize the map, line chart, and legend display as needed
