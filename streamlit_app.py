import streamlit as st
import pandas as pd
import numpy as np
import os

# Get the current working directory
base_dir = os.getcwd()

# Define the file paths relative to the current working directory
naics_definitions_path = os.path.join(base_dir, 'NAICS_definitions.xlsx')
ctyname_definitions_path = os.path.join(base_dir, 'Geographical Designations.xlsx')

# Function to load NAICS definitions from the Excel file
def load_naics_definitions():
    return pd.read_excel(naics_definitions_path)

# Function to filter data for specific industries related to selected NAICS codes
def apply_filters(naics_definitions, selected_naics):
    # Your filtering logic here to process the data
    # ...
    return filtered_data, fipstate_data, filtered_data_list

def main():
    st.title('NAICS Checklist and Line Charts')

    # Load the NAICS definitions
    naics_definitions = load_naics_definitions()

    # List to store the selected NAICS codes
    selected_naics = []

    st.sidebar.header('Select NAICS Codes:')

    # Create a checkbox for each NAICS code
    for index, row in naics_definitions.iterrows():
        naics_code = row['NAICS']
        naics_description = row['Description']
        checkbox = st.sidebar.checkbox(f"{naics_code} - {naics_description}")
        if checkbox:
            selected_naics.append(naics_code)

    # Display the selected NAICS codes
    if selected_naics:
        st.sidebar.subheader('Selected NAICS Codes:')
        st.sidebar.write(selected_naics)

    # Button to apply filters and plot line charts
    plot_button = st.sidebar.button('Apply Filters and Plot Line Charts')

    # If the user has selected some NAICS codes and clicked the plot button, apply filters and plot line charts
    if selected_naics and plot_button:
        fipstate_data, filtered_data_list = apply_filters(naics_definitions, selected_naics)

        # Plot line chart for total estimates per fipstate
        for fipstate, data in fipstate_data.items():
            years = np.array([year for year, _ in data])
            totals = np.array([total for _, total in data])

            st.subheader(f"Total Companies per Fipstate ({fipstate})")
            st.line_chart(pd.DataFrame({'Year': years, 'Total Estimates': totals}))

        # Plot line charts for individual ctynames
        for fipstate, fipscty, city_name, est_values in filtered_data_list:
            years = np.array([year for year, _ in est_values])
            estimates = np.array([est for _, est in est_values])

            st.subheader(f"Companies in {city_name} ({fipstate}-{fipscty})")
            st.line_chart(pd.DataFrame({'Year': years, '# of Companies': estimates}))

if __name__ == '__main__':
    main()
