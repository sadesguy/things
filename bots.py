_____________PUMP/DUMP____________

import requests
import time

url = "https://api.bitget.com/api/mix/v1/market/tickers?productType=umcbl"

prices = {}  # store last price of all coins
chat_id = "-1001888585058"
bot_token = "6096943261:AAH63gKN-oLHWTuVN00Q8wdpsfI4FW_rvko"
alert_sent = {}  # track the last time an alert was sent


def get_last_price():
    try:
        response = requests.get(url)
        data = response.json()

        for coin in data["data"]:
            symbol = coin["symbol"]
            last_price = float(coin["last"])
            usdt_volume = float(coin["usdtVolume"])

            if usdt_volume == 0:  # skip entries with usdtVolume equal to 0
                continue

            if symbol in prices:
                prices[symbol].append(last_price)
                prices[symbol] = prices[symbol][-30:]  # keep only the last 30 prices
            else:
                prices[symbol] = [last_price]
    except Exception as e:
        print(f"Error occurred while fetching price data: {str(e)}")


def analyze_price_change():
    get_last_price()
    time.sleep(60)  # wait for 1 minute

    if len(prices[list(prices.keys())[0]]) < 2:  # check if enough data is available
        return

    for symbol, price_history in prices.items():
        if symbol not in alert_sent:
            alert_sent[symbol] = 0

        if time.time() - alert_sent[symbol] < 300:  # 5 minutes cooldown for alerts
            continue

        price_change = price_history[-1] - price_history[0]  # calculate the change in price over the last 1 minute
        change_percent = price_change / price_history[0] * 100

        if change_percent > 2 or change_percent < -2:
            message = f"{symbol} has {'increased' if change_percent > 0 else 'decreased'} by {abs(change_percent):.2f}% in the last 1 minute"
            print(message)
            send_alert(message)
            alert_sent[symbol] = time.time()
            continue

        if len(price_history) >= 6:
            price_change = price_history[-1] - price_history[-5]  # calculate the change in price over the last 5 minutes
            change_percent = price_change / price_history[-5] * 100

            if change_percent > 4 or change_percent < -4:
                message = f"{symbol} has {'increased' if change_percent > 0 else 'decreased'} by {abs(change_percent):.2f}% in the last 5 minutes"
                print(message)
                send_alert(message)
                alert_sent[symbol] = time.time()
                continue

        if len(price_history) >= 30:
            price_change = price_history[-1] - price_history[-30]  # calculate the change in price over the last 30 minutes
            change_percent = price_change / price_history[-30] * 100

            if change_percent > 10 or change_percent < -10:
                message = f"{symbol} has {'increased' if change_percent > 0 else 'decreased'} by {abs(change_percent):.2f}% in the last 30 minutes"
                print(message)
                send_alert(message)
                alert_sent[symbol] = time.time()

def send_alert(message):
    urlt = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(urlt)
    print(response.json())

if __name__ == "__main__":
    while True:
        try:
            analyze_price_change()
        except Exception as B:
            print(B)
            time.sleep(10)




_______________KIR_______________


# -*- coding: utf-8 -*-

import requests
import time
import pandas_ta as ta
import pandas as pd
import numpy as np

def usdtpare():
  final = pd.DataFrame()
  prom = pd.DataFrame()
  url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
  params = {}
  r = requests.get(url, params = params)
  if r.status_code == 200:
    df = pd.DataFrame(r.json()["symbols"])
    df = df[df['status'] == 'TRADING']
    df = df[df['symbol'].str.contains('USDT')]
    df = df[df['contractType'] == 'PERPETUAL']
  final["pair"] = df["pair"]
  final["pricePrec"] = df["pricePrecision"].astype(int)
  final["qtyPrec"] = df["quantityPrecision"].astype(int)
  final = final.sort_values(by=['pair'])
  final = final.reset_index(drop=True)
  prom = pd.DataFrame.from_records(df["filters"])
  final['minPrice'] = pd.DataFrame.from_records(prom[0])['minPrice'].astype(float)
  final['maxPrice'] = pd.DataFrame.from_records(prom[0])['maxPrice'].astype(float)
  final['tickSize'] = pd.DataFrame.from_records(prom[0])['tickSize'].astype(float)
  final['stepSize'] = pd.DataFrame.from_records(prom[2])['stepSize'].astype(float)
  final['maxQty'] = pd.DataFrame.from_records(prom[2])['maxQty'].astype(float)
  final['minQty'] = pd.DataFrame.from_records(prom[2])['minQty'].astype(float)
  pare = list(final["pair"])
  return pare



