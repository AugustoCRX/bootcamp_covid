### Projeto Blue - Bootcamp 2
### Grupo 02
### Turma: C014
### Integrantes:

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
    │   ├── external       <- Data from third party sources.
    │   ├── bi_data        <- Data used for BI analysis
    │   ├── results_model_forecast <- Results from forecast model
    │   ├── twitter_ai     <- Results from Twitter sentiment analysis
    │   ├── silver         <- Intermediate data that has been transformed.
    │   ├── golden         <- The final, canonical data sets for modeling.
    │   └── bronze         <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── env                <- Virtual environment
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │   ├── MySQL models   <- MYSQL Models
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
