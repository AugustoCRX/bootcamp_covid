# -*- coding: utf-8 -*-
"""make_dataset_countries_bot.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-zv_1ZgFhSKo7EFJTxAE1Ljn3PHGewPq
"""

# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
!pip install clean-text
from cleantext import clean
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
from string import punctuation
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import os
import json
from keras.models import model_from_json
import time
import datetime
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('output_filepath', type=click.Path(), default = Path(__file__).resolve().parents[2])
def main(output_filepath):
    start_time = time.time()
    print("\nLoading Argentina's dataset...")
    """ Execute data processing scripts to gather country dataset data (../raw) and
        and make them ready for sorting (saved in ../processed).
    """
    print('Loading data...')
    caminho_countries = r"{}/content/drive/MyDrive/Blue Edtech 1semestre/Módulo 7/data/publicacoes".format(project_dir)
    print('Loading csv files...')
    publicacoes = pd.read_csv(caminho_countries)

    # removing emoji
    publicacoes['text'] = publicacoes['text'].apply(lambda x: clean(x, no_emoji=True))

    # removing stopwords and punctuation
    tt = TweetTokenizer()
    publicacoes['text'] = publicacoes['text'].apply(tt.tokenize)
    stopwords = set(stopwords.words('spanish') + list(punctuation))
    publicacoes['text'] = publicacoes['text'].apply(lambda x: ' '.join([word for word in x if word not in (stopwords)]))

    # padding the dataset
    train = pd.read_csv('/content/drive/MyDrive/Blue Edtech 1semestre/Módulo 7/data/treino')
    tk = Tokenizer()
    tk.fit_on_texts(train['review_es'].apply(str))
    tk_publicacoes = tk.texts_to_sequences(publicacoes['text'].apply(str))
    publicacoes_pad = pad_sequences(tk_publicacoes,padding="post",maxlen = 725)

    # adding the prediction dimensionality to the dataset
    # loading the model and its parameters
    json_file = open('/content/drive/MyDrive/Blue Edtech 1semestre/Módulo 7/data/model2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("/content/drive/MyDrive/Blue Edtech 1semestre/Módulo 7/data/model2.h5")
    print("Loaded model from disk")
    # sorting the data
    predicao = loaded_model.predict(publicacoes_pad)
    lista = []
    for i in range(0,280558):
      soma = 0
      for j in range(0,725):
        soma = predicao[i][j] + soma
      pontuacao = soma/725
      if pontuacao < 0.5:
        lista.append(0)
      else:
        lista.append(1)
    publicacoes['prediction'] = lista

    # selecting the time range
    publicacoes['date'] = pd.to_datetime(publicacoes.date, format="%Y-%m-%d")
    data_inicio = datetime.datetime(2020, 2, 1)
    data_final = datetime.datetime(2020, 7, 31)
    df_analise = publicacoes[(data_inicio <= publicacoes['date']) &  (data_final > publicacoes['date']) ]


    # saving the dataset
    df_analise.to_csv(r'{}\data\results_twitter\df_analise.csv'.format(output_filepath))
    print("Finishing Prediction's dataset...\n")
    print("Execution time: %s seconds \n" % (time.time() - start_time))
    

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()