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
    stockCodeSql1 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY FROM financial_reports where BASE_DATE = '201912' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    stockCodeSql2 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY FROM financial_reports where BASE_DATE = '201812' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    stockCodeSql3 = """SELECT BASE_DATE, STOCKK_CODE,COMPANY_NAME,TOTAL_STOCKHOLDER_EQUITY,OWNERS_OF_PARENT_EQUITY,PROFIT,NET_INCOME_OWNERS_OF_PARENT_EQUITY FROM financial_reports where BASE_DATE = '201712' and TOTAL_STOCKHOLDER_EQUITY != ''"""
    curs.execute(stockCodeSql1)
    financialList1 = curs.fetchall(); #2019

    curs.execute(stockCodeSql2)
    financialList2 = curs.fetchall(); #2018

    curs.execute(stockCodeSql3)
    financialList3 = curs.fetchall(); #2017

    srimiList =[];
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
        ROE = ((ROE1 * 3) + (ROE2 * 2) + (ROE3 * 1)) / 6
        SRIM = int(OWNERS_OF_PARENT_EQUITY) +int(int(OWNERS_OF_PARENT_EQUITY)*((ROE - 10.0)/10.0))

        srimDic['COMPANY_NAME'] = COMPANY_NAME
        srimDic['OWNERS_OF_PARENT_EQUITY'] = OWNERS_OF_PARENT_EQUITY
        srimDic['ROE'] = ROE
        srimDic['SRIM'] = SRIM/100000

        # print(COMPANY_NAME)
        # print(OWNERS_OF_PARENT_EQUITY)
        # print(ROE)
        # print(SRIM/100000) #억단위로 바꿔줌

        srimiList.append({ "COMPANY_NAME" : COMPANY_NAME,
                           "OWNERS_OF_PARENT_EQUITY" : OWNERS_OF_PARENT_EQUITY,
                           "ROE" : ROE,
                           "SRIM" : SRIM/1000,})

    data = sorted(srimiList, key=lambda srimiList: (srimiList['SRIM']) ,reverse=True)


    for i in data:
        print(i['SRIM'])


    db.commit()
    db.close()
