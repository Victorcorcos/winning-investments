#!/usr/bin/env python3

# Para a análise, são utilizados princípios do Joseph D. Piotroski
# Estipulados no livro: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers"
# No estudo original de Piotroski, ao longo de 20 anos (1976–1996), uma estratégia de investimento baseado nessa pontuação, com a compra de empresas com F-Score alto e a venda de empresas com F-Score baixo, gerou um retorno anual de 23%, bem superior à media do mercado.
# Piotroski elaborou um Score chamado "Piotroski F-score" que varia de 0 a 9, quanto maior, por mais filtros as ações passaram

# Esse é o método avançado, onde além de ser comparado dados do ano passado e do ano atual
# Também é comparado dados do ano retrasado com do ano passado

# Princípios utilizados:

# Ano Passado e Atual
# 1. ROA > 0 (ano corrente)
# 2. FCO > 0 (ano corrente)
# 3. FCO > Lucro Líquido (ano corrente)
# 4. ROA atual > ROA ano anterior
# 5. Alavancagem atual < ano passado (Dívida Líquida / Patrimônio Líquido)
# 6. Liquidez Corrente atual > Liquidez Corrente ano anterior
# 7. Nro. Ações atual = Nro. Ações ano anterior
# 8. Margem Bruta atual > Margem Bruta ano anterior
# 9. Giro Ativo atual > Giro Ativo ano anterior

# Ano Retrasado e Passado
# 10. ROA > 0 (ano passado)
# 11. FCO > 0 (ano passado)
# 12. FCO > Lucro Líquido (ano passado)
# 13. ROA passado > ROA 2 anos atrás
# 14. Alavancagem ano passado < 2 anos atrás (Dívida Líquida / Patrimônio Líquido)
# 15. Liquidez Corrente ano passado > Liquidez Corrente 2 anos atrás
# 16. Nro. Ações ano passado = Nro. Ações 2 anos atrás
# 17. Margem Bruta ano passado > Margem Bruta 2 anos atrás
# 18. Giro Ativo ano passado > Giro Ativo 2 anos atrás

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
  
  if year == None:
    shares = stocks.shares()
  else:
    shares = fundamentus.shares(year)
  
  shares = shares[shares['Cotação'] > 0]
  shares = shares[shares['Liquidez 2 meses'] > 0]
  shares['Ranking (Piotrotski)'] = 0
  
  fill_infos(shares)
  
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
    'giro_ativo_crescente': False,
    'roa_positivo_antigo': False,
    'fco_positivo_antigo': False,
    'fco_saudavel_antigo': False,
    'roa_crescente_antigo': False,
    'alavancagem_decrescente_antigo': False,
    'liquidez_crescente_antigo': False,
    'no_acoes_constante_antigo': False,
    'margem_bruta_crescente_antigo': False,
    'giro_ativo_crescente_antigo': False
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

    infos[ticker]['roa_positivo_antigo'] = company_indicators[1]['roa'] > 0
    infos[ticker]['fco_positivo_antigo'] = company_indicators[1]['fco'] > 0
    infos[ticker]['fco_saudavel_antigo'] = company_indicators[1]['fco'] > company_indicators[1]['lucroLiquido']
  
  if (len(company_indicators) > 1):
    infos[ticker]['roa_crescente'] = company_indicators[0]['roa'] > company_indicators[1]['roa']
    infos[ticker]['alavancagem_decrescente'] = company_indicators[0]['dlpl'] < company_indicators[1]['dlpl']
    infos[ticker]['liquidez_crescente'] = company_indicators[0]['liqCorrent'] > company_indicators[1]['liqCorrent']
    infos[ticker]['no_acoes_constante'] = company_indicators[0]['qntAcoes'] == company_indicators[1]['qntAcoes']
    infos[ticker]['margem_bruta_crescente'] = company_indicators[0]['margBruta'] > company_indicators[1]['margBruta']
    infos[ticker]['giro_ativo_crescente'] = company_indicators[0]['giroAtivos'] > company_indicators[1]['giroAtivos']
    
    infos[ticker]['roa_crescente_antigo'] = company_indicators[1]['roa'] > company_indicators[2]['roa']
    infos[ticker]['alavancagem_decrescente_antigo'] = company_indicators[1]['dlpl'] < company_indicators[2]['dlpl']
    infos[ticker]['liquidez_crescente_antigo'] = company_indicators[1]['liqCorrent'] > company_indicators[2]['liqCorrent']
    infos[ticker]['no_acoes_constante_antigo'] = company_indicators[1]['qntAcoes'] == company_indicators[2]['qntAcoes']
    infos[ticker]['margem_bruta_crescente_antigo'] = company_indicators[1]['margBruta'] > company_indicators[2]['margBruta']
    infos[ticker]['giro_ativo_crescente_antigo'] = company_indicators[1]['giroAtivos'] > company_indicators[2]['giroAtivos']