def rsi_usdt(symb, tf, p):
  pare = symb
  url = 'https://fapi.binance.com/fapi/v1/klines'
  params = {'symbol': pare, 'interval': tf, 'limit': 30}
  r = requests.get(url, params = params)
  if r.status_code == 200:
    df = pd.DataFrame(r.json())
    m = pd.DataFrame()
    m['date'] = df.iloc[:, 0].astype(int)
    m['close'] = df.iloc[:, 4].astype(float)
    m[''+symb+''] = ta.rsi(m['close'], lenght=p)
    m = m.dropna()
    m[''+symb+''] = m[''+symb+''].round(1)
    return m[''+symb+'']
  else:
    return print('ошибка, проверьте правильность исходных данных')

def rsi_allsort(tf, p):
  max = pd.DataFrame()
  final = pd.DataFrame()
  USDTPARE = usdtpare()
  for i in USDTPARE:
    sim = rsi_usdt(i, tf, p)
    max = pd.concat([max, sim], axis=1)
  g = pd.DataFrame(max.iloc[-1,:])
  g[''] = g.iloc[:,0]
  g['pare'] = g.index
  g = g.sort_values(by='', ascending=False)
  g = g.dropna()
  final[''] = g['']
  return final


def funding(symb):
  pare = symb
  url = 'https://fapi.binance.com/fapi/v1/fundingRate'
  params = {'symbol': pare, 'limit' : 1}
  r = requests.get(url, params = params)
  if r.status_code == 200:
    df = pd.DataFrame(r.json())
    df['fundingRate'] = df['fundingRate'].astype(float)
    df[''+pare+''] = df['fundingRate'].copy()
  
  return df[''+pare+'']

def top_fund():
  max = pd.DataFrame()
  USDTPARE = usdtpare()
  for i in USDTPARE:
    sim = funding(i)
    max = pd.concat([max, sim], axis=1)
  g = pd.DataFrame(max.loc[0])
  g[''] = 100*g.iloc[:,0]
  g['pare'] = g.index
  g = g.sort_values(by='', ascending=False)
  g = g.drop(columns=0)
  g = g.drop(columns='pare')
  return g


def maxd(symb):
  pare = symb
  url = 'https://fapi.binance.com/fapi/v1/klines'
  params = {'symbol': pare, 'interval': '1d', 'limit': 1}
  r = requests.get(url, params = params)
  if r.status_code == 200:
    df = pd.DataFrame(r.json())
    m = pd.DataFrame()
    m['date'] = df.iloc[:, 0].astype(int)
    m['open'] = df.iloc[:, 1].astype(float)
    m['close'] = df.iloc[:, 4].astype(float)
    m[''+symb+''] = round(100*(m['close'] - m['open'])/m['open'], 2) 
    m = m.dropna()
    return m

def sort():
  max = pd.DataFrame()
  final = pd.DataFrame()
  USDTPARE = usdtpare()
  for i in USDTPARE:
    sim = maxd(i)
    max = pd.concat([max, sim], axis=1)
  max = max.drop(columns = ['date', 'open', 'close'])
  max = max.transpose()
  max = max.sort_values(by=0, ascending=False)
  max = max.rename(columns={0: ""})
  max = max[max[""] != 0]
  return max


def history_usdt(symb, tf, p):
  pare = symb
  url = 'https://fapi.binance.com/fapi/v1/klines'
  params = {'symbol': pare, 'interval': tf, 'limit': p}
  r = requests.get(url, params = params)
  if r.status_code == 200:
    df = pd.DataFrame(r.json())
    m = pd.DataFrame()
    m[''+symb+''] = df.iloc[:, 4].astype(float)
    return m[''+symb+'']
  else:
    return print('ошибка, проверьте правильность исходных данных')


