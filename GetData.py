import requests
import pandas as pd

class Ticker:
    
    def __init__(self, horas_min, currencia, lenDF):
        
        self.horas_min = horas_min
        self.currencia = currencia
        self.lenDF = lenDF
        
        #return self.horas_min , self.currencia, self.lenDF
                
    def GetData(self):

        x_Hour = 0
        
        dates_MainTF_Temp = []
        open_data_MainTF_Temp = []
        high_data_MainTF_Temp = []
        low_data_MainTF_Temp = []
        close_data_MainTF_Temp = []
        
        candles_cor = []
        rsi_data_MainTF = []
        
        try:
            
            MainTF_Temp_Req = requests.get('https://api.twelvedata.com/time_series?symbol='+self.currencia+'&interval='+self.horas_min+'&apikey=6887f0edb3a04235a1b6943a8a1b9e38')
            MainTF_Temp = MainTF_Temp_Req.json()
                
            for EachCandle_MainTF_Temp in MainTF_Temp["values"]:
                dates_MainTF_Temp.append(MainTF_Temp["values"][x_Hour]['datetime'])
                open_data_MainTF_Temp.append(MainTF_Temp["values"][x_Hour]['open'])
                high_data_MainTF_Temp.append(MainTF_Temp["values"][x_Hour]['high'])
                low_data_MainTF_Temp.append(MainTF_Temp["values"][x_Hour]['low'])
                close_data_MainTF_Temp.append(MainTF_Temp["values"][x_Hour]['close'])
                #rsi_data_MainTF.append("---")
                
                if MainTF_Temp["values"][x_Hour]['open'] < MainTF_Temp["values"][x_Hour]['close']: #vela verde
                    candles_cor.append("Green")
                else:
                    candles_cor.append("Red")
                
                x_Hour = x_Hour + 1
            x_Hour = 0
        except:
            print("erro ao recolher dados")
            pass
        
        pd.set_option('display.max_rows',self.lenDF)
        MainTF_Temp = {'time': dates_MainTF_Temp, 'open': open_data_MainTF_Temp,  'high': high_data_MainTF_Temp, 'low': low_data_MainTF_Temp, 'close': close_data_MainTF_Temp, 'color': candles_cor} #, 'RSI': rsi_data_MainTF}
        MainTF_Temp_pd = pd.DataFrame(MainTF_Temp)
        MainTF_Temp_pd = MainTF_Temp_pd.iloc[0:self.lenDF]
        MainTF_Temp_pd=MainTF_Temp_pd.reset_index(drop=True)
        
        #MAIN DATA FRAME 
        MainTF =  MainTF_Temp_pd  ##### MainTF =  MainTF_Temp_pd.head(24)
        MainTF['open'] = MainTF['open'].astype(float)
        MainTF['high'] = MainTF['high'].astype(float)
        MainTF['low'] = MainTF['low'].astype(float)
        MainTF['close'] = MainTF['close'].astype(float)
        
        self.MainTF = MainTF
        self.ColOpen = MainTF['open']
        self.ColHigh = MainTF['high']
        self.ColLow = MainTF['low']
        self.ColClose = MainTF['close']
        self.ColColor = MainTF["color"]
        
        #return MainTF
        