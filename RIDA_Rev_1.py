
import requests
import json
import numpy as np
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta, time
import time
import smtplib # INSTALAR ESTA NOVA LIVRARIA / 22/05/2021
from GetData import Ticker


HammerStar_Found = False
ShootingStar_Found = False

BearishEng_Found = False
BullishEng_Found = False

ResSup_Found = True
Res1_val = 0
Sup1_val = 0

Res2_val = 0
Sup2_val = 0


def GetData(horas_min,currencia,ATR_Length,ResSup_Found):
    
    global HammerStar_Found
    global ShootingStar_Found
    global BearishEng_Found
    global BullishEng_Found
    global MainTF

   # global ResSup_Found 
    global Res1_val 
    global Sup1_val
    
    global  Res2_val 
    global  Sup2_val 
     
    
    BE_i  = False 
    BE_ii  = False 
    BE_iii = False 
    
    BU_i  = False 
    BU_ii  = False 
    BU_iii = False 

    Body_SS = 0 
    Wick_SS = 0
    
    Body_HS = 0 
    Wick_HS = 0
    
    ########################################################3
    
    # Define o Stock e o time Frame atraves da class Ticker()
    Stock = Ticker(horas_min,currencia,ATR_Length)
    Stock.GetData()
    MainTF = Stock.MainTF
    
     ###############################################################
     
    # Procura suporte e resistencia no primeiro grafico
    
    if ResSup_Found == True:
        print("\n")
        
        PontoPivot = ( MainTF['high'][1] + MainTF['low'][1] + MainTF['close'][1] ) / 3
            
        Res1_val = (2 * PontoPivot) -  MainTF['low'][1]
        Sup1_val = (2 * PontoPivot) -  MainTF['high'][1]
        
        Res2_val = PontoPivot + (Res1_val - Sup1_val)
        Sup2_val = PontoPivot - (Res1_val - Sup1_val)
        
        print("\nPonto Pivot, Resistencias e Suporte em TimeFrame: ",ATR_Length,"\n\nPonto Pivot: ",PontoPivot,"\n\nResistencia 1_val: ",Res1_val,"\nSuporte 1_val: ",Sup1_val,"\n\nResistencia 2_val: ",Res2_val,"\nSuporte 2_val: ",Sup2_val)
        
        
    else:
        pass
        
    '''
    Ponto Pivot = (máxima anterior + mínima anterior + fechamento anterior) / 3
    Resistência 1 = (2 * Ponto Pivot) - mínima anterior
    Suporte 1 = (2 * Ponto Pivot) - maxima anterior
    
    Segundo suporte e resistência:
    
    Resistência 2 = Ponto Pivot + (Resistência 1 - Suporte 1)
    Suporte 2 = Ponto Pivot - (Resistência 1 - Suporte 1)
    
    '''
     ###############################################################
    
     ###############################################################
     
    # ATR Periodo 1h, 24 horas
    ATR = MainTF.ta.atr(length=ATR_Length) # funçao automatica de livraria
    #print("\nATR: \n", ATR)
    
     ###############################################################
     
    # Ve se e subida ou descida 24 atraves do Max e Min
    
    StartDate = MainTF['time'].iloc[0]
    EndDate =   MainTF['time'].iloc[-1]
     
    #Periodo de 24h 
    MaxVal =  max(MainTF['high'].iloc[0:]) # get max value on column "high" from cell to cell
    MinVal =  min(MainTF['low'].iloc[0:]) #get min value on column "high" from cell to cell
    
    #get index
    indHigh = MainTF.high[MainTF.high == MaxVal].index.tolist()#  get row index maximo
    indLow = MainTF.low[MainTF.low == MinVal].index.tolist()
    
    
    
    # verifica se ha mais que 1 high com o mesmo valor
    if len(indHigh) > 1:
           intIndHigh_0 = indHigh[0] #primeira posicao do high
           intIndHigh_1 = indHigh[-1] #ultima posicao do high
    else:
         intIndHigh_0 = indHigh[0] # posicao do high
         intIndHigh_1 = indHigh[0] # posicao do high
     
    # verifica se ha mais que 1 low com o mesmo valor
    if len(indLow) > 1:
    
        intIndLow_0 = indLow[0] #primeira posicao do low
        intIndLow_1 = indLow[-1] #ultima posicao do low
    else:
        intIndLow_0 = indLow[0] # posicao do low
        intIndLow_1 = indLow[0] # posicao do low
    
    
    #####
    
    # dias e horas em que esteve no ponto mais alto / baixo
    TdHigh = MainTF['time'].iloc[indHigh].tolist() # da os dias e horas em que esteve no ponto mais alto
    TdLow = MainTF['time'].iloc[indLow].tolist() # da os dias e horas em que esteve no ponto mais baixo
                  
    #print("\nHourly DataFrame \n", MainTF.head(24))
    print("\nHigh value: ", MaxVal," / Horas : ",TdHigh,"\n","Low value: ",MinVal," / Horas : ",TdLow)
    
    
    # Ve se e subida ou descida 24
    
    #vai buscar o maior timeframe entre high e low na subida
        
    if  TdHigh  > TdLow:
         intIndHigh = intIndHigh_0
         intIndLow = intIndLow_1
         
    else:
         intIndLow = intIndLow_0
         intIndHigh = intIndHigh_1
         
    TF_subida = abs(intIndLow - intIndHigh)
    TF_descida = abs(intIndHigh - intIndLow)
     
    #Subida
    if TdHigh > TdLow and TF_subida > 5: # subida e high e low diferenca de horas ou dias maior que xxx
     
         print("\nPeriodo de ",ATR_Length,": subida")
         print(TF_subida, " horas")
         print("\nHora High : " , TdHigh," Posicao High  : " , intIndHigh )
         print("\nHora low : " , TdLow," Posicao low : " , intIndLow ) 
         
         MainTF_Subida = True
         MainTF_descida = False             
    
    #Descida
    elif TdLow > TdHigh and TF_descida > 5: # descida e high e low diferenca de horas ou dias maior que xxx
         
         print("\nPeriodo de ",ATR_Length,": descida")
         print(TF_descida, " horas")
         print("\nHora High : " , TdHigh,"Posicao High : " , intIndHigh )
         print("\nHora low  : " , TdLow,"Posicao Low : " , intIndLow )  
         
         MainTF_Subida = False
         MainTF_descida = True
         
    else:
         MainTF_Subida = False
         MainTF_descida = False
         print("\n No Periodo de ",ATR_Length," a subida / descida nao cumpre criterios de tamanho minimo de 5 velas")
          
     ###############################################################
      
     # SUBIDA SUBIDA SUBIDA 24 velas / hora 
     
    if MainTF_Subida:
        
         # SHOOTING STAR CANDLESTICK 24 velas / hora subida
         MaxVal_Low = MainTF['low'].iloc[intIndHigh].tolist() # low corresponde a vela com maior high
         
         Diff_Candle_SS = MaxVal - MaxVal_Low #comprimento da vela
         
         Diff_HL = MainTF['high'].iloc[intIndLow:] - MainTF['low'].iloc[intIndLow:] # diferenca entre high e low. desde o low ate high
         
         Diff_MinVal = Diff_Candle_SS  > min(Diff_HL) # comprimento da vela Shooting Star e' maior que o comprimento da vela mais pequena
      
         # Close price > Open price / Vela Verde
         if MainTF['close'].iloc[intIndHigh].tolist() >  MainTF['open'].iloc[intIndHigh].tolist() :
             if Diff_MinVal:
                 
                 # Numa shooting star body da candle  = (close price - open price) 
                 Body_SS =  MainTF['close'].iloc[intIndHigh].tolist() - MainTF['open'].iloc[intIndHigh].tolist()
            
                 # Wick = Higher price - Close price
                 Wick_SS = MainTF['high'].iloc[intIndHigh].tolist() - MainTF['close'].iloc[intIndHigh].tolist()
              
                 # É válido caso: wick > Corpo da candle"    
                 if Wick_SS > Body_SS  :   ########################  1 TRADE ######################
                   
                     SL_SS = MaxVal + ATR[0]
                    # TP_SS = 0
                    
                     ShootingStar_Found = True
                     
                     print("\n ENCONTROU Condicoes validas para Shooting star",ATR_Length," / Vela verde.\n Stop loss: ",SL_SS,"\n","\n")
                     
                     ShootingStar_Found = True
                     return ShootingStar_Found
                     
             # com while voltar a por       #break
                     
                 else:
                     print("\n Nao cumpre condicoes validas para Shooting star",ATR_Length," / Vela verde.\n")
                     ShootingStar_Found = False
            
             else:
                 print("\nDiferença minima nao e valida")
                 ShootingStar_Found = False
        
        
         else: # Open price >  Close price / vela Vermelha
             if Diff_MinVal:
                 
                 # Corpo da candle = (open price - close price)  
                 Body_SS =  MainTF['open'].iloc[intIndHigh].tolist() - MainTF['close'].iloc[intIndHigh].tolist()      
                 # Wick = higher price - open price 
                 Wick_SS = MainTF['high'].iloc[intIndHigh].tolist() - MainTF['open'].iloc[intIndHigh].tolist()
                 
                 # É válido caso: wick > corpo da candle
                 if Wick_SS > Body_SS  : ########################  1 TRADE ######################
                     
                     SL_SS = MaxVal + ATR[0]
                    # TP_SS = 0    
                     print(" \n ENCONTROU Condicoes validas para Shooting star",ATR_Length," / vela Vermelha ","\n Stop Loss: ",SL_SS,"\n","\n")
                        
                    
                     ShootingStar_Found = True
                     return ShootingStar_Found
                     print("\n")
                     
                    # break com while voltar a por
                 else:
                     print("\n Nao cumpre condicoes validas para Shooting star ",ATR_Length," / Vela Vermelha.\n")
                     print("\n")
                     ShootingStar_Found = False
                   
             else:
                 print("\nDiferença minima nao e valida")
                 ShootingStar_Found = False
                 
     ###############################################################
     ###############################################################
        
        #  # BEARISH ENGULFING 24  BEARISH ENGULFING24  BEARISH ENGULFING  24
        
        
         # Vela com o maior high nao pode ser a mesma vela que faz bearish engulfing 
         if MainTF['time'].iloc[0] > MainTF['time'].iloc[intIndHigh] and ShootingStar_Found == False :  # uso vela posicao 1, pq a 0(mais recente) ainda esta a decorrer
            
            BE_nI = intIndHigh - 1    # inteiro . Valor que vai desde o index do ponto mais alto ate ao inicio do data frame
            print("\nVai procurar Bearish engulfing desde o high ate ao inicio data frame")
            print("\nCondicoes:\n -> BE_i  =  BE_OH and BE_CL ", "\n", "-> BE_ii = ( Body_BE > Body_SS) and  (Body_BE >  2*Wick_BE )" , "\n", "-> BE_iii = ( Body_BE > Body_SS)")
    
    
            for i in (MainTF['high'].iloc[intIndHigh:0:-1]):
              
                #i) Candle abre acima da anterior e fecha abaixo da anterior 
                BE_OH =  MainTF['open'].iloc[BE_nI].tolist() >  MaxVal  # Bearish Engulfing = Open maior que o Higher High
                BE_CL =  MainTF['close'].iloc[BE_nI].tolist() <  MaxVal_Low  # Bearish Engulfing = Close mais pequeno que o Low correspondente a vela High max val 
                BE_i  =  BE_OH and BE_CL
    
              # ii) Sem grande wick, quase só corpo de vela e "engole" a anterior. # Q.: Quanto maior? neste momento esta so a verificar se e' maior ou nao
        
              # vela vermelha
              # open price > close price 
                if MainTF['open'].iloc[BE_nI] >  MainTF['close'].iloc[BE_nI]:
             
                      # body da candle  mais recente = (close price - open price) 
                      Body_BE =  MainTF['open'].iloc[BE_nI] - MainTF['close'].iloc[BE_nI]
                     
                      Wick_BE = MainTF['high'].iloc[BE_nI] - MainTF['open'].iloc[BE_nI]
                     
                      BE_ii = ( Body_BE > Body_SS) and  (Body_BE >  2*Wick_BE )
                   
                      # iii) O corpo da candle é maior do o corpo da candle anterior
                         
                      BE_iii = ( Body_BE > Body_SS)
                      
                      print("\nVela :",BE_nI,"Vela vermelha \nBody_BE: ",Body_BE ,"\n","Wick_BE: ",Wick_BE,"\n","BE_i:",BE_i ,"\n","BE_ii:",BE_ii ,"\n","BE_iii:",BE_iii)
                else:
                    print("\nVela :",BE_nI," nao e vela vermelha, nao pode ser BEARISH ENGULFING")
                    BearishEng_Found = False
                        
              
                # Condicoes para bearish engulfing encontradas
                if BE_i and BE_ii and BE_iii:
                    
                    print( MainTF['time'].iloc[BE_nI] , " ->\n ENCONTROU BEARISH ENGULFING CANDLE " )
                    
                    
                    BearishEng_Found = True
                    return BearishEng_Found
                    
                    break
                 
                if BE_nI > 0:
                    BE_nI = BE_nI - 1
                
                     
     ###############################################################
     
     # DESCIDA DESCIDA DESCIDA 24 24 24
      
     # HAMMER STAR CANDLESTICK 24 HAMMER STAR CANDLESTICK 24 HAMMER STAR CANDLESTICK 24 velas 
     
         
    elif MainTF_descida:
     
         MinVal_High = MainTF['high'].iloc[intIndLow].tolist() # low da vela com maior high
         
         Diff_Candle_HS = MaxVal - MinVal_High #comprimento da vela
         
         Diff_LH = MainTF['low'].iloc[intIndHigh:] - MainTF['high'].iloc[intIndHigh:] # diferenca entre high e low. desde o low ate high
         
         Diff_MaxVal = Diff_Candle_HS  > min(Diff_LH) # comprimento da vela Shooting Star e' maior que o comprimento da vela mais pequena
             # Close price > Open price #vela verde
         if MainTF['close'].iloc[intIndLow].tolist() >  MainTF['open'].iloc[intIndLow].tolist() and Diff_MaxVal:
     
             # Numa hammer star body da candle  = (close price- open price) 
             Body_HS =  MainTF['close'].iloc[intIndLow].tolist() - MainTF['open'].iloc[intIndLow].tolist()
        
             # Wick = open price - low price
             Wick_HS = MainTF['open'].iloc[intIndLow].tolist() - MainTF['low'].iloc[intIndLow].tolist()
           
             # É válido caso: wick > Corpo da candle" 
             if Wick_HS > Body_HS  :   ########################  1 TRADE ######################
                 
                 SL_HS = MinVal + ATR[0]
                 #TP_HS = 0
                 print("\n Encontrou Condicoes validas para Hammer star",ATR_Length," / Vela verde","\n","StopLoss: ",SL_HS,"\n")

                 
                 HammerStar_Found = True
                 return HammerStar_Found
             #com while voltar a por    break
                 
             else:
                print("\n Nao cumpre condicoes validas para Hammer star",ATR_Length," / Vela verde.\n")
                HammerStar_Found = False
       
        
         elif MainTF['open'].iloc[intIndLow].tolist() > MainTF['close'].iloc[intIndLow].tolist() and Diff_MaxVal:
         #Corpo da candle = (open price - close price)
         #wick = higher price - open price
         #É válido caso: wick > corpo da candle
             
             Body_HS =  MainTF['open'].iloc[intIndHigh].tolist() - MainTF['close'].iloc[intIndHigh].tolist()
             Wick_HS = MainTF['close'].iloc[intIndHigh].tolist() - MainTF['low'].iloc[intIndHigh].tolist()
             
             if Wick_HS > Body_HS  : ########################  1 TRADE ######################
                 
                 SL_HS = MinVal + ATR[0]
                 #TP_HS = 0 
                 
                 print(" \nEncontrou Condicoes validas para Hammer star",ATR_Length," / vela Vermelha ","\n Stop Loss: ",SL_HS,"\n")
                 
                 
                 HammerStar_Found = True
                 return HammerStar_Found
                   #
        
             else:
                 print("\n Nao cumpre condicoes validas para Hammer star ",ATR_Length," / Vela Vermelha.\n") 
                 
                 HammerStar_Found = False
                   
         else:
             print("\n\nDiferença minima nao e valida")
             
             HammerStar_Found = False
                
             
      #  # BULLISH ENGULFING 24  BULLISH ENGULFING24  BULLISH ENGULFING  24
                           
            # Vela com o maior high nao pode ser a mesma vela que faz bearish engulfing 
         if MainTF['time'].iloc[0] > MainTF['time'].iloc[intIndLow] and HammerStar_Found == False:  # uso vela posicao 1, pq a 0(mais recente) ainda esta a decorrer
           
            BU_nI = intIndLow - 1    # inteiro . Valor que vai desde o index do ponto mais alto ate ao inicio do data frame
           
            print("\nVai procurar BULLISH engulfing desde o low ate ao inicio data frame")
            print("\nCondicoes:\n -> BU_i  = BU_OL and BU_CH ", "\n", "-> BU_ii = ( Body_BU > Body_HS) and  (Body_BU >  2*Wick_BU )" , "\n", "-> BU_iii = ( Body_BU > Body_HS)")
    
            for i in (MainTF['low'].iloc[intIndLow:0:-1]):
              
                #i) Candle abre acima da anterior e fecha abaixo da anterior 
                BU_OL =  MainTF['open'].iloc[BU_nI].tolist()  <  MinVal  # Bullish Engulfing = Open menor que o Lower Low
                BU_CH =  MainTF['close'].iloc[BU_nI].tolist() >  MinVal_High  # Bullish Engulfing = Close maior que o Low correspondente a vela High max val 
                BU_i  =  BU_OL and BU_CH
    
        # ii) Sem grande wick, quase só corpo de vela e "engole" a anterior. # Q.: Quanto maior? neste momento esta so a verificar se e' maior ou nao
        
              # vela verde
              # close price >  open price 
                if MainTF['close'].iloc[BU_nI] >  MainTF['open'].iloc[BU_nI]:
             
                      # body da candle  mais recente = (close price - open price) 
                      Body_BU =  MainTF['close'].iloc[BU_nI] - MainTF['open'].iloc[BU_nI]
                     
                      Wick_BU = MainTF['high'].iloc[BU_nI] - MainTF['open'].iloc[BU_nI]
                     
                      BU_ii = ( Body_BU > Body_HS) and  (Body_BU >  2*Wick_BU )
                   
                          # iii) O corpo da candle é maior do o corpo da candle anterior
                         
                      BU_iii = ( Body_BU > Body_HS)
                      
                      print("\nvela :",BU_nI,"Vela Verde \nBody_BU: ",Body_BU ,"\n","Wick_BE: ",Wick_BU,"\n","BU_i:",BU_i ,"\n","BU_ii:",BU_ii ,"\n","BU_iii:",BU_iii)
                else:
                    print("\nvela :",BU_nI," Nao e Vela Verde, nao pode ser BULLISH engulfing")
                    BullishEng_Found = False
              
                # Condicoes para bearish engulfing encontradas
                if BU_i and BU_ii and BU_iii:
                    
                    print( MainTF['time'].iloc[BU_nI] , " ->\n ENCONTROU BULLISH ENGULFING CANDLE " )
           
                    
                    BullishEng_Found = True
                    return BullishEng_Found
                    break
                   
                if BU_nI > 0:
                    BU_nI = BU_nI - 1
    else:
        
        # HammerStar_Found = False
        # ShootingStar_Found = False
        
        # BearishEng_Found = False
        # BullishEng_Found = False

        # BE_i  = False 
        # BE_ii  = False 
        # BE_iii = False 

        # Body_SS = 0 
        # Wick_SS = 0 

        pass
    
    time.sleep(60)
    
        
    ##########################################################################################
    ##########################################################################################
    
  
