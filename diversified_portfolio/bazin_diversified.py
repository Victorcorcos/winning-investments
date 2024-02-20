#!/usr/bin/env python3

# A idéia é calcular o ranking (Bazin) das ações analisando os dados fundamentalistas de todas as empresas da bolsa B3

# Para a análise, são utilizados princípios do Décio Bazin
# Ele é autor do livro: "Faça Fortuna Com Ações", que é tido como literatura indicada
# por Luis Barsi, o maior investidor na bolsa brasileira.

# Princípios utilizados:

# - [x] 1. Preço Justo (Bazin) > 1.5 * Preço. Preço Justo (Bazin) => Dividend Yield * 16.67 (Por: Décio Bazin)
# - [x] 2. Dívida Bruta/Patrimônio < 0.5 (50%)
# - [x] 3. Dividend Yield > 0.06 (6%)
# - [x] 4. Média do Dividend Yield nos últimos 5 anos > 0.05 (5%)
# - [x] 5. Pagamento positivo de dividendos nos últimos 5 anos
# - [x] 6. Pagamento crescente de dividendos nos últimos 5 anos
# - [x] 7. 0 < Payout < 1

# === Parallel fetching... https://stackoverflow.com/questions/16181121/a-very-simple-multithreading-parallel-url-fetching-without-queue

# Pega o histórico dos Dividendos...
# DPA => Dividendo Por Ação. Esse que é importante!
# https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsYear?ticker=PETR4
# Pega Histórico de: year, cresRec, divBruta, data, qntAcoes, cotacao, pl, pvp, pebit, pfco, psr, pAtivos, pCapGiro, pAtivCLiq, divYeld, evebit, valordaFirma, valordeMercado, fci, dbPl, vpa, margBruta, capex, margLiq, capexLL, giroAtivos, fcf, caixaLivre, fcl, payout, lpa, margEbit, roic, ebitAtivo, fco, dpa, liqCorrent, divBrPatrim, capexFco, fct, ativoCirculante, fciLL, capexDetails, roe, roa, dlpl, payoutDetails, ebit, lucroLiquido, receitaLiquida

# Pega o histórico de Dividend Yield...
# Últimos 5 anos...
# https://statusinvest.com.br/acao/companytickerprovents?ticker=TRPL4&chartProventsType=1

# Últimos 20 anos...
# https://statusinvest.com.br/acao/companytickerprovents?ticker=TRPL4&chartProventsType=2

# Futura análise da análise ()
# https://statusinvest.com.br/acao/getrevenue?companyName=enauta&type=0&trimestral=false

import sys, os
sys.path.extend([f'../{name}' for name in os.listdir("..") if os.path.isdir(f'../{name}')])
sys.path.extend(['..'])

import pyperclip

import bazin
import fundamentus
import backtest
import time

# python3 bazin_diversified.py "{ 'year': 2015 }"
if __name__ == '__main__':  
  year = bazin.current_year()
  if len(sys.argv) > 1:
    year = int(eval(sys.argv[1])['year'])
  
  shares = bazin.populate_shares(year)
  
  shares.sort_values(by=['Bazin Score', 'Preço Justo (Bazin) / Cotação'], ascending=[False, False], inplace=True)

  shares = shares.drop_duplicates(subset='Segmento')
  
  shares['Ranking (Bazin)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != bazin.current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
