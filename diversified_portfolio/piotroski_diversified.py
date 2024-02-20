#!/usr/bin/env python3

# Para a análise, são utilizados princípios do Joseph D. Piotroski
# Estipulados no livro: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers"
# No estudo original de Piotroski, ao longo de 20 anos (1976–1996), uma estratégia de investimento baseado nessa pontuação, com a compra de empresas com F-Score alto e a venda de empresas com F-Score baixo, gerou um retorno anual de 23%, bem superior à media do mercado.
# Piotroski elaborou um Score chamado "Piotroski F-score" que varia de 0 a 9, quanto maior, por mais filtros as ações passaram

# Princípios utilizados:

# 1. ROA > 0 (ano corrente)
# 2. FCO > 0 (ano corrente)
# 3. FCO > Lucro Líquido (ano corrente)
# 4. ROA atual > ROA ano anterior
# 5. Alavancagem atual < ano passado (Dívida Líquida / Patrimônio Líquido)
# 6. Liquidez Corrente atual > Liquidez Corrente ano anterior
# 7. Nro. Ações atual = Nro. Ações ano anterior
# 8. Margem Bruta atual > Margem Bruta ano anterior
# 9. Giro Ativo atual > Giro Ativo ano anterior

# Referência: https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
# Backtesting on USA: https://www.quant-investing.com/blogs/backtests/2018/11/06/piotroski-f-score-back-test

import sys, os
sys.path.extend([f'../{name}' for name in os.listdir("..") if os.path.isdir(f'../{name}')])
sys.path.extend(['..'])

import pyperclip

import piotroski
import fundamentus
import backtest
import time

# python3 piotroski_diversified.py "{ 'year': 2015 }"
if __name__ == '__main__':
  year = piotroski.current_year()
  if len(sys.argv) > 1:
    year = int(eval(sys.argv[1])['year'])
  
  shares = piotroski.populate_shares(year)
  
  shares.sort_values(by=['Piotroski Score', 'Cotação'], ascending=[False, True], inplace=True)
  
  shares = shares.drop_duplicates(subset='Segmento')
  
  shares['Ranking (Piotrotski)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != piotroski.current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
