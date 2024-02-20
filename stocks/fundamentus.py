#!/usr/bin/env python3

# Captura os dados iniciais a partir do site www.fundamentus.com.br

import re
import urllib.request
import urllib.parse
import http.cookiejar
import pandas
import time

from lxml.html import fragment_fromstring
from decimal import Decimal

# Setores das ações da bolsa!
# Preenchidos a partir da lista oficial da B3!
# http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/acoes/consultas/classificacao-setorial/
categories = {
  'CSAN': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'DMMO': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'ENAT': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'RPMG': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'PETR': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'BRDT': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'PRIO': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'UGPA': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'UGPA': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Exploração, Refino e Distribuição'
  },
  'LUPA': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Equipamentos e Serviços'
  },
  'OSXB': {
    'setor': 'Petróleo, Gás e Biocombustíveis',
    'subsetor': 'Petróleo, Gás e Biocombustíveis',
    'segmento': 'Equipamentos e Serviços'
  },
  'BRAP': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Mineração',
    'segmento': 'Minerais Metálicos'
  },
  'LTEL': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Mineração',
    'segmento': 'Minerais Metálicos'
  },
  'LTLA': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Mineração',
    'segmento': 'Minerais Metálicos'
  },
  'MMXM': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Mineração',
    'segmento': 'Minerais Metálicos'
  },
  'VALE': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Mineração',
    'segmento': 'Minerais Metálicos'
  },
  'FESA': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Siderurgia'
  },
  'GGBR': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Siderurgia'
  },
  'GOAU': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Siderurgia'
  },
  'CSNA': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Siderurgia'
  },
  'USIM': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Siderurgia'
  },
  'MGEL': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Artefatos de Ferro e Aço'
  },
  'PATI': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Artefatos de Ferro e Aço'
  },
  'TKNO': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Artefatos de Ferro e Aço'
  },
  'PMAM': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Siderurgia e Metalurgia',
    'segmento': 'Artefatos de Cobre'
  },
  'BRKM': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Petroquímicos'
  },
  'ELEK': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Petroquímicos'
  },
  'GPCP': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Petroquímicos'
  },
  'FHER': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Fertilizantes e Defensivos'
  },
  'NUTR': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Fertilizantes e Defensivos'
  },
  'CRPG': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Químicos Diversos'
  },
  'UNIP': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Químicos',
    'segmento': 'Químicos Diversos'
  },
  'DTEX': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Madeira'
  },
  'EUCA': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Madeira'
  },
  'RANI': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Papel e Celulose'
  },
  'KLBN': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Papel e Celulose'
  },
  'MSPA': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Papel e Celulose'
  },
  'STTZ': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Papel e Celulose'
  },
  'NEMO': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Papel e Celulose'
  },
  'SUZB': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Madeira e Papel',
    'segmento': 'Papel e Celulose'
  },
  'MTIG': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Embalagens',
    'segmento': 'Embalagens'
  },
  'SNSY': {
    'setor': 'Materiais Básicos',
    'subsetor': 'Materiais Diversos',
    'segmento': 'Materiais Diversos'
  },
  'ETER': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Produtos para Construção'
  },
  'HAGA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Produtos para Construção'
  },
  'PTBL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Produtos para Construção'
  },
  'AZEV': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Construção Pesada'
  },
  'SOND': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Engenharia Consultiva'
  },
  'TCNO': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Engenharia Consultiva'
  },
  'MILS': {
    'setor': 'Bens Industriais',
    'subsetor': 'Construção e Engenharia',
    'segmento': 'Serviços Diversos'
  },
  'EMBR': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Aeronáutico e de Defesa'
  },
  'FRAS': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'POMO': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'RAPT': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'RCSL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'RSUL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'TUPY': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'MWET': {
    'setor': 'Bens Industriais',
    'subsetor': 'Material de Transporte',
    'segmento': 'Material Rodoviário'
  },
  'SHUL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Motores, Compressores e Outros'
  },
  'WEGE': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Motores, Compressores e Outros'
  },
  'EALT': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'BDLL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'ROMI': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'INEP': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'KEPL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'FRIO': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'NORD': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'PTCA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Industriais'
  },
  'MTSA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Construção e Agrícolas'
  },
  'STTR': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Máq. e Equip. Construção e Agrícolas'
  },
  'TASA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Máquinas e Equipamentos',
    'segmento': 'Armas e Munições'
  },
  'AZUL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Aéreo'
  },
  'GOLL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Aéreo'
  },
  'FRRN': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Ferroviário'
  },
  'GASC': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Ferroviário'
  },
  'RLOG': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Ferroviário'
  },
  'VSPT': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Ferroviário'
  },
  'MRSA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Ferroviário'
  },
  'RAIL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Ferroviário'
  },
  'LOGN': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Hidroviário'
  },
  'LUXM': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Hidroviário'
  },
  'JSLG': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Rodoviário'
  },
  'TGMA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Transporte Rodoviário'
  },
  'ANHB': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'CCRO': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'RPTA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'CRTE': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'ERDV': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'ECNT': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'ASCP': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'ECOR': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'ECOV': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'COLN': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'RDVT': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'CRBD': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'TRIA': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'TPIS': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'VOES': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Exploração de Rodovias'
  },
  'AGRU': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Serviços de Apoio e Armazenagem'
  },
  'PSVM': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Serviços de Apoio e Armazenagem'
  },
  'IVPR': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Serviços de Apoio e Armazenagem'
  },
  'SAIP': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Serviços de Apoio e Armazenagem'
  },
  'STBP': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Serviços de Apoio e Armazenagem'
  },
  'WSON': {
    'setor': 'Bens Industriais',
    'subsetor': 'Transporte',
    'segmento': 'Serviços de Apoio e Armazenagem'
  },
  'ATMP': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'BBML': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'CARD': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'DTCY': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'ALPK': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'FLEX': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'PRNR': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'VLID': {
    'setor': 'Bens Industriais',
    'subsetor': 'Serviços Diversos',
    'segmento': 'Serviços Diversos'
  },
  'BTTL': {
    'setor': 'Bens Industriais',
    'subsetor': 'Comércio',
    'segmento': 'Material de Transporte'
  },
  'MMAQ': {
    'setor': 'Bens Industriais',
    'subsetor': 'Comércio',
    'segmento': 'Material de Transporte'
  },
  'WLMM': {
    'setor': 'Bens Industriais',
    'subsetor': 'Comércio',
    'segmento': 'Material de Transporte'
  },
  'APTI': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Agropecuária',
    'segmento': 'Agricultura'
  },
  'AGRO': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Agropecuária',
    'segmento': 'Agricultura'
  },
  'FRTA': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Agropecuária',
    'segmento': 'Agricultura'
  },
  'SLCE': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Agropecuária',
    'segmento': 'Agricultura'
  },
  'TESA': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Agropecuária',
    'segmento': 'Agricultura'
  },
  'BSEV': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Açucar e Alcool'
  },
  'RESA': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Açucar e Alcool'
  },
  'SMTO': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Açucar e Alcool'
  },
  'BRFS': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Carnes e Derivados'
  },
  'BAUH': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Carnes e Derivados'
  },
  'JBSS': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Carnes e Derivados'
  },
  'MRFG': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Carnes e Derivados'
  },
  'BEEF': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Carnes e Derivados'
  },
  'MNPR': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Carnes e Derivados'
  },
  'CAML': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Alimentos Diversos'
  },
  'JMCD': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Alimentos Diversos'
  },
  'JOPA': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Alimentos Diversos'
  },
  'MDIA': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Alimentos Diversos'
  },
  'ODER': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Alimentos Processados',
    'segmento': 'Alimentos Diversos'
  },
  'ABEV': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Bebidas',
    'segmento': 'Cervejas e Refrigerantes'
  },
  'NTCO': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Produtos de Uso Pessoal e de Limpeza',
    'segmento': 'Produtos de Uso Pessoal'
  },
  'BOBR': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Produtos de Uso Pessoal e de Limpeza',
    'segmento': 'Produtos de Limpeza'
  },
  'CRFB': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Comércio e Distribuição',
    'segmento': 'Alimentos'
  },
  'PCAR': {
    'setor': 'Consumo não Cíclico',
    'subsetor': 'Comércio e Distribuição',
    'segmento': 'Alimentos'
  },
  'CALI': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'CRDE': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'CYRE': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'DIRR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'EVEN': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'EZTC': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'GFSA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'HBOR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'INNT': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'JHSF': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'JFEN': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'MTRE': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'MDNE': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'MRVE': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'PDGR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'RDNI': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'RSID': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'TCSA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'TEND': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'TRIS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'VIVR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Construção Civil',
    'segmento': 'Incorporações'
  },
  'CEDO': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'CTNM': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'DOHL': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'ECPR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'CATA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'CTKA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'PTNT': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'CTSA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'SGPS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'TEKA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'TXRX': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Fios e Tecidos'
  },
  'HGTX': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Vestuário'
  },
  'ALPA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Calçados'
  },
  'CAMB': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Calçados'
  },
  'GRND': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Calçados'
  },
  'VULC': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Calçados'
  },
  'MNDL': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Acessórios'
  },
  'TECN': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Acessórios'
  },
  'VIVA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Tecidos, Vestuário e Calçados',
    'segmento': 'Acessórios'
  },
  'WHRL': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Utilidades Domésticas',
    'segmento': 'Eletrodomésticos'
  },
  'UCAS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Utilidades Domésticas',
    'segmento': 'Móveis'
  },
  'HETA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Utilidades Domésticas',
    'segmento': 'Utensílios Domésticos'
  },
  'MYPK': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Automóveis e Motocicletas',
    'segmento': 'Automóveis e Motocicletas'
  },
  'LEVE': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Automóveis e Motocicletas',
    'segmento': 'Automóveis e Motocicletas'
  },
  'PLAS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Automóveis e Motocicletas',
    'segmento': 'Automóveis e Motocicletas'
  },
  'HOOT': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Hoteis e Restaurantes',
    'segmento': 'Hotelaria'
  },
  'BKBR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Hoteis e Restaurantes',
    'segmento': 'Restaurante e Similares'
  },
  'MEAL': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Hoteis e Restaurantes',
    'segmento': 'Restaurante e Similares'
  },
  'BMKS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Viagens e Lazer',
    'segmento': 'Bicicletas'
  },
  'ESTR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Viagens e Lazer',
    'segmento': 'Brinquedos e Jogos'
  },
  'AHEB': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Viagens e Lazer',
    'segmento': 'Produção de Eventos e Shows'
  },
  'SHOW': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Viagens e Lazer',
    'segmento': 'Produção de Eventos e Shows'
  },
  'CVCB': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Viagens e Lazer',
    'segmento': 'Viagens e Turismo'
  },
  'SMFT': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Viagens e Lazer',
    'segmento': 'Atividades Esportivas'
  },
  'ANIM': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Serviços Educacionais'
  },
  'BAHI': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Serviços Educacionais'
  },
  'COGN': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Serviços Educacionais'
  },
  'SEER': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Serviços Educacionais'
  },
  'YDUQ': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Serviços Educacionais'
  },
  'RENT': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Aluguel de carros'
  },
  'LCAM': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Aluguel de carros'
  },
  'MSRO': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Aluguel de carros'
  },
  'MOVI': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Aluguel de carros'
  },
  'UNID': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Aluguel de carros'
  },
  'SMLS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Diversos',
    'segmento': 'Programas de Fidelização'
  },
  'ARZZ': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'CEAB': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'CGRA': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'GUAR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'LLIS': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'AMAR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'LREN': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Tecidos, Vestuário e Calçados'
  },
  'MGLU': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Eletrodomésticos'
  },
  'VVAR': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Eletrodomésticos'
  },
  'BTOW': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Produtos Diversos'
  },
  'CNTO': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Produtos Diversos'
  },
  'LAME': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Produtos Diversos'
  },
  'SLED': {
    'setor': 'Consumo Cíclico',
    'subsetor': 'Comércio',
    'segmento': 'Produtos Diversos'
  },
  'BIOM': {
    'setor': 'Saúde',
    'subsetor': 'Medicamentos e Outros Produtos',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'GBIO': {
    'setor': 'Saúde',
    'subsetor': 'Medicamentos e Outros Produtos',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'NRTQ': {
    'setor': 'Saúde',
    'subsetor': 'Medicamentos e Outros Produtos',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'OFSA': {
    'setor': 'Saúde',
    'subsetor': 'Medicamentos e Outros Produtos',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'ADHM': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'AALR': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'DASA': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'FLRY': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'HAPV': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'PARD': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'GNDI': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'ODPV': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'QUAL': {
    'setor': 'Saúde',
    'subsetor': 'Análises e Diagnósticos',
    'segmento': 'Análises e Diagnósticos'
  },
  'BALM': {
    'setor': 'Saúde',
    'subsetor': 'Equipamentos',
    'segmento': 'Equipamentos'
  },
  'LMED': {
    'setor': 'Saúde',
    'subsetor': 'Equipamentos',
    'segmento': 'Equipamentos'
  },
  'PNVL': {
    'setor': 'Saúde',
    'subsetor': 'Comércio e Distribuição',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'HYPE': {
    'setor': 'Saúde',
    'subsetor': 'Comércio e Distribuição',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'PFRM': {
    'setor': 'Saúde',
    'subsetor': 'Comércio e Distribuição',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'RADL': {
    'setor': 'Saúde',
    'subsetor': 'Comércio e Distribuição',
    'segmento': 'Medicamentos e Outros Produtos'
  },
  'POSI': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Computadores e Equipamentos',
    'segmento': 'Computadores e Equipamentos'
  },
  'BRQB': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Programas e Serviços',
    'segmento': 'Programas e Serviços'
  },
  'LINX': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Programas e Serviços',
    'segmento': 'Programas e Serviços'
  },
  'LWSA': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Programas e Serviços',
    'segmento': 'Programas e Serviços'
  },
  'QUSW': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Programas e Serviços',
    'segmento': 'Programas e Serviços'
  },
  'SQIA': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Programas e Serviços',
    'segmento': 'Programas e Serviços'
  },
  'TOTS': {
    'setor': 'Tecnologia da Informação',
    'subsetor': 'Programas e Serviços',
    'segmento': 'Programas e Serviços'
  },
  'ALGT': {
    'setor': 'Comunicações',
    'subsetor': 'Telecomunicações',
    'segmento': 'Telecomunicações'
  },
  'OIBR': {
    'setor': 'Comunicações',
    'subsetor': 'Telecomunicações',
    'segmento': 'Telecomunicações'
  },
  'TELB': {
    'setor': 'Comunicações',
    'subsetor': 'Telecomunicações',
    'segmento': 'Telecomunicações'
  },
  'VIVT': {
    'setor': 'Comunicações',
    'subsetor': 'Telecomunicações',
    'segmento': 'Telecomunicações'
  },
  'TIMP': {
    'setor': 'Comunicações',
    'subsetor': 'Telecomunicações',
    'segmento': 'Telecomunicações'
  },
  'CNSY': {
    'setor': 'Comunicações',
    'subsetor': 'Mídia',
    'segmento': 'Produção e Difusão de Filmes e Programas'
  },
  'AESL': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'TIET': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'AFLT': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ALUP': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CBEE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CPTE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CEBR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CEED': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EEEL': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CLSC': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'GPAR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CEPE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CMIG': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CMGD': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CMGT': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CESP': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CEEB': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'COCE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CPLE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CSRN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CPFE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CPFG': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CPFP': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CPRE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EBEN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EKTR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ELET': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'LIPR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EMAE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ENBR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ENGI': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ENMT': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ENER': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ENEV': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EGIE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EQPA': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EQMA': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'EQTL': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ESCE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'FGEN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'GEPA': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'ITPB': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'LIGH': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'LIGT': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'NEOE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'OMGE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'PALF': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'PRMN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'REDE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'RNEW': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'STKF': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'STEN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'TAEE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'TMPE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'TEPE': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'TRPL': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'UPKP': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Energia Elétrica',
    'segmento': 'Energia Elétrica'
  },
  'CASN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Água e Saneamento',
    'segmento': 'Água e Saneamento'
  },
  'CSMG': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Água e Saneamento',
    'segmento': 'Água e Saneamento'
  },
  'IGSN': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Água e Saneamento',
    'segmento': 'Água e Saneamento'
  },
  'SBSP': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Água e Saneamento',
    'segmento': 'Água e Saneamento'
  },
  'SAPR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Água e Saneamento',
    'segmento': 'Água e Saneamento'
  },
  'SNST': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Água e Saneamento',
    'segmento': 'Água e Saneamento'
  },
  'CEGR': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Gás',
    'segmento': 'Gás'
  },
  'CGAS': {
    'setor': 'Utilidade Pública',
    'subsetor': 'Gás',
    'segmento': 'Gás'
  },
  'ABCB': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'RPAD': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BRIV': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BAZA': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BMGB': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BIDI': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BPAN': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BGIP': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BEES': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BPAR': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BRSR': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BBDC': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BBAS': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BSLI': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BPAC': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'IDVL': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'ITSA': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'ITUB': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BMEB': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BMIN': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'BNBR': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'PRBC': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'PINE': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'SANB': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Bancos'
  },
  'CRIV': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Soc. Crédito e Financiamento'
  },
  'FNCN': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Soc. Crédito e Financiamento'
  },
  'MERC': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Soc. Crédito e Financiamento'
  },
  'BDLS': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Soc. Arrendamento Mercantil'
  },
  'BVLS': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Soc. Arrendamento Mercantil'
  },
  'DBEN': {
    'setor': 'Financeiro',
    'subsetor': 'Intermediários Financeiros',
    'segmento': 'Soc. Arrendamento Mercantil'
  },
  'BZRS': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'BSCS': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'BRCS': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'WTVR': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'CBSC': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'ECOA': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'GAFL': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'GAIA': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'OCTS': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'PDGS': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'PLSC': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'RBRA': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'APCS': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'VERT': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'WTPI': {
    'setor': 'Financeiro',
    'subsetor': 'Securitizadoras de Recebíveis',
    'segmento': 'Securitizadoras de Recebíveis'
  },
  'BNDP': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Gestão de Recursos e Investimentos'
  },
  'BFRE': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Gestão de Recursos e Investimentos'
  },
  'GPIV': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Gestão de Recursos e Investimentos'
  },
  'IDNT': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Gestão de Recursos e Investimentos'
  },
  'PPLA': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Gestão de Recursos e Investimentos'
  },
  'B3SA': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Serviços Financeiros Diversos'
  },
  'CIEL': {
    'setor': 'Financeiro',
    'subsetor': 'Serviços Financeiros Diversos',
    'segmento': 'Serviços Financeiros Diversos'
  },
  'BRGE': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Seguradoras'
  },
  'BBSE': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Seguradoras'
  },
  'IRBR': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Seguradoras'
  },
  'PSSA': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Seguradoras'
  },
  'CSAB': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Seguradoras'
  },
  'SULA': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Seguradoras'
  },
  'APER': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Corretoras de Seguros'
  },
  'WIZS': {
    'setor': 'Financeiro',
    'subsetor': 'Previdência e Seguros',
    'segmento': 'Corretoras de Seguros'
  },
  'ALSO': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'BRML': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'BRPR': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'CORR': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'CCPR': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'GSHP': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'HBTS': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'IGBR': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'IGTA': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'JPSA': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'LOGG': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'MNZC': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'MULT': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'SCAR': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Exploração de Imóveis'
  },
  'BBRK': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Intermediação Imobiliária'
  },
  'LPSB': {
    'setor': 'Financeiro',
    'subsetor': 'Exploração de Imóveis',
    'segmento': 'Intermediação Imobiliária'
  },
  'MOAR': {
    'setor': 'Financeiro',
    'subsetor': 'Holdings Diversificadas',
    'segmento': 'Holdings Diversificadas'
  },
  'PEAB': {
    'setor': 'Financeiro',
    'subsetor': 'Holdings Diversificadas',
    'segmento': 'Holdings Diversificadas'
  },
  'SPRI': {
    'setor': 'Financeiro',
    'subsetor': 'Holdings Diversificadas',
    'segmento': 'Holdings Diversificadas'
  },
  'CTBA': {
    'setor': 'Financeiro',
    'subsetor': 'Outros Títulos',
    'segmento': 'Outros Títulos'
  },
  'MCRJ': {
    'setor': 'Financeiro',
    'subsetor': 'Outros Títulos',
    'segmento': 'Outros Títulos'
  },
  'PMSP': {
    'setor': 'Financeiro',
    'subsetor': 'Outros Títulos',
    'segmento': 'Outros Títulos'
  },
  'QVQP': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'ALEF': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'ATOM': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'BETP': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'CABI': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'CACO': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'CPTP': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'MAPT': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'CMSA': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'OPGM': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'FIGE': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'JBDU': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'SPRT': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'MGIP': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'OPHE': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'PPAR': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'PRPT': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'SLCT': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'OPSE': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
  'OPTS': {
    'setor': 'Outros',
    'subsetor': 'Outros',
    'segmento': 'Outros'
  },
}

