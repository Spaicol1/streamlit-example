import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

# Function to filter data based on user selection
def filter_data(data, column, min_val, max_val):
    return data[(data[column] >= min_val) & (data[column] <= max_val)]

def main():
    st.title('Line Chart with Selection Bars')

    # Sidebar selection bars
    selected_column = st.sidebar.selectbox('Select Column to Filter', chart_data.columns)
    min_value = st.sidebar.slider('Select Min Value', float(chart_data[selected_column].min()), float(chart_data[selected_column].max()), float(chart_data[selected_column].min()))
    max_value = st.sidebar.slider('Select Max Value', float(chart_data[selected_column].min()), float(chart_data[selected_column].max()), float(chart_data[selected_column].max()))

    # Filter data based on user selection
    filtered_data = filter_data(chart_data, selected_column, min_value, max_value)

    # Display the filtered data
    st.write(filtered_data)

    # Plot the line chart for the filtered data
    st.line_chart(filtered_data)

if __name__ == '__main__':
    main()
