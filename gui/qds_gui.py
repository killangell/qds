# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qds_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import os
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from xml_rc import *

start_point = 0
enable_read_log = False
system_running = False


class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # self._signal.emit('hello');  # 可以在这里写信号焕发
        while enable_read_log:
            # self._signal.emit('hello');  # 可以在这里写信号焕发
            self.read_logs()
            time.sleep(5)

    def callback(self, msg):
        pass

    def read_logs(self):
        log_file = "{0}\\..\\qds.log".format(os.getcwd())
        fo = open(log_file, "rb")  # 一定要用'rb'因为seek 是以bytes来计算的
        # print("文件名为: ", fo.name)
        global start_point  # 使用全局变量，让start_point 时刻保持在已经输出过的那个字节位
        fo.seek(start_point, 1)  # 移动文件读取指针到指定位置
        for line in fo.readlines():
            # print("读取的数据为:" + str(line.decode()))
            self._signal.emit(str(line.decode()))
        # 输出后的指针位置赋值给start_piont
        start_point = fo.tell()
        fo.close()


# 信号焕发，我是通过我封装类的回调来发起的


class Ui_qds_gui(object):
    def run_reading_log(self):
        global enable_read_log
        # 创建线程
        self.thread = Runthread()
        # 连接信号
        self.thread._signal.connect(self.callbacklog)
        # 开始线程
        enable_read_log = True
        self.thread.start()

    def run_reading_thread(self, enabled):
        global enable_read_log
        if enabled:
            # 创建线程
            self.thread = Runthread()
            # 连接信号
            self.thread._signal.connect(self.callbacklog)
            # 开始线程
            enable_read_log = True
            self.thread.start()
        else:
            enable_read_log = False
            self.thread._signal.disconnect(self.callbacklog)

    def callbacklog(self, msg):
        # 将回调数据输出到文本框
        self.txt_log.appendPlainText(msg)

    def setupUi(self, qds_gui):
        qds_gui.setObjectName("qds_gui")
        qds_gui.resize(941, 770)
        qds_gui.setMinimumSize(QtCore.QSize(0, 0))
        qds_gui.setAutoFillBackground(True)
        self.groupBox = QtWidgets.QGroupBox(qds_gui)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 401, 441))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 100, 54, 12))
        self.label.setObjectName("label")
        self.cbx_category = QtWidgets.QComboBox(self.groupBox)
        self.cbx_category.setGeometry(QtCore.QRect(100, 90, 81, 31))
        self.cbx_category.setObjectName("cbx_category")
        self.cbx_category.addItems(['BTC'])
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 160, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(230, 160, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 220, 54, 12))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(30, 280, 54, 12))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(30, 340, 54, 12))
        self.label_9.setObjectName("label_9")
        self.txt_ema_fast = QtWidgets.QTextEdit(self.groupBox)
        self.txt_ema_fast.setGeometry(QtCore.QRect(100, 150, 81, 31))
        self.txt_ema_fast.setObjectName("txt_ema_fast")
        self.txt_ema_slow = QtWidgets.QTextEdit(self.groupBox)
        self.txt_ema_slow.setGeometry(QtCore.QRect(300, 150, 81, 31))
        self.txt_ema_slow.setObjectName("txt_ema_slow")
        self.txt_one_time = QtWidgets.QTextEdit(self.groupBox)
        self.txt_one_time.setGeometry(QtCore.QRect(100, 210, 81, 31))
        self.txt_one_time.setObjectName("txt_one_time")
        self.txt_stop_earning_offset = QtWidgets.QTextEdit(self.groupBox)
        self.txt_stop_earning_offset.setGeometry(QtCore.QRect(100, 270, 81, 31))
        self.txt_stop_earning_offset.setObjectName("txt_stop_earning_offset")
        self.txt_level_rate = QtWidgets.QTextEdit(self.groupBox)
        self.txt_level_rate.setGeometry(QtCore.QRect(100, 330, 81, 31))
        self.txt_level_rate.setObjectName("txt_level_rate")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(230, 100, 54, 12))
        self.label_10.setObjectName("label_10")
        self.cbx_period = QtWidgets.QComboBox(self.groupBox)
        self.cbx_period.setGeometry(QtCore.QRect(300, 90, 81, 31))
        self.cbx_period.setObjectName("cbx_period")
        self.cbx_period.addItems(['1min', '5min', '15min', '30min', '60min', '4hour', '1day', '1mon'])
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(230, 340, 54, 12))
        self.label_12.setObjectName("label_12")
        self.txt_max_num = QtWidgets.QTextEdit(self.groupBox)
        self.txt_max_num.setGeometry(QtCore.QRect(300, 330, 81, 31))
        self.txt_max_num.setObjectName("txt_max_num")
        self.txt_stop_loss_offset = QtWidgets.QTextEdit(self.groupBox)
        self.txt_stop_loss_offset.setGeometry(QtCore.QRect(300, 270, 81, 31))
        self.txt_stop_loss_offset.setObjectName("txt_stop_loss_offset")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(230, 280, 54, 12))
        self.label_11.setObjectName("label_11")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(230, 220, 54, 12))
        self.label_13.setObjectName("label_13")
        self.txt_multi_times = QtWidgets.QTextEdit(self.groupBox)
        self.txt_multi_times.setGeometry(QtCore.QRect(300, 210, 81, 31))
        self.txt_multi_times.setObjectName("txt_multi_times")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 40, 54, 12))
        self.label_4.setObjectName("label_4")
        self.cbx_exchange = QtWidgets.QComboBox(self.groupBox)
        self.cbx_exchange.setGeometry(QtCore.QRect(100, 30, 281, 31))
        self.cbx_exchange.setObjectName("cbx_exchange")
        self.cbx_exchange.addItems(['Huobi'])
        self.btn_switch = QtWidgets.QPushButton(self.groupBox)
        self.btn_switch.setGeometry(QtCore.QRect(100, 390, 81, 31))
        self.btn_switch.setObjectName("btn_switch")
        self.btn_reset = QtWidgets.QPushButton(self.groupBox)
        self.btn_reset.setGeometry(QtCore.QRect(300, 390, 81, 31))
        self.btn_reset.setObjectName("btn_reset")
        self.lbl_total_cash = QtWidgets.QLabel(qds_gui)
        self.lbl_total_cash.setGeometry(QtCore.QRect(440, 20, 111, 41))
        self.lbl_total_cash.setObjectName("lbl_total_cash")
        self.frame = QtWidgets.QFrame(qds_gui)
        self.frame.setGeometry(QtCore.QRect(430, 80, 491, 311))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-image: url(:/newPrefix/back.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.txt_log = QtWidgets.QPlainTextEdit(qds_gui)
        self.txt_log.setGeometry(QtCore.QRect(10, 460, 921, 301))
        self.txt_log.setObjectName("txt_log")

        self.retranslateUi(qds_gui)
        self.txt_one_time.textChanged.connect(self.txt_multi_times_clear)
        self.txt_multi_times.textChanged.connect(self.txt_one_time_clear)
        self.btn_switch.clicked.connect(self.btn_switch_click)
        self.btn_reset.clicked.connect(self.set_default)
        QtCore.QMetaObject.connectSlotsByName(qds_gui)

    def txt_multi_times_clear(self):
        self.txt_multi_times.textChanged.disconnect(self.txt_one_time_clear)
        self.txt_multi_times.setText('')
        self.txt_multi_times.textChanged.connect(self.txt_one_time_clear)

    def txt_one_time_clear(self):
        self.txt_one_time.textChanged.disconnect(self.txt_multi_times_clear)
        self.txt_one_time.setText('')
        self.txt_one_time.textChanged.connect(self.txt_multi_times_clear)

    def btn_switch_click(self):
        global system_running
        if not system_running:
            exchange = self.cbx_exchange.currentText()
            category = self.cbx_category.currentText()
            period = self.cbx_period.currentText()
            ema_slow = self.txt_ema_slow.toPlainText()
            ema_fast = self.txt_ema_fast.toPlainText()
            one_time_offset_to_ema_slow = self.txt_one_time.toPlainText()
            multi_times_offset_to_ema_slow = self.txt_multi_times.toPlainText()
            stop_earning_offset_to_ema_slow = self.txt_stop_earning_offset.toPlainText()
            stop_loss_offset_to_ema_slow = self.txt_stop_loss_offset.toPlainText()
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

            if one_time_offset_to_ema_slow and not self.is_number(one_time_offset_to_ema_slow):
                self.txt_one_time.setText('请输入整数')
                self.txt_one_time.setFocus()
                return
            if multi_times_offset_to_ema_slow and not self.is_number(multi_times_offset_to_ema_slow):
                self.txt_multi_times.setText('请输入整数')
                self.txt_multi_times.setFocus()
                return
            if not one_time_offset_to_ema_slow and not multi_times_offset_to_ema_slow:
                self.txt_one_time.setText('请输入整数')
                self.txt_one_time.setFocus()
                return

            if not self.is_number(stop_earning_offset_to_ema_slow):
                self.txt_stop_earning_offset.setText('请输入大于0整数')
                self.txt_stop_earning_offset.setFocus()
                return
            if not self.is_number(stop_loss_offset_to_ema_slow):
                self.txt_stop_loss_offset.setText('请输入大于0整数')
                self.txt_stop_loss_offset.setFocus()
                return

            if not self.is_number(level_rate):
                self.txt_level_rate.setText('请输入大于0整数')
                self.txt_level_rate.setFocus()
                return
            if not self.is_number(max_number):
                self.max_number.setText('请输入大于0整数')
                self.max_number.setFocus()
                return

            self.btn_switch.setText('停止')
            # self.run_reading_log()
            self.run_reading_thread(True)
            self.set_all_enabled(False)
            system_running = True
        else:
            self.btn_switch.setText('开始')
            # self.run_reading_log()
            self.run_reading_thread(False)
            self.set_all_enabled(True)
            system_running = False

        '''
        a = self.tail('test.py')
        this_file_absolute_path1 = os.path.realpath('test.py')
        tail = '{0}\\tail.exe'.format(os.getcwd())
        cmd = '{0} -f {1}'.format(tail, this_file_absolute_path1)
        content = os.popen(cmd).read()
        cmd = 'dir {0}'.format(os.getcwd())
        content = os.popen(cmd).read()
        print(os.getcwd())  # 获取当前工作目录路径
        print(os.path.abspath('.')) # 获取当前工作目录路径
        print(os.path.abspath('test.txt')) # 获取当前目录文件下的工作目录路径
        print(os.path.abspath('..')) # 获取当前工作的父目录 ！注意是父目录路径
        print(os.path.abspath(os.curdir)) # 获取当前工作目录路径
        b = 1
        '''

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
        qds_gui.setWindowTitle(_translate("qds_gui", "EMA双均线交易系统"))
        self.groupBox.setTitle(_translate("qds_gui", "参数设置"))
        self.label.setText(_translate("qds_gui", "交易品种"))
        self.label_2.setText(_translate("qds_gui", "EMA 快线"))
        self.label_3.setText(_translate("qds_gui", "EMA 慢线"))
        self.label_7.setText(_translate("qds_gui", "一次建仓"))
        self.label_8.setText(_translate("qds_gui", "止盈偏移"))
        self.label_9.setText(_translate("qds_gui", "杠杆倍数"))
        self.label_10.setText(_translate("qds_gui", "交易周期"))
        self.label_12.setText(_translate("qds_gui", "最大数量"))
        self.label_11.setText(_translate("qds_gui", "止损偏移"))
        self.label_13.setText(_translate("qds_gui", "分批建仓"))
        self.label_4.setText(_translate("qds_gui", "交易所"))
        self.btn_switch.setText(_translate("qds_gui", "开始/停止"))
        self.btn_reset.setText(_translate("qds_gui", "重置参数"))
        self.lbl_total_cash.setText(_translate("qds_gui", "总金额: $50"))
        self.set_default()

    def set_default(self):
        global system_running
        if system_running:
            return

        self.cbx_exchange.setCurrentIndex(0)
        self.cbx_category.setCurrentIndex(0)
        self.cbx_period.setCurrentIndex(5)
        self.txt_ema_fast.setText('7')
        self.txt_ema_slow.setText('30')
        self.txt_one_time.setText('')
        self.txt_multi_times.setText('30')
        self.txt_stop_earning_offset.setText('100')
        self.txt_stop_loss_offset.setText('100')
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
        self.txt_one_time.setEnabled(en)
        self.txt_multi_times.setEnabled(en)
        self.txt_stop_earning_offset.setEnabled(en)
        self.txt_stop_loss_offset.setEnabled(en)
        self.txt_level_rate.setEnabled(en)
        self.txt_max_num.setEnabled(en)


import xml_rc
