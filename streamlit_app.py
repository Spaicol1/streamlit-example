import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Set Streamlit theme and custom styles
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .st-bk {
        font-size: 16px;
        padding: 0.5rem 1rem;
    }
    .st-dd {
        font-size: 16px;
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .st-bk, .st-dd {
        color: #333;
        background-color: #f8f8f8;
    }
    .st-dd:hover {
        background-color: #e0e0e0;
    }
    .st-dd.st-dd-options {
        color: #007BFF;
        background-color: #f8f8f8;
    }
    .st-dd.st-dd-options:hover {
        background-color: #007BFF;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-ec {
        font-size: 16px;
        border-radius: 8px;
        padding: 0.25rem 0.5rem;
        background-color: #007BFF;
        color: white;
    }
    .stTitle {
        font-size: 32px !important;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .stSidebarTitle {
        font-size: 24px !important;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .stSubheader {
        font-size: 20px !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    line_chart = alt.Chart(df).mark_line(color='blue').encode(
        x='x_values',
        y='y_values'
    )

    # Add interactive data points using the `circle` mark
    data_points = line_chart.mark_circle(color='orange', size=60).encode(
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
    avg_line = alt.Chart(pd.DataFrame({'avg_value': [avg_value]})).mark_rule(color='red').encode(y='avg_value')

    # Combine the line chart, data points, and average line using Altair's layer
    chart = alt.layer(line_chart, data_points, avg_line).interactive()

    # Add a title to the chart
    st.markdown("<h1 class='stTitle'>Line Chart with Hover Data Points</h1>", unsafe_allow_html=True)

    # Add the chart
    st.altair_chart(chart, use_container_width=True)

    # Add a header for the page
    st.title("My Streamlit App")

    # Add metrics for average growth, lowest, highest, and average
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average Growth", f"{avg_growth:.2f}%", delta="3.27%")

    with col2:
        st.metric("Lowest Value", lowest_value, delta="-2.12")

    with col3:
        st.metric("Highest Value", highest_value, delta="4.63")

    with col4:
        st.metric("Average Value", avg_value, delta="1.09")

    # Add a sidebar for selecting different sets of data and years
    with st.sidebar:
        st.markdown("<h2 class='stSidebarTitle'>Data Selection</h2>", unsafe_allow_html=True)

        # Custom dropdown styles
        selected_establishment_type = st.selectbox("Select Establishment Type:", establishment_types, key="est_type",
                                                  format_func=lambda x: "Select Establishment Type" if x == "" else x,
                                                  help="Choose an establishment type")
        selected_state = st.selectbox("Select State:", states, key="state",
                                      format_func=lambda x: "Select State" if x == "" else x, help="Choose a state")
        selected_county = st.selectbox("Select County:", counties, key="county",
                                       format_func=lambda x: "Select County" if x == "" else x, help="Choose a county")
        selected_naics = st.selectbox("Select NAICs:", naics, key="naics",
                                      format_func=lambda x: "Select NAICs" if x == "" else x, help="Choose a NAICs")

        st.subheader("Time Range")
        start_year = st.slider("Select start year:", min_value=min(years), max_value=max(years), value=min(years))
        end_year = st.slider("Select end year:", min_value=min(years), max_value=max(years), value=max(years))

    # Filter the data based on the selected dropdown values and years
    filtered_data = df[(df['x_values'] >= start_year) & (df['x_values'] <= end_year)]

    # Display the filtered data as a table
    st.table(filtered_data)

    # Add a button to download the chart as PNG
    if st.button("Download Chart as PNG", key="download_chart"):
        chart.save("chart.png")
        st.success("Chart downloaded successfully!")

if __name__ == '__main__':
    main()
