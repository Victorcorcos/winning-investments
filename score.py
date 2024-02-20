#!/usr/bin/env python3

# A idéia é calcular um ranking analisando os dados fundamentalistas de todas as empresas da bolsa B3
# Para a análise, são utilizados ensinamentos do livro "O Investidor Inteligente" de Benjamin Graham
# Também é calcula o Valor Intrínseco (Preço Justo) e Margem de Segurança, ambos também definidos por Benjamin Graham.
# Benjamin Graham foi o mentor dos melhores investidores do mundo, como o grandíssimo Warren Buffet,
# além do Irving Kahn e Walter Schloss.

# Aqui também é utilizado ensinamentos de Kenneth Fisher (PSR) e alguns outros grandes investidores fundamentalistas

# A coluna "Graham Score" é a mais importante. Quanto maior o valor dela, melhor!
# Ela representa a quantidade de filtros fundamentalistas que cada ação da bolsa de valores conseguiu ultrapassar.


# Princípios utilizados:

# - [x] 0. Todos os 14 Princípios de Graham (Ver graham.py)
# - [x] 1. ROIC (Return on Invested Capital) => Quanto maior, melhor (ideal, > 15%) https://www.youtube.com/watch?v=vXZkqDpFs0g https://www.sunoresearch.com.br/artigos/o-investidor-inteligente-entenda-a-obra-de-benjamin-graham/
# - [x] 2. PSR (Price Sales Ratio) => Quanto menor, melhor (ideal, < 0.75) https://www.moneyshow.com/articles/tptp072513-46306/
# - [x] 3. Margem Líquida => Quanto maior melhor (ideal, > 10%) https://www.youtube.com/watch?v=7tB_ym4Cabc E https://www.sunoresearch.com.br/artigos/5-indicadores-para-avaliar-solidez-de-uma-empresa/
# - [x] 4. Dívida Líquida/EBIT => Quanto menor melhor (ideal, <= 3) https://www.sunoresearch.com.br/artigos/5-indicadores-para-avaliar-solidez-de-uma-empresa/
# - [x] 5. Dívida Líquida/Patrimônio => Quanto menor, melhor (ideal < 50%) https://www.sunoresearch.com.br/artigos/5-indicadores-para-avaliar-solidez-de-uma-empresa/
# - [x] 6. EV/EBITDA (Enterprise Value / EBITDA) => Quanto menor melhor (ideal, < 10) https://www.investopedia.com/ask/answers/072715/what-considered-healthy-evebitda.asp
# - [x] 7. Peg Ratio (P/L / CAGRLucros5Anos) => Quanto menor melhor (ideal <= 1) https://bugg.com.br/2018/01/24/buggpedia-o-que-e-o-peg-ratio/

########### Precisa Capturar ###########
#### Outros ####
# * ROA > 0.05. (https://www.disruptiveadvertising.com/marketing/roas-return-on-ad-spend/)
# * P/L ideal aproximadamente 5 # ?
# * PSR ideal aproximadamente 1 # ?
# * Nova Formula Graham (https://www.oldschoolvalue.com/stock-valuation/benjamin-graham-formula/)
# * Filtros Graham (https://www.scielo.br/scielo.php?script=sci_arttext&pid=S1519-70772010000100003)

################### Novo Warren Buffet (Qualitativo) ###################
# * ROE, ROIC, ROA altos
# * Margem Líquida alta em relação a concorrentes
#    => https://api-analitica.sunoresearch.com.br/api/Company/GetRelatedCompanies?ticker=SQIA3&quantity=20
# * Grande resultado histórico de Lucros Crescentes
#    => https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker=TGMA3
### Buffet: “Nós fomos mudando para este enfoque ao longo dos anos. Não é muito difícil ficar observando negócios por 50 anos e aprender aonde se faz dinheiro de verdade.”

# MacOS related Error...
# socket.gaierror: [Errno 8] nodename nor servname provided, or not known
# 
# How to fix...
# System Preference > Sharing > Enable all sharings!

