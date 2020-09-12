# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'risk.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_obj_risk(object):
    def setupUi(self, obj_risk):
        obj_risk.setObjectName("obj_risk")
        obj_risk.setWindowModality(QtCore.Qt.ApplicationModal)
        obj_risk.resize(433, 300)
        self.txt_risk = QtWidgets.QPlainTextEdit(obj_risk)
        self.txt_risk.setGeometry(QtCore.QRect(0, 0, 431, 301))
        self.txt_risk.setObjectName("txt_risk")

        self.retranslateUi(obj_risk)
        QtCore.QMetaObject.connectSlotsByName(obj_risk)

    def retranslateUi(self, obj_risk):
        _translate = QtCore.QCoreApplication.translate
        obj_risk.setWindowTitle(_translate("obj_risk", "交易警告"))
        self.txt_risk.setPlainText("1. 该系统为一种以EMA金叉死叉为依据的辅助交易系统，并不提供具体交易策略，盈亏自负。\n"
                                    "2. 系统依赖第三方交易机构的的API接口，所以在网络连接不畅，或者网络中断，以及第三方交易机构服务异常的情况下，会出现挂单/平仓失败的情况，盈亏自负。\n"
                                    "3. 软件本身可能有逻辑或者功能问题，也可能导致挂单/平仓出现问题，切忌重仓操作，盈亏自负。"
                                   )
