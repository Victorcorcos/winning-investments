# This file is intended to automate the back test and...
# * Get the plot graph of the backtest

python3

import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

import backtest

year = {
  2008: '2008-06-13', # https://web.archive.org/web/20080613050801/http://www.fundamentus.com.br/resultado.php 
  2009: '2009-01-23', # https://web.archive.org/web/20090123022224/http://www.fundamentus.com.br/resultado.php 
  2010: '2010-01-15', # https://web.archive.org/web/20100115191626/http://www.fundamentus.com.br/resultado.php 
  2011: '2011-01-13', # https://web.archive.org/web/20110113192117/http://www.fundamentus.com.br/resultado.php 
  2012: '2012-01-06', # https://web.archive.org/web/20120106023830/http://www.fundamentus.com.br/resultado.php 
  2013: '2013-01-05', # https://web.archive.org/web/20130105004012/http://www.fundamentus.com.br/resultado.php 
  2014: '2014-01-08', # https://web.archive.org/web/20140108164618/http://www.fundamentus.com.br/resultado.php 
  2015: '2015-01-19', # https://web.archive.org/web/20150119231047/http://www.fundamentus.com.br/resultado.php 
  2016: '2016-01-06', # https://web.archive.org/web/20160106101916/http://www.fundamentus.com.br/resultado.php 
  2017: '2017-05-05', # https://web.archive.org/web/20170505164235/http://www.fundamentus.com.br/resultado.php 
  2018: '2018-01-05', # https://web.archive.org/web/20180105120409/http://www.fundamentus.com.br/resultado.php 
  2019: '2019-01-02'  # https://web.archive.org/web/20190102202956/http://www.fundamentus.com.br/resultado.php
}

#####################
## Benjamin Graham ##
#####################
graham_2008 = ['ELET6', 'BRGE6', 'CPLE3', 'CPLE6', 'CSMG3', 'BRGE7', 'BRGE8', 'BRGE12', 'BRGE3', 'SAPR4']
backtest.run(start=year[2008], tickers=graham_2008, display=True)

graham_2009 = ['FESA4', 'CSMG3', 'USIM3', 'BRAP3', 'PEAB3', 'PEAB4', 'SAPR4', 'PATI4', 'CPLE3', 'CPLE6']
backtest.run(start=year[2009], tickers=graham_2009, display=True)

graham_2010 = ['CSMG3', 'EQTL3', 'CTSA4', 'CTSA3', 'SBSP3', 'BRGE3', 'BRGE6', 'BSLI3', 'BGIP3', 'BGIP4']
backtest.run(start=year[2010], tickers=graham_2010, display=True)

graham_2011 = ['BMEB4', 'BMEB3', 'BSLI3', 'WHRL3', 'WHRL4', 'ELET3', 'CTSA3', 'CTSA4', 'CSMG3', 'SBSP3']
backtest.run(start=year[2011], tickers=graham_2011, display=True)

graham_2012 = ['CPLE3', 'BBAS3', 'PETR4', 'RAPT3', 'VALE3', 'CMIG3', 'ECPR3', 'ECPR4', 'CTSA3', 'CTSA4']
backtest.run(start=year[2012], tickers=graham_2012, display=True)

graham_2013 = ['DOHL4', 'CTSA4', 'CESP3', 'CTSA3', 'BRSR3', 'BBAS3', 'CMIG3', 'BNBR3', 'CMIG4', 'VALE3']
backtest.run(start=year[2013], tickers=graham_2013, display=True)

graham_2014 = ['BBAS3', 'BNBR3', 'SOND6', 'SOND5', 'CTSA3', 'CTSA4', 'CMIG4', 'CMIG3', 'BRSR3', 'SAPR4']
backtest.run(start=year[2014], tickers=graham_2014, display=True)

graham_2015 = ['EZTC3', 'EVEN3', 'DOHL4', 'MRVE3', 'SAPR4', 'CMIG4', 'CMIG3', 'VIVT3', 'ETER3', 'BRSR3']
backtest.run(start=year[2015], tickers=graham_2015, display=True)

