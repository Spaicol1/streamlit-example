import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to filter data based on user selection
def filter_data(data, column, min_val, max_val):
    return data[(data[column] >= min_val) & (data[column] <= max_val)]

def main():
    st.title('NAICS Checklist')

    # Read the Excel file containing the NAICS definitions
    naics_definitions = pd.read_excel('C:/Users/SONY/Desktop/NAICS_definitions.xlsx')

    # Read the Excel file containing the definitions of ctynames
    ctyname_definitions = pd.read_excel('C:/Users/SONY/Desktop/Geographical Designations.xlsx')

    # List of file paths and corresponding years
    file_years = [
        ('C:/Users/SONY/Desktop/CompleteCounty2021.txt', 2021),
        ('C:/Users/SONY/Desktop/CompleteCounty2020.txt', 2020),
        ('C:/Users/SONY/Desktop/CompleteCounty2019.txt', 2019),
        ('C:/Users/SONY/Desktop/CompleteCounty2018.txt', 2018),
        ('C:/Users/SONY/Desktop/CompleteCounty2017.txt', 2017),
        # Add more file paths and years as needed
    ]

    # Create a checklist for NAICS codes
    selected_naics = st.multiselect('Select NAICS Codes:', naics_definitions['Description'])

    # Apply filters and display the data
    if selected_naics:
        filtered_data = apply_filters(selected_naics, file_years, naics_definitions, ctyname_definitions)
        st.dataframe(filtered_data)

        # Plot line chart for total estimates per fipstate
        fipstate_data = get_fipstate_data(filtered_data)
        for fipstate, data in fipstate_data.items():
            years = np.array([year for year, _ in data])
            totals = np.array([total for _, total in data])

            plt.figure()
            plt.plot(years, totals, marker='o')
            plt.xlabel('Year')
            plt.ylabel('Total Estimates')
            plt.title(f"Total Companies per Fipstate ({fipstate})")
            plt.xticks(years, years.astype(int))  # Set x-axis ticks as full numbers
            st.pyplot()

        # Plot line charts for individual ctynames
        filtered_data_list = get_filtered_data_list(filtered_data)
        for fipstate, fipscty, city_name, est_values in filtered_data_list:
            years = np.array([year for year, _ in est_values])
            estimates = np.array([est for _, est in est_values])

            plt.figure()
            plt.plot(years, estimates, marker='o')
            plt.xlabel('Year')
            plt.ylabel('# of Companies')
            plt.title(f"Companies in {city_name} ({fipstate}-{fipscty})")
            plt.xticks(years, years.astype(int))  # Set x-axis ticks as full numbers
            st.pyplot()

def apply_filters(selected_naics, file_years, naics_definitions, ctyname_definitions):
    filtered_data = pd.DataFrame()
    for file_path, year in file_years:
        data = pd.read_csv(file_path, delimiter=',')
        data['year'] = year
        naics_values = naics_definitions['NAICS'].astype(str).values
        data = data[data['naics'].astype(str).isin(naics_values)]
        filtered_data = pd.concat([filtered_data, data])
    merged_data = pd.merge(filtered_data, ctyname_definitions, how='left', left_on=['fipstate', 'fipscty'], right_on=['st', 'cty'])
    merged_data.drop_duplicates(subset=['fipstate', 'fipscty', 'year'], inplace=True)
    return merged_data

def get_fipstate_data(merged_data):
    fipstate_data = {}
    est_sum_data_dict = merged_data.groupby(['year', 'fipstate'])['est'].sum().reset_index()
    for year, fipstate, total in zip(est_sum_data_dict['year'], est_sum_data_dict['fipstate'], est_sum_data_dict['est']):
        if fipstate not in fipstate_data:
            fipstate_data[fipstate] = []
        fipstate_data[fipstate].append((year, total))
    return fipstate_data

def get_filtered_data_list(merged_data):
    fipstate_fipscty = merged_data.groupby(['fipstate', 'fipscty'])
    filtered_data_list = []
    for (fipstate, fipscty), group_data in fipstate_fipscty:
        city_name = group_data['ctyname'].iloc[0]
        est_values = [(year, est) for year, est in zip(group_data['year'], group_data['est'])]
        filtered_data_list.append((fipstate, fipscty, city_name, est_values))
    return filtered_data_list

if __name__ == '__main__':
    main()
