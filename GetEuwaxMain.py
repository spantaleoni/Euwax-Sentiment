import requests
import re
from bs4 import BeautifulSoup
from datetime import date, time, datetime, timedelta
import numpy as np
from w3lib.html import replace_entities
import pandas as pd
import matplotlib.pyplot as plt
from pykalman import KalmanFilter

import telegram_send

''' https://api.onvista.de/api/v1/instruments/INDEX/59198950/times_and_sales?endDate=2022-11-14T23:59:59.000+00:00&idNotation=59198950&order=DESC&startDate=2022-11-14T00:00:00.000+00:00

'''



G_TITLE = '** EUWAX SENTIMENT **'
G_EUWPeriod = 48

G_BASEURL = 'https://api.onvista.de/api/v1/instruments/INDEX/59198950/times_and_sales?endDate='
#G_BASEURL2 = '2022-11-14T23:59:59.000+00:00&idNotation=59198950&order=DESC&startDate='
G_BASEURL2 = 'T23:59:59.000+00:00&idNotation=59198950&order=DESC&startDate='
#G_BASEURL3 = '2022-11-14T00:00:00.000+00:00'
G_BASEURL3 = 'T00:00:00.000+00:00'
G_Filename = 'EuwaxSentiment_'

G_TodayDate = date.today()
#G_TodayDate = date.today() - timedelta(days=1)

TelegramFLAG = True
#https://www.global-rates.com/en/interest-rates/central-banks/central-banks.aspx

#page = requests.get('https://intomillion.com/central-bank-rates/') # Getting page HTML through request
page = requests.get('https://www.boerse-stuttgart.de/en/products/indices/a1maa5-euwax-sentiment-index')
soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup


#print(soup)
#links = soup.select("tr class=""tabledata1"") # Selecting all of the anchors with titles
rows = soup.find_all('div', {'class': re.compile('bsg-card__wrapper*')})

#lines = rows.find_all('td')
#results = [r.text.split(' ')[0].strip() for r in rows]
res = [r.text.strip() for r in rows]
res = [BeautifulSoup(r, "lxml").text for r in res]
res = [r.replace('\t', '') for r in res]
res = [r.replace('\r', '') for r in res]
res = [r.replace('\n', ' ') for r in res]
results = [r.split('\n') for r in res]
results = results[:4]


def main():
    if TelegramFLAG:
        telegram_send.send(messages=[G_TITLE])
        telegram_send.send(messages=res)
    
    
    CompileUrl = G_BASEURL + str(G_TodayDate) + G_BASEURL2 + str(G_TodayDate) + G_BASEURL3
    HttpResp = requests.get(CompileUrl)
    jsonHttpResp = HttpResp.json()
    
    EuwaxDay = pd.DataFrame(columns=['Date', 'Price', 'Mean', 'Kalman'])
    print("Print each key-value pair from JSON response")
    for key, value in jsonHttpResp.items():
        if key == 'price':
            #print(key, ":", value)
            t_prices = value
        if key == 'datetimePrice':
            print(key, ":", value)
            t_dates = value

    series_1 = pd.Series(t_prices)
    series_2 = pd.Series(t_dates)
    
    
    EuwaxDay['Date'] = series_2
    EuwaxDay['Price'] = series_1
    EuwaxDay = EuwaxDay.iloc[::-1]
    EuwaxDay = EuwaxDay.loc[(EuwaxDay['Price']!=0)]
    # Get the window of series
    # of observations of specified window size
    windows = EuwaxDay['Price'].rolling(G_EUWPeriod)
    moving_averages = windows.mean()
      
    # Convert pandas series back to list
    moving_averages_list = moving_averages.tolist()
    EuwaxDay['Mean'] = moving_averages_list
    
    for i in range(len(EuwaxDay)):
        if i > G_EUWPeriod:
            prices = EuwaxDay['Price'][:(i)][-G_EUWPeriod:]
            L = np.array(prices)
        
            kf = KalmanFilter(transition_matrices = [1],
                     observation_matrices = [1],
                     initial_state_mean = 1,
                     initial_state_covariance = 1.5,
                     observation_covariance=1,
                     transition_covariance=.01)
        
            kf,_ = kf.filter(L)
            EuwaxDay.loc[i, 'Kalman'] = kf[-1]
        else:
            EuwaxDay.loc[i, 'Kalman'] = 0
    
    
    EuwaxDay.plot(x='Date', y=['Price', 'Mean'], figsize=(15, 8))
    filename = G_Filename + str(G_TodayDate) + '.jpeg'
    title = 'EUWAX Sentiment ' + str(G_TodayDate)
    plt.grid(True)
    plt.title(title)
    plt.axis('tight')
    plt.xlabel('Time')
    plt.savefig(filename)
    
    if TelegramFLAG:
        with open(filename, "rb") as fmarket:
            telegram_send.send(images=[fmarket])
            
main()