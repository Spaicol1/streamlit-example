import streamlit as st
from st.nivo import geomap, line
import pandas as pd

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

# Sidebar for variable selection
st.sidebar.title("Map Selection")

# Placeholder to display selected location information
selected_location = st.sidebar.empty()

# Placeholder for the map
map_container = st.empty()

# Placeholder for line charts
line_chart_container = st.empty()

# Create a map with a default view of Italy
italian_map_data = {
    "features": [],
    "config": {
        "center": [41.87194, 12.56738],  # Centered on Italy
        "zoom": 5,
    },
}

italian_map = geomap(italian_map_data, height=400)
map_container.st_nivo_chart(italian_map)

# Right side for displaying charts and legend
st.title("Real Estate Dashboard")

# Display line chart
st.write("Line Chart:")
if st.checkbox("Valore di Mercato $mq"):
    line_chart_fig = line(df, x='Year', y='Valore_Mercato', height=400)
    line_chart_container.st_nivo_chart(line_chart_fig)

if st.checkbox("Valore Locazione $mq"):
    line_chart_fig = line(df, x='Year', y='Valore_Locazione', height=400)
    line_chart_container.st_nivo_chart(line_chart_fig)

# Display legend
st.write("Legend:")
if st.checkbox("Show Legend"):
    legend_text = "\n".join([f"{fascia}: {df[df['Fascia_Zona'] == fascia]['Valore_Mercato'].mean():.2f}" for fascia in df['Fascia_Zona'].unique()])
    st.write(legend_text)
