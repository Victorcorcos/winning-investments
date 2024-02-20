#!/usr/bin/env python3

# Este algoritmo aplica a formula de Joel Greenblatt em todas as ações do Brasil
# Livro: https://www.amazon.com/Little-Book-That-Beats-Market/dp/0471733067
# Breve Explicação: https://comoinvestir.thecap.com.br/joel-greenblatt-estrategia-investimentos/

# Em sua fórmula mágica ele se utiliza dos seguintes indicadores: ROE e a relação P/L.
# Através desses 2 indicadores ele monta um ranking (Greenblatt) com as empresas de maior ROE (mais rentáveis) e de menor P/L (mais baratas).
# Fazendo os 2 rankings, ele soma a posição de cada uma delas nos rankings.
# As empresas de menor soma são aquelas escolhidas para montar a carteira pois seriam as mais baratas e mais rentáveis.

# Outra variação da Fórmula de Greenblatt é
# usando o Enterprise Value (EV) dividido pelo EBIT, em conjunto com o ROIC como um indicador de rentabilidade da empresa.
# A ideia segue sendo a mesma, ou seja, comprar boas empresas a preços baratos.

# Formula Mágica 1: Melhores Empresas: > ROE  e < P/L
# Formula Mágica 2: Melhores Empresas: > ROIC e < EV/EBIT (EV/EBITDA não tem no fundamentus)

# Cases de sucesso dessas fórmula...
# https://investidoringles.com/2019/01/formula-magica-de-joel-greenblatt.html
# http://bibliotecadigital.fgv.br/dspace/bitstream/handle/10438/15280/Tese%20-%20Leonardo%20Milane%20-%20Magic%20Formula.pdf?sequence=1

# Princípios utilizados:

# - [x] Fórmula Mágica 1): > ROIC e < EV/EBIT e > ROE e < P/L
# - [x] Fórmula Mágica 2): > ROIC e < EV/EBIT
# - [x] Fórmula Mágica 3): > ROE e < P/L

import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

import fundamentus
import stocks
import backtest

import pandas
import numpy
import time
import pyperclip

from math import sqrt
from decimal import Decimal

def populate_shares(year, formula):
  globals()['year'] = year
  globals()['infos'] = {}
  
  if year == current_year():
    shares = stocks.shares()
  else:
    shares = fundamentus.shares(year)
  
  shares = shares[shares['Cotação'] > 0]
  shares = shares[shares['Liquidez 2 meses'] > 10000]

  return setup(shares, formula, year)

def setup(shares, formula, year):
  explain(formula)
  init(shares, formula)
  remove_bad_shares(shares, formula)
  calculate(shares, formula)
  return reorder_columns(shares, formula)

def explain(formula):
  print("\n\nCalculating the Joel Greenblatt formula using...")
  if formula in ('ROE', None):
    print("ROE and P/L")
  if formula in ('ROIC', None):
    print("ROIC and EV/EBIT")
  print('')

def init(shares, formula):
  shares['Ranking (Greenblatt)'] = 0
  if formula in ('ROE', None):
    shares['ROE placement'] = 0
    shares['P/L placement'] = 0
  if formula in ('ROIC', None):
    shares['ROIC placement'] = 0
    shares['EV/EBIT placement'] = 0

def remove_bad_shares(shares, formula):
  if formula in ('ROE', None):
    shares.drop(shares[shares['P/L'] <= 0].index, inplace=True)
    shares.drop(shares[shares['ROE'] <= 0].index, inplace=True)
  if formula in ('ROIC', None):
    shares.drop(shares[shares['EV/EBIT'] <= 0].index, inplace=True)
    shares.drop(shares[shares['ROIC'] <= 0].index, inplace=True)

def calculate(shares, formula):
  shares['Magic Formula'] = 0
  
  if formula in ('ROE', None):
    shares.sort_values(by='ROE', ascending=False, inplace=True)
    shares['ROE placement'] = range(0, len(shares))
    shares.sort_values(by='P/L', ascending=True, inplace=True)
    shares['P/L placement'] = range(0, len(shares))
    shares['Magic Formula'] += shares['ROE placement'] + shares['P/L placement']
  if formula in ('ROIC', None):
    shares.sort_values(by='ROIC', ascending=False, inplace=True)
    shares['ROIC placement'] = range(0, len(shares))
    shares.sort_values(by='EV/EBIT', ascending=True, inplace=True)
    shares['EV/EBIT placement'] = range(0, len(shares))
    shares['Magic Formula'] += shares['ROIC placement'] + shares['EV/EBIT placement']
  
  return shares

def reorder_columns(shares, formula):
  columns = ['Ranking (Greenblatt)', 'Cotação', 'Magic Formula', 'Setor', 'Subsetor', 'Segmento']
  
  if formula in ('ROE', None):
    columns.extend(['P/L', 'ROE'])
  if formula in ('ROIC', None):
    columns.extend(['EV/EBIT', 'ROIC'])
  
  return shares[columns + [col for col in shares.columns if col not in tuple(columns)]]

# Get the current_year integer value, for example: 2020
def current_year():
  return int(time.strftime("%Y"))

# Chame a função main de acordo com qual formula você quer aplicar: roe OU roic
# Formula ROE:  Utiliza ROE  e P/L
# Formula ROIC: Utiliza ROIC e EV/EBIT (EV/EBITDA não tem no fundamentus)
# ================ Exemplos ================
# python3 greenblatt.py "{ 'formula': 'ROE', 'year': 2013 }"
# python3 greenblatt.py "{ 'formula': 'ROIC', 'year': 2020 }"
# python3 greenblatt.py "{ 'year': 2019 }"
if __name__ == '__main__':
  year = current_year()
  formula = None
  if len(sys.argv) > 1:
    arguments = eval(sys.argv[1])
    year = int(arguments.get('year', current_year()))
    formula = arguments.get('formula', None)
  
  shares = populate_shares(year, formula)
  
  shares.sort_values(by=['Magic Formula', 'Cotação'], ascending=[True, True], inplace=True)
  shares['Ranking (Greenblatt)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
