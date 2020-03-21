import pandas as pd
import streamlit as st
import csv

def main():
    st.title("Visualization of current Statistics regarding COVID-19")
    st.markdown('Developed by Dustin Werner & Fabian-Malte Moeller #WeVSVirus')
    sidebar()

def sidebar():
    selectDataSource = st.sidebar.selectbox('Choose your preferred DataSource',('RKI','John Hopkins'))
    if selectDataSource == 'RKI':
        # load csv with RKI data
        pass
    if selectDataSource == 'John Hopkins':
        # load csv with CCSE Data
        selectStats = st.sidebar.selectbox('Choose the statistics you want to look at',('Confirmed cases', 'Deaths', 'Recovered'))
        if selectStats == 'Confirmed cases':
            df_confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', error_bad_lines=False)
            st.markdown('Confirmed Cases')
            st.dataframe(df_confirmed_cases)  # just printing df - later i want to produce a chart

def preparingDF(): # maybe no need for this method
    # I want to prepare the df in this method (delete rows,columns etc.)
    # Also the markdown of the plots we can implement in here! -> can discuss this point
    pass

main()