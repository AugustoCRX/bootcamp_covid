# -*- coding: utf-8 -*-
"""make_dataset_publicacoes_bot.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-zv_1ZgFhSKo7EFJTxAE1Ljn3PHGewPq
"""

# -*- coding: utf-8 -*-

# necessário instalar os pacotes: pip install clean-text e pip install python-dotenv

import click
import logging
from pathlib import Path
import cleantext
from cleantext import clean
import nltk
from nltk.tokenize import TweetTokenizer
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords.words('spanish')
from string import punctuation
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import os
import json
from keras.models import model_from_json
import time
import datetime
import dotenv
from dotenv import find_dotenv, load_dotenv

@click.command()
@click.argument('output_filepath', type=click.Path(), default = Path(__file__).resolve().parents[2])
def main(output_filepath):
    start_time = time.time()
    print("\nLoading countries's dataset...")
    """ Execute data processing scripts to gather country dataset data (../raw)
        and make them ready for sorting (saved in ../processed).
    """
    print('Loading data...')
    print('Loading csv files...')
    countries = os.listdir(r'{}\data\external\twitter'.format(project_dir))
    dict_df = {}
    for i in countries:
      dict_df[i] = pd.read_csv(r'{}\data\bronze\twitter_bronze\{}_raw_data.csv'.format(project_dir, "".join(list(i)[0:2]).upper()))
      dict_df[i]['country'] = i.capitalize()

    publications = pd.concat([dict_df[i] for i in list(dict_df.keys())])

    # removing emoji
    publications['text'] = publications['text'].apply(lambda x: clean(x, no_emoji=True))

    # removing stopwords and punctuation
    tt = TweetTokenizer()
    publications['text'] = publications['text'].apply(tt.tokenize)
    list_stopwords_punctuation = set(stopwords.words('spanish') + list(punctuation))
    publications['text'] = publications['text'].apply(lambda x: ' '.join([word for word in x if word not in (list_stopwords_punctuation)]))

    # padding the dataset
    train = pd.read_csv(r'{}\data\twitter_ai\train\train.csv'.format(project_dir))
    tk = Tokenizer()
    tk.fit_on_texts(train['review_es'].apply(str))
    tk_publications = tk.texts_to_sequences(publications['text'].apply(str))
    publications_pad = pad_sequences(tk_publications,padding="post",maxlen = 725)

    # adding the prediction dimensionality to the dataset
    # loading the model and its parameters
    json_file = open(r'{}\data\twitter_ai\models\model.json'.format(project_dir), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(r'{}\data\twitter_ai\models\model.h5'.format(project_dir))
    print("Loaded model from disk")
    
    # classifying the data
    prediction = loaded_model.predict(publications_pad)
    list_size = len(prediction)
    list1 = []
    for i in range(0,list_size):
      sum = 0
      for j in range(0,725):
        sum = prediction[i][j] + sum
      pontuacao = sum/725
      if pontuacao < 0.5:
        list1.append(0)
      else:
        list1.append(1)
    publications['prediction'] = list1

    # selecting the time range
    # converting column 'date' from a string to datetime.
    publications['date'] = pd.to_datetime(publications['date'])

    # set the index to the 'date' column
    publications.set_index('date', inplace=True)

    # select time range
    start_date = '2020-01-02'
    end_date = '2020-07-31'
    df_analise = publications.loc[start_date:end_date]
    df = df_analise['Unnamed: 0'].reset_index()
    df_analise.set_index('Unnamed: 0', inplace=True)
    df_analise['date'] = df['date']

    # saving the dataset
    df_analise.to_csv(r'{}\data\twitter_ai\results\df_analise.csv'.format(output_filepath))
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