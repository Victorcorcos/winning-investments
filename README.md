<p align="center">
  <img src="https://i.imgur.com/D7YneT5.png" alt="Winning Investments Logo" width="40%" />
</p>

Winning Investments é um Sistema em Python que aplica as estratégias e técnicas empregadas pelos mais renomados investidores do mundo aqui no mercado de ações brasileiro, visando um rigoroso processo de análise fundamentalista comparativa. 🥋

Ao eleger uma estratégia, o sistema desencadeia um processo de ranqueamento, revelando as jóias do mercado até as oportunidades menos promissoras, sempre alinhado com a estratégia selecionada do investidor desejado.

Os dados essenciais são minuciosamente capturados através de diversas APIs disponíveis gratuitamente na vasta rede da internet.

Neste momento, é possível aplicar as estratégias dos seguintes mestres da arte financeira:

1. **Benjamin Graham**
2. **Joel Greenblatt**
3. **Décio Bazin**
4. **Joseph D. Piotroski**
5. **Kenneth Fisher**

Além de outras estratégias bastante interessantes, como encontrar as Dividend Aristocrats aqui no Mercado Brasileiro, que era uma estratégia adotada somente no Mercado de Ações Americano.

É importante ressaltar que também foi empreendida uma extensa busca na literatura especializada, com o propósito de identificar e incorporar as estratégias de investimento mais promissoras e eficazes. Este projeto, de minha autoria, promete desvendar jóias do mercado brasileiro e auxiliar na tomada de decisões estratégicas do investidor, já que agora suas decisões terão o alicerce nas decisões dos maiores investidores do mundo  🙌


# Pré-requisitos 🎓

* Python 3
* Libs (`pip3 install them`)
  * pandas
  * lxml
  * yfinance
  * pyfolio
  * click
  * tabulate
  * matplotlib
  * pyperclip


# Como usar 🎯

Basta rodar um destes comandos, dependendo da estratégia que deseja-se aplicar.

Ao final de cada comando, é mostrado no terminal a tabela resultante e salvo no Ctrl+C.
Para melhor visualizar o resultado, basta colar via Ctrl+V em algum editor de Markdown, como o site https://dillinger.io/

```rb
python3 graham.py
```

```rb
python3 greenblatt.py # Aplica tanto ROE e P/L quanto ROIC e EV/EBIT
python3 greenblatt.py "{ 'formula': 'ROE' }" # Aplica ROE e P/L
python3 greenblatt.py "{ 'formula': 'ROIC' }" # Aplica ROIC e EV/EBIT
```

```rb
python3 bazin.py
```

```rb
python3 piotroski.py
```

```rb
python3 fisher.py
```


# Estratégias 📚

## Benjamin Graham 📈

* Arquivo: <kbd><code>**graham.py**</code></kbd>

