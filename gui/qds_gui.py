# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qds_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import logging
import os
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from gui.risk_window import RiskWindow
from gui.sw_doc_window import SWDOCWindow
# from gui.xml_rc import *
from qds import set_buniness_enabled, get_business_enabled, run_business, cancell_all_contract, close_all_contract
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from gui.sys_setting_window import SysSettingWindow
from utils.config_helper import ConfigHelper, ConfigData
from global_data.system import set_system_running, get_system_running, get_margin
from res_rc import *

start_point = 0
lbl_cash = None
g_config = ConfigData()

class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一�?
    #  通过类成员对象定义信号对�?
    _signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # self._signal.emit('hello');  # 可以在这里写信号焕发
        while True:
            # self._signal.emit('hello');  # 可以在这里写信号焕发
            self.read_logs()
            available, balance = get_margin()
            if lbl_cash:
                lbl_cash.setText("BTC: 可用：{0}  资产：{1}".format(available, balance))
            time.sleep(1)
        # logging.debug("stop reading logs")

    def callback(self, msg):
        pass

    def read_logs(self):
        log_file = "qds.log".format(os.getcwd())
        if not os.path.exists(log_file):
            return
        fo = open(log_file, "rb")
        # print("文件名为: ", fo.name)
        global start_point  # 使用全局变量，让start_point 时刻保持在已经输出过的那个字节位
        fo.seek(start_point, 1)  # 移动文件读取指针到指定位�?
        for line in fo.readlines():
            # print("读取的数据为:" + str(line.decode()))
            self._signal.emit(str(line.decode()))
        # 输出后的指针位置赋值给start_piont
        start_point = fo.tell()
        fo.close()