def correl_all(tf, p, cond = 'lower', up = None, down = None):
  h = pd.DataFrame()
  USDTPARE = usdtpare()
  for i in USDTPARE:
    g = history_usdt(i, tf, p)
    h = pd.concat([h, g], axis=1)
  h = h.drop(['BTCDOMUSDT'], axis = 1)
  corr = round(h.corr(),2)
  if cond == 'lower':
    kl = corr[(corr.iloc[:,:] < down)]
    s = kl.unstack()
    so = s.sort_values(kind="mergesort")
    gg = pd.DataFrame(so).dropna()
    gg = gg.drop_duplicates()
  if cond == 'higher':
    kl = corr[(corr.iloc[:,:] > up)]
    s = kl.unstack()
    so = s.sort_values(kind="mergesort")
    gg = pd.DataFrame(so).dropna()
    gg = gg.drop_duplicates()
  if cond == 'medium':
    kl = corr[(corr.iloc[:,:] < up) & (corr.iloc[:,:] > down)]
    s = kl.unstack()
    so = s.sort_values(kind="mergesort")
    gg = pd.DataFrame(so).dropna()
    gg = gg.drop_duplicates()
    gg.rename(columns={0: ''})
  return gg, corr



import telebot
from telebot import types
token = '5746127569:AAHmY4uuKGaWRCSkzofkuAAxYsTuotHIGIo'

bot = telebot.TeleBot(token)
@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('RSI top 1h')
    item2 = types.KeyboardButton('RSI aut 1h')
    item3 = types.KeyboardButton('Correlation')
    item4 = types.KeyboardButton('Funding +')
    item5 = types.KeyboardButton('Funding -')
    item6 = types.KeyboardButton('Top day')
    item7 = types.KeyboardButton('Aut day')
    item8 = types.KeyboardButton('RSI top 1d')
    item9 = types.KeyboardButton('RSI aut 1d')

    markup.add(item1,item2,item3,item4,item5,item6,item7,item8,item9)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!' .format(message.from_user), reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'RSI top 1h':
            rsi1htop = rsi_allsort('1h', 14).head(10)
            bot.send_message(message.chat.id, f'RSI лидеры часовки :\n{rsi1htop}')
        elif message.text == 'RSI aut 1h':
            rsi1haut = rsi_allsort('1h', 14).tail(10)
            bot.send_message(message.chat.id, f'RSI аутсайдеры часовки :\n{rsi1haut}')
        elif message.text == 'RSI top 1d':
            rsi1dtop = rsi_allsort('1d', 14).head(10)
            bot.send_message(message.chat.id, f'RSI лидеры дневки :\n{rsi1dtop}')
        elif message.text == 'RSI aut 1d':
            rsi1daut = rsi_allsort('1d', 14).tail(10)
            bot.send_message(message.chat.id, f'RSI аутсайдеры дневки :\n{rsi1daut}')
        elif message.text == 'Funding +':
          funpl = top_fund()
          funpl = funpl.sort_values(by='', ascending=False)
          funpl = funpl.head(10)
          bot.send_message(message.chat.id, f'Лидеры положительного фандинга в % : \n{funpl}')
        elif message.text == 'Funding -':
          funm = top_fund()
          funm = funm.sort_values(by='', ascending=True)
          funm = funm.head(10)
          bot.send_message(message.chat.id, f'Лидеры отрицательного фандинга в % : \n{funm}')
        elif message.text == 'Top day':
          rost = sort().head(20)
          rost = rost[rost[''] > 0].head(10)
          bot.send_message(message.chat.id, f'Лидеры роста дня в % : \n{rost}')            
        elif message.text == 'Aut day':
          pad = sort().tail(20)
          pad = pad[pad[''] < 0]
          pad = pad.sort_values(by='', ascending=True)
          pad = pad.head(5)
          bot.send_message(message.chat.id, f'Лидеры падения дня в % : \n{pad}') 
        elif message.text == 'Correlation':
          corr = correl_all('1h', 72, 'lower', down = 0.0)[0].head().rename(columns={0: ''})
          bot.send_message(message.chat.id, f'Лидеры антикорреляции:\n{corr}')
        else:
          bot.send_message(message.chat.id, 'Не верно введены данные')

