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


def criar_serie(df, nome_pais):

    filtro = df[df['Country/Region'] == nome_pais]
    pais = filtro[['Date', 'Confirmed', 'Deaths']]
    
    pd.to_datetime(pais.Date)
    pais.set_index('Date', inplace=True)
    
    return pais


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

    def evaluate(self):
        print(f"R²: {r2_score(self.test, self.predictions):.2f}")
        print(f"MAE: {mean_absolute_error(self.test, self.predictions):.2f}")
        print(f"RMSE: {mean_squared_error(self.test, self.predictions, squared=False):.2f}")
        print(f"MAPE: {mean_absolute_percentage_error(self.test, self.predictions)}")

    def plot(self):
        fig, axs = plt.subplots(2, 1, figsize=(10, 4), constrained_layout=True)

        ax = axs[0]
        ax.set_title(f'Prediction for {self.column}')
        ax.plot(self.test, label='Test')
        ax.plot(self.predictions, label='Prediction')
        ax.legend(loc='best')

        ax = axs[1]
        ax.set_title(f'Prediction for {self.column}')
        ax.plot(self.train, label='Train')
        ax.plot(self.test, label='Test')
        ax.plot(self.predictions, label='Prediction')
        ax.legend(loc='best')

        plt.show()


data = pd.read_csv(r'D:\Blue EdTech\Bootcamp\notebooks\bootcamp_covid-1\data\bronze\covid_raw\full_grouped.csv')
df = data[data['Country/Region'].isin(['Mexico', 'Argentina', 
                                        'Ecuador', 'Chile', 'Spain'])]
df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")

# rodando = True
# while rodando:
#     print("""
# Deseja criar a previsão para o numero de confirmados para qual pais?

#     Todos     : 0
#     Argentina : 1
#     Chile     : 2
#     Equador   : 3
#     México    : 4
#     Espanha   : 5
#     """)

#     países = ['Argentina', 'Chile', 'Ecuador', 'Mexico', 'Spain']
#     escolha = int(input('Digite o número: '))
#     país = países[escolha - 1]

#     if escolha == 0:
#         serie = criar_serie(df, df['Country/Region'])
#     else:
#         serie = criar_serie(df, país)

#     print('Previsão em andamento...')
#     predicao = Modelo_SARIMAX(  serie = serie,
#                                 coluna = ['Confirmed'])
#     predicao.autoarima_e_treino()
#     print('Previsão realizada com sucesso!\n')

#     predicao_csv = predicao.test.copy()
#     predicao_csv['pred'] = predicao.pred.copy()
#     predicao_csv.to_csv(f"D:\\Blue EdTech\\Bootcamp\\notebooks\\bootcamp_covid-1\\data\\results_model_forecast\\{país}.csv")
#     print(f"Arquivo '{país}.csv' foi gerado!")
#     print(f"Ele pode ser encontrado em 'data/results_model_forecast/'")

#     print('\nGostaria de realizar novas previsões?\nNão : 0\nSim : 1')
#     escolha_continuar = int(input('Digite o número: '))
#     if escolha_continuar == 0:
#         rodando = False
#         print('\nPROGRAMA FINALIZADO!\n')


def create_forecast(df):
    countries = ['Argentina', 'Chile', 'Ecuador', 'Mexico', 'Spain']
    running = True
    while running:
        print("""
    Which country would you like to create the forecast for?

    All       : 0
    Argentina : 1
    Chile     : 2
    Ecuador   : 3
    Mexico    : 4
    Spain     : 5
    """)

        choice = int(input('Enter the number: '))
        country = countries[choice - 1] if choice != 0 else None

        series = create_series(df, country)
        print('Forecasting in progress...')
        forecast = SARIMAXModel(series, ['Confirmed'])
        forecast.fit_and_predict()
        print('Forecast completed successfully!\n')

        forecast_csv = forecast.test.copy()
        forecast_csv['prediction'] = forecast.predictions.copy()
        forecast_csv.to_csv(f"D:\\Blue EdTech\\Bootcamp\\notebooks\\bootcamp_covid-1\\data\\results_model_forecast\\{country}.csv")
        print(f"File '{country}.csv' was generated!")
        print(f"It can be found in 'data/results_model_forecast/'")

        print('\nWould you like to make new forecasts?\nNo : 0\nYes : 1')
        continue_choice = int(input('Enter the number: '))
        if continue_choice == 0:
            running = False
            print('\nPROGRAM ENDED!\n')
