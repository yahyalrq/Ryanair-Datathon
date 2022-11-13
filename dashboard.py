import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataset2


def render_dashboard():
    st.markdown(""" 
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="../css/style.css">
        <link href='https://fonts.googleapis.com/css?family=Allerta Stencil' rel='stylesheet'>
    <style>
            h1{font-display: aligncenter;
                font-family: 'Allerta Stencil';
                color: white;}
    </style>
    <h1><center>Dashboard</center></h1>
    </head>
    </html>
    """, unsafe_allow_html=True)

    with st.spinner('''Warming up the dashboard's data...'''):
        df = load_dataset2()
        df = df.drop(columns='Unnamed: 0')

    custom, predefined = st.tabs(["Make your own", "Predefined"])
    
    with custom:
        col1, col2, col3, col4 = st.columns(4)
        
        variable = col1.selectbox(
        'Select variable to measure',
        ('TeledyneRampWeight', 'Fuel_consumed', 'Fuel_planned', 'Extra-fuel',
        'realZTFW', 'Extraplannedfuelratio', 'CO2emmited',
        'BlockTime', 'TaxiOut', 'Burnoff', 'Adults', 'Children',
        'Freight', 'Infants', 'Bags', 'PlannedZeroFuelWeight', 'PlannedTOW'))

        top = col3.selectbox(
        'Select number of features',
        ('Top 10', 'Top 25', 'Top 50', 'Top 100', 'Top 1000'))

        if top == 'Top 10':
            topn = 10
        elif top == 'Top 25':
            topn = 25
        elif top == 'Top 50':
            topn = 50
        elif top == 'Top 100':
            topn = 100
        elif top == 'Top 1000':
            topn = 1000

        chart = col4.selectbox(
        'Select type of chart',
        ('Histogram', 'Pie Chart'))

        group = col2.selectbox(
        'Select variable to group by',
        ('None', 'AircraftRegistration', 'AircraftCapacity',
        'AircraftTypeGroup', 'ServiceDescription', 'Carrier', 'AOCDescription',
        'ScheduledRoute'))
        if group != 'None':
            value = st.selectbox(
            'Select value to measure',
            ('Mean', 'Maximum', 'Minimum'))

        else:
            value = st.selectbox(
            'Select value to measure',
            ('Sum', 'Maximum', 'Minimum'))
        


        st.write('')
        
        if group == 'None':
            if chart == 'Histogram':
                if value == 'Sum':
                    st.bar_chart(df[variable].value_counts().head(topn), height=500, use_container_width=True)
                if value == 'Maximum':
                    st.bar_chart(df[variable].sort_values(ascending = True).head(topn), height=500, use_container_width=True)
                if value == 'Minimum':
                    st.bar_chart(df[variable].sort_values(ascending = False).head(topn), height=500, use_container_width=True)
            elif chart == 'Pie Chart':
                if value == 'Sum':
                    extrabydensity = pd.cut(df[variable].value_counts().head(topn), 5).value_counts(sort=False).head(5)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Maximum':
                    extrabydensity = pd.cut(df[variable].sort_values(ascending = True).head(topn), 5).value_counts(sort=False).head(5)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Minimum':
                    extrabydensity = pd.cut(df[variable].sort_values(ascending = False).head(topn), 5).value_counts(sort=False).head(5)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)

        if group != 'None':
            if chart == 'Histogram':
                if value == 'Mean':
                    st.bar_chart(df.groupby([group])[variable].mean().head(topn), height=500, use_container_width=True)
                if value == 'Maximum':
                    st.bar_chart(df.groupby([group])[variable].mean().sort_values(ascending = False).head(topn), height=500, use_container_width=True)
                if value == 'Minimum':
                    st.bar_chart(df.groupby([group])[variable].mean().sort_values(ascending = True).head(topn), height=500, use_container_width=True)
            elif chart == 'Pie Chart':
                if value == 'Mean':
                    extrabydensity = df.groupby([group])[variable].mean().head(topn)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Maximum':
                    extrabydensity = df.groupby([group])[variable].mean().sort_values(ascending = False).head(topn)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Minimum':
                    extrabydensity = df.groupby([group])[variable].mean().sort_values(ascending = True).head(topn)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)


    with predefined:
        col1, col2 = st.columns([2,1])
        
        col1.subheader('Top 20 Routes With Extra Planned Fuel Ratio')
        blabla=df[df['Extra-fuel']>=0].groupby(["ScheduledRoute"])["Extraplannedfuelratio"].mean().sort_values(ascending=False).head(20)
        col1.bar_chart(blabla, height=500, use_container_width=True)
        
        with col2:
            st.subheader('Amount of extra fuel (by density)')
            extrabydensity = pd.cut(df[df['Extra-fuel']>=0]['Extra-fuel'], 10).value_counts(sort=False).head(5)
            fig = px.pie(extrabydensity, values='Extra-fuel', names=extrabydensity.index.array.unique().astype('str'))
            st.plotly_chart(fig, use_container_width=True)
            #col1.bar_chart(df[df['Extra-fuel']>=0]['Extra-fuel'], use_container_width=True)

        st.subheader('Count of 20 Most Frequent Teledyne Weights')
        st.bar_chart(df["TeledyneRampWeight"].value_counts().head(20), height=500, use_container_width=True)


        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        with kpi1:
            st.markdown('#### Money Saved')
            st.markdown('# $70.000')

        with kpi2:
            st.markdown('#### Fuel Saved')
            st.markdown('# 85 Tons')

        with kpi3:
            st.markdown('#### CO2 Reduction')
            st.markdown('# 307 Tons')      
