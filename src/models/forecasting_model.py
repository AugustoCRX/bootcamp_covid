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
    """)

        choice = int(input('Digite um número: '))
        country = countries[choice]

        series = create_series(df, country)
        print('Previsão em andamento...')
        forecast = SARIMAXModel(series, ['Confirmed'])
        forecast.fit_and_predict()
        print('Previsão realizada com sucesso!\n')

        forecast_csv = forecast.test.copy()
        forecast_csv['prediction'] = forecast.predictions.copy()
        forecast_csv.to_csv(r"{}\data\results_model_forecast\{}.csv".format(path, country.lower()))
        print(f"Arquivo '{country}.csv' foi gerado!")
        print(f"Ele pode ser encontrado em 'data/results_model_forecast/'")

        print('\nGostaria de realizar novas previsões?\nNão : 0\nSim : 1')
        continue_choice = int(input('Digite um número: '))
        if continue_choice == 0:
            running = False
            print('\nPROGRAMA FINALIZADO!\n')


path = Path(__file__).resolve().parents[2]
data = pd.read_csv(r'{}\data\external\covid_data\full_grouped.csv'.format(path))
df = data[data['Country/Region'].isin(['Mexico', 'Argentina', 
                                        'Ecuador', 'Chile', 'Spain'])]
df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")

create_forecast(df)
