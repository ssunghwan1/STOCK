import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime
import time
import pymysql

srimiList = []
if __name__ == "__main__":
    app = QApplication(sys.argv)


    db = pymysql.connect(host="127.0.0.1", user="root", passwd="1111", db="STOCK", charset="utf8")
    curs = db.cursor(pymysql.cursors.DictCursor)
    cur_date = datetime.today().strftime("%Y%m%d")
    #for i in range(len(list_str)):
    #800 기준으로 등호를 바꾸어주어야 함
    stockCodeSql1 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY,CASH_FLOWS_FROM_INVESTING,NET_SALES FROM financial_reports where BASE_DATE = '201912' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    stockCodeSql2 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY,CASH_FLOWS_FROM_INVESTING,NET_SALES FROM financial_reports where BASE_DATE = '201812' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    stockCodeSql3 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY,CASH_FLOWS_FROM_INVESTING,NET_SALES FROM financial_reports where BASE_DATE = '201712' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    baseDataSql = """SELECT * FROM BASE_DATA WHERE RGS_DTM = '20200501'"""
    curs.execute(stockCodeSql1)
    financialList1 = curs.fetchall(); #2019

    curs.execute(stockCodeSql2)
    financialList2 = curs.fetchall(); #2018

    curs.execute(stockCodeSql3)
    financialList3 = curs.fetchall(); #2017

    curs.execute(baseDataSql)
    baseDataList = curs.fetchall();
    priceList = []
    for stock in baseDataList:
        STOCK_CODE = stock['STOCK_CODE']
        TOTAL =  stock['TOTAL']
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

    print(priceList)
    srimiList =[]
    srimDic ={}
    for stock in financialList1:
        BASE_DATE = stock['BASE_DATE']
        STOCKK_CODE = stock['STOCKK_CODE']
        COMPANY_NAME = stock['COMPANY_NAME']
        TOTAL_STOCKHOLDER_EQUITY = stock['TOTAL_STOCKHOLDER_EQUITY']
        OWNERS_OF_PARENT_EQUITY = stock['OWNERS_OF_PARENT_EQUITY']

        PROFIT = stock['NET_INCOME_OWNERS_OF_PARENT_EQUITY']

        if OWNERS_OF_PARENT_EQUITY == '':
            continue
        if TOTAL_STOCKHOLDER_EQUITY =='':
            TOTAL_STOCKHOLDER_EQUITY = 0
        if OWNERS_OF_PARENT_EQUITY == '':
            OWNERS_OF_PARENT_EQUITY = 0
        if PROFIT == '':
            PROFIT = 0

        ROE1 = int(PROFIT)/int(OWNERS_OF_PARENT_EQUITY)
        ROE2 = 0
        ROE3 = 0
        for stock2 in financialList2:
            if STOCKK_CODE == stock2['STOCKK_CODE']:
                OWNERS_OF_PARENT_EQUITY2 = stock2['OWNERS_OF_PARENT_EQUITY']
                PROFIT = stock2['NET_INCOME_OWNERS_OF_PARENT_EQUITY']
                ROE2 = int(PROFIT)/int(OWNERS_OF_PARENT_EQUITY2)
        for stock3 in financialList3:
            if STOCKK_CODE == stock3['STOCKK_CODE']:
                OWNERS_OF_PARENT_EQUITY3 = stock3['OWNERS_OF_PARENT_EQUITY']
                PROFIT = stock3['NET_INCOME_OWNERS_OF_PARENT_EQUITY']
                ROE3 = int(PROFIT)/int(OWNERS_OF_PARENT_EQUITY3)
        #ROE = ((ROE1 * 3) + (ROE2 * 2) + (ROE3 * 1)) / 6
        ROE  = ROE1
        SRIM = int(OWNERS_OF_PARENT_EQUITY) +int(int(OWNERS_OF_PARENT_EQUITY)*((ROE - 10.0)/10.0))

        srimDic['COMPANY_NAME'] = COMPANY_NAME
        srimDic['OWNERS_OF_PARENT_EQUITY'] = OWNERS_OF_PARENT_EQUITY
        srimDic['ROE'] = ROE
        srimDic['SRIM'] = SRIM/100000

        # print(COMPANY_NAME)
        # print(OWNERS_OF_PARENT_EQUITY)
        # print(ROE)
        # print(SRIM/100000) #억단위로 바꿔줌
        currentPrice= 987654321
        TOTAL = 987654321000
        for price in priceList:
            if price['STOCK_CODE'] == STOCKK_CODE[1:]:
                currentPrice = int(price['CURRENT_PRICE'])
                TOTAL = int(price['TOTAL'])
                PBR = price['PBR']
                PER = price['PER']
                STOCK_CODE = price['STOCK_CODE']
        #조건 입력부
        #if abs(ROE1 - ROE2) < 0.2 and abs(ROE2 - ROE3) < 0.2 and TOTAL < 5000 and ROE1 > 0.1:
        if TOTAL < 1000:
            srimiList.append({ "STOCK_CODE" : STOCK_CODE,
                                "COMPANY_NAME" : COMPANY_NAME,
                               #"OWNERS_OF_PARENT_EQUITY" : OWNERS_OF_PARENT_EQUITY,
                               "PBR" :PBR,
                               "PER" :PER,
                               "ROE1" : round(ROE1,2),
                               "ROE2": round(ROE2,2),
                               "ROE3": round(ROE3,2),
                               "SRIM" : SRIM/1000,
                               "CURRENT_PRICE" : currentPrice,
                               "TOTAL" : TOTAL,
                               "UPTO" : (((SRIM/1000)-TOTAL)/TOTAL) *100 })

    data = sorted(srimiList, key=lambda srimiList: (srimiList['UPTO']) ,reverse=True)


    for i in data:
        print(i)

    cur_date = datetime.today().strftime("%Y%m%d")
    selectSS_VALUEsql ="""SELECT * FROM SS_VALUE where rgs_dtm = %s """
    updateSS_VALUEsql = """update SS_VALUE set SS_PRICE =%s WHERE STOCK_CODE =%s and RGS_DTM =%s"""

    curs.execute(selectSS_VALUEsql,cur_date)
    selectSS_VALUElist = curs.fetchall();

    for i in selectSS_VALUElist:
        for j in srimiList:
            if i['STOCK_CODE'] == j['STOCK_CODE']:
                SS_PRICE = j['SRIM']
                STOCK_CODE =i['STOCK_CODE']
                curs.execute(updateSS_VALUEsql,(SS_PRICE,STOCK_CODE,cur_date))
    db.commit()
    db.close()
