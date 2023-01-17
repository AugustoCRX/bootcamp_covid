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
import warnings
warnings.filterwarnings("ignore")
sns.set_style()

#!pip install pmdarima
from pmdarima import auto_arima
from pathlib import Path


def create_sentiment_series(df, country, sentiment):

    country_filter = df[df['país'] == country]
    sentiment_filter = country_filter[country_filter['prediction'] == sentiment]
    country_data = sentiment_filter.groupby('date')[['prediction']].count()    

    
    country_data['date'] = pd.to_datetime(country_data.index)
    country_data.set_index('date', inplace=True)
    
    return country_data

class SARIMAXModel_sentiment():
    def __init__(self, serie, coluna):
        self.serie = serie
        self.coluna = coluna


    def fit_and_predict(self):
        
        # auto_arima
        #X = self.serie.groupby('date')[self.coluna].sum().copy()
        X = self.serie
        
        auto_arima(X,seasonal=True,m=7)
        stepwise_fit = auto_arima(X, start_p=0, start_q=0, 
                                    max_p=6, max_q=3, m=7,
                                    seasonal=True,
                                    trace=False, # True caso queira observar os valores de cada fit
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)
        results = [ stepwise_fit.get_params()['order'], 
                    stepwise_fit.get_params()['seasonal_order']]

        # Treinamento
        cut = int(X.shape[0] * 0.80)
        self.train = X.iloc[:cut]
        self.test = X.iloc[cut:]

        start = self.train.shape[0]
        end   = X.shape[0] - 1

        model = SARIMAX(self.train, 
                        order=results[0],
                        seasonal_order=results[1]).fit(dis=1)

        self.pred = model.predict(  start=start,
                                    end=end,
                                    dynamic=False,
                                    typ='levels')
        
        self.pred.index = self.test.index


def create_sentiment_forecast(df):
    countries = ['argentina', 'chile', 'equador', 'espanha', 'mexico']
    running = True
    while running:
        print("""
    Deseja criar a previsão de sentimentos negativos para qual pais?

    Argentina  : 0
    Chile      : 1
    Ecuador    : 2
    Espanha    : 3
    Mexico     : 4
    """)

        choice = int(input('Digite um número: '))
        country = countries[choice]

        series = create_sentiment_series(df, country, 0).rolling(7).mean().dropna()
        print('Previsão em andamento...')
        forecast = SARIMAXModel_sentiment(serie = series,
                                          coluna = series.values)
        forecast.fit_and_predict()
        print(f'Previsão para "{country}" realizada com sucesso!\n')
        

        forecast_csv = forecast.test.copy()
        forecast_csv['prediction'] = forecast.pred.copy()
        forecast_csv.to_csv(r"{}\data\results_model_forecast\Sent_negative_{}.csv".format(path, country))
        print(f"Arquivo 'Sent_negative_{country}.csv' foi gerado!")
        print(f"Ele pode ser encontrado em 'data/results_model_forecast/'")

        print('\nGostaria de realizar novas previsões?\nNão : 0\nSim : 1')
        continue_choice = int(input('Digite um número: '))
        if continue_choice == 0:
            running = False
            print('\nPROGRAMA FINALIZADO!\n')
            
            
path = Path(__file__).resolve().parents[2]
df = pd.read_csv(r'{}\notebooks\data\df_analise.csv'.format(path))


create_sentiment_forecast(df)
