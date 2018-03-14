# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import xml.dom.minidom

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
        self.parseConfXML()



    def parseConfXML(self):
        def get_xmlData(root, tagName):
            itemList = root.getElementsByTagName(tagName)
            return itemList[0].firstChild.data

        doc = xml.dom.minidom.parse("config.xml")
        root = doc.documentElement
        # print("nodeName:", root.nodeName)
        ipAddr = get_xmlData(root, "ipAddr")
        macStart = get_xmlData(root, "macStart")
        macEnd = get_xmlData(root, "macEnd")
        macInter = get_xmlData(root, "macInter")
        self.macCurrent = get_xmlData(root, "macCurrent")
        snStart = get_xmlData(root, "snStart")
        snEnd = get_xmlData(root, "snEnd")
        snInter = get_xmlData(root, "snInter")
        self.snCurrent = get_xmlData(root, "snCurrent")

        self.lineEdit_ipAddr.setText(ipAddr)
        self.lineEdit_macStart.setText(macStart)
        self.lineEdit_macEnd.setText(macEnd)
        self.lineEdit_macCurrent.setText(self.macCurrent)
        self.lineEdit_macInterval.setText(macInter)
        self.lineEdit_SNStart.setText(snStart)
        self.lineEdit_SNEnd.setText(snEnd)
        self.lineEdit_SNInterval.setText(snInter)
        self.lineEdit_SNCurrent.setText(self.snCurrent)


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
        self.lineEdit_macStart.setEnabled(not checked)
        self.lineEdit_macEnd.setEnabled(not checked)
        self.checkBox_MAC.setEnabled(not checked)
        self.lineEdit_macInterval.setEnabled(not checked)
        self.lineEdit_SNStart.setEnabled(not checked)
        self.lineEdit_SNEnd.setEnabled(not checked)
        self.lineEdit_SNInterval.setEnabled(not checked)
        self.checkBox_SN.setEnabled(not checked)
        if checked:
            self.lineEdit_macCurrent.clear()
            self.lineEdit_SNCurrent.clear()
        else:
            self.lineEdit_macCurrent.setText(self.macCurrent)
            self.lineEdit_SNCurrent.setText(self.snCurrent)

    @pyqtSlot(bool)
    def on_radioButton_singal_clicked(self, checked):
        self.on_radioButton_manual_clicked(not checked)
    @pyqtSlot(bool)
    def on_radioButton_continuous_clicked(self, checked):
        self.on_radioButton_manual_clicked(not checked)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
    

