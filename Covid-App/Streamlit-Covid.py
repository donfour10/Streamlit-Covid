import pandas as pd
import streamlit as st
import csv
import numpy as np
from bokeh.plotting import figure

def main():
    st.title("Visualization of current Statistics regarding COVID-19")
    st.markdown('Developed by Dustin Werner & Fabian-Malte Möller #WeVSVirus')
    sidebar()

def sidebar():
    selectDataSource = st.sidebar.selectbox('Choose your preferred DataSource',('-','John Hopkins'))
    if selectDataSource == 'John Hopkins':
        # load csv with CCSE Data
        df_confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', error_bad_lines=False)
        df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv', error_bad_lines=False)
        df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
        countryList = df_confirmed_cases['Country/Region'].tolist()
        selectCountry = st.sidebar.selectbox('Please choose your Country/Region',countryList)
        provinceList = df_confirmed_cases.loc[df_confirmed_cases['Country/Region']== selectCountry]['Province/State'].tolist()
        if provinceList != [np.nan]:
            province_available = True
            selectProvince = st.sidebar.selectbox('Please choose your Province/State', provinceList)
        else:
            province_available = False
        x = list(df_confirmed_cases.loc[:,'1/22/20':])
        p = figure(
                title = 'line chart',
                x_axis_label = 'Date',
                x_range = x,
                y_axis_label = 'Number of persons'
            )
        ckb_cc = st.sidebar.checkbox('cofirmed cases', value = True)
        if ckb_cc:
            # st.write(df_confirmed_cases)  # just printing df - later i want to produce a chart
            if province_available == False:
                y_cc = list(df_confirmed_cases.loc[df_confirmed_cases['Country/Region']==selectCountry].loc[:,'1/22/20':].iloc[0])
            else:
                y_cc = list(df_confirmed_cases.loc[(df_confirmed_cases['Country/Region']==selectCountry) & (df_confirmed_cases['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
            p.line(x,y_cc, legend = 'confirmed Cases' ,line_width = 2)

        ckb_d = st.sidebar.checkbox('deaths')
        if ckb_d:
            # st.write(df_deaths)
            if province_available == False:
                y_d = list(df_deaths.loc[df_deaths['Country/Region']==selectCountry].loc[:,'1/22/20':].iloc[0])
            else:
                y_d = list(df_deaths.loc[(df_deaths['Country/Region']==selectCountry) & (df_deaths['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
            p.line(x, y_d, legend='deaths', line_width=2, color= 'red')

        ckb_r = st.sidebar.checkbox('recovered')
        if ckb_r:
            if province_available == False:
                y_r = list(df_recovered.loc[df_recovered['Country/Region']==selectCountry].loc[:,'1/22/20':].iloc[0])
            else:
                y_r = list(df_recovered.loc[(df_recovered['Country/Region']==selectCountry) & (df_recovered['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
            p.line(x, y_r, legend='recovered', line_width=2, color = 'green')
            # st.write(df_recovered)
        st.bokeh_chart(p)

def preparingDF(): # maybe no need for this method
    # I want to prepare the df in this method (delete rows,columns etc.)
    # Also the markdown of the plots we can implement in here! -> can discuss this point
    pass

main()