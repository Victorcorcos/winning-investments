#!/usr/bin/env python3

# Princípios utilizados:

# - [x] 1.  Sobrevivência: Sobreviveu nos últimos 10 anos. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
# - [x] 2.  Estabilidade ds Lucros: Lucro > 0 nos últimos 10 anos. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
# - [x] 3.  Crescimento dos Lucros: Lucros crescentes nos últimos 10 anos https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
# - [x] 4.  Crescimento dos Lucro Por Ação: LPA atual > 1.33 * LPA 10 anos atrás. (Calculado através da média dos 3 anos do começo e dos 3 anos do fim deste período) http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
# - [x] 5.  Estabilidade dos Dividendos: Dividendos pagos nos últimos 10 anos. http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
# - [x] 6.  raíz_quadrada_de(22.5 * VPA * LPA) => Quanto maior, melhor. Ideal > 1.5 * Preço. https://www.sunoresearch.com.br/artigos/valor-intrinseco/?utm_source=PR&utm_medium=artigo&utm_campaign=investing_05122019
# - [x] 7.  P/L (Preço/Lucro) => Quanto menor, melhor (ideal, < 15 E >= 0) http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
# - [x] 8.  P/VP (Preço/Valor Patrimonial) => Quanto menor, melhor (ideal, < 1.5 E >= 0) http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
# - [x] 9.  Crescimento em 5 anos => Quanto maior, melhor (ideal, > 5%) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
# - [x] 10. ROE (Return On Equity) => Quanto maior, melhor (ideal, superior a 20%) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
# - [x] 11. Dividend Yield (Rendimento de Dividendo) => Quanto maior, melhor (ideal, > Taxa Selic (4.5%)) https://foconomilhao.com/acoes-com-dividend-yield-maior-que-a-selic/
# - [x] 12. Liquidez Corrente => Quanto maior, melhor (ideal > 1.5) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
# - [x] 13. Dívida Bruta/Patrimônio => Quanto menor, melhor (ideal < 50%) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
# - [x] 14. Patrimônio Líquido => Quanto maior, melhor (ideal > 2000000000)

#### Graham ####
# ===== Próximos =====
# * Valor de Mercado maior que 2.000.000 . # Benjamin Graham # https://edisciplinas.usp.br/pluginfile.php/3821144/mod_resource/content/4/245.pdf
#   => https://www.fundamentus.com.br/detalhes.php?papel=PETR4
# * Valor médio de negociações superior a R$ 1 milhão. # Benjamin Graham # https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
#   ~> Vol $ méd (2m) > 1.000.000
#   => https://www.fundamentus.com.br/detalhes.php?papel=PETR4
# * Endividamento de longo prazo < Capital de Giro # Benjamin Graham # https://www.sunoresearch.com.br/artigos/o-investidor-inteligente-entenda-a-obra-de-benjamin-graham/
# * Possui bom nível de governança corporativa # Benjamin Graham # https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/

# Lucros para fazer o Gráfico ;)
# https://api-analitica.sunoresearch.com.br/api/Statement/GetStatementResultsReportByTicker?type=y&ticker=WEGE3&period=10

import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

import fundamentus
import stocks
import backtest
import browser

import pandas
import numpy
import re

from math import sqrt
from decimal import Decimal

import http.cookiejar
import urllib.request
import json
import threading
import time
import pyperclip

# Populate shares panda dataframe with the provided year
def populate_shares(year):
  globals()['year'] = year
  globals()['infos'] = {}
  
  if year == current_year():
    shares = stocks.shares()
  else:
    shares = fundamentus.shares(year)
  
  shares = shares[shares['Cotação'] > 0]
  shares = shares[shares['Liquidez 2 meses'] > 0]
  shares['Ranking (Graham)'] = 0
  
  fill_infos(shares)
  
  shares = add_ratings(shares)
  
  shares = reorder_columns(shares)
  
  return shares

# infos = {
#   'TRPL4': {
#     "survivability": True/False, # Empresa com no mínimo 10 anos de sobrevivência (Graham olhava lucros e dividendos dos últimos 10 anos) # Benjamin Graham. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
#     "earnings_stability": True/False, # Estabilidade de lucros: Lucro > 0 nos últimos 10 anos # Benjamin Graham. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
#     "earnings_growth": True/False, # Crescimento dos lucros: Lucros crescentes nos últimos 10 anos # Benjamin Graham. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
#     "lpa_growth": True/False, # LPA atual > 1.33 * LPA 10 anos atrás. # Benjamin Graham. (calculado através da média dos 3 anos do começo e dos 3 anos do fim deste período) # http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
#     "dividends_stability": True/False, # Dividendos pagos nos últimos 10 anos. # Benjamin Graham # http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/   
#   }
# }

