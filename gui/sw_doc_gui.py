# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sw_doc.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

qds_version = "1.0.1"

class Ui_obj_sw_doc(object):
    def setupUi(self, obj_sw_doc):
        obj_sw_doc.setObjectName("obj_sw_doc")
        obj_sw_doc.setWindowModality(QtCore.Qt.WindowModal)
        obj_sw_doc.resize(436, 300)
        self.tab_sw_doc = QtWidgets.QTabWidget(obj_sw_doc)
        self.tab_sw_doc.setGeometry(QtCore.QRect(0, 0, 441, 301))
        self.tab_sw_doc.setObjectName("tab_sw_doc")
        self.tab_func_doc = QtWidgets.QWidget()
        self.tab_func_doc.setObjectName("tab_func_doc")
        self.txt_func_doc = QtWidgets.QPlainTextEdit(self.tab_func_doc)
        self.txt_func_doc.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_func_doc.setObjectName("txt_func_doc")
        self.tab_sw_doc.addTab(self.tab_func_doc, "")
        self.tab_params_doc = QtWidgets.QWidget()
        self.tab_params_doc.setObjectName("tab_params_doc")
        self.txt_sw_doc = QtWidgets.QPlainTextEdit(self.tab_params_doc)
        self.txt_sw_doc.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_sw_doc.setObjectName("txt_sw_doc")
        self.tab_sw_doc.addTab(self.tab_params_doc, "")
        self.tab_author_doc = QtWidgets.QWidget()
        self.tab_author_doc.setObjectName("tab_author_doc")
        self.txt_author_doc = QtWidgets.QPlainTextEdit(self.tab_author_doc)
        self.txt_author_doc.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_author_doc.setObjectName("txt_author_doc")
        self.tab_sw_doc.addTab(self.tab_author_doc, "")
        self.tab_qa = QtWidgets.QWidget()
        self.tab_qa.setObjectName("tab_qa")
        self.txt_qa = QtWidgets.QPlainTextEdit(self.tab_qa)
        self.txt_qa.setGeometry(QtCore.QRect(0, 0, 431, 281))
        self.txt_qa.setObjectName("txt_qa")
        self.tab_sw_doc.addTab(self.tab_qa, "")

        self.retranslateUi(obj_sw_doc)
        self.tab_sw_doc.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(obj_sw_doc)

    def retranslateUi(self, obj_sw_doc):
        _translate = QtCore.QCoreApplication.translate
        obj_sw_doc.setWindowTitle(_translate("obj_sw_doc", "软件说明"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_func_doc), _translate("obj_sw_doc", "功能说明"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_params_doc), _translate("obj_sw_doc", "参数说明"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_author_doc), _translate("obj_sw_doc", "关于作者"))
        self.tab_sw_doc.setTabText(self.tab_sw_doc.indexOf(self.tab_qa), _translate("obj_sw_doc", "Q && A"))
        self.txt_sw_doc.setPlainText("交易所：目前仅支持Huobi\n\n"
                                     "交易品种：目前仅支持BTC当季，后续可以考虑加入其他主流数字币\n\n"
                                     "交易周期：支持1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon\n\n"
                                     "EMA 快线：指数移动平均线快线\n\n"
                                     "EMA 慢线：指数移动平均线慢线\n\n"
                                     "建仓偏移：确定建仓点位，以EMA慢线点位为参考。"
                                     "如果等于0，则建仓位置等于EMA慢线的点位；"
                                     "如果大于0，则相对保守，做多时，建仓位置在EMA慢线以下减去偏移位置，做空时，建仓位置在EMA慢线以上加偏移位置；"
                                     "如果小于0，则相对激进，做多时，建仓位置在EMA慢线以上加偏移（绝对值）位置，做空时，建仓位置在EMA慢线以下加偏（绝对值）移位置。\n\n"
                                     "建仓间隔：如果该值为0，则所有仓位均建在建仓偏移处。"
                                     "如果该值大于0，则分3次建仓，1/3建仓在（建仓点位-建仓间隔）处；1/3建仓在建仓点位处；1/3建仓在（建仓点位+建仓间隔）处。\n\n"
                                     "止盈偏移：基于EMA慢线的偏移，假设为100，则如果顺利止盈，则最终盈利点位为（建仓偏移+止盈偏移）。\n\n"
                                     "止损偏移：暂不支持。\n\n"
                                     "杠杆倍数：参考交易所杠杆倍数。\n\n"
                                     "最大数量：最大建仓数量（张数），请自行在交易所系统确保当前杠杆倍数下，最大数量确定有效，否则可能引起建仓，平仓操作异常。\n\n"
                                     "切忌满仓操作！！！"
                                     )
        self.txt_func_doc.setPlainText("软件版本：{0}\n\n"
                                       "本软件目前只支持Huobi当季BTC的交易，其他币种，其他类型合约（当周/次周/次季/永续等）目前暂未实现，如果有这方面需求后面会考虑增加。"
                                       "软件采用火币同步接口，如果操作出现卡顿，失败，则与网速或者火币接口响应速度有关，如果因为网络的原因在日志种显示某些操作失败，不用担心，软件会每隔1分钟运行，在网络恢复的时候，自动继续之前的操作。"
                                       "由于合约交易的风险很高，所以软件对交易数量（张数)做了限制，最大只支持30张。\n\n"
                                       "软件原理：在当前周期（举例：1小时/4小时/...）下，参考EMA快慢线，以最近的一次完整周期EMA值为依据，EMA快线大于EMA慢线，多头趋势只做多，EMA快线小于EMA慢线，空头趋势只作空。"
                                       "趋势（金叉死叉）变化时，立即平仓所有持仓和挂单，重新按新趋势的点位重新挂单。一次交易开始之后（有部分或者全部建仓挂单成交），未止盈或者趋势变化之前，不再进行新的挂单操作。"
                                       "如果挂单一直未成交（一张都没有成交），按照时间推移，新的EMA周期值出现，则取消之前挂单并按照最新EMA的值设置挂单。\n\n"
                                       "通过设置建仓偏移和止盈偏移可实现两种交易方式。\n\n"
                                       "1. 上涨回调到EMA慢线的时候建仓，下跌过程中反弹到EMA慢线的时候建仓，如果止盈偏移设置得当，可能在趋势不变的情况下，多次建仓并止盈。"
                                        "必须要说明的是，趋势变化的过程中，最后一笔一定是亏损的，或者是收益回撤。如果想实现收益覆盖亏损（回撤），则需要从历史行情找到一个合适的建仓点位和止盈点位。\n\n"
                                       "2. 实现金叉买入，死叉卖出（建仓偏移设置为负数，表示激进建仓；止盈点位设置为一个相对较大的值（该值依赖于交易所限制）），这种方式有可能有很大收益同时也会有很大的亏损，可自行参考历史行情。"
                                       .format(qds_version)
                                       )
        self.txt_author_doc.setPlainText("数字货币圈韭菜一枚，邮箱：313970187@qq.com。")

        self.txt_qa.setPlainText(
            "1. Q：软件有什么优势？\n"
            "   A：1. 人是比较感性的动物，特别是交易者，该入场的时候一等再等而错失机会，该止损的时候不忍止损，该止盈的时候却期待更大利润。软件的交易是理性的，一旦设置好参数，就会严格执行。\n"
            "      2. 人是需要休息的，如果在半夜或者凌晨出现了交易机会，人一般是把握不住的，而软件可以24小时盯盘，可以把握更多的机会。\n\n"
            "2. Q：软件是否能保证盈利？\n"
            "   A：不能保证。软件不是神，开发者也不是。只是提供给会使用EMA快慢线交易的人，本软件只是一个辅助挂单，撤单，设置止盈的工具，具体点位信息，止赢多少，是交易者自己设置的，软件只是照章执行。交易者需要参考历史行情，在能容忍最大损失的前提下去设置合适的参数进行交易。\n\n"
            "3. Q：为什么在开始和停止交易的时候会出现卡顿？\n"
            "   A：软件采用 Huobi 同步操作接口，受网络速度以及 Huobi 的 API 服务接口的速度影响，所以建议将电脑放置于网络信号良好的位置交易。\n\n"
            "4. Q：为什么有时候，挂单数量 + 持仓数量 不等于最大数量？\n"
            "   A：在软件运行的过程中，请不要手动建仓，平仓或者挂单取消挂单，这样会对软件的交易会造成一些影响。还有在软件有部分持仓的情况下，停止并重新运行软件，软件的默认行为在开始运行的时候，会取消所有挂单以及平掉所有逆势持仓。这时，如果有顺势持仓的情况，软件只会设置止盈挂单，在这笔交易完成（止盈或者止损）之前，软件不会挂挂新的开仓挂单。\n\n"
            "5. Q：什么是顺势？什么是逆势？\n"
            "   A：只是本软件所认为的趋势，并不代表大趋势，只是表示当前周期下的趋势。顺势：EMA快线 大于 EMA慢线；逆势：EMA快线 小于 EMA慢线。\n\n"
            "6. Q：为什么没有实现止损？\n"
            "   A：不是没有考虑过，首先承认，实现止损对代码的逻辑处理带来一定困难，容易引入问题影响交易系统的稳定。另外，我在Huobi测试过，例如：如果同时设置止盈止损，价格上升到达止盈触发价位，但是却没能到达止盈点位，就发生趋势变化，价格下降，这时止损触发就会失败。\n\n"
            "7. Q：在软件运行过程中，可以手动平仓吗？\n"
            "   A：不建议这样操作，如果一定要操作，可以停止运行，再平仓。\n\n"
            "8. Q：如果不想交易了，只是停止软件运行就可以了吗？\n"
            "   A：如果不想交易了，需要：\n"
            "      1. 停止软件运行\n"
            "      2. 菜单选择：撤销所有挂单\n"
            "      3. 菜单选择：平仓所有持仓\n\n"
        )
