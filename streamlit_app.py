import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

def calculate_cagr(start_value, end_value, num_years):
    return (end_value / start_value) ** (1 / num_years) - 1

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

    # Calculate mean, median, and CAGR
    mean_value = np.mean(y_values)
    median_value = np.median(y_values)
    start_value, end_value = y_values[0], y_values[-1]
    num_years = len(years) - 1
    cagr_value = calculate_cagr(start_value, end_value, num_years)

    # Create mean, median, and CAGR lines
    mean_line = alt.Chart(pd.DataFrame({'mean_value': [mean_value]})).mark_rule(color='red').encode(y='mean_value')
    median_line = alt.Chart(pd.DataFrame({'median_value': [median_value]})).mark_rule(color='green').encode(y='median_value')
    cagr_line = alt.Chart(pd.DataFrame({'cagr_value': [cagr_value]})).mark_rule(color='blue').encode(y='cagr_value')

    # Combine the line chart, data points, and lines
    chart = (line_chart + data_points + mean_line + median_line + cagr_line).interactive()

    # Add a title to the chart
    st.title("Line Chart with Hover Data Points")

    # Add checkboxes to toggle mean, median, and CAGR lines
    show_mean = st.checkbox("Show Mean Line", value=True)
    show_median = st.checkbox("Show Median Line", value=True)
    show_cagr = st.checkbox("Show CAGR Line", value=True)

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
