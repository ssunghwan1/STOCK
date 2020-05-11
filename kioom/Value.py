import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime
import time
import pymysql
count = 0
srimiList = []
if __name__ == "__main__":
    app = QApplication(sys.argv)


    db = pymysql.connect(host="127.0.0.1", user="root", passwd="1111", db="STOCK", charset="utf8")
    curs = db.cursor(pymysql.cursors.DictCursor)
    cur_date = datetime.today().strftime("%Y%m%d")
    #for i in range(len(list_str)):
    #800 기준으로 등호를 바꾸어주어야 함
    stockCodeSql1 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY,CASH_FLOWS_FROM_OPERATINGS,NET_SALES FROM financial_reports where BASE_DATE = '201912' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    stockCodeSql2 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY,CASH_FLOWS_FROM_OPERATINGS,NET_SALES FROM financial_reports where BASE_DATE = '201812' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    stockCodeSql3 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY,CASH_FLOWS_FROM_OPERATINGS,NET_SALES FROM financial_reports where BASE_DATE = '201712' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    baseDataSql = """SELECT * FROM BASE_DATA WHERE RGS_DTM = '20200507' AND TOTAL < 1000"""
    curs.execute(stockCodeSql1)
    financialList1 = curs.fetchall(); #2019

    curs.execute(baseDataSql)
    baseDataList = curs.fetchall();
    priceList = []
    #print(len(baseDataList))
    for stock in baseDataList:
        STOCK_CODE = stock['STOCK_CODE']
        TOTAL = stock['TOTAL']
        CURRENT_PRICE = stock['CURRENT_PRICE']
        PER = stock['PER']
        PBR = stock['PBR']
        if CURRENT_PRICE[:1] == '+':
            CURRENT_PRICE = CURRENT_PRICE[1:]
        if CURRENT_PRICE[:1] == '-' :
            CURRENT_PRICE = CURRENT_PRICE[1:]
        priceList.append({"STOCK_CODE": STOCK_CODE,
                          "TOTAL": TOTAL,
                          "CURRENT_PRICE": CURRENT_PRICE,
                          "PER": PER,
                          "PBR": PBR})
    srimiList =[]
    srimDic ={}
    for stock in financialList1:
        BASE_DATE = stock['BASE_DATE']
        STOCKK_CODE = stock['STOCKK_CODE']
        COMPANY_NAME = stock['COMPANY_NAME']
        TOTAL_STOCKHOLDER_EQUITY = stock['TOTAL_STOCKHOLDER_EQUITY']
        OWNERS_OF_PARENT_EQUITY = stock['OWNERS_OF_PARENT_EQUITY']
        CASH_FLOWS_FROM_OPERATINGS = stock['CASH_FLOWS_FROM_OPERATINGS']
        NET_SALES = stock['NET_SALES']
        PROFIT = stock['NET_INCOME_OWNERS_OF_PARENT_EQUITY']

        if NET_SALES == '':
            continue
        for price in priceList:
            if price['STOCK_CODE'] == STOCKK_CODE[1:]:
                count +=1
                currentPrice = int(price['CURRENT_PRICE'])
                TOTAL = int(price['TOTAL'])
                PBR = price['PBR']
                PER = price['PER']
                PCR = TOTAL/(int(CASH_FLOWS_FROM_OPERATINGS)/100000)
                PSR = TOTAL/(int(NET_SALES)/100000)
                STOCK_CODE = price['STOCK_CODE']
                if PBR =='' or PER =='' or PCR < 0:
                    continue
                srimiList.append({"STOCK_CODE" : STOCK_CODE,
                                  "COMPANY_NAME": COMPANY_NAME,
                                  # "OWNERS_OF_PARENT_EQUITY" : OWNERS_OF_PARENT_EQUITY,
                                  "PBR": PBR,
                                  "PER": PER,
                                  "CURRENT_PRICE": currentPrice,
                                  "CASH_FLOWS_FROM_OPERATINGS" : CASH_FLOWS_FROM_OPERATINGS,
                                  "TOTAL": TOTAL,
                                  "PCR" : PCR,
                                  "PSR" : PSR})
    print(srimiList)
    dataList = sorted(srimiList, key=lambda srimiList: (srimiList['PBR']))
    finaldata = []

    for num,data in enumerate(dataList):
        #print(data)
        finaldata.append({
            "STOCK_CODE" : data['STOCK_CODE'],
            "COMPANY_NAME" : data['COMPANY_NAME'],
            "TOTAL" : data['TOTAL'],
            "PBR": data['PBR'],
            "PER": data['PER'],
            "PCR": data['PCR'],
            "PSR": data['PSR'],
            "PBR_RANK" : num + 1
        })
    dataList = sorted(srimiList, key=lambda srimiList: (srimiList['PER']))
    for num, data in enumerate(dataList):
        #print(data)
        for tmpNum,tmpData in enumerate(finaldata):
            if data['STOCK_CODE'] == tmpData['STOCK_CODE']:
                finaldata[tmpNum]['PER_RANK'] = num
    dataList = sorted(srimiList, key=lambda srimiList: (srimiList['PCR']))
    for num, data in enumerate(dataList):
        #print(data)
        for tmpNum,tmpData in enumerate(finaldata):
            if data['STOCK_CODE'] == tmpData['STOCK_CODE']:
                finaldata[tmpNum]['PCR_RANK'] = num
    dataList = sorted(srimiList, key=lambda srimiList: (srimiList['PSR']))
    for num, data in enumerate(dataList):
        #print(data)
        for tmpNum,tmpData in enumerate(finaldata):
            if data['STOCK_CODE'] == tmpData['STOCK_CODE']:
                finaldata[tmpNum]['PSR_RANK'] = num

    #print(finaldata)
    for i in finaldata:
        i['SUM_RANK'] = i['PER_RANK'] +i['PBR_RANK'] +i['PCR_RANK'] +i['PSR_RANK']

    finaldata = sorted(finaldata, key=lambda finaldata: (finaldata['SUM_RANK']))
    print(len(finaldata))
    for i in finaldata:
        print(i)

    resetSS_VALUEsql ="""delete from SS_VALUE WHERE STOCK_CODE = %s and RGS_DTM =%s"""
    isnertSS_VALUEsql = """insert into SS_VALUE(RGS_DTM,STOCK_CODE,COMPANY_NAME,TOTAL,PBR,PER,PCR,PSR,PBR_RANK,PER_RANK,PCR_RANK,PSR_RANK,SUM_RANK)
              values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    for i in finaldata:
        curs.execute(resetSS_VALUEsql, (i['STOCK_CODE'], cur_date))
        curs.execute(isnertSS_VALUEsql, (cur_date, i['STOCK_CODE'], i['COMPANY_NAME'], i['TOTAL'],i['PBR'], i['PER'], i['PCR']
                           , i['PSR'], i['PBR_RANK'], i['PER_RANK'], i['PCR_RANK'],i['PSR_RANK'],i['SUM_RANK']))


    db.commit()
    db.close()
