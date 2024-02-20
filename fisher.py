#!/usr/bin/env python3

# Para a análise, são utilizados princípios do Kenneth Fisher
# Ele filho de Philip Fisher, têm uma fortuna atual de 4 bilhões de dólares e é dono de um fundo de investimento (Fisher Investments)
# Com base nas suas ações públicas, estimate-se que o desempenho de Ken Fisher tenha superado o mercado de ações dos EUA em uma média de 4,2 potos percentuais por ano.
# https://comoinvestir.thecap.com.br/quem-e-kenneth-fisher-o-jeito-ken-investir/
# http://investidoremvalor.com/filosofia-ken-fisher/

# Princípios utilizados:

# - [x] 1. PSR < 3 => Aumenta 1 ponto
# - [x] 2. PSR < 1 => Aumenta 1 ponto
# - [x] 3. PSR < 0.75 => Aumenta 1 ponto
# - [x] 4. Taxa de Rentabilidade alta: L/P > Selic

import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

import time
import pyperclip

import fundamentus
import stocks
import backtest

from decimal import Decimal

def populate_shares(year):
  globals()['year'] = year
  globals()['infos'] = {}
  
  if year == None:
    shares = stocks.shares()
  else:
    shares = fundamentus.shares(year)
  
  shares = shares[shares['Cotação'] > 0]
  shares = shares[shares['Liquidez 2 meses'] > 0]
  shares['Ranking'] = 0
  
  shares = add_ratings(shares)
  
  shares = reorder_columns(shares)
  
  return shares

def add_ratings(shares):
  add_fisher_columns(shares)
  fill_score(shares)
  fill_score_explanation(shares)
  return shares

def add_fisher_columns(shares):
  shares['Fisher Score'] = 0

def fill_score(shares):
  shares['Fisher Score'] += (shares['PSR'] < 1.0).astype(int)
  shares['Fisher Score'] += (shares['PSR'] < 0.75).astype(int)
  shares['Fisher Score'] += (shares['PSR'] < 3).astype(int)
  shares['Fisher Score'] += ((shares['P/L'] ** -1) > 0.3).astype(int)

# Mostra quais filtros a ação passou para pontuar seu Score
def fill_score_explanation(shares):
  shares['PSR < 3'] = shares['PSR'] < 3
  shares['PSR < 1.0'] = shares['PSR'] < 1.0
  shares['PSR < 0.75'] = shares['PSR'] < 0.75
  shares['L/P > Taxa Selic'] = (shares['P/L'] ** -1) > 0.3

# Reordena a tabela para mostrar a Cotação, o Valor Intríseco e o Graham Score como primeiras colunass
def reorder_columns(shares):
  columns = ['Ranking', 'Cotação', 'Fisher Score', 'Setor', 'Subsetor', 'Segmento']
  return shares[columns + [col for col in shares.columns if col not in tuple(columns)]]

# Get the current_year integer value, for example: 2020
def current_year():
  return int(time.strftime("%Y"))

if __name__ == '__main__':
  year = current_year()
  portfolio = None
  if len(sys.argv) > 1:
    arguments = eval(sys.argv[1])
    year = int(arguments.get('year', current_year()))
    portfolio = arguments.get('portfolio', None)
  
  shares = populate_shares(year)
  
  shares.sort_values(by=['Fisher Score', 'Cotação'], ascending=[False, True], inplace=True)
  
  shares['Ranking'] = range(1, len(shares) + 1)

  if portfolio != None:
    shares = portfolios.filter(shares, portfolio)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  # backtest.display_shares(shares, year)

  if year != current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))

# Outros ensinamentos de Kenneth Fisher

# * Evite a Imprensa e Modismos: Para Fisher, para se ter sucesso o investidor precisa desviar do que está em foco e é muito óbvio, e isso inclui qualquer coisa que esteja na mídia.
# * Evite Profissionais de Investimento: Se eles soubessem o que fazem, não seriam tão incompetentes em seus resultados. Para Fisher, analistas e gestores são limitados e muitos seguem alguma cartilha para não se distanciarem muito de seus pares.
# * Não seja Exatamente do Contra: Pensar de forma  diferente não quer dizer que o investidor deve ser do contra. Ele deve ser independente e assumir suas próprias decisões, não delegando para terceiros.
# * Aceite que Você pode estar Errado: Fisher defende a diversificação pois acredita que todos podem estar errados. Ao diversificar, você reduz o risco de seus investimentos e evita erros de julgamento que levam a prejuízos financeiros.
# * Pense Relativamente: nesta dica Fisher diz para sempre pensarmos os números também nos valores relativos. Uma desastre econômico com uma perda de 20 bilhões de dólares significa apenas 0,1% de um País com PIB de 24 trilhões. Portanto, sempre que ver ou ouvir algum número, tente imaginar de forma relativa. Ou seja, esse valor é grande em relação ao que? Será que ele é realmente significativo?
# * Pense Globalmente: as tendências globais prevalecem sobre as locais em qualquer país, incluindo os EUA. O dinheiro atravessa fronteiras com relativa liberdade. Portanto, se você já possui uma grande quantidade de capital acumulado, talvez seja o momento ideal de investir em outros países e bolsas. Além de ter acesso a grandes empresas e mercados mais maduros, vai diversificar sua carteira, diluindo o risco.
