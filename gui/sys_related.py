# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sys_related.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!



from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_obj_sys_related(object):
    def setupUi(self, obj_sys_related):
        obj_sys_related.setObjectName("obj_sys_related")
        obj_sys_related.setWindowModality(QtCore.Qt.ApplicationModal)
        obj_sys_related.resize(439, 300)
        self.tabWidget = QtWidgets.QTabWidget(obj_sys_related)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 441, 301))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_params = QtWidgets.QWidget()
        self.tab_params.setObjectName("tab_params")
        self.textEdit = QtWidgets.QTextEdit(self.tab_params)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 441, 281))
        self.textEdit.setObjectName("textEdit")
        self.tabWidget.addTab(self.tab_params, "")
        self.tab_authorize = QtWidgets.QWidget()
        self.tab_authorize.setObjectName("tab_authorize")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_authorize)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 441, 281))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_huobi = QtWidgets.QWidget()
        self.tab_huobi.setObjectName("tab_huobi")
        self.label = QtWidgets.QLabel(self.tab_huobi)
        self.label.setGeometry(QtCore.QRect(30, 60, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_huobi)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 61, 16))
        self.label_2.setObjectName("label_2")
        self.txt_access_key = QtWidgets.QTextEdit(self.tab_huobi)
        self.txt_access_key.setGeometry(QtCore.QRect(110, 50, 291, 31))
        self.txt_access_key.setObjectName("txt_access_key")
        self.txt_secret_key = QtWidgets.QTextEdit(self.tab_huobi)
        self.txt_secret_key.setGeometry(QtCore.QRect(110, 100, 291, 31))
        self.txt_secret_key.setObjectName("txt_secret_key")
        self.tabWidget_2.addTab(self.tab_huobi, "")
        self.tab_okex = QtWidgets.QWidget()
        self.tab_okex.setObjectName("tab_okex")
        self.tabWidget_2.addTab(self.tab_okex, "")
        self.tabWidget.addTab(self.tab_authorize, "")
        self.tab_register = QtWidgets.QWidget()
        self.tab_register.setObjectName("tab_register")
        self.label_3 = QtWidgets.QLabel(self.tab_register)
        self.label_3.setGeometry(QtCore.QRect(30, 80, 71, 16))
        self.label_3.setObjectName("label_3")
        self.txt_mail_address = QtWidgets.QTextEdit(self.tab_register)
        self.txt_mail_address.setGeometry(QtCore.QRect(110, 70, 291, 31))
        self.txt_mail_address.setObjectName("txt_mail_address")
        self.btn_register = QtWidgets.QPushButton(self.tab_register)
        self.btn_register.setGeometry(QtCore.QRect(110, 120, 121, 31))
        self.btn_register.setObjectName("btn_register")
        self.tabWidget.addTab(self.tab_register, "")

        self.retranslateUi(obj_sys_related)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(obj_sys_related)

    def retranslateUi(self, obj_sys_related):
        _translate = QtCore.QCoreApplication.translate
        obj_sys_related.setWindowTitle(_translate("obj_sys_related", "系统相关"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_params), _translate("obj_sys_related", "参数说明"))
        self.label.setText(_translate("obj_sys_related", "Access Key"))
        self.label_2.setText(_translate("obj_sys_related", "Secret Key"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_huobi), _translate("obj_sys_related", "Huobi"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_okex), _translate("obj_sys_related", "OKEx"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_authorize), _translate("obj_sys_related", "交易授权"))
        self.label_3.setText(_translate("obj_sys_related", "您的邮箱地址"))
        self.btn_register.setText(_translate("obj_sys_related", "提交注册"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_register), _translate("obj_sys_related", "软件注册"))
