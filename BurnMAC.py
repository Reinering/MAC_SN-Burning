# -*- coding: utf-8 -*-
#python35
"""
Module implementing MainWindow.
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import xml.dom.minidom
from hgu import *
from queue import Queue
import codecs

from Ui_BurnMAC import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        # self.macPro = "类属性"  # 烧写MAC

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        self.logQueue = Queue()
        self.proMode = 0
        self.macPro = ""                           #烧写MAC
        self.snPro = ""                                 #烧写SN
        self.ipAddr = ""
        self.macBool= True
        self.snBool = True

        self.parseConfXML()                             #UI界面数据初始化

    def get_xmlData(self, root, tagName):
        itemList = root.getElementsByTagName(tagName)
        return itemList[0].firstChild.data
    def set_xmlData(self, root, tagName, data):
        itemList = root.getElementsByTagName(tagName)
        # itemList[0].setAttribute(tagName, data)       #设置节点属性
        itemList[0].firstChild.data = data

    def parseConfXML(self):                             #初始化、读取XML
        doc = xml.dom.minidom.parse("config.xml")
        root = doc.documentElement
        self.ipAddr = self.get_xmlData(root, "ipAddr")
        self.macStart = self.get_xmlData(root, "macStart")
        self.macEnd = self.get_xmlData(root, "macEnd")
        self.macInter = self.get_xmlData(root, "macInter")
        self.macCurrent = self.get_xmlData(root, "macCurrent")
        self.snStart = self.get_xmlData(root, "snStart")
        self.snEnd = self.get_xmlData(root, "snEnd")
        self.snInter = self.get_xmlData(root, "snInter")
        self.snCurrent = self.get_xmlData(root, "snCurrent")

        self.lineEdit_ipAddr.setText(self.ipAddr)

        self.lineEdit_macStart.setText(self.macStart)
        self.lineEdit_macEnd.setText(self.macEnd)
        self.lineEdit_macInterval.setText(self.macInter)

        if self.macCurrent == self.lineEdit_macEnd.text():
            self.textBrowser.append("此MAC号段已使用完，请另准备烧写号段")
        else:
            if self.macCurrent == "000000000000":
                self.macCurrent = "000000000001"
            elif self.macCurrent == "":
                if self.lineEdit_macStart.text() is "000000000000":
                    self.macCurrent = "000000000001"
                else:
                    self.macCurrent = self.lineEdit_macStart.text()
            self.macPro = self.macCurrent
            self.lineEdit_macCurrent.setText(self.macCurrent)
        print("macPro初始化", self.macPro)

        self.lineEdit_SNStart.setText(self.snStart)
        self.lineEdit_SNEnd.setText(self.snEnd)
        self.lineEdit_SNInterval.setText(self.snInter)
        if self.snCurrent == self.lineEdit_SNEnd.text():
            self.textBrowser.append("此SN号段已使用完，请另准备烧写号段")
        else:
            if self.snCurrent == "":
                self.snCurrent = self.lineEdit_SNStart.text()
            self.snPro = self.snCurrent
            self.lineEdit_SNCurrent.setText(self.snCurrent)
        print("snPro初始化", self.snPro)
    def writeConfXML(self):
        doc = xml.dom.minidom.parse("config.xml")
        root = doc.documentElement
        data = self.lineEdit_macStart.text()
        self.set_xmlData(root, "macStart", data)
        data = self.lineEdit_macEnd.text()
        self.set_xmlData(root, "macEnd", data)
        data = self.lineEdit_macInterval.text()
        self.set_xmlData(root, "macInter", data)
        data = self.lineEdit_SNStart.text()
        self.set_xmlData(root, "snStart", data)
        data = self.lineEdit_SNEnd.text()
        self.set_xmlData(root, "snEnd", data)
        data = self.lineEdit_SNInterval.text()
        self.set_xmlData(root, "snInter", data)
        f = codecs.open("config.xml", "w+", "utf-8")
        doc.writexml(f, addindent="", newl='', encoding="utf-8")        #格式控制 缩进-换行-编码
        f.close()

    def macCal(self):
        mac_StartDec = self.hexCimDec(self.lineEdit_macStart.text())
        mac_EndDec = self.hexCimDec(self.lineEdit_macEnd.text())
        mac_CurDec = self.hexCimDec(self.macPro)
        mac_Inter = self.lineEdit_macInterval.text()
        mac_CurDec = mac_CurDec + mac_Inter
        if mac_CurDec >= mac_StartDec and mac_CurDec <= mac_EndDec:
            self.macCurrent = self.decCimHex(mac_CurDec)
            self.macBool = True
            self.lineEdit_macCurrent.setText(self.macCurrent)
            self.macPro = self.macCurrent
        else:
            self.lineEdit_macCurrent.clear()
            self.macBool = False
        print(mac_CurDec)

    def snCal(self):
        sn_StartDec = self.hexCimDec(self.lineEdit_SNStart.text())
        sn_EndDec = self.hexCimDec(self.lineEdit_SNEnd.text())
        sn_CurDec = self.hexCimDec(self.snPro)
        sn_Inter = self.lineEdit_SNInterval.text()

        sn_CurDec = sn_CurDec + sn_Inter
        if sn_CurDec >= sn_StartDec and sn_CurDec <= sn_EndDec:
            self.snCurrent = self.decCimHex(sn_CurDec)
            self.snBool = True
            self.lineEdit_SNCurrent.setText(self.snCurrent)
            self.snPro = self.snCurrent
        else:
            self.lineEdit_SNCurrent.clear()
            self.snBool = False
        print(sn_CurDec)

    def hexCimDec(self, hexStr):
        print("hexStr:", hexStr)
        return str(int(hexStr.upper(), 16))

    def decCimHex(self, decStr):
        print("decStr:", decStr)
        return  str(hex(decStr))


    @pyqtSlot(str)
    def on_comboBox_proMode_currentTextChanged(self, p0):
        # print(p0)
        if p0 == "Serial":
            # self.lineEdit_comPort.setReadOnly(False)
            self.lineEdit_comPort.setEnabled(True)
        else:
            # self.lineEdit_comPort.setReadOnly(True)
            self.lineEdit_comPort.setEnabled(False)

    @pyqtSlot(bool)
    def on_checkBox_MAC_clicked(self, checked):
        # print(checked)
        self.lineEdit_macInterval.setEnabled(checked)

    @pyqtSlot(bool)
    def on_checkBox_SN_clicked(self, checked):
        # print(checked)
        self.lineEdit_SNInterval.setEnabled(checked)

    @pyqtSlot(bool)
    def on_radioButton_manual_clicked(self, checked):
        if checked:
            self.lineEdit_macCurrent.clear()
            self.lineEdit_SNCurrent.clear()
            self.lineEdit_macCurrent.setReadOnly(False)
            self.lineEdit_SNCurrent.setReadOnly(False)
            self.proMode = 3
        else:
            self.lineEdit_macCurrent.setText(self.macCurrent)
            self.lineEdit_SNCurrent.setText(self.snCurrent)
            self.lineEdit_macCurrent.setReadOnly(True)
            self.lineEdit_SNCurrent.setReadOnly(True)
    @pyqtSlot(bool)
    def on_radioButton_singal_clicked(self, checked):
        self.on_radioButton_manual_clicked(not checked)
        self.proMode = 1
    @pyqtSlot(bool)
    def on_radioButton_continuous_clicked(self, checked):
        self.on_radioButton_manual_clicked(not checked)
        self.proMode = 2

    #修改烧写配置
    @pyqtSlot()
    def on_pushButton_modify_clicked(self):
        if self.pushButton_modify.text() == "保存":
            self.pushButton_modify.setText(self._translate("MainWindow", "编辑"))
            self.lineEdit_macStart.setEnabled(not True)
            self.lineEdit_macEnd.setEnabled(not True)
            self.lineEdit_macInterval.setEnabled(not True)
            self.lineEdit_SNStart.setEnabled(not True)
            self.lineEdit_SNEnd.setEnabled(not True)
            self.lineEdit_SNInterval.setEnabled(not True)
            self.writeConfXML()
            # self.macCal()
            # self.snCal()
        elif self.pushButton_modify.text() == "编辑":
            self.pushButton_modify.setText(self._translate("MainWindow", "保存"))
            self.lineEdit_macStart.setEnabled(not False)
            self.lineEdit_macEnd.setEnabled(not False)
            self.lineEdit_macInterval.setEnabled(not False)
            self.lineEdit_SNStart.setEnabled(not False)
            self.lineEdit_SNEnd.setEnabled(not False)
            self.lineEdit_SNInterval.setEnabled(not False)
            # self.macCurrent = self.lineEdit_macStart
            # self.lineEdit_macCurrent.setText(self.macCurrent)

    @pyqtSlot(str)
    def on_lineEdit_macStart_textChanged(self, p0):
        pass

    @pyqtSlot(str)
    def on_lineEdit_SNStart_textChanged(self, p0):
        pass

    @pyqtSlot(str)
    def on_lineEdit_ipAddr_textChanged(self, p0):
        self.ipAddr = p0

    #点击开始按钮
    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        print("macPro", self.macPro)
        ip = self.lineEdit_ipAddr.text()
        if self.snBool and self.macBool:
            self.pushButton_start.setEnabled(False)
            self.proTh = ProThread(self.proMode, ip, self.macPro, self.snPro, self.logQueue)
            self.proTh.signal.connect(self.on_pushButton_start_enable)
            self.tbTh = TBThread(self.logQueue, self.textBrowser)
            self.proTh.start()
            self.tbTh.start()
            # self.macCal()
            # self.snCal()
        elif self.snBool:
            self.textBrowser.append("SN地址已超出使用完毕，请重新设置新号段")
        elif self.macBool:
            self.textBrowser.append("MAC地址已超出使用完毕，请重新设置新号段")
        else:
            print("烧写状态获取失败")

    def on_pushButton_start_enable(self, checked):
        self.pushButton_start.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_stop_clicked(self):
        self.pushButton_start.setEnabled(True)

class ProThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(bool)
    def __init__(self, proMode, ipAddr, macPro, snPro, queue, parent=None):
        super(ProThread,self).__init__(parent)
        self.programing = Programing()
        self.proMode = proMode
        self.ipAddr = ipAddr
        self.macPro = macPro
        self.snPro = snPro
        self.logQueue = queue

    def run(self):
        if self.proMode == 1:
            self.programing.signalPro(self.ipAddr, self.macPro, self.snPro, self.logQueue)
        elif self.proMode == 2:
            pass
        elif self.proMode == 3:
            pass
        elif self.proMode == 0:
            self.logQueue.put("请选择升级方式...")
        self.signal.emit(True)

class TBThread(QtCore.QThread):

    def __init__(self, queue, textBrowser, parent=None):
        super(TBThread, self).__init__(parent)
        self.logQueue = queue
        self.textBrowser = textBrowser

    def run(self):
        logStr = ""
        while  logStr != "finish" and logStr != "interrupt":
            self.textBrowser.append(logStr)
            logStr = self.logQueue.get()

class BurnLog(object):

    def __init__(self):
        pass






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
    

