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

# Princípios utilizados:

# - [x] Fórmula Mágica 1): > ROIC e < EV/EBIT e > ROE e < P/L
# - [x] Fórmula Mágica 2): > ROIC e < EV/EBIT
# - [x] Fórmula Mágica 3): > ROE e < P/L

import sys, os
sys.path.extend([f'../{name}' for name in os.listdir("..") if os.path.isdir(f'../{name}')])
sys.path.extend(['..'])

import pyperclip

import greenblatt
import fundamentus
import backtest
import time

# Chame a função main de acordo com qual formula você quer aplicar: roe OU roic
# Formula ROE:  Utiliza ROE  e P/L
# Formula ROIC: Utiliza ROIC e EV/EBIT (EV/EBITDA não tem no fundamentus)
# ================ Exemplos ================
# python3 greenblatt_diversified.py "{ 'formula': 'ROE', 'year': 2013 }"
# python3 greenblatt_diversified.py "{ 'formula': 'ROIC', 'year': 2020 }"
# python3 greenblatt_diversified.py "{ 'year': 2019 }"
if __name__ == '__main__':
  year = greenblatt.current_year()
  formula = None
  if len(sys.argv) > 1:
    arguments = eval(sys.argv[1])
    year = int(arguments.get('year', greenblatt.current_year()))
    formula = arguments.get('formula', None)
  
  shares = greenblatt.populate_shares(year, formula)
  
  shares.sort_values(by=['Magic Formula', 'Cotação'], ascending=[True, True], inplace=True)
  
  shares = shares.drop_duplicates(subset='Segmento')
  
  shares['Ranking (Greenblatt)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != greenblatt.current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
