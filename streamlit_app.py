import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

def main():
    # Sample data with years from 1900 to 2023 and randomly generated y-values
    years = list(range(1900, 2024))
    y_values = np.random.randint(0, 100, len(years))

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

    # Combine the line chart and data points
    chart = (line_chart + data_points).interactive()

    # Add a title to the chart
    st.title("Line Chart with Hover Data Points")

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

    # Add a slider to tweak the years selected
    start_year = st.slider("Select start year:", min_value=min(df['x_values']), max_value=max(df['x_values']), value=min(df['x_values']))
    end_year = st.slider("Select end year:", min_value=min(df['x_values']), max_value=max(df['x_values']), value=max(df['x_values']))

    # Filter the data based on the selected years
    filtered_data = df[(df['x_values'] >= start_year) & (df['x_values'] <= end_year)]

    # Display the filtered data as a table
    st.dataframe(filtered_data)

if __name__ == '__main__':
    main()
