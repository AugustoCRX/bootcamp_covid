# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
import os
import glob
import json
from textblob import TextBlob as tb
from selenium import webdriver
import time
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('output_filepath', type=click.Path(), default = Path(__file__).resolve().parents[2])
def main(output_filepath):
    start_time = time.time()

    print("\nStarting Chile's dataset...")

    def read_json_file(file):
        with open(file, "r", encoding='utf8') as r:
            response = r.read()
            response = response.replace('\n', '')
            response = response.replace('}{', '},{')
            response = "[" + response + "]"
            return json.loads(response)

    def flatten_list(_2d_list):
        flat_list = []
        for element in _2d_list:
            if type(element) is list:
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        return flat_list

    caminho_CL = r"{}\data\external\twitter\CHILE\DATA".format(project_dir)
    list_CL = glob.glob(os.path.join(caminho_CL, '*/*'))
    print('Loading json files...')
    # extraindo json e criando lista
    dict_CL = list()
    for i in range(len(list_CL)):
        dict_CL.append(read_json_file(list_CL[i]))
    dict_CL = flatten_list(dict_CL)
    
    #Extração do "place_id" para coleta de dados geográficos
    data_extraction = []
    for i in range(len(dict_CL)):
        try:
            for j in range(len(dict_CL[i]['data'])):
                place_id = dict_CL[i]['data'][j]['geo']['place_id']
                data_extraction.append(place_id) 
        except:
            continue  
    data_extraction = list(set(data_extraction))
    bot_activation = input('Digite 1 para ativar o bot de coleta de dados geográficos')
    if bot_activation == 1:
        # Bot de extração de dados geográficos
        # Para execução é necessário tirar os comentários do código
        login = input('Insira seu nome no twitter (tag)') #Colocar como input
        password = input('Insira sua senha') #Colocar como input
        options = webdriver.ChromeOptions() #Execução do webdriver do google
        options.add_experimental_option("prefs", {
        "download.default_directory": r"E:\Blue\Bootcamp 2\github\bootcamp_covid\data_extraction\CHILE\GEO"
        })
        browser = webdriver.Chrome(options=options)
        browser.get('https://twitter.com/')
        time.sleep(2)
        # Os elementos serão acessados via xpath, que é o path do HTML do site, buscando botões e caixa de interação
        browser.find_element('xpath', '/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div/span/span').click()
        time.sleep(2)
        # É seguro inserir seus dados, visto que o algoritmo só guardará seus dados na memória do seu computador
        browser.find_element('xpath', '//html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(login)
        time.sleep(2)
        browser.find_element('xpath', '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
        time.sleep(2)
        browser.find_element('xpath', '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(password)
        time.sleep(2)
        browser.find_element('xpath', '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span').click()
        time.sleep(2)
        # Um loop para acessar os dados do "place_id" que estão dentro da lista data_extraction
        for place_id in data_extraction:  
            browser.get(f'https://api.twitter.com/1.1/geo/id/{place_id}.json')
        # A API do twitter restringe o uso da coleta de "place_id" em 100 vezes/hora então esse tempo é calculado
        # prevendo possíveis "bugs" e considerando o tempo limite por hora
        time.sleep(40)

    #Leitura dos dados geográficos
    print('Reading geographical data...')
    geo_path = r"{}\data\external\twitter\CHILE\GEO".format(project_dir)
    itens = os.listdir(geo_path)
    dict_CL_GEO = list()
    for i in itens:
        with open(f'{geo_path}/{i}', 'r', encoding='utf8') as f:
            dict_CL_GEO.append(json.load(f))
    print('Building the data...')
    #Construção dos dados
    all_text = []
    for i in range(len(dict_CL)):
        try:
            for j in range(len(dict_CL[i]['data'])):
                text = dict_CL[i]['data'][j]['text']
                for tweet in [dict_CL[i]['data'][j]['text']]:
                    analysis = tb(tweet)
                    polarity = analysis.sentiment.polarity
                retweet = dict_CL[i]['data'][j]['public_metrics']['retweet_count']
                like = dict_CL[i]['data'][j]['public_metrics']['like_count']
                date = dict_CL[i]['data'][j]['created_at'].split('T')[0]
                for z in range(len(dict_CL_GEO)):
                    if dict_CL_GEO[z]['id'] == dict_CL[i]['data'][j]['geo']['place_id']:
                        lat = dict_CL_GEO[z]['centroid'][1]
                        long = dict_CL_GEO[z]['centroid'][0]
                all_text.append(dict(text = text,
                                    score = polarity,
                                    retweet = retweet,
                                    like = like,
                                    date = date,
                                    lat = lat,
                                    long = long
                                    )) 
        except:
            continue 
    
    CL_df = pd.DataFrame(all_text)
    CL_df.to_csv(r'{}\data\bronze\twitter_bronze\CL_raw_data.csv'.format(output_filepath))
    print("Finishing Chile's dataset...\n")
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