# More Strategies right below
# Altman Z Score
# Ohlson's O Score
# Montier C Score
# Declining Wedge
# Ascending Triangle
# Quality Minus Junk
# Book Value
# Stock Idiosyncratic Risk
# Leverage Ratio
# Weighted Average Cost of Capital
# Interest Coverage Ratio

import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

import graham
import backtest

import pandas
import pyperclip
import numpy

from math import sqrt
from decimal import Decimal

def improve_ratings(shares, year):
  shares['CAGR Lucros 5 Anos'] = pandas.to_numeric(shares['CAGR Lucros 5 Anos'], errors='coerce')
  shares['CAGR Lucros 5 Anos'] = shares['CAGR Lucros 5 Anos'].fillna(0)
  
  shares['P/L'] = pandas.to_numeric(shares['P/L'], errors='coerce')
  shares['P/L'] = shares['P/L'].fillna(0)
  
  improve_score(shares, year)
  improve_score_explanation(shares, year)

def improve_score(shares, year):
  shares['Graham Score'] += (shares['ROIC'] > 0.15).astype(int)
  shares['Graham Score'] += (shares['PSR'] < 0.75).astype(int)
  shares['Graham Score'] += (shares['Margem Líquida'] > 0.1).astype(int)
  if year == None or year >= 2020:
    shares['Graham Score'] += ((shares['Dívida Líquida/EBIT']).astype(float) <= 3.0).astype(int)
    shares['Graham Score'] += ((shares['Dívida Líquida/Patrimônio']).astype(float) < 0.5).astype(int)
    shares['Graham Score'] += ((shares['EV/EBITDA'] < 10.0) & (shares['EV/EBITDA'] > 0)).astype(int)
    shares['Graham Score'] += ((shares['P/L'] > 0) & (shares['CAGR Lucros 5 Anos'].astype(float) > 0) & ((shares['P/L'] / shares['CAGR Lucros 5 Anos'].astype(float) < 1.0))).astype(int)

# Mostra quais filtros a ação passou para pontuar seu Graham Score
def improve_score_explanation(shares, year):
  shares['ROIC > 15%'] = shares['ROIC'] > 0.15
  shares['PSR < 0.75'] = shares['PSR'] < 0.75
  shares['Margem Líquida > 10%'] = shares['Margem Líquida'] > 0.1
  if year == None or year >= 2020:
    shares['Dívida Líquida/EBIT <= 3.0'] = (shares['Dívida Líquida/EBIT']).astype(float) <= 3.0
    shares['Dívida Líquida/Patrimônio < 0.5'] = (shares['Dívida Líquida/Patrimônio']).astype(float) < 0.5
    shares['EV/EBITDA < 10'] = (shares['EV/EBITDA'] < 10.0) & (shares['EV/EBITDA'] > 0)
    shares['PEG Ratio <= 1'] = (shares['P/L'] > 0) & (shares['CAGR Lucros 5 Anos'].astype(float) > 0) & ((shares['P/L'] / shares['CAGR Lucros 5 Anos'].astype(float) < 1.0))
    shares['PEG Ratio'] = shares['P/L'] / shares['CAGR Lucros 5 Anos']

# Reordena a tabela para mostrar a Cotação, o Valor Intríseco e o Graham Score como primeiras colunass
def reorder_columns(shares):
  columns = ['Ranking', 'Cotação', 'Preço Justo', 'Graham Score', 'Setor', 'Subsetor', 'Segmento', 'PEG Ratio']
  return shares[columns + [col for col in shares.columns if col not in tuple(columns)]]

# python3 score.py "{ 'year': 2013 }"
if __name__ == '__main__':
  from waitingbar import WaitingBar
  progress_bar = WaitingBar('[*] Calculating...')
  
  shares = graham.populate_shares(sys)
  year = graham.year
  
  improve_ratings(shares, year)
  
  shares.sort_values(by=['Graham Score', 'Cotação'], ascending=[False, True], inplace=True)
  
  shares['Ranking'] = range(1, len(shares) + 1)
  
  shares = reorder_columns(shares)
  
  backtest.display_shares(shares, year)
  
  progress_bar.stop()
