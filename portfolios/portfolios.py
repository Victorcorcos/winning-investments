# Add your portfolio here

# import sys, os
# sys.path.extend([f'../{name}' for name in os.listdir("..") if os.path.isdir(f'../{name}')])

import operator

# Filter the shares based on your portfolio name
def filter(shares, name):
  return shares[shares.index.isin(get(name))]

# Calls the right portfolio method based on it's name.
# For e.g. if name = 'victor', it calls the victor() method
def get(name):
  return eval(name)()

# Define methods here with the names of your portfolios
def victor():
  carteira = {
    'etfs': ['SMAL11'],
    'fiis': ['KNRI11', 'XPLG11', 'HGBS11', 'IRDM11'],
    'stocks': ['BRSR3', 'CGRA3', 'BBDC3', 'VVAR3', 'CARD3', 'PETR4', 'TRPL4', 'BBAS3', 'SAPR4', 'POMO3', 'QUAL3', 'WIZS3', 'BRSR6', 'BBSE3', 'CRIV4']
  }
  
  return carteira['stocks']