def fill_infos(shares):
  cookie_jar = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
  opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                       ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
  tickers = list(shares.index)
  threads = [threading.Thread(target=fill_infos_by_ticker, args=(ticker,opener,)) for ticker in tickers]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()

def fill_infos_by_ticker(ticker, opener):
  infos[ticker] = {
    'survivability': False,
    'earnings_stability': False,
    'earnings_growth': False,
    'lpa_growth': False,
    'dividends_stability': False
  }

  # Suno disabled it's API access
  return None
  
  # Fetching Lucro Liquido
  url = f'https://api-analitica.sunoresearch.com.br/api/Statement/GetStatementResultsReportByTicker?type=y&ticker={ticker}&period=999'
  with opener.open(url) as link:
    company_results = link.read().decode('ISO-8859-1')
  company_results = json.loads(company_results)
  
  current_year = year
  
  lucros = [r for r in company_results if r['description'] == 'Lucro LÃ\xadquido'][0]
  years = [x for x in lucros.keys() if re.match('C_\w{4}$', x)]
  if (len(years) == 0):
    return
  years = [x for x in years if int(re.findall('C_(\w{4})$', x)[0]) < current_year]
  list.sort(years)
  lucros = { year: lucros[year] for year in years }
  ultimos_lucros = list(lucros.values())[-10:]
  
  # Ugly Fix for missing data :( Looks like the API have missing data -_-
  # Fill None values with the Mean earning
  present_lucros = [i for i in ultimos_lucros if i]
  if (len(present_lucros) == 0):
    mean = 0
  else:
    mean = sum(present_lucros) / len(present_lucros)
  ultimos_lucros = [mean if v is None else v for v in ultimos_lucros]
  # End of Ugly Fix
  
  infos[ticker]['survivability'] = f'C_{current_year - 10}' in lucros.keys()
  infos[ticker]['earnings_stability'] = all(ultimos_lucros[i] > 0 for i in range(len(ultimos_lucros)))
  infos[ticker]['earnings_growth'] = all(ultimos_lucros[i] <= ultimos_lucros[i+1] for i in range(len(ultimos_lucros)-1)) # Isso aqui deve virar uma função e devemos ver a tendência dessa função!
  
  # Fetching LPA's and DPA's
  url = f'https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker={ticker}'
  with opener.open(url) as link:
    company_indicators = link.read().decode('ISO-8859-1')
  company_indicators = json.loads(company_indicators)
  
  # Only consider company indicators before the current_year (robust solution for backtesting purposes)
  company_indicators = [ci for ci in company_indicators if ci['year'] < current_year]
  
  last_dpas = [fundament['dpa'] for fundament in company_indicators]
  last_lpas = [fundament['lpa'] for fundament in company_indicators]
  
  if (len(last_lpas[:10]) > 0):
    infos[ticker]['lpa_growth'] = (sum(last_lpas[:3]) / 3) >= (sum(last_lpas[-3:]) / 3)
  
  if (len(last_dpas[:10]) > 0):
    infos[ticker]['dividends_stability'] = all(last_dpas[:10][i] > 0 for i in range(len(last_dpas[:10])))

def add_ratings(shares):
  add_graham_columns(shares)
  fill_fair_price(shares)
  fill_score(shares)
  fill_score_explanation(shares)
  return fill_special_infos(shares)

# Inicializa os índices
def add_graham_columns(shares):
  shares['Preço Justo (Graham)'] = 0
  shares['Graham Score'] = 0
  shares['Preço Justo (Graham) / Cotação'] = 0
  shares['10 Anos de Sobrevivencia'] = False
  shares['Lucros Positivos nos Ultimos 10 Anos'] = False
  shares['Lucros Crescentes nos Ultimos 10 Anos'] = False
  shares['LPA atual > 1.33 * LPA 10 anos atrás'] = False
  shares['Dividendos Positivos nos Ultimos 10 Anos'] = False

# Benjamin Graham elaborou a seguinte fórmula para calcular o Valor Intríseco (Preço Justo (Graham)):
# => sqrt(22.5 * VPA * LPA)
def fill_fair_price(shares):
  shares['Cotação'] = pandas.to_numeric(shares['Cotação'], errors='coerce')
  shares['P/L'] = pandas.to_numeric(shares['P/L'], errors='coerce')
  shares['P/VP'] = pandas.to_numeric(shares['P/VP'], errors='coerce')
  for index in range(len(shares)):
    if ((shares['P/L'][index] > 0) & (shares['P/VP'][index] > 0)):
      shares['Preço Justo (Graham)'][index] = sqrt(22.5 * (shares['Cotação'][index] / shares['P/L'][index]) * (shares['Cotação'][index] / shares['P/VP'][index]))
    else:
      shares['Preço Justo (Graham)'][index] = 0
  shares['Preço Justo (Graham)'] = pandas.to_numeric(shares['Preço Justo (Graham)'], errors='coerce')
  # Ideal > 1. Quanto maior, melhor! Significa que a ação deveria estar valendo 1 vezes mais, 2 vezes mais, 3 vezes mais, etc.
  shares['Preço Justo (Graham) / Cotação'] = shares['Preço Justo (Graham)'] / shares['Cotação']

