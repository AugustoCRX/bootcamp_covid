import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error

from statsmodels.tsa.statespace.sarimax import SARIMAX

import csv
import re
import warnings
warnings.filterwarnings("ignore")
sns.set_style()

from pmdarima import auto_arima
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine


def create_series(df, country):
    country_filter = df[df['Country/Region'] == country]
    country_data = country_filter[['Date', 'Confirmed', 'Deaths']]
    country_data['Date'] = pd.to_datetime(country_data['Date'])
    country_data.set_index('Date', inplace=True)
    return country_data


class SARIMAXModel():
    def __init__(self, data, column):
        self.data = data
        self.column = column

    def fit_and_predict(self):
        X = self.data.groupby('Date')[self.column].sum().copy()
        stepwise_fit = auto_arima(X, start_p=0, start_q=0, 
                                    max_p=6, max_q=3, m=7,
                                    seasonal=True,
                                    trace=False,
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)
        self.params = [ stepwise_fit.get_params()['order'], 
                        stepwise_fit.get_params()['seasonal_order']]

        cut = int(X.shape[0] * 0.80)
        self.train = X.iloc[:cut]
        self.test = X.iloc[cut:]

        start = self.train.shape[0]
        end   = X.shape[0] - 1

        self.model = SARIMAX(self.train, 
                            order=self.params[0],
                            seasonal_order=self.params[1]).fit(disp=False)

        self.predictions = self.model.predict(start=start, end=end, dynamic=False, typ='levels')
        self.predictions.index = self.test.index


def create_forecast(df):
    countries = ['Argentina', 'Chile', 'Ecuador', 'Mexico', 'Spain']
    running = True
    while running:
        print("""
    Deseja criar a previsão para o numero de confirmados para qual pais?

    Argentina : 0
    Chile     : 1
    Ecuador   : 2
    Mexico    : 3
    Spain     : 4
    All       : 5
    """)

        choice = int(input('Digite um número: '))

        if choice > 5:
            print('Número invalido!\n')
            
        elif choice == 5:
            print('Previsão em andamento...')
            for i in countries:
                series = create_series(df, i)
                forecast = SARIMAXModel(series, ['Confirmed'])
                forecast.fit_and_predict()

                forecast_csv = forecast.test.copy()
                forecast_csv['prediction'] = forecast.predictions.copy()
                forecast_csv.to_sql(name=f'covid_{i.lower()}_pred', con=engine, if_exists='replace')
            print('Previsão realizada com sucesso!\n')
            print("Todos os arquivos foram gerados!")
                
        else:
            country = countries[choice]
            series = create_series(df, country)
            print('Previsão em andamento...')
            forecast = SARIMAXModel(series, ['Confirmed'])
            forecast.fit_and_predict()
            print('Previsão realizada com sucesso!\n')

            forecast_csv = forecast.test.copy()
            forecast_csv['prediction'] = forecast.predictions.copy()
            forecast_csv.to_sql(name=f'covid_{country.lower()}_pred', con=engine, if_exists='replace')
            print(f"Arquivo '{country}.csv' foi gerado!")


        print('\nGostaria de realizar novas previsões?\nNão : 0\nSim : 1')
        continue_choice = int(input('Digite um número: '))
        if continue_choice == 0:
            running = False
            print('\nPROGRAMA FINALIZADO!\n')


# AWS
engine = create_engine("mysql+mysqlconnector://admin:bootcamp_covid@database-1.cjpz0qecuge2.sa-east-1.rds.amazonaws.com/bootcamp_covid")
port = int(input('port: '))
user = input('user: ')
password = input('password: ')
cnx = mysql.connector.connect(
                                host="database-1.cjpz0qecuge2.sa-east-1.rds.amazonaws.com",
                                port=port,
                                user=user,
                                password=password,
                                database='bootcamp_covid'
                             )
cur = cnx.cursor()

# Selecionando a query no servidor
query_ts = 'SELECT * FROM covid_raw_data'
data = pd.read_sql(query_ts, engine).drop('index', 1)

# Alterando colunas
for i in data.columns:
    if i != 'country_region':
        data.rename(columns = {i:re.sub(r'\s|_', r' ', i).capitalize()}, inplace = True)
    else:
        data.rename(columns= {i:"Country/Region"}, inplace=True)

# Df com países escolhidos
df = data[data['Country/Region'].isin(['Mexico', 'Argentina', 
                                        'Ecuador', 'Chile', 'Spain'])]
df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")

create_forecast(df)
