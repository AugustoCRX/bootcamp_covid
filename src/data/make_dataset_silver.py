# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
import time
import os
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('output_filepath', type=click.Path(), default = Path(__file__).resolve().parents[2])
def main(output_filepath):
    start_time = time.time()

    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    print('Reading files...')
    countries = os.listdir(r'{}\data\external\twitter'.format(project_dir))
    dict_df = {'COVID all data': pd.read_csv(r'{}\data\external\covid_data\full_grouped.csv'.format(project_dir))}
    for i in countries:
        dict_df[i] = pd.read_csv(r'{}\data\bronze\twitter_bronze\{}_raw_data.csv'.format(project_dir, "".join(list(i)[0:2]).upper()))
    #A utilização destes dados se da por conta da origem dos dados do kaggle virem desses dados e já foi verificado que os dados são os mesmos,
    #com isso será utilizado os dados gerados na variável "df" para o andamento do trabalho
    all = pd.concat([dict_df[i] for i in list(dict_df.keys())[1::]])
    all.drop('Unnamed: 0', axis = 1)
    # carrega os dados em um dicionário
    # print(dict_df['COVID all data']['location'].isin([i.capitalize() for i in countries]))
    query_country = dict_df['COVID all data'].isin({'location':[i.capitalize() for i in countries]})
    # pd.display(dict_df['COVID all data']['location'].isin([i.capitalize() for i in countries]))
     #Cria as colunas target
    print('Saving data...')
    query_country.to_csv(r'{}\data\silver\covid\covid_silver.csv'.format(output_filepath))
    all.to_csv(r'{}\data\silver\twitter\twitter_data.csv'.format(output_filepath))
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    print('''
    Finishing script
    Execution time:
    ''')

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
