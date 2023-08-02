import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data for 2020 and 2021, replace with your own data
data_2020 = pd.DataFrame({
    'Date': pd.date_range(start='2020-01-01', periods=12, freq='M'),
    'Value': [10, 12, 15, 8, 10, 11, 14, 17, 20, 21, 19, 18]
})

data_2021 = pd.DataFrame({
    'Date': pd.date_range(start='2021-01-01', periods=12, freq='M'),
    'Value': [11, 13, 16, 9, 11, 12, 15, 18, 21, 22, 20, 19]
})

# Combine the datasets
all_data = {'2020': data_2020, '2021': data_2021}

def plot_line_chart(data, title):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Date', y='Value', data=data, marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    st.pyplot()

def main():
    st.title('Line Chart with Slider and Filters')

    # Year range slider
    years = list(all_data.keys())
    year_range = st.sidebar.slider('Select Year Range', min_value=years[0], max_value=years[-1], value=(years[0], years[-1]))

    # Dataset selection filter
    selected_dataset = st.sidebar.selectbox('Select Dataset', years)

    # Filter data based on selected year range and dataset
    filtered_data = pd.concat([all_data[year] for year in years if year_range[0] <= year <= year_range[1]])

    # Plot the line chart
    plot_line_chart(filtered_data, f'Line Chart for {selected_dataset}')

if __name__ == '__main__':
    main()