graham_2016 = ['ITSA4', 'ITSA3', 'ITUB3', 'CMIG4', 'CMIG3', 'BBAS3', 'CGRA4', 'CGRA3', 'EZTC3', 'TAEE11']
backtest.run(start=year[2016], tickers=graham_2016, display=True)

graham_2017 = ['TRPL3', 'TRPL4', 'BNBR3', 'BSLI4', 'CGRA3', 'CGRA4', 'BMIN4', 'SAPR3', 'BEES3', 'BEES4']
backtest.run(start=year[2017], tickers=graham_2017, display=True)

graham_2018 = ['BNBR3', 'TRPL3', 'TRPL4', 'ABCB4', 'BEES3', 'BEES4', 'CCPR3', 'SAPR4', 'FESA3', 'FESA4']
backtest.run(start=year[2018], tickers=graham_2018, display=True)

graham_2019 = ['FESA4', 'TRPL3', 'TRPL4', 'BNBR3', 'BPAR3', 'FESA3', 'MRVE3', 'VIVT3', 'BRSR3', 'NAFG3']
backtest.run(start=year[2019], tickers=graham_2019, display=True)


#################
## Décio Bazin ##
#################
bazin_2008 = ['CSAB3', 'CSAB4', 'SULT3', 'SULT4', 'TRPL3', 'TRPL4', 'VIVT3', 'VIVT4', 'GRND3', 'SANB4']
backtest.run(start=year[2008], tickers=bazin_2008, display=True)

bazin_2009 = ['GRND3', 'FESA4', 'LREN3', 'PATI4', 'POSI3', 'ETER3', 'SOND3', 'IGTA3', 'TKNO4', 'POMO3']
backtest.run(start=year[2009], tickers=bazin_2009, display=True)

bazin_2010 = ['CTSA4', 'JHSF3', 'PEAB4', 'PEAB3', 'WHRL4', 'WHRL3', 'CRIV4', 'CTSA3', 'BGIP4', 'EKTR4']
backtest.run(start=year[2010], tickers=bazin_2010, display=True)

bazin_2011 = ['WHRL3', 'WHRL4', 'ODPV3', 'SOND3', 'ELET3', 'BGIP4', 'PATI4', 'ETER3', 'CSAB3', 'CSAB4']
backtest.run(start=year[2011], tickers=bazin_2011, display=True)

bazin_2012 = ['PATI4', 'GRND3', 'MERC4', 'ETER3', 'CGRA3', 'CGRA4', 'BGIP4', 'BGIP3', 'NAFG4', 'BBAS3']
backtest.run(start=year[2012], tickers=bazin_2012, display=True)

bazin_2013 = ['PATI4', 'ETER3', 'BGIP3', 'BGIP4', 'BEES4', 'WHRL4', 'WHRL3', 'GRND3', 'CMIG3', 'BRIV4']
backtest.run(start=year[2013], tickers=bazin_2013, display=True)

bazin_2014 = ['BRIV4', 'PINE4', 'BBAS3', 'GUAR3', 'WHRL4', 'ELET3', 'WHRL3', 'ENGI4', 'ENGI3', 'CRIV4']
backtest.run(start=year[2014], tickers=bazin_2014, display=True)

bazin_2015 = ['CRIV4', 'PINE4', 'SAPR4', 'BBAS3', 'BEES4', 'BEES3', 'DOHL4', 'WHRL4', 'WHRL3', 'BMEB4']
backtest.run(start=year[2015], tickers=bazin_2015, display=True)

bazin_2016 = ['BBSE3', 'CRIV4', 'ITSA4', 'BRIV4', 'ITSA3', 'FESA4', 'BBAS3', 'CGRA4', 'CGRA3', 'EZTC3']
backtest.run(start=year[2016], tickers=bazin_2016, display=True)

bazin_2017 = ['CRIV4', 'BRIV4', 'ITSA4', 'FESA4', 'CGRA4', 'CGRA3', 'BMEB4', 'AFLT3', 'MERC4', 'LCAM3']
backtest.run(start=year[2017], tickers=bazin_2017, display=True)