class Runthread_Business(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一�?
    #  通过类成员对象定义信号对�?
    _signal = pyqtSignal(str)

    def __init__(self, p=None, mf=None, ms=None, oo=None, oi=None, so=None, lr=None, mn=None, parent=None):
        super(Runthread_Business, self).__init__()
        self.period = p
        self.ma_fast = mf
        self.ma_slow = ms
        self.open_offset = oo
        self.open_interval = oi
        self.stop_offset = so
        self.level_rate = lr
        self.max_open_number = mn

        self.setTerminationEnabled(True)

    def __del__(self):
        self.wait()

    def run(self):
        # self._signal.emit('hello');  # 可以在这里写信号焕发
        count = 0
        while get_system_running():
            set_buniness_enabled(True)
            if count % 60 == 0:
                try:
                    logging.debug("running count={0}".format(int(count / 60)))
                    run_business(self.period, self.ma_fast, self.ma_slow, self.open_offset, self.open_interval,
                                 self.stop_offset, self.level_rate, self.max_open_number)
                except Exception as e:
                    pass
            count += 1
            time.sleep(1)

        logging.debug("stop trading")
        set_buniness_enabled(False)



class Ui_qds_gui(object):
    def run_reading_thread(self, enabled):
        if enabled:
            # 创建线程
            self.thread = Runthread()
            # 连接信号
            self.thread._signal.connect(self.callbacklog)
            # 开始线�?
            self.thread.start()
        else:
            self.thread._signal.disconnect(self.callbacklog)
            self.thread.wait()

    def callbacklog(self, msg):
        # 将回调数据输出到文本�?
        self.txt_log.appendPlainText(msg)

    def run_business_thread(self, enabled, period=None, ema_fast=None, ema_slow=None, open_offset=None,
                            open_interval=None, stop_offset=None, level_rate=None, max_number=None):
        if enabled:
            set_buniness_enabled(True)
            self.thread2 = Runthread_Business(period, ema_fast, ema_slow, open_offset, open_interval,
                                              stop_offset, level_rate, max_number)
            self.thread2.start()
        else:
            set_buniness_enabled(False)
            # self.thread2.terminate()
            self.thread2.wait()

    def setupUi(self, qds_gui):
        qds_gui.setObjectName("qds_gui")
        qds_gui.resize(940, 800)
        qds_gui.setMinimumSize(QtCore.QSize(0, 0))
        qds_gui.setAutoFillBackground(True)
        self.groupBox = QtWidgets.QGroupBox(qds_gui)
        self.groupBox.setGeometry(QtCore.QRect(10, 40, 401, 381))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 90, 54, 12))
        self.label.setObjectName("label")
        self.cbx_category = QtWidgets.QComboBox(self.groupBox)
        self.cbx_category.setGeometry(QtCore.QRect(100, 80, 81, 31))
        self.cbx_category.setObjectName("cbx_category")
        self.cbx_category.addItems(['BTC当季'])
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 140, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(230, 140, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 190, 54, 12))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(30, 240, 54, 12))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(30, 290, 54, 12))
        self.label_9.setObjectName("label_9")
        self.txt_ema_fast = QtWidgets.QTextEdit(self.groupBox)
        self.txt_ema_fast.setGeometry(QtCore.QRect(100, 130, 81, 31))
        self.txt_ema_fast.setObjectName("txt_ema_fast")
        self.txt_ema_slow = QtWidgets.QTextEdit(self.groupBox)
        self.txt_ema_slow.setGeometry(QtCore.QRect(300, 130, 81, 31))
        self.txt_ema_slow.setObjectName("txt_ema_slow")
        self.txt_open_offset = QtWidgets.QTextEdit(self.groupBox)
        self.txt_open_offset.setGeometry(QtCore.QRect(100, 180, 81, 31))
        self.txt_open_offset.setObjectName("txt_open_offset")
        self.txt_stop_earning_offset = QtWidgets.QTextEdit(self.groupBox)
        self.txt_stop_earning_offset.setGeometry(QtCore.QRect(100, 230, 81, 31))
        self.txt_stop_earning_offset.setObjectName("txt_stop_earning_offset")
        self.txt_level_rate = QtWidgets.QTextEdit(self.groupBox)
        self.txt_level_rate.setGeometry(QtCore.QRect(100, 280, 81, 31))
        self.txt_level_rate.setObjectName("txt_level_rate")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(230, 90, 54, 12))
        self.label_10.setObjectName("label_10")
        self.cbx_period = QtWidgets.QComboBox(self.groupBox)
        self.cbx_period.setGeometry(QtCore.QRect(300, 80, 81, 31))
        self.cbx_period.setObjectName("cbx_period")
        self.cbx_period.addItems(['1min', '5min', '15min', '30min', '60min', '4hour', '1day', '1mon'])
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(230, 290, 54, 12))
        self.label_12.setObjectName("label_12")
        self.txt_max_num = QtWidgets.QTextEdit(self.groupBox)
        self.txt_max_num.setGeometry(QtCore.QRect(300, 280, 81, 31))
        self.txt_max_num.setObjectName("txt_max_num")
        self.txt_stop_loss_offset = QtWidgets.QTextEdit(self.groupBox)
        self.txt_stop_loss_offset.setGeometry(QtCore.QRect(300, 230, 81, 31))
        self.txt_stop_loss_offset.setObjectName("txt_stop_loss_offset")
        self.txt_stop_loss_offset.setEnabled(False)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(230, 240, 54, 12))
        self.label_11.setObjectName("label_11")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(230, 190, 54, 12))
        self.label_13.setObjectName("label_13")
        self.txt_open_interval = QtWidgets.QTextEdit(self.groupBox)
        self.txt_open_interval.setGeometry(QtCore.QRect(300, 180, 81, 31))
        self.txt_open_interval.setObjectName("txt_open_interval")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 40, 54, 12))
        self.label_4.setObjectName("label_4")
        self.cbx_exchange = QtWidgets.QComboBox(self.groupBox)
        self.cbx_exchange.setGeometry(QtCore.QRect(100, 30, 281, 31))
        self.cbx_exchange.setObjectName("cbx_exchange")
        self.cbx_exchange.addItems(['Huobi'])
        self.btn_switch = QtWidgets.QPushButton(self.groupBox)
        self.btn_switch.setGeometry(QtCore.QRect(100, 330, 81, 31))
        self.btn_switch.setObjectName("btn_switch")
        self.btn_reset = QtWidgets.QPushButton(self.groupBox)
        self.btn_reset.setGeometry(QtCore.QRect(300, 330, 81, 31))
        self.btn_reset.setObjectName("btn_reset")
        self.lbl_total_cash = QtWidgets.QLabel(qds_gui)
        self.lbl_total_cash.setGeometry(QtCore.QRect(440, 30, 300, 41))
        self.lbl_total_cash.setObjectName("lbl_total_cash")
        self.frame = QtWidgets.QFrame(qds_gui)
        self.frame.setGeometry(QtCore.QRect(430, 80, 491, 311))
        self.frame.setAutoFillBackground(False)
        # self.frame.setStyleSheet("background-image: url(:/newPrefix/back.png);")
        self.frame.setStyleSheet("background-image: url(:/res/res/back.png);")
        self.setWindowIcon(QIcon('res/qds.ico'))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.txt_log = QtWidgets.QPlainTextEdit(qds_gui)
        self.txt_log.setGeometry(QtCore.QRect(10, 430, 921, 361))
        self.txt_log.setObjectName("txt_log")

        # 实例化主窗口的QMenuBar对象
        bar = self.menuBar()
        sys_menu = bar.addMenu('系统设置')
        sys_authorize = QAction('交易授权', self)
        sys_authorize.triggered.connect(self.authorize_window)
        sys_menu.addAction(sys_authorize)
        sys_action_register = QAction('软件注册', self)
        sys_action_register.triggered.connect(self.register_window)
        sys_menu.addAction(sys_action_register)

        trade_menu = bar.addMenu('交易操作')
        trade_call_all_contract = QAction('撤销所有挂单', self)
        trade_call_all_contract.triggered.connect(self.cancell_all_contract)
        trade_menu.addAction(trade_call_all_contract)
        trade_close_all_contract = QAction('平仓所有持仓', self)
        trade_close_all_contract.triggered.connect(self.close_all_contract)
        trade_menu.addAction(trade_close_all_contract)

        sw_doc_menu = bar.addMenu("软件说明")
        func_doc = QAction("功能说明", self)
        func_doc.triggered.connect(self.func_window)
        sw_doc_menu.addAction(func_doc)
        param_doc = QAction('参数说明', self)
        param_doc.triggered.connect(self.params_window)
        sw_doc_menu.addAction(param_doc)
        author_doc = QAction("关于作者", self)
        author_doc.triggered.connect(self.author_window)
        sw_doc_menu.addAction(author_doc)
        qa_doc = QAction("Q && A", self)
        qa_doc.triggered.connect(self.qa_window)
        sw_doc_menu.addAction(qa_doc)

        risk_menu = bar.addMenu("交易风险")
        warning_action = QAction("交易警告", self)
        warning_action.triggered.connect(self.risk)
        risk_menu.addAction(warning_action)

        self.retranslateUi(qds_gui)
        self.btn_switch.clicked.connect(self.btn_switch_click)
        self.btn_reset.clicked.connect(self.set_default)
        QtCore.QMetaObject.connectSlotsByName(qds_gui)

        self.thread = Runthread()
        # 连接信号
        self.thread._signal.connect(self.callbacklog)
        # 开始线程
        self.thread.start()
        self.get_params()
        self.pop_risk_window()

        global lbl_cash
        lbl_cash = self.lbl_total_cash

    def cancell_all_contract(self):
        if get_system_running():
            QMessageBox.information(self, '提示', '该功能只能在停止运行后使用')
        else:
            cancell_all_contract()

    def close_all_contract(self):
        if get_system_running():
            QMessageBox.information(self, '提示', '该功能只能在停止运行后使用')
        else:
            close_all_contract()

    def get_params(self):
        file = 'config.xml'
        config_helper = ConfigHelper(file)
        config = ConfigData()
        global g_config
        g_config = config
        ret = config_helper.init_root()
        if ret:
            config_helper.parse(config)
            self.cbx_period.setCurrentText(config._period)
            self.txt_ema_fast.setText(config._ema_fast)
            self.txt_ema_slow.setText(config._ema_slow)
            self.txt_open_offset.setText(config._open_offset)
            self.txt_open_interval.setText(config._open_interval)
            self.txt_stop_earning_offset.setText(config._stop_earning_offset)
            self.txt_stop_loss_offset.setText("0")
            self.txt_level_rate.setText(config._level_rate)
            self.txt_max_num.setText(config._max_open_number)
        else:
            QMessageBox.information(self, '提示', '配置文件config.xml出错')

    def set_params(self):
        period = self.cbx_period.currentText().strip()
        ema_fast = self.txt_ema_fast.toPlainText().strip()
        ema_slow = self.txt_ema_slow.toPlainText().strip()
        open_offset = self.txt_open_offset.toPlainText().strip()
        open_interval = self.txt_open_interval.toPlainText().strip()
        stop_earning_offset = self.txt_stop_earning_offset.toPlainText().strip()
        stop_loss_offset = self.txt_stop_loss_offset.toPlainText().strip()
        level_rate = self.txt_level_rate.toPlainText().strip()
        max_number = self.txt_max_num.toPlainText().strip()

        file = 'config.xml'
        config_helper = ConfigHelper(file)
        config_to_save = ConfigData()
        ret = config_helper.init_root()
        if ret:
            config_helper.parse(config_to_save)
            config_to_save._period = period
            config_to_save._ema_fast = ema_fast
            config_to_save._ema_slow = ema_slow
            config_to_save._open_offset = open_offset
            config_to_save._open_interval = open_interval
            config_to_save._stop_earning_offset = stop_earning_offset
            config_to_save._level_rate = level_rate
            config_to_save._max_open_number = max_number
            config_helper.save(config_to_save)
        else:
            QMessageBox.information(self, '提示', '配置文件config.xml出错')

    def pop_sys_setting_window(self, page_index=0):
        self.ui = SysSettingWindow()
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.tab_sys_setting.setCurrentIndex(page_index)
        self.ui.show()

    def authorize_window(self):
        self.pop_sys_setting_window(0)

    def register_window(self):
        self.pop_sys_setting_window(1)

    def pop_sw_doc_window(self, page_index=0):
        self.ui = SWDOCWindow()
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.tab_sw_doc.setCurrentIndex(page_index)
        self.ui.show()

    def func_window(self):
        self.pop_sw_doc_window(0)

    def params_window(self):
        self.pop_sw_doc_window(1)

    def author_window(self):
        self.pop_sw_doc_window(2)

    def qa_window(self):
        self.pop_sw_doc_window(3)

    def pop_risk_window(self):
        self.ui = RiskWindow()
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.show()

    def risk(self):
        self.pop_risk_window()

    def btn_switch_click(self):
        if not get_system_running():
            exchange = self.cbx_exchange.currentText()
            category = self.cbx_category.currentText()
            period = self.cbx_period.currentText()
            ema_slow = self.txt_ema_slow.toPlainText()
            ema_fast = self.txt_ema_fast.toPlainText()
            open_offset = self.txt_open_offset.toPlainText()
            open_interval = self.txt_open_interval.toPlainText()
            stop_earning_offset = self.txt_stop_earning_offset.toPlainText()
            stop_loss_offset = self.txt_stop_loss_offset.toPlainText()
            level_rate = self.txt_level_rate.toPlainText()
            max_number = self.txt_max_num.toPlainText()

            ema_fast_good = True
            ema_slow_good = True
            if not self.is_number(ema_fast) or int(ema_fast) < 0:
                ema_fast_good = False
                self.txt_ema_fast.setText('请输入大于0的整数')
                self.txt_ema_fast.setFocus()
                return
            if not self.is_number(ema_slow) or int(ema_slow) < 0:
                ema_slow_good = False
                self.txt_ema_slow.setText('请输入大于0的整数')
                self.txt_ema_slow.setFocus()
                return
            if ema_fast_good and ema_slow_good and int(ema_fast) >= int(ema_slow):
                self.txt_ema_slow.setText('慢线需大于快线')
                self.txt_ema_slow.setFocus()
                return

            if open_offset and not self.is_number(open_offset):
                self.txt_open_offset.setText('请输入整数')
                self.txt_open_offset.setFocus()
                return
            if open_interval and not self.is_number(open_interval):
                self.txt_open_interval.setText('请输入整数')
                self.txt_open_interval.setFocus()
                return

            if not self.is_number(stop_earning_offset):
                self.txt_stop_earning_offset.setText('请输入大于0的整数')
                self.txt_stop_earning_offset.setFocus()
                return
            if not self.is_number(stop_loss_offset):
                self.txt_stop_loss_offset.setText('请输入大于0的整数')
                self.txt_stop_loss_offset.setFocus()
                return

            if not self.is_number(level_rate):
                self.txt_level_rate.setText('请输入大于0的整数')
                self.txt_level_rate.setFocus()
                return
            if not self.is_number(max_number):
                self.txt_max_num.setText('请输入大于0的整数')
                self.txt_max_num.setFocus()
                return
            global g_config
            if int(max_number) > 30 and not g_config._max_open_number_limit:
                self.txt_max_num.setText('最大只支持30张')
                self.txt_max_num.setFocus()
                return


            self.btn_switch.setText('停止')
            set_system_running(True)
            self.set_all_enabled(False)
            self.run_business_thread(True, period, ema_fast, ema_slow, open_offset, open_interval,
                                     stop_earning_offset, level_rate, max_number)
            self.set_params()
        else:
            self.btn_switch.setText('开始')
            set_system_running(False)
            self.run_business_thread(False)
            # self.run_reading_thread(False)
            self.set_all_enabled(True)

    def is_number(self, s):
        if s[0] == "-" or s[0] in "0123456789":
            if s.count(".") <= 1 and s.count("-") <= 1:
                s = s.replace("-", "").replace(".", "")
                # print (s)
                for i in s:
                    if i not in "0123456789":
                        return False
                else:  # 这个else与for对应
                    return True
            else:
                return False
        else:
            return False

    def retranslateUi(self, qds_gui):
        _translate = QtCore.QCoreApplication.translate
        qds_gui.setWindowTitle(_translate("qds_gui", "EMA双均线交易辅助系统"))
        self.groupBox.setTitle(_translate("qds_gui", "参数设置"))
        self.label_4.setText(_translate("qds_gui", "交易所"))
        self.label.setText(_translate("qds_gui", "交易品种"))
        self.label_10.setText(_translate("qds_gui", "交易周期"))
        self.label_2.setText(_translate("qds_gui", "EMA 快线"))
        self.label_3.setText(_translate("qds_gui", "EMA 慢线"))
        self.label_7.setText(_translate("qds_gui", "建仓偏移"))
        self.label_13.setText(_translate("qds_gui", "建仓间隔"))
        self.label_8.setText(_translate("qds_gui", "止盈偏移"))
        self.label_11.setText(_translate("qds_gui", "止损偏移"))
        self.label_9.setText(_translate("qds_gui", "杠杆倍数"))
        self.label_12.setText(_translate("qds_gui", "最大数量"))
        self.btn_switch.setText(_translate("qds_gui", "开始"))
        self.btn_reset.setText(_translate("qds_gui", "重置"))
        self.lbl_total_cash.setText(_translate("qds_gui", "总金额 $50"))
        self.set_default()

    def set_default(self):
        if get_system_running():
            return

        self.cbx_exchange.setCurrentIndex(0)
        self.cbx_category.setCurrentIndex(0)
        self.cbx_period.setCurrentIndex(3)
        self.txt_ema_fast.setText('7')
        self.txt_ema_slow.setText('30')
        self.txt_open_offset.setText('20')
        self.txt_open_interval.setText('0')
        self.txt_stop_earning_offset.setText('100')
        self.txt_stop_loss_offset.setText('0')
        self.txt_level_rate.setText('10')
        self.txt_max_num.setText('3')
        self.btn_switch.setText('开始')
        # self.txt_log.setPlainText('')

    def set_all_enabled(self, en):
        self.cbx_exchange.setEnabled(en)
        self.cbx_category.setEnabled(en)
        self.cbx_period.setEnabled(en)
        self.txt_ema_fast.setEnabled(en)
        self.txt_ema_slow.setEnabled(en)
        self.txt_open_offset.setEnabled(en)
        self.txt_open_interval.setEnabled(en)
        self.txt_stop_earning_offset.setEnabled(en)
        self.txt_stop_loss_offset.setEnabled(False)
        self.txt_level_rate.setEnabled(en)
        self.txt_max_num.setEnabled(en)
        self.btn_reset.setEnabled(en)

# import xml_rc
