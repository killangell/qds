# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sys_setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from qds import qds_test_authorize, qds_test_registration
from utils.config_helper import ConfigData, ConfigHelper


class Ui_obj_sys_setting(object):
    def setupUi(self, obj_sys_setting):
        obj_sys_setting.setObjectName("obj_sys_setting")
        obj_sys_setting.setWindowModality(QtCore.Qt.ApplicationModal)
        obj_sys_setting.resize(439, 300)
        self.tab_sys_setting = QtWidgets.QTabWidget(obj_sys_setting)
        self.tab_sys_setting.setGeometry(QtCore.QRect(0, 0, 441, 301))
        self.tab_sys_setting.setObjectName("tab_sys_setting")
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
        self.btn_authorize = QtWidgets.QPushButton(self.tab_huobi)
        self.btn_authorize.setGeometry(QtCore.QRect(110, 150, 121, 31))
        self.btn_authorize.setObjectName("btn_authorize")
        self.btn_authorize_test = QtWidgets.QPushButton(self.tab_huobi)
        self.btn_authorize_test.setGeometry(QtCore.QRect(280, 150, 121, 31))
        self.btn_authorize_test.setObjectName("btn_authorize_test")
        self.tabWidget_2.addTab(self.tab_huobi, "")
        """
        self.tab_okex = QtWidgets.QWidget()
        self.tab_okex.setObjectName("tab_okex")
        self.tabWidget_2.addTab(self.tab_okex, "")
        """
        self.tab_sys_setting.addTab(self.tab_authorize, "")
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
        self.btn_save_registration_info = QtWidgets.QPushButton(self.tab_register)
        self.btn_save_registration_info.setGeometry(QtCore.QRect(110, 220, 121, 31))
        self.btn_save_registration_info.setObjectName("btn_save_registration_info")
        self.txt_registration_info = QtWidgets.QTextEdit(self.tab_register)
        self.txt_registration_info.setGeometry(QtCore.QRect(110, 170, 291, 31))
        self.txt_registration_info.setObjectName("txt_registration_info")
        self.label_4 = QtWidgets.QLabel(self.tab_register)
        self.label_4.setGeometry(QtCore.QRect(20, 20, 401, 21))
        self.label_4.setObjectName("label_4")
        self.btn_registration_info_test = QtWidgets.QPushButton(self.tab_register)
        self.btn_registration_info_test.setGeometry(QtCore.QRect(280, 220, 121, 31))
        self.btn_registration_info_test.setObjectName("btn_registration_info_test")
        self.tab_sys_setting.addTab(self.tab_register, "")

        self.retranslateUi(obj_sys_setting)
        self.tab_sys_setting.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(obj_sys_setting)

        self.setup_connection()

    def retranslateUi(self, obj_sys_setting):
        _translate = QtCore.QCoreApplication.translate
        obj_sys_setting.setWindowTitle(_translate("obj_sys_setting", "系统设置"))
        self.label.setText(_translate("obj_sys_setting", "Access Key"))
        self.label_2.setText(_translate("obj_sys_setting", "Secret Key"))
        self.btn_authorize.setText(_translate("obj_sys_setting", "确认授权"))
        self.btn_authorize_test.setText(_translate("obj_sys_setting", "测试授权"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_huobi), _translate("obj_sys_setting", "Huobi"))
        # self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_okex), _translate("obj_sys_setting", "OKEx"))
        self.tab_sys_setting.setTabText(self.tab_sys_setting.indexOf(self.tab_authorize), _translate("obj_sys_setting", "交易授权"))
        self.label_3.setText(_translate("obj_sys_setting", "您的邮箱地址"))
        self.btn_register.setText(_translate("obj_sys_setting", "提交注册"))
        self.btn_save_registration_info.setText(_translate("obj_sys_setting", "保存注册信息"))
        self.label_4.setText(_translate("obj_sys_setting", "第一步:提交注册，第二步:等待作者返回注册信息，第三步:保存注册信息"))
        self.btn_registration_info_test.setText(_translate("obj_sys_setting", "测试注册信息"))
        self.tab_sys_setting.setTabText(self.tab_sys_setting.indexOf(self.tab_register), _translate("obj_sys_setting", "软件注册"))
        self.get_authorize()
        self.get_registration_info()

    def setup_connection(self):
        self.btn_authorize.clicked.connect(self.set_authorize)
        self.btn_authorize_test.clicked.connect(self.test_authorize)
        self.btn_save_registration_info.clicked.connect(self.save_registration_info)
        self.btn_registration_info_test.clicked.connect(self.test_registration_info)

    def set_authorize(self):
        access_key = self.txt_access_key.toPlainText().strip()
        secret_key = self.txt_secret_key.toPlainText().strip()
        if not access_key or not secret_key:
            QMessageBox.information(self, '提示', '信息不完整')
            return
        file = 'config.xml'
        config_helper = ConfigHelper(file)
        config_to_save = ConfigData()
        ret = config_helper.init_root()
        if ret:
            config_helper.parse(config_to_save)
            config_to_save._access_key = access_key
            config_to_save._secret_key = secret_key
            config_helper.save(config_to_save)
            QMessageBox.information(self, '提示', '信息已保存，重启软件生效')
        else:
            QMessageBox.information(self, '提示', '配置文件config.xml出错')

    def test_authorize(self):
        ret = qds_test_authorize()
        if ret:
            QMessageBox.information(self, '提示', '授权测试成功')
        else:
            QMessageBox.information(self, '提示', '授权测试失败')

    def get_authorize(self):
        file = 'config.xml'
        config_helper = ConfigHelper(file)
        config = ConfigData()
        ret = config_helper.init_root()
        if ret:
            config_helper.parse(config)
            self.txt_access_key.setText(config._access_key)
            self.txt_secret_key.setText(config._secret_key)
        else:
            QMessageBox.information(self, '提示', '配置文件config.xml出错')

    def save_registration_info(self):
        registration_info = self.txt_registration_info.toPlainText().strip()
        if not registration_info:
            QMessageBox.information(self, '提示', '注册信息不完整')
            return
        file = 'config.xml'
        config_helper = ConfigHelper(file)
        config_to_save = ConfigData()
        ret = config_helper.init_root()
        if ret:
            config_helper.parse(config_to_save)
            config_to_save._qds_id = registration_info
            config_helper.save(config_to_save)
            QMessageBox.information(self, '提示', '信息已保存, 重启软件生效')
        else:
            QMessageBox.information(self, '警告', '配置文件config.xml出错')

    def test_registration_info(self):
        ret = qds_test_registration()
        if ret:
            QMessageBox.information(self, '提示', '注册信息正确')
        else:
            QMessageBox.information(self, '提示', '注册信息错误')

    def get_registration_info(self):
        file = 'config.xml'
        config_helper = ConfigHelper(file)
        config = ConfigData()
        ret = config_helper.init_root()
        if ret:
            config_helper.parse(config)
            self.txt_registration_info.setText(config._qds_id)
        else:
            QMessageBox.information(self, '提示', '配置文件config.xml出错')