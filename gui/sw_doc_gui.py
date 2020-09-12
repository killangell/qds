# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sw_doc.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_obj_sw_doc(object):
    def setupUi(self, obj_sw_doc):
        obj_sw_doc.setObjectName("obj_sw_doc")
        obj_sw_doc.setWindowModality(QtCore.Qt.WindowModal)
        obj_sw_doc.resize(436, 300)
        self.tab_sw_doc = QtWidgets.QTabWidget(obj_sw_doc)
        self.tab_sw_doc.setGeometry(QtCore.QRect(0, 0, 441, 301))
        self.tab_sw_doc.setObjectName("tab_sw_doc")
        self.tab_params_doc = QtWidgets.QWidget()
        self.tab_params_doc.setObjectName("tab_params_doc")
        self.txt_sw_doc = QtWidgets.QPlainTextEdit(self.tab_params_doc)
        self.txt_sw_doc.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_sw_doc.setObjectName("txt_sw_doc")
        self.tab_sw_doc.addTab(self.tab_params_doc, "")
        self.tab_func_doc = QtWidgets.QWidget()
        self.tab_func_doc.setObjectName("tab_func_doc")
        self.txt_func_doc = QtWidgets.QPlainTextEdit(self.tab_func_doc)
        self.txt_func_doc.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_func_doc.setObjectName("txt_func_doc")
        self.tab_sw_doc.addTab(self.tab_func_doc, "")
        self.tab_author_doc = QtWidgets.QWidget()
        self.tab_author_doc.setObjectName("tab_author_doc")
        self.txt_author_doc = QtWidgets.QPlainTextEdit(self.tab_author_doc)
        self.txt_author_doc.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_author_doc.setObjectName("txt_author_doc")
        self.tab_sw_doc.addTab(self.tab_author_doc, "")

        self.retranslateUi(obj_sw_doc)
        self.tab_sw_doc.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(obj_sw_doc)

    def retranslateUi(self, obj_sw_doc):
        _translate = QtCore.QCoreApplication.translate
        obj_sw_doc.setWindowTitle(_translate("obj_sw_doc", "软件说明"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_params_doc), _translate("obj_sw_doc", "参数说明"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_func_doc), _translate("obj_sw_doc", "功能说明"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_author_doc), _translate("obj_sw_doc", "关于作者"))
        self.txt_sw_doc.setPlainText("交易所：目前仅支持Huobi\n\n"
                                     "交易品种：目前仅支持BTC，后续可以考虑加入其他主流数字币\n\n"
                                     "交易周期：支持1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon\n\n"
                                     "EMA 快线：指数移动平均线快线\n\n"
                                     "EMA 慢线：指数移动平均线慢线\n\n"
                                     "建仓偏移：确定建仓点位，以EMA慢线点位为参考。"
                                     "如果等于0，则建仓位置等于EMA慢线的点位；"
                                     "如果大于0，则相对保守，做多时，建仓位置在EMA慢线以下减去偏移位置，做空时，建仓位置在EMA慢线以上加偏移位置；"
                                     "如果小于0，则相对激进，做多时，建仓位置在EMA慢线以上加偏移（绝对值）位置，做空时，建仓位置在EMA慢线以下加偏（绝对值）移位置。\n\n"
                                     "建仓间隔：如果该值为0，则所有仓位均建在建仓偏移处。"
                                     "如果该值大于0，则1/3建仓在（建仓点位-建仓间隔）处；1/3建仓在建仓点位处；1/3建仓在（建仓点位+建仓间隔）处。\n\n"
                                     "止盈偏移：基于EMA慢线的偏移，假设为100，则如果顺利止盈，则最终盈利点位为（建仓偏移+止盈偏移）。\n\n"
                                     "止损偏移：暂不支持。\n\n"
                                     "杠杆倍数：参考交易所杠杆倍数。\n\n"
                                     "最大数量：最大建仓数量（张数），请自行在交易所系统确保当前杠杆倍数下，最大数量确定有效，否则可能引起建仓，平仓操作异常。"
                                     )
        self.txt_func_doc.setPlainText("在当前周期下，EMA慢线和EMA快线，金叉只做多，死叉的时候只作空。通过设置建仓偏移和止盈偏移可实现两种交易方式\n\n"
                                       "1. 上涨回调到EMA慢线的时候建仓，下跌过程中反弹到EMA慢线的时候建仓，如果止盈偏移设置得当，可能在趋势不变的情况下，多次建仓并止盈。"
                                        "必须要说明的是，趋势变化的过程中，最后一笔一定是亏损的，或者是收益回撤。如果想实现收益覆盖亏损（回撤），则需要从历史行情找到一个合适的建仓点位和止盈点位。\n\n"
                                       "2. 实现金叉买入，死叉卖出（建仓偏移设置为负数，表示激进建仓；止盈点位设置为一个相对较大的值（该值依赖于交易所限制）），这种方式有可能有很大收益同时也会有很大的亏损，可自行参考历史行情。"
                                       )
        self.txt_author_doc.setPlainText("数字货币圈韭菜一枚，邮箱：313970187@qq.com。")