import pandas as pd
import streamlit as st
import csv
import numpy as np
from bokeh.plotting import figure

def main():
    st.title("Visualization of current Statistics regarding COVID-19")
    st.markdown('Developed by Dustin Werner & Fabian-Malte Moeller #WeVSVirus')
    sidebar()

def sidebar():
    selectDataSource = st.sidebar.selectbox('Choose your preferred DataSource',('-','John Hopkins'))
    if selectDataSource == 'John Hopkins':
        # load csv with CCSE Data
        selectStats = st.sidebar.selectbox('Choose the statistics you want to look at',('Confirmed cases', 'Deaths', 'Recovered'))
        if selectStats == 'Confirmed cases':
            df_confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', error_bad_lines=False)
            st.write(df_confirmed_cases)  # just printing df - later i want to produce a chart
            del df_confirmed_cases['Province/State']
            del df_confirmed_cases['Country/Region']
            del df_confirmed_cases['Lat']
            del df_confirmed_cases['Long']
            x = list(df_confirmed_cases)
            y = list(df_confirmed_cases.iloc[0])
            st.write(x)
            st.write(y)
            p = figure(
                title = 'line chart',
                x_axis_label = 'Date',
                x_range = x,
                y_axis_label = 'Number of persons'
            )
            p.line(x,y, legend = 'Confirmed Cases' ,line_width = 2)
            st.bokeh_chart(p)

        if selectStats == 'Deaths':
            df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv', error_bad_lines=False)
            st.write(df_deaths)
            x = [1, 2, 3, 4, 5]
            y = [6, 7, 2, 4, 5]
            p = figure(
                title='simple line example',
                x_axis_label='x',
                y_axis_label='y')
            p.line(x, y, legend='Trend', line_width=2)
            st.bokeh_chart(p)

        if selectStats == 'Recovered':
            df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
            st.write(df_recovered)

def preparingDF(): # maybe no need for this method
    # I want to prepare the df in this method (delete rows,columns etc.)
    # Also the markdown of the plots we can implement in here! -> can discuss this point
    pass

main()