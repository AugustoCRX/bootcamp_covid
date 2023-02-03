import re
import csv
import numpy as np
import pandas as pd

from pathlib import Path
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings("ignore")


def create_series(df, country):
    """
    Cria uma série temporal para o país selecionado a partir de um dataframe.

    :param df: Dataframe original
    :param country: Nome do país
    :return: Série temporal com a quantidade de casos confirmados e mortes.
    """
    
    country_filter = df[df['Country/Region'] == country]
    country_data = country_filter[['Date', 'Confirmed', 'Deaths']]
    country_data['Date'] = pd.to_datetime(country_data['Date'])
    country_data.set_index('Date', inplace=True)
    return country_data


class SARIMAXModel():
    def __init__(self, data, column):
        """
        Inicializa o modelo SARIMAX.

        :param data: Série temporal
        :param column: Coluna a ser utilizada no modelo
        """
        
        self.data = data
        self.column = column

    def fit_and_predict(self):
        """
        Executa o processo de treinamento e previsão do modelo SARIMAX.
        """
        
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
    """
    Cria um arquivo .csv com as previsão de casos de COVID-19 para cada país.
    
    :param df: Dataframe original
    :return: Armazena as previsões em um arquivo .csv no servidor AWS 
    """

    # Lista de países para seleção
    countries = ['Argentina', 'Chile', 'Ecuador', 'Mexico', 'Spain']
    running = True
    while running:
        print(
    """
    Deseja criar a previsão para o numero de confirmados para qual pais?

    Argentina : 0
    Chile     : 1
    Ecuador   : 2
    Mexico    : 3
    Spain     : 4
    All       : 5
    """)

        choice = int(input('Digite um número: '))

        # Caso seja escolhido todos os países
        if choice > 5:
            print('Número invalido!\n')
            
        elif choice == 5:
            print('Previsão em andamento...')
            
            # Loop para previsão de todos os países
            for i in countries:
                series = create_series(df, i)
                forecast = SARIMAXModel(series, ['Confirmed'])
                forecast.fit_and_predict()

                # Cria um DataFrame com os resultados
                forecast_csv = forecast.test.copy()
                forecast_csv['prediction'] = forecast.predictions.copy()
                
                # Salva os resultados em formato SQL
                forecast_csv.to_sql(name=f'covid_{i.lower()}_pred', con=engine, if_exists='replace')
            print('Previsão realizada com sucesso!\n')
            print("Todos os arquivos foram gerados!")
            
        # Caso seja escolhido apenas um país
        else:
            country = countries[choice]
            series = create_series(df, country)
            print('Previsão em andamento...')
            forecast = SARIMAXModel(series, ['Confirmed'])
            forecast.fit_and_predict()
            print('Previsão realizada com sucesso!\n')
            
            # Cria um DataFrame com os resultados
            forecast_csv = forecast.test.copy()
            forecast_csv['prediction'] = forecast.predictions.copy()
            
            # Salva o resultado em formato SQL
            forecast_csv.to_sql(name=f'covid_{country.lower()}_pred', con=engine, if_exists='replace')
            print(f"Arquivo '{country}.csv' foi gerado!")


        # Pergunta ao usuário se ele quer continuar a executar o programa
        print('\nGostaria de realizar novas previsões?\nNão : 0\nSim : 1')
        continue_choice = int(input('Digite um número: ')) 
        if continue_choice == 0:
            running = False
            print('\nPROGRAMA FINALIZADO!\n')


# Criação do motor de conexão com o banco de dados
engine = create_engine("mysql+mysqlconnector://admin:bootcamp_covid@database-1.cjpz0qecuge2.sa-east-1.rds.amazonaws.com/bootcamp_covid")
port = int(input('port: '))
user = input('user: ')
password = input('password: ')
cnx = mysql.connector.connect(
                                host="database-1.cjpz0qecuge2.sa-east-1.rds.amazonaws.com",
                                port=port,
                                user=user,
                                password=password,
                                database='bootcamp_covid' # Nome do banco de dados a ser utilizado
                             )

cur = cnx.cursor() # Criação do cursor para manipulação do banco de dados
query_ts = 'SELECT * FROM covid_raw_data' # String com a query a ser executada
data = pd.read_sql(query_ts, engine).drop('index', 1)

# Alterando colunas
for i in data.columns:
    if i != 'country_region':
        data.rename(columns = {i:re.sub(r'\s|_', r' ', i).capitalize()}, inplace = True)
    else:
        data.rename(columns= {i:"Country/Region"}, inplace=True)


df = data[data['Country/Region'].isin(['Mexico', 'Argentina', 
                                        'Ecuador', 'Chile', 'Spain'])] # Seleção apenas dos países escolhidos
df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")


create_forecast(df) # função para criar as previsões
