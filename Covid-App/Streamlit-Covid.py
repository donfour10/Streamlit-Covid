import pandas as pd
import streamlit as st
import csv
import numpy as np
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from datetime import datetime, timedelta
import math

def main():
    st.title("Visualization of current Statistics regarding COVID-19")
    st.markdown('Developed by Dustin Werner & Fabian-Malte Möller #WeVSVirus')
    sidebar()

def latlong2merc(lat, long):
    radius = 6378137.0
    x = math.radians(long)*radius
    y = math.log(math.tan(math.pi/4+math.radians(lat)/2))*radius
    return(x,y)

def sidebar():
    selectDataSource = st.sidebar.selectbox('Choose your preferred DataSource',('-','John Hopkins'))
    if selectDataSource == 'John Hopkins':
        # load csv with CCSE Data
        df_confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', error_bad_lines=False)
        df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', error_bad_lines=False)
        df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', error_bad_lines=False)
        selectVisualization = st.sidebar.selectbox('Which visualization do you want to look at?', ('-','line chart','world map'))
        if selectVisualization == 'line chart':
            countryList = df_confirmed_cases['Country/Region'].tolist()
            countryList = list(set(countryList))
            countryList.sort()
            selectCountry = st.sidebar.selectbox('Please choose your Country/Region',countryList)
            provinceList = df_confirmed_cases.loc[df_confirmed_cases['Country/Region']== selectCountry]['Province/State'].tolist()
            if provinceList != [np.nan]:
                province_available = True
                provinceList = df_confirmed_cases.loc[df_confirmed_cases['Country/Region']== selectCountry].fillna(0)['Province/State'].tolist()
                for i in range(len(provinceList)):
                    if provinceList[i] == 0:
                        provinceList[i] = selectCountry
                provinceList.sort()
                selectProvince = st.sidebar.selectbox('Please choose your Province/State', provinceList)
            else:
                province_available = False
            datestrList = list(df_confirmed_cases.loc[:,'1/22/20':])
            x = []
            for date in datestrList:
                datetime_obj = datetime.strptime(date, '%m/%d/%y')
                # datetime_obj = np.datetime64(datetime_obj)
                x.append(datetime_obj)
            p = figure(
                    title = 'line chart',
                    x_axis_label = 'Date',
                    x_axis_type = 'datetime',
                    # x_range = x,
                    y_axis_label = 'Number of persons'
                )
            ckb_cc = st.sidebar.checkbox('cofirmed cases', value = True)
            if ckb_cc:
                # st.write(df_confirmed_cases)  # just printing df - later i want to produce a chart
                if province_available == False:
                    y_cc = list(df_confirmed_cases.loc[df_confirmed_cases['Country/Region']==selectCountry].loc[:,'1/22/20':].iloc[0])
                else:
                    if selectCountry == selectProvince:
                        df_country_cc = df_confirmed_cases.loc[(df_confirmed_cases['Country/Region']==selectCountry)].fillna(selectCountry)
                        y_cc = list(df_country_cc.loc[(df_country_cc['Country/Region']==selectCountry) & (df_country_cc['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
                    else:
                        y_cc = list(df_confirmed_cases.loc[(df_confirmed_cases['Country/Region']==selectCountry) & (df_confirmed_cases['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
                p.line(x,y_cc, legend = 'confirmed cases' ,line_width = 2)

            ckb_d = st.sidebar.checkbox('deaths', value= True)
            if ckb_d:
                # st.write(df_deaths)
                if province_available == False:
                    y_d = list(df_deaths.loc[df_deaths['Country/Region']==selectCountry].loc[:,'1/22/20':].iloc[0])
                else:
                    if selectCountry == selectProvince:
                        df_country_d = df_deaths.loc[(df_deaths['Country/Region']==selectCountry)].fillna(selectCountry)
                        y_d = list(df_country_d.loc[(df_country_d['Country/Region']==selectCountry) & (df_country_d['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
                    else:
                        y_d = list(df_deaths.loc[(df_deaths['Country/Region']==selectCountry) & (df_deaths['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
                p.line(x, y_d, legend='deaths', line_width=2, color= 'red')

            ckb_r = st.sidebar.checkbox('recovered', value = True)
            if ckb_r:
                if province_available == False:
                    y_r = list(df_recovered.loc[df_recovered['Country/Region']==selectCountry].loc[:,'1/22/20':].iloc[0])
                else:
                    if selectCountry == selectProvince:
                        df_country_r = df_recovered.loc[(df_recovered['Country/Region']==selectCountry)].fillna(selectCountry)
                        y_r = list(df_country_r.loc[(df_country_r['Country/Region']==selectCountry) & (df_country_r['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
                    else:
                        y_r = list(df_recovered.loc[(df_recovered['Country/Region']==selectCountry) & (df_recovered['Province/State']==selectProvince)].loc[:,'1/22/20':].iloc[0])
                p.line(x, y_r, legend='recovered', line_width=2, color = 'green')
                # st.write(df_recovered)
            st.bokeh_chart(p)
        if selectVisualization == 'world map':
            # implemet world map visualization with circles to hover over
            selectDate = st.sidebar.date_input('On which day would you like to see the map?', datetime.today()- timedelta(days=1))
            tile_provider = get_provider(Vendors.CARTODBPOSITRON)
            p = figure(x_range=(-17000000, 17000000),y_range=(-6000000, 8000000),
                    x_axis_type="mercator", y_axis_type="mercator", plot_width= 800, plot_height= 400)
            p.add_tile(tile_provider)
            for i in range(len(df_confirmed_cases)):
                lat = df_confirmed_cases.at[i, 'Lat']
                lon = df_confirmed_cases.at[i, 'Long']
                x_merc, y_merc = latlong2merc(lat,lon)
                p.circle(x=x_merc, y=y_merc, size= 10, color='blue')
            st.bokeh_chart(p)

def preparingDF(): # maybe no need for this method
    # I want to prepare the df in this method (delete rows,columns etc.)
    # Also the markdown of the plots we can implement in here! -> can discuss this point
    pass

main()