while True:
  try:
    bot.polling(none_stop = True)
    time.sleep(1)
  except Exception as e:
    print(e) 
    time.sleep(15)
_______________IMPULSE_____________

#!/usr/bin/env python3

import requests
import json
import time

# Telegram bot token and chat id
bot_token = "5859050982:AAEKeSkmMhTMTutB0dK0dr6xPg0Wwzva4gs"
chat_id = "-1001816696532"

# Store the previous high and low prices
previous_high_prices = {}
previous_low_prices = {}

while True:
    try:
        # Get the current high and low prices of the top 50 cryptocurrencies
        response = requests.get("https://api.bitget.com/api/mix/v1/market/tickers?productType=umcbl")
        data = json.loads(response.text)
        messages = []
        for coin in data["data"]:
            if coin["symbol"] in ["VETUSDT_UMCBL", "INJUSDT_UMCBL", "ANKRUSDT_UMCBL", "BATUSDT_UMCBL"]:
                continue
            if coin["usdtVolume"] == 0:
                continue
            high_price = coin["high24h"]
            low_price = coin["low24h"]
            symbol = coin["symbol"]
            previous_high_price = previous_high_prices.get(symbol, 0)
            previous_low_price = previous_low_prices.get(symbol, 0)

            if previous_high_price == 0:
                previous_high_prices[symbol] = high_price
            if previous_low_price == 0:
                previous_low_prices[symbol] = low_price

            if str(previous_high_price) == "0":
                high_change = 0
            else:
                high_change = (float(high_price) - float(previous_high_price)) / float(previous_high_price) * 100

            if str(previous_low_price) == "0":
                low_change = 0
            else:
                low_change = (float(low_price) - float(previous_low_price)) / float(previous_low_price) * 100

            # Check if the high price percent change exceeds 0.1%
            if abs(high_change) > 0.1:
            # Create the message for high price increase
                high_message = f"{symbol} max price increased by {high_change:.2f}%"
            # Add the message to the message string
                if high_change > 0:
                    messages.append(high_message)
            # Check if the low price percent change is less than -0.1%
            if low_change < -0.1:
                low_message = f"{symbol} min price decreased by {abs(low_change):.2f}%"
            # Add the message to the message string
                if low_change != 0:
                    messages.append(low_message)
            
            # Print the current high/low
            print(f"{symbol} current high price: {high_price}")
            print(f"{symbol} current low price: {low_price}")
            # Print the previous high and low price
            print(f"Previous high price: {previous_high_price}")
            print(f"Previous low price: {previous_low_price}")
            # Print the percent change
            print(f"High price percent change: {high_change:.2f}%")
            print(f"Low price percent change: {low_change:.2f}%\n")
           
            # Update the previous high and low prices
            previous_high_prices[symbol] = high_price
            previous_low_prices[symbol] = low_price

        # Send the message through Telegram if there are any messages
        if messages:
            message = "\n".join(messages)
            requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}")
            # Reset the messages list after sending
            messages = []

        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(10)


_______________IMPULSE BINANCE___________

import requests
import json
import time

# Telegram bot token and chat id
bot_token = "5859050982:AAEKeSkmMhTMTutB0dK0dr6xPg0Wwzva4gs"
chat_id = "-1001816696532"

# Store the previous high and low prices
previous_high_prices = {}
previous_low_prices = {}

# Binance Futures API endpoint for getting all symbols and their 24 hour high and low prices
binance_endpoint = "https://fapi.binance.com/fapi/v1/ticker/24hr"

