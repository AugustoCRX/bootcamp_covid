# Extração de dados

Nessa seção é possível consultar as metodologias empregadas na extração de dados do twitter

## Tecnologias utilizadas:

<ul>
<li>Python</li>
<li>Selenium</li>
<li>JSON</li>
<li>Pandas</li>
</ul>


## Dicionário de dados:

### Dados do twitter

| Nome da coluna | Tipo | Descrição | Observação |
| :---- | :---- | :--- | :--- |
| text | Categórico nominal | Texto presente no tweet | - |
| polarity  | Categorico ordinal | Pontuação dos sentimentos | Está definido entre -1 e 1 |
| retweet | Numérica contínua | Número de retweets da publicação | - |
| like | Numérica contínua | Número de likes da publicação | - |
| date | Numérica contínua | Data da criação do tweet | - |
| lat | Numérica discreta | Latitude | - |
| long | Numérica discreta | Longitude | - |
| sentiment (implementação futura) | Categórico nominal | Descrição do sentimento do tweet | - |

OBS: OS DADOS DO MÉXICO E ESPANHA ESTÃO SEM LATITUDE E LONGITUDE, POIS A COLETA DE DADOS IRÁ DEMORAR
