# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
import time
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('output_filepath', type=click.Path(), default = Path(__file__).resolve().parents[2])
def main(output_filepath):
    start_time = time.time()

    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    print('Reading files...')
    df = pd.read_csv(r'{}\data\external\covid_data\owid-covid-data.csv'.format(project_dir))
    df0 = pd.read_csv(r'{}\data\bronze\twitter_bronze\AR_raw_data.csv'.format(project_dir))
    df0['Country'] = 'Argentina'
    df1 = pd.read_csv(r'{}\data\bronze\twitter_bronze\CL_raw_data.csv'.format(project_dir))
    df1['Country'] = 'Chile'
    df2 = pd.read_csv(r'{}\data\bronze\twitter_bronze\MX_raw_data.csv'.format(project_dir))
    df2['Country'] = 'Mexico'
    df3 = pd.read_csv(r'{}\data\bronze\twitter_bronze\EQ_raw_data.csv'.format(project_dir))
    df3['Country'] = 'Ecuador'
    df4 = pd.read_csv(r'{}\data\bronze\twitter_bronze\ES_raw_data.csv'.format(project_dir)) 
    #A utilização destes dados se da por conta da origem dos dados do kaggle virem desses dados e já foi verificado que os dados são os mesmos,
    #com isso será utilizado os dados gerados na variável "df" para o andamento do trabalho
    paises = ['Mexico', 'Argentina', 'Ecuador', 'Chile', 'Spain']
    all = pd.concat([df0,df1,df2,df3,df4])
    all.drop('Unnamed: 0', axis = 1)
    # carrega os dados em um dicionário
    query_country = df[df['location'].isin(paises)]
     #Cria as colunas target
    columns = ['date','population', 'diabetes_prevalence', 'median_age', 'total_vaccinations', 'hosp_patients','people_fully_vaccinated', 'total_vaccinations_per_hundred','people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','population_density', 'cardiovasc_death_rate','female_smokers', 'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand', 'life_expectancy', 'human_development_index']
    print('Quering data...')
    add_info_data = query_country.loc[:, columns]
    print('Saving data...')
    add_info_data.to_excel(r'{}\data\silver\add_info.xlsx'.format(output_filepath))
    all.to_excel(r'{}\data\silver\twitter_data.xlsx'.format(output_filepath))
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
