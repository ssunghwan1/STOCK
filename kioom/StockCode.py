import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pykiwoom.kiwoom import *
from datetime import datetime
import time
import pymysql

TR_REQ_TIME_INTERVAL = 1
dic1 = {}
Lst = list()
test11 = 0

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10001_req":
            self._opt10001(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10001(self, rqname, trcode):
        STOCK_CODE = self._comm_get_data(trcode, "", rqname, 0, "종목코드")
        STOCK_NAME = self._comm_get_data(trcode, "", rqname, 0, "종목명")
        output2 = self._comm_get_data(trcode, "", rqname, 0, "결산월")
        output3 = self._comm_get_data(trcode, "", rqname, 0, "액면가")
        output4 = self._comm_get_data(trcode, "", rqname, 0, "자본금")
        output5 = self._comm_get_data(trcode, "", rqname, 0, "상장주식")
        output6 = self._comm_get_data(trcode, "", rqname, 0, "신용비율")
        output7 = self._comm_get_data(trcode, "", rqname, 0, "연중최고")
        output8 = self._comm_get_data(trcode, "", rqname, 0, "연중최저")
        TOTAL = self._comm_get_data(trcode, "", rqname, 0, "시가총액")
        output10 = self._comm_get_data(trcode, "", rqname, 0, "시가총액비중")
        output11 = self._comm_get_data(trcode, "", rqname, 0, "외인소진률")
        output12 = self._comm_get_data(trcode, "", rqname, 0, "대용가")
        PER = self._comm_get_data(trcode, "", rqname, 0, "PER")
        EPS = self._comm_get_data(trcode, "", rqname, 0, "EPS")
        ROE = self._comm_get_data(trcode, "", rqname, 0, "ROE")
        PBR = self._comm_get_data(trcode, "", rqname, 0, "PBR")
        output17 = self._comm_get_data(trcode, "", rqname, 0, "EV")
        BPS = self._comm_get_data(trcode, "", rqname, 0, "BPS")
        SALES = self._comm_get_data(trcode, "", rqname, 0, "매출액")
        BENEFIT = self._comm_get_data(trcode, "", rqname, 0, "영업이익")
        AFTERBENEFIT = self._comm_get_data(trcode, "", rqname, 0, "당기순이익")
        output22 = self._comm_get_data(trcode, "", rqname, 0, "250최고")
        output23 = self._comm_get_data(trcode, "", rqname, 0, "250최저")
        output24 = self._comm_get_data(trcode, "", rqname, 0, "시가총액고가")
        output25 = self._comm_get_data(trcode, "", rqname, 0, "저가")
        output26 = self._comm_get_data(trcode, "", rqname, 0, "상한가")
        output27 = self._comm_get_data(trcode, "", rqname, 0, "하한가")
        output28 = self._comm_get_data(trcode, "", rqname, 0, "기준가")
        output29 = self._comm_get_data(trcode, "", rqname, 0, "예상체결가")
        output30 = self._comm_get_data(trcode, "", rqname, 0, "예상체결수량")
        output31 = self._comm_get_data(trcode, "", rqname, 0, "250최고가일")
        output32 = self._comm_get_data(trcode, "", rqname, 0, "250최저가일")
        output33 = self._comm_get_data(trcode, "", rqname, 0, "250최저가대비율")
        CURRENT_PRICE = self._comm_get_data(trcode, "", rqname, 0, "현재가")
        output35 = self._comm_get_data(trcode, "", rqname, 0, "대비기호")
        output36 = self._comm_get_data(trcode, "", rqname, 0, "전일대비")
        output37 = self._comm_get_data(trcode, "", rqname, 0, "등락율")
        output38 = self._comm_get_data(trcode, "", rqname, 0, "거래량")
        output39 = self._comm_get_data(trcode, "", rqname, 0, "거래대비")
        output40 = self._comm_get_data(trcode, "", rqname, 0, "액면가단위")
        output41 = self._comm_get_data(trcode, "", rqname, 0, "유통주식")
        output42 = self._comm_get_data(trcode, "", rqname, 0, "유통비율")
        global dic1
        global Lst
        dic1 = {'STOCK_CODE':STOCK_CODE, 'STOCK_NAME':STOCK_NAME
            , 'TOTAL':TOTAL, 'PER':PER, 'EPS':EPS
                , 'ROE':ROE, 'PBR':PBR, 'BPS':BPS
                , 'SALES':SALES, 'BENEFIT':BENEFIT, 'AFTERBENEFIT':AFTERBENEFIT, 'CURRENT_PRICE':CURRENT_PRICE}
        Lst.append(dic1)
        #print((output0,output1,output2,output3,output4,output5,output6,output7,output8,output9,output10,output11,output12,output13,output14,output15,output16,output17,output18,output19,output20,output21,output22,output23,output24,output25,output26,output27,output28,output29,output30,output31,output32,output33,output34,output35,output36,output37,output38,output39,output40,output41,output42))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    #0:장내, 10:코스닥
    kospi = kiwoom.GetCodeListByMarket('0')
    print(kospi)
    list_str = kospi.split(';');
    db = pymysql.connect(host="127.0.0.1", user="root", passwd="1111", db="STOCK", charset="utf8")
    curs = db.cursor()
    print(list_str)
    print(len(list_str))
    cur_date = datetime.today().strftime("%Y%m%d")
    sql = """insert into STOCK_CODE(STOCK_CODE,RGS_DTM)
                    values (%s,%s)"""
    resetSql = """delete from STOCK_CODE WHERE RGS_DTM =%s"""
    curs.execute(resetSql,  cur_date)

    for i in range(len(list_str)):
        if list_str[i] == '':
            break
        curs.execute(sql,(list_str[i],cur_date))

    db.commit()
    db.close()