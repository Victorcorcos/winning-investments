#!/usr/bin/env python3

# Para a análise, são utilizados princípios do Joseph D. Piotroski
# Estipulados no livro: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers"
# No estudo original de Piotroski, ao longo de 20 anos (1976–1996), uma estratégia de investimento baseado nessa pontuação, com a compra de empresas com F-Score alto e a venda de empresas com F-Score baixo, gerou um retorno anual de 23%, bem superior à media do mercado.
# Piotroski elaborou um Score chamado "Piotroski F-score" que varia de 0 a 9, quanto maior, por mais filtros as ações passaram

# Princípios utilizados:

# Piotroski:
# 1. ROA > 0 (ano corrente)
# 2. FCO > 0 (ano corrente)
# 3. FCO > Lucro Líquido (ano corrente)
# 4. ROA atual > ROA ano anterior
# 5. Alavancagem atual < ano passado (Dívida Líquida / Patrimônio Líquido)
# 6. Liquidez Corrente atual > Liquidez Corrente ano anterior
# 7. Nro. Ações atual = Nro. Ações ano anterior
# 8. Margem Bruta atual > Margem Bruta ano anterior
# 9. Giro Ativo atual > Giro Ativo ano anterior

# Greenblatt:
# * Fórmula Mágica adaptada (as duas ao mesmo tempo):
#   1) > ROIC e < EV/EBIT
#   2) > ROE e < P/L


# Referência: https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
# Backtesting on USA: https://www.quant-investing.com/blogs/backtests/2018/11/06/piotroski-f-score-back-test

import sys, os
sys.path.extend([f'../{name}' for name in os.listdir("..") if os.path.isdir(f'../{name}')])

import fundamentus
import stocks
import backtest
import browser

import pandas
import numpy

import http.cookiejar
import urllib.request
import json
import threading
import time
import pyperclip

# def print(thing):
#   import pprint
#   return pprint.PrettyPrinter(indent=4).pprint(thing)

def populate_shares(year):
  globals()['year'] = year
  globals()['infos'] = {}
  
  if year == current_year():
    shares = stocks.shares()
  else:
    shares = fundamentus.shares(year)
  
  shares = shares[shares['Cotação'] > 0]
  shares = shares[shares['Liquidez 2 meses'] > 10000]
  
  shares['Ranking (Piotroski)'] = 0
  shares['Ranking (Greenblatt)'] = 0
  shares['Ranking (Sum)'] = 0
  shares['Ranking (Final)'] = 0
  
  fill_infos(shares)
  remove_bad_shares(shares)
  
  shares = add_ratings(shares)
  
  shares = reorder_columns(shares)
  
  return shares

# infos = {
#   'TRPL4': {
#     'roa_positivo': True/False,
#     'fco_positivo': True/False,
#     'fco_saudavel': True/False,
#     'roa_crescente': True/False,
#     'alavancagem_decrescente': True/False,
#     'liquidez_crescente': True/False,
#     'no_acoes_constante': True/False,
#     'margem_bruta_crescente': True/False,
#     'giro_ativo_crescente': True/False
#   }
# }

def fill_infos(shares):
  cookie_jar = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
  opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                       ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
  tickers = list(shares.index)
  # import pry; pry()
  threads = [threading.Thread(target=fill_infos_by_ticker, args=(ticker,opener,)) for ticker in tickers]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()

def fill_infos_by_ticker(ticker, opener):
  infos[ticker] = {
    'roa_positivo': False,
    'fco_positivo': False,
    'fco_saudavel': False,
    'roa_crescente': False,
    'alavancagem_decrescente': False,
    'liquidez_crescente': False,
    'no_acoes_constante': False,
    'margem_bruta_crescente': False,
    'giro_ativo_crescente': False
  }
  
  current_year = year
  
  # Fetching Current Year Indicators
  current_indicators_url = f'https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsDashboard?ticker={ticker}'
  with opener.open(current_indicators_url) as link:
    company_indicators = link.read().decode('ISO-8859-1')
  company_indicators = json.loads(company_indicators)
  
  # Fetching Previous Years Indicators
  yearly_indicators_url = f'https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker={ticker}'
  with opener.open(yearly_indicators_url) as link:
    yearly_indicators = link.read().decode('ISO-8859-1')
  yearly_indicators = json.loads(yearly_indicators)
  
  company_indicators.extend(yearly_indicators)
  
  # Only consider company indicators before OR EQUAL to the current_year (robust solution for backtesting purposes)
  company_indicators = [ci for ci in company_indicators if ci['year'] <= current_year]
  
  if (len(company_indicators) > 0):
    infos[ticker]['roa_positivo'] = company_indicators[0]['roa'] > 0
    infos[ticker]['fco_positivo'] = company_indicators[0]['fco'] > 0
    infos[ticker]['fco_saudavel'] = company_indicators[0]['fco'] > company_indicators[0]['lucroLiquido']
  
  if (len(company_indicators) > 1):
    infos[ticker]['roa_crescente'] = company_indicators[0]['roa'] > company_indicators[1]['roa']
    infos[ticker]['alavancagem_decrescente'] = company_indicators[0]['dlpl'] < company_indicators[1]['dlpl']
    infos[ticker]['liquidez_crescente'] = company_indicators[0]['liqCorrent'] > company_indicators[1]['liqCorrent']
    infos[ticker]['no_acoes_constante'] = company_indicators[0]['qntAcoes'] == company_indicators[1]['qntAcoes']
    infos[ticker]['margem_bruta_crescente'] = company_indicators[0]['margBruta'] > company_indicators[1]['margBruta']
    infos[ticker]['giro_ativo_crescente'] = company_indicators[0]['giroAtivos'] > company_indicators[1]['giroAtivos']