bazin_2018 = ['CRIV4', 'BRIV4', 'HGTX3', 'CGRA4', 'CGRA3', 'CSAB4', 'CSAB3', 'BMEB4', 'AFLT3', 'TRIS3']
backtest.run(start=year[2018], tickers=bazin_2018, display=True)

bazin_2019 = ['CRIV4', 'BRIV4', 'ITSA4', 'ITSA3', 'ITUB3', 'BBSE3', 'BMEB4', 'PTNT4', 'TRIS3', 'GRND3']
backtest.run(start=year[2019], tickers=bazin_2019, display=True)


#####################
## Joel Greenblatt ##
##   ROE + ROIC    ##
#####################
greenblatt_2008 = ['CEBR5', 'CEBR6', 'CEBR3', 'CEEB3', 'ENGI4', 'ENGI3', 'FBMC4', 'TIET4', 'VIVT4', 'WHRL3']
backtest.run(start=year[2008], tickers=greenblatt_2008, display=True)

greenblatt_2009 = ['FESA4', 'CEBR6', 'CEBR3', 'CEBR5', 'GGBR4', 'MYPK3', 'FBMC4', 'RAPT3', 'RAPT4', 'LPSB3']
backtest.run(start=year[2009], tickers=greenblatt_2009, display=True)

greenblatt_2010 = ['TIET3', 'TIET4', 'ETER3', 'EKTR4', 'SCAR3', 'SOND5', 'SOND6', 'GRND3', 'CGAS3', 'WEGE3']
backtest.run(start=year[2010], tickers=greenblatt_2010, display=True)

greenblatt_2011 = ['COCE3', 'COCE5', 'CEEB5', 'WHRL3', 'CAMB4', 'CIEL3', 'TIET3', 'CGAS3', 'WHRL4', 'CEEB3']
backtest.run(start=year[2011], tickers=greenblatt_2011, display=True)

greenblatt_2012 = ['AELP3', 'FHER3', 'VALE5', 'VALE3', 'COCE3', 'COCE5', 'RAPT3', 'CSNA3', 'RAPT4', 'TAEE11']
backtest.run(start=year[2012], tickers=greenblatt_2012, display=True)

greenblatt_2013 = ['WHRL3', 'WHRL4', 'TIET3', 'TIET4', 'ETER3', 'CSRN5', 'COCE5', 'COCE3', 'CMIG3', 'TRPL4']
backtest.run(start=year[2013], tickers=greenblatt_2013, display=True)

greenblatt_2014 = ['SOND5', 'BAUH4', 'WHRL3', 'WHRL4', 'TIET3', 'TIET4', 'ETER3', 'CMIG4', 'CMIG3', 'PTBL3']
backtest.run(start=year[2014], tickers=greenblatt_2014, display=True)

greenblatt_2015 = ['OGXP3', 'WHRL3', 'WHRL4', 'VVAR3', 'TIET3', 'CMIG4', 'PSSA3', 'CMIG3', 'TIET4', 'PTBL3']
backtest.run(start=year[2015], tickers=greenblatt_2015, display=True)

greenblatt_2016 = ['AGRO3', 'PTBL3', 'CMIG4', 'CMIG3', 'SEER3', 'BRKM3', 'EQTL3', 'COCE5', 'PMAM3', 'VVAR3']
backtest.run(start=year[2016], tickers=greenblatt_2016, display=True)

greenblatt_2017 = ['TRPL3', 'TRPL4', 'MSPA4', 'CGAS3', 'CGAS5', 'BAUH4', 'BRKM3', 'BRKM5', 'BEEF3', 'SMLS3']
backtest.run(start=year[2017], tickers=greenblatt_2017, display=True)

greenblatt_2018 = ['IDNT3', 'BAUH4', 'UNIP6', 'UNIP5', 'UNIP3', 'WIZS3', 'PSSA3', 'CRPG6', 'FESA4', 'CRPG5']
backtest.run(start=year[2018], tickers=greenblatt_2018, display=True)

