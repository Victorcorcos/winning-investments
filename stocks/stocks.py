# This algorithmn fetch all the share infos from fundamentus system and fill all the missing info using the statusinvest system.

# For example: The TAEE11 (Taesa) share on the fundamentus website is missing most part of info (http://www.fundamentus.com.br/detalhes.php?papel=TAEE11)
#              However, on the statusinvest website, all of these infos are filled (https://statusinvest.com.br/acoes/taee11)
#              This algorithmn will fill the fundamentus missing info using the infos from the statusinvest system
#              stocks.shares() return a panda dataset with all of these infos

import sys, os
sys.path.extend(['../waiting_bar'])

import fundamentus

import pandas
import pyperclip
import numpy

from math import sqrt
from decimal import Decimal

import http.cookiejar
import urllib.request
import urllib.parse
import json

import string
import warnings

# Ações
# https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%220%3B25%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1

# Fundos Imobiliários
# https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%220%3B25%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=2

def print(thing):
  import pprint
  return pprint.PrettyPrinter(indent=4).pprint(thing)

def shares(*args, **kwargs):
  url = 'https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%220%3B25%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1'
  cookie_jar = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
  opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                       ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
  with opener.open(url, urllib.parse.urlencode({}).encode('UTF-8')) as link:
    content = link.read().decode('ISO-8859-1')
  status_invest_shares = json.loads(content)
  statuses_result = {}
  for item in status_invest_shares:
    statuses_result[item['ticker']] = item
  mapper = {
    # fundamentus fields => status_invest fields
    'Cotação': 'price',
    'P/L': 'p_L',
    'P/VP': 'p_VP',
    'PSR': 'p_SR',
    'Dividend Yield': 'dy',
    'P/Ativo': 'p_Ativo',
    'P/Capital de Giro': 'p_CapitalGiro',
    'P/EBIT': 'p_Ebit',
    'P/ACL': 'p_AtivoCirculante',
    'EV/EBIT': 'eV_Ebit',
    'Margem Ebit': 'margemEbit',
    'Margem Líquida': 'margemLiquida',
    'Liquidez Corrente': 'liquidezCorrente',
    'ROIC': 'roic',
    'ROE': 'roe',
    'Liquidez 2 meses': '?1', # Somente no fundamentus
    'EV/EBITDA': '?2', # Somente no fundamentus
    'Patrimônio Líquido': '?3', # Somente no fundamentus
    'Dívida Bruta/Patrimônio': '?4', # Somente no fundamentus
    'Crescimento em 5 anos': '?5' # Somente no fundamentus
  }
  new_status = {
    # more readable fields => status_invest fields
    'CAGR Lucros 5 Anos': 'lucros_Cagr5',
    'CAGR Receitas 5 Anos': 'receitas_Cagr5',
    'Dívida Líquida/Patrimônio': 'dividaliquidaPatrimonioLiquido',
    'Dívida Líquida/EBIT': 'dividaLiquidaEbit',
    'ROA': 'roa',
    'Patrimonio/Ativos': 'pl_Ativo',
    'Giro Ativos': 'giroAtivos',
    'Margem Bruta': 'margemBruta',
    'Passivo/Ativo': 'passivo_Ativo',
    'Liquidez Média Diária': 'liquidezMediaDiaria'
  }
  mapper.update(new_status)
  shares = fundamentus.shares()
  shares = add_invest_columns(shares, new_status)
  for index in range(len(shares)):
    ticker = shares.index[index]
    if statuses_result.get(ticker):
      shares['Cotação'][index] = Decimal(str(statuses_result[ticker].get(mapper['Cotação'], shares['Cotação'][index])))
      shares['P/L'][index] = Decimal(str(statuses_result[ticker].get(mapper['P/L'], shares['P/L'][index])))
      shares['P/VP'][index] = Decimal(str(statuses_result[ticker].get(mapper['P/VP'], shares['P/VP'][index])))
      shares['PSR'][index] = Decimal(str(statuses_result[ticker].get(mapper['PSR'], shares['PSR'][index])))
      shares['Dividend Yield'][index] = Decimal(str(statuses_result[ticker].get(mapper['Dividend Yield'], shares['Dividend Yield'][index]))) / 100
      shares['P/Ativo'][index] = Decimal(str(statuses_result[ticker].get(mapper['P/Ativo'], shares['P/Ativo'][index])))
      shares['P/Capital de Giro'][index] = Decimal(str(statuses_result[ticker].get(mapper['P/Capital de Giro'], shares['P/Capital de Giro'][index])))
      shares['P/EBIT'][index] = Decimal(str(statuses_result[ticker].get(mapper['P/EBIT'], shares['P/EBIT'][index])))
      shares['P/ACL'][index] = Decimal(str(statuses_result[ticker].get(mapper['P/ACL'], shares['P/ACL'][index])))
      shares['EV/EBIT'][index] = Decimal(str(statuses_result[ticker].get(mapper['EV/EBIT'], shares['EV/EBIT'][index])))
      shares['EV/EBITDA'][index] = Decimal(str(statuses_result[ticker].get(mapper['EV/EBITDA'], shares['EV/EBITDA'][index])))
      shares['Margem Ebit'][index] = Decimal(str(statuses_result[ticker].get(mapper['Margem Ebit'], shares['Margem Ebit'][index])))
      shares['Margem Líquida'][index] = Decimal(str(statuses_result[ticker].get(mapper['Margem Líquida'], shares['Margem Líquida'][index])))
      shares['Liquidez Corrente'][index] = Decimal(str(statuses_result[ticker].get(mapper['Liquidez Corrente'], shares['Liquidez Corrente'][index])))
      shares['ROIC'][index] = Decimal(str(statuses_result[ticker].get(mapper['ROIC'], shares['ROIC'][index]))) / 100
      shares['ROE'][index] = Decimal(str(statuses_result[ticker].get(mapper['ROE'], shares['ROE'][index]))) / 100
      # Below are new columns from status_invest
      shares['CAGR Lucros 5 Anos'][index] = Decimal(str(statuses_result[ticker].get(mapper['CAGR Lucros 5 Anos'], numpy.nan)))
      shares['CAGR Receitas 5 Anos'][index] = Decimal(str(statuses_result[ticker].get(mapper['CAGR Receitas 5 Anos'], numpy.nan)))
      shares['Dívida Líquida/Patrimônio'][index] = Decimal(str(statuses_result[ticker].get(mapper['Dívida Líquida/Patrimônio'], numpy.nan)))
      shares['Dívida Líquida/EBIT'][index] = Decimal(str(statuses_result[ticker].get(mapper['Dívida Líquida/EBIT'], numpy.nan)))
      shares['ROA'][index] = Decimal(str(statuses_result[ticker].get(mapper['ROA'], numpy.nan))) / 100
      shares['Patrimonio/Ativos'][index] = Decimal(str(statuses_result[ticker].get(mapper['Patrimonio/Ativos'], numpy.nan)))
      shares['Giro Ativos'][index] = Decimal(str(statuses_result[ticker].get(mapper['Giro Ativos'], numpy.nan)))
      shares['Margem Bruta'][index] = Decimal(str(statuses_result[ticker].get(mapper['Margem Bruta'], numpy.nan))) / 100
      shares['Passivo/Ativo'][index] = Decimal(str(statuses_result[ticker].get(mapper['Passivo/Ativo'], numpy.nan)))
      shares['Liquidez Média Diária'][index] = Decimal(str(statuses_result[ticker].get(mapper['Liquidez Média Diária'], numpy.nan)))
  return shares

def add_invest_columns(shares, new_status):
  for column in new_status.keys():
    shares[column] = Decimal(numpy.nan)
  return shares

# Reordena a tabela para mostrar a Cotação, o Valor Intríseco e o Graham Score como primeiras colunass
def reorder_columns(shares):
  return shares[['Cotação'] + [col for col in shares.columns if col not in ('Cotação')]]

if __name__ == '__main__':
  from waitingbar import WaitingBar
  progress_bar = WaitingBar('[*] Calculating...')
  shares = shares()
  shares = reorder_columns(shares)
  shares = shares.sort_values(by=['Cotação'], ascending=[True])
  pyperclip.copy(shares.to_markdown())
  print(shares)
  progress_bar.stop()
