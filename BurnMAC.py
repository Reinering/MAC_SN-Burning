# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import xml.dom.minidom
from hgu import *
from queue import Queue

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
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        self.logQueue = Queue()
        self.parseConfXML()
        self.proMode = 0
        self.macPro = ""
        self.snPro = ""
        self.ipAddr = ""

    def parseConfXML(self):
        def get_xmlData(root, tagName):
            itemList = root.getElementsByTagName(tagName)
            return itemList[0].firstChild.data

        doc = xml.dom.minidom.parse("config.xml")
        root = doc.documentElement
        # print("nodeName:", root.nodeName)
        self.ipAddr = get_xmlData(root, "ipAddr")
        self.macStart = get_xmlData(root, "macStart")
        self.macEnd = get_xmlData(root, "macEnd")
        self.macInter = get_xmlData(root, "macInter")
        self.macCurrent = get_xmlData(root, "macCurrent")
        self.snStart = get_xmlData(root, "snStart")
        self.snEnd = get_xmlData(root, "snEnd")
        self.snInter = get_xmlData(root, "snInter")
        self.snCurrent = get_xmlData(root, "snCurrent")

        self.lineEdit_ipAddr.setText(self.ipAddr)
        self.lineEdit_macStart.setText(self.macStart)
        self.lineEdit_macEnd.setText(self.macEnd)
        self.lineEdit_macInterval.setText(self.macInter)
        self.lineEdit_SNStart.setText(self.snStart)
        self.lineEdit_SNEnd.setText(self.snEnd)
        self.lineEdit_SNInterval.setText(self.snInter)

        if self.snCurrent == "" :
            self.snCurrent = self.lineEdit_SNStart
            self.lineEdit_SNCurrent.setText(self.snCurrent)
        elif self.snCurrent == self.lineEdit_macEnd:
            self.textBrowser.append("此SN号段已使用完，请另准备烧写号段")
        else:
            self.lineEdit_SNCurrent.setText(self.snCurrent)

        if self.macCurrent == "" and self.macCurrent == "000000000000":
            self.macCurrent = "000000000001"
            self.lineEdit_macCurrent.setText(self.macCurrent)
        elif self.macCurrent == self.lineEdit_macEnd:
            self.textBrowser.append("此MAC号段已使用完，请另准备烧写号段")
        elif self.macCurrent == "":
            self.macCurrent = self.lineEdit_macStart
            self.lineEdit_macCurrent.setText(self.macCurrent)
        else:
            self.lineEdit_macCurrent.setText(self.macCurrent)


    def writeConfXML(self):
        pass

    def macCal(self):
        mac_StartDec = self.hexCimDec(self.lineEdit_macStart.text())
        mac_EndDec = self.hexCimDec(self.lineEdit_macEnd.text())
        mac_CurDec = self.hexCimDec(self.lineEdit_macCurrent.text())
        mac_Inter = self.lineEdit_macInterval.text()







    def snCal(self):
        pass

    def hexCimDec(self, hexStr):
        return str(int(hexStr.upper(), 16))

    def decCimHex(self, decStr):
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

    @pyqtSlot()
    def on_pushButton_modify_clicked(self):
        if self.lineEdit_macStart.isEnabled():
            self.pushButton_modify.setText(self._translate("MainWindow", "编辑"))
            self.lineEdit_macStart.setEnabled(not True)
            self.lineEdit_macEnd.setEnabled(not True)
            self.lineEdit_macInterval.setEnabled(not True)
            self.lineEdit_SNStart.setEnabled(not True)
            self.lineEdit_SNEnd.setEnabled(not True)
            self.lineEdit_SNInterval.setEnabled(not True)
        else:
            self.pushButton_modify.setText(self._translate("MainWindow", "取消编辑"))
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

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        self.pushButton_start.setEnabled(False)
        print(self.proMode)
        self.proTh = ProThread(self.proMode, self.ipAddr, self.macPro, self.snPro, self.logQueue)
        self.proTh.signal.connect(self.on_pushButton_start_enable)
        self.tbTh = TBThread(self.logQueue, self.textBrowser)
        self.proTh.start()
        self.tbTh.start()
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
        while  logStr != "finish":
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
    

