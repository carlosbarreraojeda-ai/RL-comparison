
import datetime as dt 
#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import util as ut  


def bb_value(symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),):
    syms = [symbol]  		  	   		  	  			  		 			     			  	 
    date = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = ut.get_data(syms, date)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
    price = prices_all[symbol]
    sma = price.copy()
    upBB = price.copy()
    lowerBB = price.copy()
    N = 20
    for i in range(N, len(price)+1):
        priceStd = price.iloc[i-N:i].std()
        sma.iloc[i-1] = price.iloc[i-N:i].mean()
        upBB.iloc[i-1] = sma.iloc[i-1] + priceStd * 2
        lowerBB.iloc[i-1] = sma.iloc[i-1] - priceStd * 2
    
    sma.iloc[0:N] = sma.iloc[N-1]
    upBB.iloc[0:N] = upBB.iloc[N-1]
    lowerBB.iloc[0:N] = lowerBB.iloc[N-1]
    
    
    
    return (price - lowerBB)/(upBB-lowerBB)

    
def momentum(symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),):
    syms = [symbol]  		  	   		  	  			  		 			     			  	 
    date = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = ut.get_data(syms, date)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
    price = prices_all[symbol]
    momentum = price.copy()
    N = 9
    for i in range(N,len(price)):
        momentum.iloc[i] = (price.iloc[i]/price.iloc[i-N]) - 1
    momentum.iloc[0:N] = momentum.iloc[N]
    
    #dfPortValue = pd.DataFrame(momentum)
    #dfPortValue.to_csv('momentum.csv')
    
    return momentum
    
    
def SMA(N = 25,
        symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),):
    
    syms = [symbol]  		  	   		  	  			  		 			     			  	 
    date = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = ut.get_data(syms, date)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
    price = prices_all[symbol]
    sma = price.copy()
    price_sma = price.copy()
    
    for i in range(N,len(price)):
       sma.iloc[i] = price.iloc[i-N:i+1].mean() 
       
    #dfPortValue = pd.DataFrame(price / sma)
    #dfPortValue.to_csv('SMA.csv')
       
    return price / sma

    
def stochasticOscillator(
        symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),):
    #Add subplot of price
    syms = [symbol]  		  	   		  	  			  		 			     			  	 
    date = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = ut.get_data(syms, date,colname="Close")
    highPrices_all = ut.get_data(syms, date,colname="High")	
    lowPrices_all = ut.get_data(syms, date,colname="Low") 	   		  	  			  		 			     			  	 
    price = prices_all[symbol]
    
    highPrice = highPrices_all[symbol]
    lowPrice = lowPrices_all[symbol]

    
    N = 18
    K = price.copy()
    D = price.copy()
    for i in range(N,len(price)+1):
        current = price.iloc[i-1]
        low = lowPrice.iloc[i-N:i].min()
        high = highPrice.iloc[i-N:i].max()
        K.iloc[i-1] = (current - low)/(high-low) * 100   
        
    K.iloc[0:N] = K.iloc[N-1]
    
    for i in range(3,len(price)+1):
        D.iloc[i-1] = K.iloc[i-3:i].mean()
        
    #return pd.concat([K,D])
    return K
        
    
def EMA(N=10, signal=None,symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),):
    if signal is None:
        syms = [symbol]  		  	   		  	  			  		 			     			  	 
        date = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
        prices_all = ut.get_data(syms, date)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
        price = prices_all[symbol]
    else:
        price = signal
    ema = price.copy()
    ema.iloc[N-1] = price.iloc[0:N].mean() # initial ema aka seed ema == sma
    multi = 2/(N+1) # weighting multiplier
    for i in range(N,len(price)):
        ema.iloc[i] = (price.iloc[i] - ema.iloc[i-1]) * multi + ema.iloc[i-1]
    ema.iloc[0:N-1] = ema.iloc[N-1]
    return ema

    
    
def MACD(symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),):
    
    ema_short = EMA(18,None,symbol,sd,ed)
    ema_long = EMA(30,None,symbol,sd,ed)
    macdLine = ema_short - ema_long
    signalLine = EMA(9,macdLine,symbol,sd,ed)
    macdHist = macdLine-signalLine
    
    return macdLine
    