def start_date(year):
  if year == current_year():
    return time.strftime("%Y-%m-%d")
  
  date = re.findall(r".*web\/(\w{4})(\w{2})(\w{2})(\w{2})(\w{2})(\w{2})\/.*", backtest(year))
  return f"{date[0][0]}-{date[0][1]}-{date[0][2]}"

# Get the current_year integer value, for example: 2020
def current_year():
  return int(time.strftime("%Y"))

def shares(year = None):
  url = backtest(year)
  cookie = http.cookiejar.CookieJar()
  request = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
  request.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
    ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')
  ]
  
  # Aqui estão os parâmetros de busca das ações
  # Estão em branco para que retorne todas as disponíveis
  data = {'pl_min': '', 'pl_max': '', 'pvp_min': '', 'pvp_max' : '', 'psr_min': '', 'psr_max': '', 'divy_min': '', 'divy_max': '', 'pativos_min': '', 'pativos_max': '', 'pcapgiro_min': '', 'pcapgiro_max': '', 'pebit_min': '', 'pebit_max': '', 'fgrah_min': '', 'fgrah_max': '', 'firma_ebit_min': '', 'firma_ebit_max': '', 'margemebit_min': '', 'margemebit_max': '', 'margemliq_min': '', 'margemliq_max': '', 'liqcorr_min': '', 'liqcorr_max': '', 'roic_min': '', 'roic_max': '', 'roe_min': '', 'roe_max': '', 'liq_min': '', 'liq_max': '', 'patrim_min': '', 'patrim_max': '', 'divbruta_min': '', 'divbruta_max': '', 'tx_cresc_rec_min': '', 'tx_cresc_rec_max': '', 'setor': '', 'negociada': 'ON', 'ordem': '1', 'x': '28', 'y': '16'}
  
  with request.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
      content = link.read().decode('ISO-8859-1')
  
  pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
  content = re.findall(pattern, content)[0]
  page = fragment_fromstring(content)
  result = pandas.DataFrame(dataframe_opts(year))
  
  for rows in page.xpath('tbody')[0].findall("tr"):
      new_row = pandas.DataFrame(index=[rows.getchildren()[0][0].getchildren()[0].text],
                                 data=dataframe_data(rows, year))
      result = result.append(new_row)
  
  result = result[result['Cotação'] > 0]

  result = add_sector(result)
  
  return result

