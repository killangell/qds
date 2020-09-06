# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
# 实例1：休眠启动
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QProgressBar


class MyThread(QThread):
    valueChangeSignal = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._isPause = False
        self._value = 0

        self.cond = QWaitCondition()
        self.mutex = QMutex()

    def pause(self):
        print("线程休眠")
        self._isPause = True

    def resume(self):
        print("线程启动")
        self._isPause = False
        self.cond.wakeAll()

    def run(self):
        while 1:
            self.mutex.lock()

            if self._isPause: self.cond.wait(self.mutex)
            if self._value > 100: self._value = 0

            self._value += 1
            self.valueChangeSignal.emit(self._value)
            self.msleep(100)

            self.mutex.unlock()


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.t = MyThread(self)

        layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)
        layout.addWidget(QPushButton('休眠', self, clicked=self.t.pause))  # self.doWait
        layout.addWidget(QPushButton('唤醒', self, clicked=self.t.resume))  # self.doWait

        self.t.valueChangeSignal.connect(self.progressBar.setValue)
        self.t.start()

        # def doWait(self):self.t.pause()
    # def doWake(self):self.t.resume()


if __name__ == '__main__':
    import sys
    import cgitb

    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()

    sys.exit(app.exec_())