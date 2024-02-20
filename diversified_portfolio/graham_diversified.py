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

# Trials to diversify the portolio...
#
# shares.drop_duplicates(subset='Segmento')
# shares['Segmento'] == 'Energia Elétrica'
# shares['Segmento'].unique().tolist()
# shares.Segmento.drop_duplicates()

import sys, os
sys.path.extend([f'../{name}' for name in os.listdir("..") if os.path.isdir(f'../{name}')])
sys.path.extend(['..'])

import pyperclip

import graham
import fundamentus
import backtest
import time

# python3 graham_diversified.py "{ 'year': 2015 }"
if __name__ == '__main__':  
  year = graham.current_year()
  if len(sys.argv) > 1:
    year = int(eval(sys.argv[1])['year'])
  
  shares = graham.populate_shares(year)
  
  shares.sort_values(by=['Graham Score', 'Preço Justo (Graham) / Cotação'], ascending=[False, False], inplace=True)
  
  shares = shares.drop_duplicates(subset='Segmento')

  shares['Ranking (Graham)'] = range(1, len(shares) + 1)
  
  print(shares)
  pyperclip.copy(shares.to_markdown())
  
  if year != graham.current_year():
    backtest.run_all(fundamentus.start_date(year), list(shares.index[:20]))