def add_sector(shares):
  shares['Setor'] = ''
  shares['Subsetor'] = ''
  shares['Segmento'] = ''
  
  missing = {'setor': 'Faltante', 'subsetor': 'Faltante', 'segmento': 'Faltante'}
  
  for index in range(len(shares)):
    ticker = shares.index[index]
    shares['Setor'][index] = categories.get(ticker[:4], missing)['setor']
    shares['Subsetor'][index] = categories.get(ticker[:4], missing)['subsetor']
    shares['Segmento'][index] = categories.get(ticker[:4], missing)['segmento']

  return shares

def backtest(year = None):
  urls = {
    2008: 'https://web.archive.org/web/20080613050801/http://www.fundamentus.com.br/resultado.php',
    2009: 'https://web.archive.org/web/20090123022224/http://www.fundamentus.com.br/resultado.php',
    2010: 'https://web.archive.org/web/20100115191626/http://www.fundamentus.com.br/resultado.php',
    2011: 'https://web.archive.org/web/20110113192117/http://www.fundamentus.com.br/resultado.php',
    2012: 'https://web.archive.org/web/20120106023830/http://www.fundamentus.com.br/resultado.php',
    2013: 'https://web.archive.org/web/20130105004012/http://www.fundamentus.com.br/resultado.php',
    2014: 'https://web.archive.org/web/20140108164618/http://www.fundamentus.com.br/resultado.php',
    2015: 'https://web.archive.org/web/20150119231047/http://www.fundamentus.com.br/resultado.php',
    2016: 'https://web.archive.org/web/20160106101916/http://www.fundamentus.com.br/resultado.php',
    2017: 'https://web.archive.org/web/20170505164235/http://www.fundamentus.com.br/resultado.php',
    2018: 'https://web.archive.org/web/20180105120409/http://www.fundamentus.com.br/resultado.php',
    2019: 'https://web.archive.org/web/20190102202956/http://www.fundamentus.com.br/resultado.php',
    2020: 'http://www.fundamentus.com.br/resultado.php'
  }
  return urls.get(year, 'http://www.fundamentus.com.br/resultado.php')