def fill_score(shares):
  shares['Graham Score'] += (shares['Preço Justo (Graham) / Cotação'] > Decimal(1.5)).astype(int)
  shares['Graham Score'] += ((shares['P/L'] < 15) & (shares['P/L'] >= 0)).astype(int)
  shares['Graham Score'] += ((shares['P/VP'] < 1.5) & (shares['P/VP'] >= 0)).astype(int)
  shares['Graham Score'] += (shares['Crescimento em 5 anos'] > 0.05).astype(int)
  shares['Graham Score'] += (shares['ROE'] > 0.2).astype(int)
  shares['Graham Score'] += (shares['Dividend Yield'] > 0.045).astype(int)
  shares['Graham Score'] += (shares['Liquidez Corrente'] > 1.5).astype(int)
  shares['Graham Score'] += (shares['Dívida Bruta/Patrimônio'] < 0.5).astype(int)
  shares['Graham Score'] += (shares['Patrimônio Líquido'] > 2000000000).astype(int)

# Mostra quais filtros a ação passou para pontuar seu Score
def fill_score_explanation(shares):
  shares['Margem de Segurança: Preço Justo (Graham) > 1.5 * Cotação'] = shares['Preço Justo (Graham) / Cotação'] > Decimal(1.5)
  shares['P/L < 15 (E não negativo)'] = (shares['P/L'] < 15) & (shares['P/L'] >= 0)
  shares['P/VP < 1.5 (E não negativo)'] = (shares['P/VP'] < 1.5) & (shares['P/VP'] >= 0)
  shares['Crescimento em 5 anos > 0.05'] = shares['Crescimento em 5 anos'] > 0.05
  shares['ROE > 20%'] = shares['ROE'] > 0.2
  shares['Dividend Yield > 0.045 (Taxa Selic)'] = shares['Dividend Yield'] > 0.045
  shares['Liquidez Corrente > 1.5'] = shares['Liquidez Corrente'] > 1.5
  shares['Dívida Bruta/Patrimônio < 0.5'] = shares['Dívida Bruta/Patrimônio'] < 0.5
  shares['Patrimônio Líquido > 2 Bilhões'] = shares['Patrimônio Líquido'] > 2000000000

def fill_special_infos(shares):
  for index in range(len(shares)):
    ticker = shares.index[index]
    shares['Graham Score'][index] += int(infos[ticker]['survivability'])
    shares['10 Anos de Sobrevivencia'][index] = infos[ticker]['survivability']
    shares['Graham Score'][index] += int(infos[ticker]['earnings_stability'])
    shares['Lucros Positivos nos Ultimos 10 Anos'][index] = infos[ticker]['earnings_stability']
    shares['Graham Score'][index] += int(infos[ticker]['earnings_growth'])
    shares['Lucros Crescentes nos Ultimos 10 Anos'][index] = infos[ticker]['earnings_growth']
    shares['Graham Score'][index] += int(infos[ticker]['lpa_growth'])
    shares['LPA atual > 1.33 * LPA 10 anos atrás'][index] = infos[ticker]['lpa_growth']
    shares['Graham Score'][index] += int(infos[ticker]['dividends_stability'])
    shares['Dividendos Positivos nos Ultimos 10 Anos'][index] = infos[ticker]['dividends_stability']
  return shares

# Reordena a tabela para mostrar a Cotação, o Valor Intríseco e o Graham Score como primeiras colunass
def reorder_columns(shares):
  columns = ['Ranking (Graham)', 'Cotação', 'Preço Justo (Graham)', 'Graham Score', 'Preço Justo (Graham) / Cotação', 'Setor', 'Subsetor', 'Segmento']
  return shares[columns + [col for col in shares.columns if col not in tuple(columns)]]

# Get the current_year integer value, for example: 2020
def current_year():
  return int(time.strftime("%Y"))

# python3 graham.py "{ 'year': 2015 }"
if __name__ == '__main__':  
  year = current_year()
  if len(sys.argv) > 1:
    year = int(eval(sys.argv[1])['year'])
  
  shares = populate_shares(year)
  
  shares.sort_values(by=['Graham Score', 'Preço Justo (Graham) / Cotação'], ascending=[False, False], inplace=True)
  
  shares['Ranking (Graham)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
