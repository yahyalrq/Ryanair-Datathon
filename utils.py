import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
import tensorflow.keras.layers as layers
import streamlit as st
import pickle


# ----------- UTILS FOR FORECASTS ----------------
@st.cache(show_spinner=False)
def load_dataset():
    return pd.read_csv('data/train_extended.csv')

@st.experimental_singleton
def load_model():
    model = Sequential([
        layers.Input(shape=(1282)),
        layers.Dense(642, activation='relu'),
        layers.Dense(321, activation='relu'),
        layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', 
                       loss='mean_absolute_error', 
                       metrics=["MeanAbsoluteError"])

    model.load_weights('data/NN3model_55')
    return model


@st.cache
def get_distance(departure, arrival):
    airports=pd.read_csv("data/GlobalAirportDatabase.txt", sep=",")
    airports['longitude']=airports['longitude'].astype(float)
    airports['latitude']=airports['latitude'].astype(float)

    val= airports[airports['iata']==departure].iloc[:, [-2,-1]].values[0]
    lon1 = val[1]
    lat1 = val[0]
    val= airports[airports['iata']==arrival].iloc[:, [-2,-1]].values[0]
    lon2 = val[1] # 'A_long'
    lat2 = val[0] # A_lat

    R=6371000  # Earth radius
    phi_1=np.radians(lat1)
    phi_2=np.radians(lat2)

    delta_phi=np.radians(lat2-lat1)
    delta_lambda=np.radians(lon2-lon1)

    a=np.sin(delta_phi/2.0)**2+\
    np.cos(phi_1)*np.cos(phi_2)*\
    np.sin(delta_lambda/2.0)**2
    c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))

    meters=R*c                         # output distance in meters
    km=meters/1000.0              # output distance in kilometers

    return km


def process_date(df):
    df["DepartureScheduled"]=pd.to_datetime(df["DepartureScheduled"])
    df["ArrivalScheduled"]=pd.to_datetime(df["ArrivalScheduled"])
    df["DepartureScheduled"]=pd.to_datetime(df["DepartureScheduled"],format='%y/%m/%d %H:%M:%S')
    df["ArrivalScheduled"]=pd.to_datetime(df["ArrivalScheduled"],format='%y/%m/%d %H:%M:%S')
    df['day_of_week'] = df['DepartureScheduled'].dt.day_name()
    df['hour_of_day'] = df['DepartureScheduled'].dt.hour
    df['month_of_year'] =df['DepartureScheduled'].dt.month
    df = df.drop(columns=["DepartureScheduled","ArrivalScheduled"])
    return df

def get_dummies(df):
    df=pd.get_dummies(df, columns=['ServiceDescription'])
    df=pd.get_dummies(df, columns=['AircraftTypeGroup'])
    df=pd.get_dummies(df,columns=['AOCDescription'])
    df=pd.get_dummies(df,columns=['Carrier'])
    df=pd.get_dummies(df,columns=['AircraftCapacity'])
    df=pd.get_dummies(df,columns=['DepartureLocation'])
    df=pd.get_dummies(df,columns=['ArrivalLocation'])
    df=pd.get_dummies(df,columns=["AircraftRegistration"])
    df=pd.get_dummies(df, columns=['month_of_year','hour_of_day','day_of_week'])
    return df


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_columns():
    columns = pickle.load(open('data/dfcolumns.pkl', 'rb'))
    complete_df = pd.DataFrame(columns = columns)
    return complete_df


def update_df(df):
    complete_df = load_columns()
    dff = pd.DataFrame(columns=['AircraftRegistration', 'AircraftCapacity',
       'AircraftTypeGroup', 'ServiceDescription', 'Carrier', 'AOCDescription',
       'DepartureLocation', 'ArrivalLocation', 'DepartureScheduled', 'ArrivalScheduled',
       'BlockTimeScheduled', 'Adults', 'Children', 'Freight', 'Infants',
       'Bags'])
    dff.loc[0] = df
    dff = process_date(dff)
    dff = get_dummies(dff)
    for column in complete_df.columns:
        if column in dff.columns:
            complete_df[column] = dff[column]
        else:
            complete_df[column] = complete_df[column].fillna(0)
    
    return np.asarray(complete_df).astype('float32')




# ------------- UTILS FOR DASHBOARD --------------

@st.cache(show_spinner=False)
def load_dataset2():
    return pd.read_csv('data/extended_insights.csv')

