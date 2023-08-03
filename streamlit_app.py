import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

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
    # Calculate the average growth over time
    avg_growth = (y_values[-1] - y_values[0]) / (years[-1] - years[0]) * 100
    # Calculate the lowest and highest values
    lowest_value = np.min(y_values)
    highest_value = np.max(y_values)

    # Create the average line
    avg_line = alt.Chart(pd.DataFrame({'avg_value': [avg_value]})).mark_rule(color='orange').encode(y='avg_value')

    # Combine the line chart, data points, and average line using Altair's layer
    chart = alt.layer(line_chart, data_points, avg_line).interactive()

    # Add a title to the chart
    st.title("Line Chart with Hover Data Points")

    # Add a header for the page
    st.header("My Streamlit App")

    # Add the chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.altair_chart(chart, use_container_width=True)

    # Add metrics for average growth, lowest, highest, and average
    with col2:
        st.metric("Average Growth", f"{avg_growth:.2f}%", delta="3.27%")
        st.metric("Lowest Value", lowest_value, delta="-2.12")
        st.metric("Highest Value", highest_value, delta="4.63")
        st.metric("Average Value", avg_value, delta="1.09")

if __name__ == '__main__':
    main()
