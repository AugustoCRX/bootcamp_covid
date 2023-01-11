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

#from pathlib import Path

#!pip install pmdarima
from pmdarima import auto_arima


def criar_serie(df, nome_pais):

    filtro = df[df['Country/Region'] == nome_pais]
    pais = filtro[['Date', 'Confirmed', 'Deaths']]
    
    pd.to_datetime(pais.Date)
    pais.set_index('Date', inplace=True)
    
    return pais


class Modelo_SARIMAX():
    def __init__(self, serie, coluna):
        self.serie = serie
        self.coluna = coluna


    def autoarima_e_treino(self):
        
        # auto_arima
        X = self.serie.groupby('Date')[self.coluna].sum().copy()
        
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
                        seasonal_order=results[1]).fit(disp=False)

        self.pred = model.predict(  start=start,
                                    end=end,
                                    dynamic=False,
                                    typ='levels')
        
        self.pred.index = self.test.index


    def metricas(self):
        print(f"R²   ---  {r2_score(self.test, self.pred):.2f}")
        print(f"MAE  ---  {mean_absolute_error(self.test, self.pred):.2f}")
        print(f"RMSE ---  {mean_squared_error(self.test, self.pred, squared=False):.2f}")
        print(f"MAPE ---  {mean_absolute_percentage_error(self.test, self.pred)}")


    def graficos(self):
        fig, axs = plt.subplots(2, 1, figsize=(10, 4), constrained_layout=True)

        ax = axs[0]
        ax.set_title(f'Predição para o Nº de {self.coluna[0]}')
        ax.plot(self.test, label='Test') # color='orange'
        ax.plot(self.pred, label='Prediction') # color='green'
        ax.legend(loc='best')

        ax = axs[1]
        ax.set_title(f'Predição para o Nº de {self.coluna[0]}')
        ax.plot(self.train, label='Train')
        ax.plot(self.test, label='Test')
        ax.plot(self.pred, label='Prediction')
        ax.legend(loc='best')

        plt.show()


#caminho = Path(__file__).resolve().parents[2]
dados = pd.read_csv(r'D:\Blue EdTech\Bootcamp\dados\full_grouped.csv')
df = dados[dados['Country/Region'].isin(['Mexico', 'Argentina', 
                                        'Ecuador', 'Chile', 'Spain'])]
df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")

rodando = True
while rodando:
    print("""
    Deseja criar a previsão para o numero de confirmados para qual pais?

    Todos     : 0
    Argentina : 1
    Chile     : 2
    Equador   : 3
    México    : 4
    Espanha   : 5
    """)

    países = ['Argentina', 'Chile', 'Ecuador', 'Mexico', 'Spain']
    escolha = int(input('Digite o número: '))
    país = países[escolha - 1]

    if escolha == 0:
        serie = criar_serie(df, df['Country/Region'])
    else:
        serie = criar_serie(df, país)

    print('Previsão em andamento...')
    predicao = Modelo_SARIMAX(  serie = serie,
                                coluna = ['Confirmed'])
    predicao.autoarima_e_treino()
    print('Previsão realizada com sucesso!\n')

    print('\nDeseja ver as Metricas?\nNão : 0\nSim : 1')
    escolha_metricas = int(input('Digite o número: '))
    if escolha_metricas == 1:
        print(f'\nMETRICAS')
        print(predicao.metricas())

    print('\nDeseja ver os graficos?\nNão : 0\nSim : 1')
    graficos = int(input('Digite o número: '))
    if graficos == 1 and escolha > 0:
        print(f'\nGraficos do numero de confirmado - {país}')
        print(predicao.graficos())
    elif graficos == 1 and escolha == 0:
        print('\nGraficos do numero de confirmado - Todos os Países')
        print(predicao.graficos())
        pass

    print('\nDeseja salvar os dados da previsão?\nNão : 0\nSim : 1')
    escolha_salvar = int(input('Digite um número: '))
    if escolha_salvar == 1:
        predicao_csv = predicao.test.copy()
        predicao_csv['pred'] = predicao.pred.copy()
        predicao_csv.to_csv(f'{str(país)}.csv')

    print('\nGostaria de realizar novas previsões?\nNão : 0\nSim : 1')
    escolha_continuar = int(input('Digite o número: '))
    if escolha_continuar == 0:
        rodando = False
        print('\nPROGRAMA FINALIZADO!\n')

