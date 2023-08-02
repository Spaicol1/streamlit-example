import streamlit as st
import pandas as pd
import altair as alt

def main():
    # Sample data
    data = {
        'x_values': [1, 2, 3, 4, 5],
        'y_values': [10, 5, 7, 12, 8]
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

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

if __name__ == '__main__':
    main()
