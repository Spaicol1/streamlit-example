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
    filtered_data = pd.DataFrame()
    naics_values = set()
    est_sum_data_dict = {}
    fipstate_data = {}

    for file_path, year in file_years:
        # Load the TXT data into a pandas DataFrame
        data = pd.read_csv(file_path, delimiter=',')
        # Assign year to the data
        data['year'] = year
        # Collect unique NAICS values in the loaded data
        naics_values.update(naics_definitions['NAICS'].astype(str).unique())
        # Filter the data based on selected NAICS codes
        for naics_code in selected_naics:
            filtered_data = pd.concat([filtered_data, data[data['naics'].astype(str) == naics_code][['naics', 'fipstate', 'est', 'fipscty', 'year']]])

    # Merge the filtered_data DataFrame with the ctyname_definitions DataFrame based on 'fipstate' and 'fipscty'
    merged_data = pd.merge(filtered_data, ctyname_definitions, how='left', left_on=['fipstate', 'fipscty'], right_on=['st', 'cty'])

    if not merged_data.empty:
        # Drop duplicates based on 'fipstate', 'fipscty', and 'year' columns
        merged_data = merged_data.drop_duplicates(subset=['fipstate', 'fipscty', 'year'])
        # Sort the merged data by year
        merged_data = merged_data.sort_values('year')

        # Match fipstate and fipscty and store est values per year with corresponding ctyname
        fipstate_fipscty = merged_data.groupby(['fipstate', 'fipscty'])
        filtered_data_list = []

        for (fipstate, fipscty), group_data in fipstate_fipscty:
            city_name = group_data['ctyname'].iloc[0]
            est_values = []
            for year, est in zip(group_data['year'], group_data['est']):
                est_values.append((year, est))
            filtered_data_list.append((fipstate, fipscty, city_name, est_values))

        # Calculate the total sum per fipstate within a year
        for year, year_data in merged_data.groupby('year'):
            est_sum_data_dict = year_data.groupby(['year', 'fipstate'])['est'].sum().reset_index()

            for fipstate, total in zip(est_sum_data_dict['fipstate'], est_sum_data_dict['est']):
                if fipstate not in fipstate_data:
                    fipstate_data[fipstate] = []
                fipstate_data[fipstate].append((year, total))

    return fipstate_data, filtered_data_list

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
    st.sidebar.subheader('Plot Line Charts')
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