greenblatt_2019 = ['WIZS3', 'UNIP6', 'UNIP5', 'UNIP3', 'CRPG6', 'CRPG5', 'AGRO3', 'SMLS3', 'CIEL3', 'BAUH4']
backtest.run(start=year[2019], tickers=greenblatt_2019, display=True)


###################
#### Piotroski ####
###################
piotroski_2008 = ['BMIN4', 'BMIN3', 'BAZA3', 'SAPR4', 'CRIV4', 'CRIV3', 'ETER3', 'JBSS3', 'MERC4', 'ITSA4']
backtest.run(start=year[2008], tickers=piotroski_2008, display=True)

piotroski_2009 = ['BBRK3', 'LAME3', 'LAME4', 'MULT3', 'BBDC3', 'COCE3', 'BBDC4', 'COCE6', 'COCE5', 'ELET6']
backtest.run(start=year[2009], tickers=piotroski_2009, display=True)

piotroski_2010 = ['BAZA3', 'SPRI3', 'KLBN4', 'KLBN3', 'ELEK4', 'TGMA3', 'ELEK3', 'RANI3', 'RANI4', 'MYPK3']
backtest.run(start=year[2010], tickers=piotroski_2010, display=True)

piotroski_2011 = ['TCNO4', 'TCNO3', 'FHER3', 'CESP3', 'EKTR4', 'CESP5', 'SMTO3', 'EKTR3', 'CESP6', 'CEDO4']
backtest.run(start=year[2011], tickers=piotroski_2011, display=True)

piotroski_2012 = ['MTSA4', 'TOTS3', 'KEPL3', 'UNIP6', 'UNIP3', 'UNIP5', 'DTCY3', 'CBEE3', 'CTSA3', 'CTSA4']
backtest.run(start=year[2012], tickers=piotroski_2012, display=True)

piotroski_2013 = ['SHUL4', 'VVAR3', 'CLSC4', 'CLSC3', 'BRFS3', 'MNDL3', 'TXRX3', 'TRIS3', 'WHRL3', 'WHRL4']
backtest.run(start=year[2013], tickers=piotroski_2013, display=True)

piotroski_2014 = ['CESP3', 'CESP6', 'CESP5', 'MULT3', 'PTNT4', 'CARD3', 'JBSS3', 'NAFG4', 'HYPE3', 'CEPE5']
backtest.run(start=year[2014], tickers=piotroski_2014, display=True)

piotroski_2015 = ['CARD3', 'BMIN4', 'ENEV3', 'GFSA3', 'SHOW3', 'ENGI3', 'BRGE11', 'ENGI4', 'BRGE3', 'BRGE8']
backtest.run(start=year[2015], tickers=piotroski_2015, display=True)

piotroski_2016 = ['VULC3', 'FRIO3', 'CARD3', 'SEER3', 'ALUP11', 'MDIA3', 'MGEL4', 'LOGN3', 'SAPR4', 'SAPR3']
backtest.run(start=year[2016], tickers=piotroski_2016, display=True)

piotroski_2017 = ['VULC3', 'MTSA4', 'NAFG4', 'ENEV3', 'ANIM3', 'NAFG3', 'TEND3', 'YDUQ3', 'SLCE3', 'IGTA3']
backtest.run(start=year[2017], tickers=piotroski_2017, display=True)

piotroski_2018 = ['CESP3', 'WIZS3', 'LAME3', 'CESP6', 'CPRE3', 'CRFB3', 'LAME4', 'VLID3', 'TUPY3', 'TEND3']
backtest.run(start=year[2018], tickers=piotroski_2018, display=True)

piotroski_2019 = ['BEEF3', 'EVEN3', 'RAPT3', 'RAPT4', 'KEPL3', 'WEGE3', 'BAZA3', 'CPLE3', 'CPLE6', 'CSMG3']
backtest.run(start=year[2019], tickers=piotroski_2019, display=True)