import bs4 as bs
import pickle
import requests
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import os
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
#import matplotlib.style
style.use('ggplot')
a = 250 # "Tickers number starting from"
b = 400 # Tickers end at

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
#    print (tickers)
    
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers, f)
        
#    print (tickers)
    
    return tickers

save_sp500_tickers()

def get_data_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists("stock_csv"):
        os.makedirs("stock_csv")
        
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2017,4,1)
    
    for ticker in tickers[a:b]: 
       "This will get only first 100 ticker values but can be changed as required"
    
       print (ticker)
       if ticker in ["BRK.B","BF.B"] :
          print ("Access Denied by Yahoo")
          continue
       else:
          if not os.path.exists("stock_csv/{}.csv".format(ticker)):
             df = web.DataReader(ticker, 'yahoo', start, end)
             df.to_csv("stock_csv/{}.csv".format(ticker))       
          else:
             print ("Already Exists :{}".format(ticker))
          

get_data_yahoo()

def compile_data():
    with open("sp500tickers.pickle", 'rb') as f:
        tickers = pickle.load(f)
        
        main_df = pd.DataFrame()

        
        for ticker in tickers[a:b]:
            if ticker in ["BRK.B","BF.B"]:
                continue
            
            else:
                if not os.path.exists("stock_csv/{}.csv".format(ticker)):
                    print("File does not exist",ticker)
                    continue
                else:
                
                    df = pd.read_csv("stock_csv/{}.csv".format(ticker))
                    df.set_index('Date', inplace = True)
                
                    df.drop(['Open','Close','High','Low','Volume'], 1, inplace=True)
                    df.rename(columns = {'Adj Close': ticker}, inplace=True)
                    
                    if main_df.empty:
                        main_df = df
                    else:
                        main_df = main_df.join(df, how = 'outer')
                        
                    print (main_df.head())
                
            
        main_df.to_csv("TickerData_{}_{}.csv".format(a,b))
        
compile_data()

def visualize():
    
    df = pd.read_csv("TickerData_{}_{}.csv".format(a,b))
#    df["AAPL"].plot()
    dfselc = df
#    print (dfselc)
    df_corr = dfselc.corr()
#    print (df_corr.head())
    

#    if not os.path.exists("df_corr"):
#        os.mkdir("df_corr")
#    
#    df_corr.to_csv("df_corr/df_corr.csv")
    
    
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor = False)
    ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor = False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    
#    column_label = df_corr.columns
#    row_label = df_corr.index
    ax.set_xticklabels(df_corr.columns)
    ax.set_yticklabels(df_corr.index)
    
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    
    plt.tight_layout()
    plt.show()
    
visualize()

    
    
    
    
    
    
    

    
    
    
    
    


    




           
        
         
    
    
    
            
    




    