while True:
    try:
        # Get the current high and low prices of all Binance Futures symbols
        response = requests.get(binance_endpoint)
        data = json.loads(response.text)
        messages = []
        for coin in data:
            if not coin["symbol"].endswith("USDT"):
                continue
            high_price = coin["highPrice"]
            low_price = coin["lowPrice"]
            symbol = coin["symbol"]
            previous_high_price = previous_high_prices.get(symbol, 0)
            previous_low_price = previous_low_prices.get(symbol, 0)

            if previous_high_price == 0:
                previous_high_prices[symbol] = high_price
            if previous_low_price == 0:
                previous_low_prices[symbol] = low_price

            if str(previous_high_price) == "0":
                high_change = 0
            else:
                high_change = (float(high_price) - float(previous_high_price)) / float(previous_high_price) * 100

            if str(previous_low_price) == "0":
                low_change = 0
            else:
                low_change = (float(low_price) - float(previous_low_price)) / float(previous_low_price) * 100

            # Check if the high price percent change exceeds 0.1%
            if abs(high_change) > 0.1:
                # Create the message for high price increase
                high_message = f"(Binance) {symbol} max price increased by {high_change:.2f}%"
                # Add the message to the message string
                if high_change > 0:
                    messages.append(high_message)
            # Check if the low price percent change is less than -0.1%
            if low_change < -0.1:
                low_message = f"(Binance) {symbol} min price decreased by {abs(low_change):.2f}%"
                # Add the message to the message string
                if low_change != 0:
                    messages.append(low_message)

            # Print the current high/low
            print(f"{symbol} current high price: {high_price}")
            print(f"{symbol} current low price: {low_price}")
            # Print the previous high and low price
            print(f"Previous high price: {previous_high_price}")
            print(f"Previous low price: {previous_low_price}")
            # Print the percent change
            print(f"High price percent change: {high_change:.2f}%")
            print(f"Low price percent change: {low_change:.2f}%\n")
            # Update the previous high and low prices
            previous_high_prices[symbol] = high_price
            previous_low_prices[symbol] = low_price

        # Join the messages together and send them through Telegram if there are any messages
        if messages:
            message = "\n".join(messages)
            requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}")

        # Wait for 60 seconds before fetching the prices again
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(10)


____________ETHER PRICE_________________

#!/usr/bin/env python3
import requests
import time
import json

# Constants
ETH_API_URL = "https://api.bitget.com/api/mix/v1/market/ticker?symbol=ETHUSDT_UMCBL"
TELEGRAM_API_URL = "https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={price}"
SLEEP_INTERVAL = 60
ERROR_SLEEP_INTERVAL = 10

# Replace YOUR_TOKEN_HERE with your Telegram bot token
bot_token = "5974203717:AAHBcl-9gTv0H3OHxQaBKjyH29SDQfog8yU"

# Replace GROUP_CHAT_IDS with a list of chat IDs of the groups you want to send the message to
group_chat_ids = ["-1001799310854"]
def get_eth_price():
    with requests.get(ETH_API_URL) as response:
        data = response.json()
        return data["data"]["last"]

def send_telegram_message(chat_id, price):
    with requests.get(TELEGRAM_API_URL.format(bot_token=bot_token, chat_id=chat_id, price=price)):
        print(f"Sent message: {price}")

while True:
    try:
        # Retrieve the current Bitcoin price
            price = get_eth_price()

        # Send the price to the group via Telegram
            for chat_id in group_chat_ids:
                send_telegram_message(chat_id, price)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(ERROR_SLEEP_INTERVAL)

    # Sleep for 1 minute
    time.sleep(SLEEP_INTERVAL)


_________BTC PRICE__________

#!/usr/bin/env python3
import requests
import time
import json

# Constants
BITCOIN_API_URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
TELEGRAM_API_URL = "https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={price}"
SLEEP_INTERVAL = 60
ERROR_SLEEP_INTERVAL = 10

# Replace YOUR_TOKEN_HERE with your Telegram bot token
bot_token = "5980258356:AAHI7CyRDwA2drnskIocFoGpDaNVUotnQ-0"

# Replace GROUP_CHAT_IDS with a list of chat IDs of the groups you want to send the message to
group_chat_ids = ["-1001883226432"]

def get_bitcoin_price():
    with requests.get(BITCOIN_API_URL) as response:
        data = response.json()
        return data["bpi"]["USD"]["rate"]

def send_telegram_message(chat_id, price):
    with requests.get(TELEGRAM_API_URL.format(bot_token=bot_token, chat_id=chat_id, price=price)):
        print(f"Sent message: {price}")

while True:
    try:
        # Retrieve the current Bitcoin price
        price = get_bitcoin_price()

        # Send the price to the group via Telegram
        for chat_id in group_chat_ids:
            send_telegram_message(chat_id, price)

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(ERROR_SLEEP_INTERVAL)

    # Sleep for 1 minute
    time.sleep(SLEEP_INTERVAL)
