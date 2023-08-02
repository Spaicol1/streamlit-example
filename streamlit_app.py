from streamlit_extras.chart_container import chart_container

chart_data = _get_random_data()
with chart_container(chart_data):
    st.write("Here's a cool chart")
    st.area_chart(chart_data)