def remove_bad_shares(shares):
  shares.drop(shares[shares['P/L'] <= 0].index, inplace=True)
  shares.drop(shares[shares['ROE'] <= 0].index, inplace=True)
  shares.drop(shares[shares['EV/EBIT'] <= 0].index, inplace=True)
  shares.drop(shares[shares['ROIC'] <= 0].index, inplace=True)

def add_ratings(shares):
  add_strategy_columns(shares)
  shares = calculate(shares)
  return fill_special_infos(shares)

# Inicializa os índices
def add_strategy_columns(shares):
  shares['Piotroski Score'] = 0
  shares['ROA positivo'] = False
  shares['FCO positivo'] = False
  shares['FCO > Lucro Líquido'] = False
  shares['ROA crescente'] = False
  shares['Alavancagem decrescente'] = False
  shares['Liquidez Corrente crescente'] = False
  shares['No Ações constante'] = False
  shares['Margem Bruta crescente'] = False
  shares['Giro Ativo crescente'] = False
  shares['ROE placement'] = 0
  shares['P/L placement'] = 0
  shares['ROIC placement'] = 0
  shares['EV/EBIT placement'] = 0

def calculate(shares):
  shares['Magic Formula'] = 0
  
  shares.sort_values(by='ROE', ascending=False, inplace=True)
  shares['ROE placement'] = range(0, len(shares))
  shares.sort_values(by='P/L', ascending=True, inplace=True)
  shares['P/L placement'] = range(0, len(shares))
  shares['Magic Formula'] += shares['ROE placement'] + shares['P/L placement']
  shares.sort_values(by='ROIC', ascending=False, inplace=True)
  shares['ROIC placement'] = range(0, len(shares))
  shares.sort_values(by='EV/EBIT', ascending=True, inplace=True)
  shares['EV/EBIT placement'] = range(0, len(shares))
  shares['Magic Formula'] += shares['ROIC placement'] + shares['EV/EBIT placement']
  
  return shares

def fill_special_infos(shares):
  for index in range(len(shares)):
    ticker = shares.index[index]
    shares['Piotroski Score'][index] += int(infos[ticker]['roa_positivo'])
    shares['ROA positivo'][index] = infos[ticker]['roa_positivo']
    shares['Piotroski Score'][index] += int(infos[ticker]['fco_positivo'])
    shares['FCO positivo'][index] = infos[ticker]['fco_positivo']
    shares['Piotroski Score'][index] += int(infos[ticker]['fco_saudavel'])
    shares['FCO > Lucro Líquido'][index] = infos[ticker]['fco_saudavel']
    shares['Piotroski Score'][index] += int(infos[ticker]['roa_crescente'])
    shares['ROA crescente'][index] = infos[ticker]['roa_crescente']
    shares['Piotroski Score'][index] += int(infos[ticker]['alavancagem_decrescente'])
    shares['Alavancagem decrescente'][index] = infos[ticker]['alavancagem_decrescente']
    shares['Piotroski Score'][index] += int(infos[ticker]['liquidez_crescente'])
    shares['Liquidez Corrente crescente'][index] = infos[ticker]['liquidez_crescente']
    shares['Piotroski Score'][index] += int(infos[ticker]['no_acoes_constante'])
    shares['No Ações constante'][index] = infos[ticker]['no_acoes_constante']
    shares['Piotroski Score'][index] += int(infos[ticker]['margem_bruta_crescente'])
    shares['Margem Bruta crescente'][index] = infos[ticker]['margem_bruta_crescente']
    shares['Piotroski Score'][index] += int(infos[ticker]['giro_ativo_crescente'])
    shares['Giro Ativo crescente'][index] = infos[ticker]['giro_ativo_crescente']
  return shares

def reorder_columns(shares):
  columns = ['Ranking (Final)', 'Ranking (Piotroski)', 'Ranking (Greenblatt)', 'Ranking (Sum)', 'Cotação', 'Piotroski Score', 'Magic Formula', 'P/L', 'ROE', 'EV/EBIT', 'ROIC']
  return shares[columns + [col for col in shares.columns if col not in tuple(columns)]]

# Get the current_year integer value, for example: 2020
def current_year():
  return int(time.strftime("%Y"))

# python3 piotroski_greenblatt_mixed.py "{ 'year': 2015 }"
if __name__ == '__main__':
  # Opening these URLs to automatically allow this API to receive more requests from local IP
  browser.open('https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsDashboard?ticker=BBAS3')
  browser.open('https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker=BBAS3')
  
  year = current_year()
  if len(sys.argv) > 1:
    year = int(eval(sys.argv[1])['year'])
  
  shares = populate_shares(year)
  
  shares.sort_values(by=['Piotroski Score', 'Cotação'], ascending=[False, True], inplace=True)
  shares['Ranking (Piotroski)'] = range(1, len(shares) + 1)

  shares.sort_values(by=['Magic Formula', 'Cotação'], ascending=[True, True], inplace=True)
  shares['Ranking (Greenblatt)'] = range(1, len(shares) + 1)

  shares['Ranking (Sum)'] = shares['Ranking (Piotroski)'] + shares['Ranking (Greenblatt)']
  shares.sort_values(by=['Ranking (Sum)'], ascending=[True], inplace=True)
  shares['Ranking (Final)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
