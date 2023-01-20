import mysql.connector
import os
import numpy as np
import pandas as pd
import re
from mysql.connector import Error
from sqlalchemy import create_engine
import click
from pathlib import Path
import logging
from dotenv import find_dotenv, load_dotenv

#This script only contains treatment and MySQL create server
#Need credentials to login in AWS Server
#SQL server created on AWS RDS service
@click.command()
@click.argument('output_filepath', type=click.Path(), default = Path(__file__).resolve().parents[2])
def main(output_filepath):

    def country_id_const(df,column):
        list_id = []
        for i in range(len(df)):
            index = int(country_id['countryID'].where(country_id['countries'] == covid[column].iloc[i]).dropna().values)
            list_id.append(index)
        df['countryID'] = list_id
        return df

    host = input('Insert host link here ')
    port = int(input('Insert port number here '))
    user = input('Insert user ')
    password = input('Insert password ')
    database = input('Insert database name ')
    
    print('Trying to connect to the database...')
    #Creating engine and connection to database
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    cnx = mysql.connector.connect(
    host=host,
    port = port,
    user=user,
    password=password,
    database =database)
    cur = cnx.cursor()
    print('Loading data...')
    
    #Create a list from analyzed countries
    countries = [i.capitalize() for i in os.listdir(r'{}\data\external\twitter'.format(output_filepath))]
    print('Creating country_id table...')
    
    #Creating id table from country list
    for i in countries:
        country_id = {v:k+1 for k,v in enumerate(countries)}
    country_id = pd.DataFrame(data = country_id, index=[0]).T.reset_index().rename({'index':'countries', 0:'countryID'}, axis = 1)
    country_id.to_sql(name=f'country_id', con=engine, if_exists='replace')
    print('-----------Complete-----------')
    print('Loading twitter data...')
    
    #Load raw twitter data
    dict_df = {}
    for i in countries:
        dict_df[i] = pd.read_csv(r'{}\data\bronze\twitter_bronze\{}_raw_data.csv'.format(project_dir, "".join(list(i)[0:2]).upper()))
        dict_df[i].drop('Unnamed: 0',axis = 1 ,inplace=True)
        dict_df[i]['date'] = pd.to_datetime(dict_df[i]['date'])
        dict_df[i]['country'] = i
        index = np.where(country_id['countries'] == i)
        dict_df[i]['countryID'] = int(country_id['countryID'].iloc[index])
    print('Creating twitter raw data table...')
    
    # Transform raw data into SQL Table
    for i in dict_df:
        dict_df[i].to_sql(name=f'{i.lower()}_raw_table', con=engine, if_exists='replace')
    print('-----------Complete-----------')
    print('Loading covid raw data...')
    
    #Load raw covid data
    covid = pd.read_csv(r'{}\data\external\covid_data\full_grouped.csv'.format(output_filepath))
    for i in covid.columns:
        covid.rename(columns = {i:re.sub(r'\s|/', r'_', i).lower()}, inplace = True)
    print('Creating covid raw data table...')
    covid.to_sql(name=f'covid_raw_data', con=engine, if_exists='replace')
    print('-----------Complete-----------')
    print('Loading covid silver data...')
   
    #Load silver covid data
    covid = pd.read_csv(r'{}\data\external\covid_data\full_grouped.csv'.format(output_filepath))
    for i in covid.columns:
        covid.rename(columns = {i:re.sub(r'\s|/', r'_', i).lower()}, inplace = True)
    covid = covid.loc[covid['country_region'].isin(countries)].drop('who_region', axis = 1)
    country_id_const(covid, 'country_region')
    print('Creating covid silver data table...')
    covid.to_sql(name=f'covid_silver_data', con=engine, if_exists='replace')
    print('-----------Complete-----------')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()