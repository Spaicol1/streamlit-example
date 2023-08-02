import streamlit as st
import pandas as pd
import numpy as np

# Load the Excel files
def load_naics_definitions():
    naics_definitions_file = 'NAICS_definitions.xlsx'
    naics_definitions = pd.read_excel(naics_definitions_file)
    return naics_definitions

def load_ctyname_definitions():
    ctyname_definitions_file = 'Geographical Designations.xlsx'
    ctyname_definitions = pd.read_excel(ctyname_definitions_file)
    return ctyname_definitions

def load_data_files():
    file_years = [
        ('CompleteCounty2021.txt', 2021),
        ('CompleteCounty2020.txt', 2020),
        ('CompleteCounty2019.txt', 2019),
        ('CompleteCounty2018.txt', 2018),
        ('CompleteCounty2017.txt', 2017),
        # Add more file paths and years as needed
    ]
    return file_years

def apply_filters(selected_naics):
    # Your filtering logic here to process the data
    # ...
    return filtered_data, fipstate_data, filtered_data_list

def main():
    st.title('NAICS Checklist and Line Charts')

    # Load the Excel files
    naics_definitions = load_naics_definitions()
    ctyname_definitions = load_ctyname_definitions()
    file_years = load_data_files()

    # List to store the selected NAICS codes
    selected_naics = []

    st.header('Select NAICS Codes:')

    # Create a checkbox for each NAICS code
    for index, row in naics_definitions.iterrows():
        naics_code = row['NAICS']
        naics_description = row['Description']
        checkbox = st.checkbox(f"{naics_code} - {naics_description}")
        if checkbox:
            selected_naics.append(naics_code)

    # Display the selected NAICS codes
    if selected_naics:
        st.subheader('Selected NAICS Codes:')
        st.write(selected_naics)

    # If the user has selected some NAICS codes, apply filters and plot line charts
    if selected_naics:
        filtered_data, fipstate_data, filtered_data_list = apply_filters(selected_naics)

        # Plot line charts for total estimates per fipstate
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