def add_ratings(shares):
  add_piotroski_columns(shares)
  return fill_special_infos(shares)

# Inicializa os índices
def add_piotroski_columns(shares):
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

  shares['ROA positivo antigo'] = False
  shares['FCO positivo antigo'] = False
  shares['FCO > Lucro Líquido antigo'] = False
  shares['ROA crescente antigo'] = False
  shares['Alavancagem decrescente antigo'] = False
  shares['Liquidez Corrente crescente antigo'] = False
  shares['No Ações constante antigo'] = False
  shares['Margem Bruta crescente antigo'] = False
  shares['Giro Ativo crescente antigo'] = False

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
    
    shares['Piotroski Score'][index] += int(infos[ticker]['roa_positivo_antigo'])
    shares['ROA positivo antigo'][index] = infos[ticker]['roa_positivo_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['fco_positivo_antigo'])
    shares['FCO positivo antigo'][index] = infos[ticker]['fco_positivo_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['fco_saudavel_antigo'])
    shares['FCO > Lucro Líquido antigo'][index] = infos[ticker]['fco_saudavel_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['roa_crescente_antigo'])
    shares['ROA crescente antigo'][index] = infos[ticker]['roa_crescente_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['alavancagem_decrescente_antigo'])
    shares['Alavancagem decrescente antigo'][index] = infos[ticker]['alavancagem_decrescente_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['liquidez_crescente_antigo'])
    shares['Liquidez Corrente crescente antigo'][index] = infos[ticker]['liquidez_crescente_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['no_acoes_constante_antigo'])
    shares['No Ações constante antigo'][index] = infos[ticker]['no_acoes_constante_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['margem_bruta_crescente_antigo'])
    shares['Margem Bruta crescente antigo'][index] = infos[ticker]['margem_bruta_crescente_antigo']
    shares['Piotroski Score'][index] += int(infos[ticker]['giro_ativo_crescente_antigo'])
    shares['Giro Ativo crescente antigo'][index] = infos[ticker]['giro_ativo_crescente_antigo']
  return shares

# Reordena a tabela para mostrar a Cotação, o Valor Intríseco e o Graham Score como primeiras colunas
def reorder_columns(shares):
  columns = ['Ranking (Piotrotski)', 'Cotação', 'Piotroski Score']
  return shares[columns + [col for col in shares.columns if col not in tuple(columns)]]

# Get the current_year integer value, for example: 2020
def current_year():
  return int(time.strftime("%Y"))

# python3 piotroski_advanced.py "{ 'year': 2015 }"
if __name__ == '__main__':
  # Opening these URLs to automatically allow this API to receive more requests from local IP
  browser.open('https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsDashboard?ticker=BBAS3')
  browser.open('https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker=BBAS3')
  
  year = current_year()
  if len(sys.argv) > 1:
    year = int(eval(sys.argv[1])['year'])
  
  shares = populate_shares(year)
  
  shares.sort_values(by=['Piotroski Score', 'Cotação'], ascending=[False, True], inplace=True)
  
  shares['Ranking (Piotrotski)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