#GetData(horas_min,currencia,ATR_Length)
print("\n Exemplo currencias : EUR/USD ;  CAD/JPY ; eth/usd ; GME;  ")

currencia = str(input("Currencia:"))
currencia_1 = currencia
currencia_2 = currencia

ATR_Length_1 = int(input("\nNumero de velas a analisar no Timeframe 1. So corre uma vez:"))
# TimeFrame 1 corre so uma vez
horas_min_1 = str(input("1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month\nTimeFrame 1 - So corre uma vez. Escrever opçao de cima: "))

# ATR_Length_2 = int(input("\nNumero de velas a analisar no Timeframe 2. Corre continuamente:"))
# # TimeFrame de 2 corre em loop
# horas_min_2 = str(input("1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month\nTimeFrame 2 - Corre continuamente: Escrever opçao de cima: "))


################################################################################

GetData(horas_min_1,currencia_1,ATR_Length_1,ResSup_Found) # Primeiro timeframe, corre so uma vez
ResSup_Found = False


# if HammerStar_Found == False and ShootingStar_Found == False and BullishEng_Found == False and BullishEng_Found == False:
    
#     while True:
        
#         GetData(horas_min_2,currencia_2,ATR_Length_2,ResSup_Found)
#         if HammerStar_Found or ShootingStar_Found and BullishEng_Found or BullishEng_Found:
#             break
#         else:
#             continue
        

print("Currencia em analise: ", currencia)