Aplica-se ensinamentos de [Benjamin Graham](https://www.investopedia.com/articles/07/ben_graham.asp) em todas as ações do mercado de ações brasileiro, que é o Mercado de Ações brasileiro, produzindo um ranking com base na análise fundamentalista dos dados de todas as empresas.

Para a análise, são utilizados ensinamentos do livro "*O Investidor Inteligente*" de **Benjamin Graham**.

Também é calculado o **Valor Intrínseco (Preço Justo)** definido por Benjamin Graham para cada ação.

Benjamin Graham foi o mentor dos melhores investidores do mundo, como o grandíssimo Warren Buffet, além do Irving Kahn e Walter Schloss.

No algoritmo, cada ação recebe uma nota que vai de 0 a 14, considerando se ela se adequou a cada uma dessas características abaixo estipuladas por Benjamin Graham.

- [x] 1.  Sobrevivência: Sobreviveu nos últimos 10 anos. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
- [x] 2.  Estabilidade ds Lucros: Lucro > 0 nos últimos 10 anos. https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
- [x] 3.  Crescimento dos Lucros: Lucros crescentes nos últimos 10 anos https://www.estrategista.net/o-fracasso-de-benjamin-graham-na-bolsa-atual/
- [x] 4.  Crescimento dos Lucro Por Ação: LPA atual > 1.33 * LPA 10 anos atrás. (Calculado através da média dos 3 anos do começo e dos 3 anos do fim deste período) http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
- [x] 5.  Estabilidade dos Dividendos: Dividendos pagos nos últimos 10 anos. http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
- [x] 6.  Preço Justo > 1.5 * Preço de Mercado. Neste caso, Preço Justo é a raíz_quadrada_de(22.5 * VPA * LPA) (Criado por Benjamin Graham) https://www.sunoresearch.com.br/artigos/valor-intrinseco/?utm_source=PR&utm_medium=artigo&utm_campaign=investing_05122019
- [x] 7.  P/L (Preço/Lucro) => Quanto menor, melhor (ideal, < 15 E >= 0) http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
- [x] 8.  P/VP (Preço/Valor Patrimonial) => Quanto menor, melhor (ideal, < 1.5 E >= 0) http://seuguiadeinvestimentos.com.br/a-tecnica-de-investimento-de-benjamin-graham-ii/
- [x] 9.  Crescimento em 5 anos => Quanto maior, melhor (ideal, > 5%) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
- [x] 10. ROE (Return On Equity) => Quanto maior, melhor (ideal, superior a 20%) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
- [x] 11. Dividend Yield (Rendimento de Dividendo) => Quanto maior, melhor (ideal, > Taxa Selic (4.5%)) https://foconomilhao.com/acoes-com-dividend-yield-maior-que-a-selic/
- [x] 12. Liquidez Corrente => Quanto maior, melhor (ideal > 1.5) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
- [x] 13. Dívida Bruta/Patrimônio => Quanto menor, melhor (ideal < 50%) https://daxinvestimentos.com/analise-fundamentalista-mais-de-200-de-rentabilidade-em-2-anos/
- [x] 14. Patrimônio Líquido => Quanto maior, melhor (ideal > 2000000000)


#### Backtests 🧐

##### 1. Literature

[<img src="https://i.imgur.com/kE1DLOp.png" width="500"/>](GrahamBacktest)

##### 2. 2009 to 2020

[<img src="https://i.imgur.com/z8Migg0.png" width="500"/>](GrahamBacktest)


#### Links 🌐

* https://www.amazon.com/Intelligent-Investor-Definitive-Investing-Essentials/dp/0060555661
* https://www.bluechipinvest.com.br/educacional-det/benjamin-graham/7

#### Artigos Científicos 🔬

1. http://dspace.insper.edu.br/xmlui/bitstream/handle/11224/2244/Rafael%20Domingues%20dos%20Santos_Trabalho.pdf?sequence=1


## Joel Greenblatt 📈

* Arquivo: <kbd><code>**greenblatt.py**</code></kbd>

Aplica-se ensinamentos de [Joel Greenblatt](https://maisretorno.com/blog/termos/j/joel-greenblatt) em todas as ações do mercado de ações brasileiro, depois rankeia das ações que mais se adequaram para as que menos se adequaram.

Para a análise, são utilizados ensinamentos do livro "*The little book that beats the Market*" de **Joel Greenblatt**

Em sua fórmula mágica, Greenblatt utiliza os seguintes indicadores: **ROE** (*indicador de Qualidade*) e o **P/L** (*indicador de Preço*).
Através desses 2 indicadores ele monta dois rankings, um com as empresas de maior **ROE** (mais rentáveis) e outro com as ações de menor **P/L** (maior custo-benefício).
Feito os 2 rankings, é somado a posição de cada ação nos rankings.
As empresas de menor soma são aquelas escolhidas para montar a carteira pois seriam as ações mais baratas e mais rentáveis ao mesmo tempo.

Uma outra abordagem dessa fórmula é utilizar os indicadores: **ROIC** (*indicador de Qualidade*) **EV/EBIT** (*indicador de Preço*).
É seguido então a mesma estratégia de usar **ROE**+**P/L**, mas substituindo **ROE** por **ROIC** e **P/L** por **EV/EBIT**.

- [x] 1. maior ROE e menor P/L
- [x] 2. maior ROIC e menor EV/EBIT

#### Backtests 🧐

##### 1. Literature

[<img src="https://i.imgur.com/YqMCGwi.png" width="500"/>](GreenblattBacktest)

##### 2. 2009 to 2020

[<img src="https://i.imgur.com/zzwikwW.png" width="500"/>](GreenblattBacktest)

#### Links 🌐

* https://www.amazon.com/Little-Book-That-Beats-Market/dp/0471733067
* https://comoinvestir.thecap.com.br/joel-greenblatt-estrategia-investimentos/

#### Artigos Científicos 🔬

1. http://bibliotecadigital.fgv.br/dspace/bitstream/handle/10438/15280/Tese%20-%20Leonardo%20Milane%20-%20Magic%20Formula.pdf?sequence=1
2. http://bibliotecadigital.fgv.br/dspace/bitstream/handle/10438/12099/Disserta%C3%A7%C3%A3o_RodolfoZeidler_MPFE_27.09.2014.pdf?sequence=1&isAllowed=y
3. http://dspace.insper.edu.br/xmlui/bitstream/handle/11224/2244/Rafael%20Domingues%20dos%20Santos_Trabalho.pdf?sequence=1


## Décio Bazin 📈

* Arquivo: <kbd><code>**bazin.py**</code></kbd>

Aplica-se ensinamentos de [Décio Bazin](https://www.sunoresearch.com.br/artigos/entenda-estrategia-de-decio-bazin/) em todas as ações do mercado de ações brasileiro, depois rankeia das ações que mais se adequaram para as que menos se adequaram.

Para a análise, são utilizados ensinamentos do livro "*Faça Fortuna Com Ações*" de **Décio Bazin**, que é tido como literatura indicada até mesmo por **Luis Barsi**, o maior investidor na bolsa brasileira de todos os tempos.

Também é calculado o **Valor Intrínseco (Preço Justo)** definido por Décio Bazin para cada ação.

No algoritmo, cada ação recebe uma nota que vai de 0 a 8, considerando se ela se adequou a cada uma dessas características abaixo estipuladas por Décio Bazin.

- [x] 1. Preço Justo (Bazin) > 1.5 * Preço. Preço Justo (Bazin) é o Dividend Yield Médio * 16.67 (Por: Décio Bazin)
- [x] 2. Dívida Bruta/Patrimônio < 0.5 (50%)
- [x] 3. Dividend Yield > 0.06 (6%)
- [x] 4. Média do Dividend Yield nos últimos 5 anos > 0.05 (5%)
- [x] 5. Mediana do Dividend Yield nos últimos 5 anos > 0.05 (5%)
- [x] 6. Pagamento constante de dividendos nos últimos 5 anos
- [x] 7. Pagamento crescente de dividendos nos últimos 5 anos
- [x] 8. 0 < Payout < 1

#### Backtests 🧐

##### 1. Literature

[<img src="https://i.imgur.com/qdkmnG4.png" width="500"/>](BazinBacktest)
[<img src="https://i.imgur.com/duKM0mN.png" width="500"/>](BazinBacktest)


##### 2. 2009 to 2020

[<img src="https://i.imgur.com/ImIuH86.png" width="500"/>](BazinBacktest)

#### Links 🌐

* https://www.amazon.com/Faca-Fortuna-com-Acoes-Antes/dp/8585454164
* https://www.sunoresearch.com.br/artigos/entenda-estrategia-de-decio-bazin/
* https://clubedovalor.com.br/blog/decio-bazin/
* https://medium.com/@lucastrcalixto/o-m%C3%A9todo-bazin-e-o-progresso-da-bolsa-ccd7ec7a144b

#### Artigos Científicos 🔬

1. Se alguém achar algum artigo de backtest, eu agradeço. No mais, essa estratégia se mostrou uma estratégia extremamente eficiente através dos backtests que eu fiz neste programa.


## Joseph D. Piotroski 📈

* Arquivo: <kbd><code>**piotroski.py**</code></kbd>

Aplica-se ensinamentos de [Joseph D. Piotroski](https://meetinvest.com/stockscreener/joseph-piotroski/) em todas as ações do mercado de ações brasileiro, depois rankeia das ações que mais se adequaram para as que menos se adequaram.

Para a análise, são utilizados ensinamentos do paper "*Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers*" de **Joseph D. Piotroski**.

No algoritmo, cada ação recebe uma nota que vai de 0 a 9, considerando se ela se adequou a cada uma dessas características abaixo estipuladas por Piotroski.

- [x] 1. ROA > 0 (Returno sobre o Ativo) https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 2. FCO > 0 (Fluxo de Caixa Operacional) https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 3. FCO > Lucro Líquido https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 4. ROA atual > ROA ano anterior https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 5. Alavancagem atual < Alavancagem ano anterior. Medida por: Dívida Líquida / Patrimônio Líquido https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 6. Liquidez Corrente atual > Liquidez Corrente ano anterior https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 7. Nro. Ações atual = Nro. Ações ano anterior https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 8. Margem Bruta atual > Margem Bruta ano anterior https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
- [x] 9. Giro Ativo atual > Giro Ativo ano anterior https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a

#### Backtests 🧐

##### 1. Literature

[<img src="https://i.imgur.com/dIiK0Va.png" width="500"/>](PiotroskiBacktest)

##### 2. 2009 to 2020

[<img src="https://i.imgur.com/TaPNJbh.png" width="500"/>](PiotroskiBacktest)

#### Links 🌐

* https://www.ivey.uwo.ca/cmsmedia/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf
* https://medium.com/@gutenbergn/piotroski-d9a722b8ef9a
* https://www.equitieslab.com/piotroski-f-score-faq/
* https://areademembros.dicadehoje7.com/wp-content/uploads/2019/09/F-Score-de-Piotroski-1.pdf

#### Artigos Científicos 🔬

1. http://dspace.insper.edu.br/xmlui/bitstream/handle/11224/1724/Felippe%20Naccarato%20Baldo_Trabalho.pdf?sequence=1
2. https://www.quant-investing.com/blogs/backtests/2018/11/06/piotroski-f-score-back-test


## Kenneth Fisher 📈

#### Está ainda em fase de desenvolvimento. 🚧

* Arquivo: <kbd><code>**fisher.py**</code></kbd>

Aplica-se ensinamentos de [Kenneth Fisher](https://www.sunoresearch.com.br/tudo-sobre/kenneth-fisher/) em todas as ações do mercado de ações brasileiro, depois rankeia das ações que mais se adequaram para as que menos se adequaram.

Kenneth Fisher é o filho de Philip Fisher, têm uma fortuna atual de 4 bilhões de dólares e é dono de um fundo de investimento (Fisher Investments). Com base nas suas ações públicas, estimate-se que o desempenho de Ken Fisher tenha superado o mercado de ações dos EUA em uma média de 4,2 potos percentuais por ano.

No algoritmo, cada ação recebe uma nota que vai de 0 a 4, considerando se ela se adequou a cada uma dessas características abaixo estipuladas por Kenneth Fisher.

- [x] 1. PSR < 3 https://www.fundamentus.com.br/pagina_do_ser/kenneth_Fisher.htm
- [x] 2. PSR < 1 https://www.fundamentus.com.br/pagina_do_ser/kenneth_Fisher.htm
- [x] 3. PSR < 0.75 https://www.fundamentus.com.br/pagina_do_ser/kenneth_Fisher.htm
- [x] 4. Taxa de Rentabilidade alta: L/P > Selic http://investidoremvalor.com/filosofia-ken-fisher/

#### Links 🌐

* https://comoinvestir.thecap.com.br/quem-e-kenneth-fisher-o-jeito-ken-investir/
* http://investidoremvalor.com/filosofia-ken-fisher/

#### Artigos Científicos 🔬

1. Se alguém achar algum artigo de backtest, eu agradeço.


## Score 📈

* Arquivo: <kbd><code>**score.py**</code></kbd>

Para compor esse Score, é aplicado um mix de estratégias.

Além dos pontos defendidos por Benjamin Graham (Veja os 14 pontos da seção de Benjamin Graham), é também avaliado o **ROIC**, **Margem Líquida**, **Endividamento**, **PSR**, **EV/EBITDA** e **Peg Ratio**. Aplicando, assim, ensinamentos também de **Kenneth Fisher** por exemplo e de outros grandes investidores.

No algoritmo, cada ação recebe uma nota que vai de 0 a 21, avaliando se cada uma se adequou às características mostradas por **Benjamin Graham**. Também é avaliado 7 características adicionais, mostradas abaixo...

- [x] 1. ROIC (Return on Invested Capital) => Quanto maior, melhor (ideal, > 10%) https://www.sunoresearch.com.br/artigos/o-investidor-inteligente-entenda-a-obra-de-benjamin-graham/
- [x] 2. PSR (Price Sales Ratio) => Quanto menor, melhor (ideal, < 0.75) https://www.moneyshow.com/articles/tptp072513-46306/
- [x] 3. Margem Líquida => Quanto maior melhor (ideal, > 10%) https://www.youtube.com/watch?v=7tB_ym4Cabc E https://www.sunoresearch.com.br/artigos/5-indicadores-para-avaliar-solidez-de-uma-empresa/
- [x] 4. Dívida Líquida/EBIT => Quanto menor melhor (ideal, <= 3) https://www.sunoresearch.com.br/artigos/5-indicadores-para-avaliar-solidez-de-uma-empresa/
- [x] 5. Dívida Líquida/Patrimônio => Quanto menor, melhor (ideal < 50%) https://www.sunoresearch.com.br/artigos/5-indicadores-para-avaliar-solidez-de-uma-empresa/
- [x] 6. EV/EBITDA (Enterprise Value / EBITDA) => Quanto menor melhor (ideal, < 10) https://www.investopedia.com/ask/answers/072715/what-considered-healthy-evebitda.asp
- [x] 7. Peg Ratio (P/L / CAGRLucros5Anos) => Quanto menor melhor (ideal <= 1) https://bugg.com.br/2018/01/24/buggpedia-o-que-e-o-peg-ratio/


## Repository Organization Structure 📂

The project is organized into several key directories and files:

```
├── diversified_portfolio/       # Combined strategy implementations
│   ├── bazin_diversified.py     # Diversified Bazin strategy
│   ├── graham_diversified.py    # Diversified Graham strategy
│   └── ...                      # Other diversified strategies

├── mixed_strategies/            # Hybrid investment approaches
│   ├── all.py                   # All strategies combined
│   ├── graham_bazin.py          # Graham+Bazin hybrid strategy
│   └── ...                      # Other strategy combinations

├── strategies/                  # Backtest results and research
│   ├── benjamin_graham/         # Graham strategy materials
│   ├── decio_bazin/             # Bazin strategy materials
│   └── ...                      # Other strategists' materials

├── stocks/                      # Stock data handling
│   ├── backtest.py              # Backtesting functionality
│   ├── fundamentus.py           # Fundamental data scraping
│   └── ...                      # Other stock utilities

├── utils/                       # Helper utilities
│   ├── browser.py               # Browser interaction
│   └── waitingbar.py            # Progress indicators

├── server/                      # Web interface
│   └── server.py                # Flask web server

├── *.py                         # Main strategy implementations
│   (graham.py, bazin.py, etc)

└── README.md                    # Project documentation
```

## Contact

* [Victor Cordeiro Costa](https://www.linkedin.com/in/victorcorcos/)

---

*This repository is maintained and developed by [Victor Cordeiro Costa](https://www.linkedin.com/in/victor-costa-0bba7197/). For inquiries, partnerships, or support, don't hesitate to get in touch.
