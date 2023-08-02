import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Custom CSS to style the sidebar and header
custom_css = """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#f9a32c, #f7941d);
    color: white;
}
.stButton button {
    background-color: #f9a32c !important;
    border-color: #f7941d !important;
    color: white !important;
}
.stSlider div {
    background-color: #f7941d !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def main():
    # Sample data with years from 1900 to 2023 and randomly generated y-values
    years = list(range(1900, 2024))
    y_values = np.random.randint(0, 100, len(years))

    # Sample data for the dropdowns (You can replace these with your own data)
    establishment_types = ['Type A', 'Type B', 'Type C']
    states = ['State A', 'State B', 'State C']
    counties = ['County A', 'County B', 'County C']
    naics = ['NAICs 1', 'NAICs 2', 'NAICs 3']

    # Combine years and y_values into tuples using zip and create a DataFrame
    data = {
        'x_values': years,
        'y_values': y_values
    }
    df = pd.DataFrame(data)

    # Create the line chart using Altair
    line_chart = alt.Chart(df).mark_line().encode(
        x='x_values',
        y='y_values'
    )

    # Add interactive data points using the `circle` mark
    data_points = line_chart.mark_circle().encode(
        tooltip=['x_values', 'y_values']  # Show x and y values on hover
    )

    # Calculate the average value
    avg_value = np.mean(y_values)

    # Create the average line
    avg_line = alt.Chart(pd.DataFrame({'avg_value': [avg_value]})).mark_rule(color='orange').encode(y='avg_value')

    # Combine the line chart, data points, and average line using Altair's layer
    chart = alt.layer(line_chart, data_points, avg_line).interactive()

    # Add a title to the chart
    st.title("Line Chart with Hover Data Points")

    # Add a sidebar for selecting different sets of data and years
    selected_establishment_type = st.sidebar.selectbox("Select Establishment Type:", establishment_types)
    selected_state = st.sidebar.selectbox("Select State:", states)
    selected_county = st.sidebar.selectbox("Select County:", counties)
    selected_naics = st.sidebar.selectbox("Select NAICs:", naics)

    # Add a slider to tweak the years selected
    start_year = st.sidebar.slider("Select start year:", min_value=min(years), max_value=max(years), value=min(years))
    end_year = st.sidebar.slider("Select end year:", min_value=min(years), max_value=max(years), value=max(years))

    # Filter the data based on the selected dropdown values and years
    filtered_data = df  # You can replace this with actual filtering logic based on the selected values and years

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

    # Display the filtered data as a table
    st.dataframe(filtered_data)

if __name__ == '__main__':
    main()

