## Projeto Blue - Bootcamp 2
## Grupo 02
## Turma: C014
## Integrantes:

<div>&nbsp;</div>
<h3>Augusto Cesar Rodrigues Xavier&nbsp;&nbsp<a href = "https://github.com/AugustoCRX" target = "_blank"><img src = "https://img.shields.io/badge/-Github-000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/AugustoCRX" target = "_blank"></img>&nbsp;&nbsp;&nbsp;&nbsp;</a><a href = "https://www.linkedin.com/in/augustocrx/" target = "_blank"><img src = "https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/augustocrx/" target = "_blank"></img></h3>
        
<h3>Lucílio Fontes Moura&nbsp;&nbsp&nbsp;<a href = "https://github.com/LucilioFM" target = "_blank"><img src = "https://img.shields.io/badge/-Github-000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/AugustoCRX" target = "_blank"></img>&nbsp;&nbsp;&nbsp;</a><a href = "https://www.linkedin.com/in/luciliofm/" target = "_blank"><img src = "https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/augustocrx/" target = "_blank"></img></h3>

<h3>Bruno Rodrigues Barbosa&nbsp;&nbsp&nbsp;<a href = "https://github.com/brunodatac" target = "_blank"><img src = "https://img.shields.io/badge/-Github-000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/AugustoCRX" target = "_blank"></img>&nbsp;&nbsp;&nbsp;</a><a href = "https://www.linkedin.com/in/bruno-datascience/" target = "_blank"><img src = "https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/augustocrx/" target = "_blank"></img></h3>


&nbsp;
# Desafio

&nbsp;&nbsp;&nbsp;&nbsp;O desafio apresentado conta com a coolaboração entre as empresas Blue EdTech e DataEX com o objetivo de utilizar a base de dados presente no site Kaggle com o título <a href = 'https://www.kaggle.com/datasets/imdevskp/corona-virus-report?resource=download' target="_blank" style = "color:blue">COVID-19 Dataset</a>, para realizar a predição temporal das mortes, e utilizar a API do twitter, para caracterizar os textos quanto ao seu sentimentos.

<p style = "font-size:12px;color:black">A documentação do twitter pode ser consultada <a href = 'https://developer.twitter.com/en/docs' style = "font-size: 12px;color:blue">clicando aqui</a></p>


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── bi_data        <- Data from third party sources.
    │   ├── bronze         <- Intermediate data that has been transformed.
    |   |       └── twitter_bronze
    │   ├── external       <- The final, canonical data sets for modeling.
    |   |       └── covid_data
    |   |       └── twitter
    |   ├── golden
    |   ├── results_model_forecast
    |   ├── results_twitter
    |   ├── silver
    |   |       └── covid
    |   |       └── twitter
    │   └── twitter_ai     <- The original, immutable data dump.
    |           └── models
    |           └── results
    |           └── train
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── env
    |
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    |
    ├── requirements.txt<- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    |
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