def dataframe_opts(year = None):
  opts = {'Cotação': [],
          'P/L': [],
          'P/VP': [],
          'PSR': [],
          'Dividend Yield': [],
          'P/Ativo': [],
          'P/Capital de Giro': [],
          'P/EBIT': [],
          'P/ACL': [],
          'EV/EBIT': [],
          'EV/EBITDA': [],
          'Margem Ebit': [],
          'Margem Líquida': [],
          'Liquidez Corrente': [],
          'ROIC': [],
          'ROE': [],
          'Liquidez 2 meses': [],
          'Patrimônio Líquido': [],
          'Dívida Bruta/Patrimônio': [],
          'Crescimento em 5 anos': []}
  if year != None and year < 2020: del opts['EV/EBITDA']
  
  return opts

def dataframe_data(rows, year = None):
  columns = ['Cotação', 'P/L', 'P/VP', 'PSR', 'Dividend Yield', 'P/Ativo','P/Capital de Giro', 'P/EBIT', 'P/ACL', 'EV/EBIT', 'EV/EBITDA', 'Margem Ebit', 'Margem Líquida', 'Liquidez Corrente', 'ROIC', 'ROE', 'Liquidez 2 meses', 'Patrimônio Líquido', 'Dívida Bruta/Patrimônio', 'Crescimento em 5 anos']
  if year != None and year < 2020: columns.remove('EV/EBITDA')
  
  return dict((val, todecimal(rows.getchildren()[index + 1].text)) for index, val in enumerate(columns))

def todecimal(string):
    string = string.replace('.', '')
    string = string.replace(',', '.')
  
    if (string.endswith('%')):
      string = string[:-1]
      return Decimal(string) / 100
    else:
      return Decimal(string)
