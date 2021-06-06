# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import requests,urllib.parse
from PyQt5.QtWidgets import QMessageBox
global who,filename,yuyinneirong
try:
    host = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=4E1BG9lTnlSeIf1NQFlrSq6h&client_secret=544ca4657ba8002e3dea3ac2f5fdd241'
    response = requests.get(host)
    r=response.json()
    access_token=r['access_token']
    print("access_token is ",r)
except:
    access_token='24.90f8a24e41294db470e9ee005d38bf68.2592000.1625394444.282335-24312819'
try:
    host = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=4E1BG9lTnlSeIf1NQFlrSq6h&client_secret=544ca4657ba8002e3dea3ac2f5fdd241'
    response = requests.get(host)
    r=response.json()
    access_token=r['access_token']
    print(r)
except:
    access_token='24.90f8a24e41294db470e9ee005d38bf68.2592000.1625394444.282335-24312819'
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(563, 535)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 30, 501, 361))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 420, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 410, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 480, 72, 15))
        self.label.setObjectName("label")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(110, 470, 181, 31))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.r=hc()#定义一个线程,用于防止界面卡顿。
        self.r.signal.connect(self.showmessage)#绑定显示消息的函数
        self.r.signal2.connect(self.showmessage2)#绑定显示消息的函数
        self.pushButton.clicked.connect(self.start)#按钮触发事件,执行self.start
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "文字转语音"))
        self.pushButton.setText(_translate("MainWindow", "合成语音"))
        self.comboBox.setItemText(0, _translate("MainWindow", "度小宇"))
        self.comboBox.setItemText(1, _translate("MainWindow", "度丫丫"))
        self.comboBox.setItemText(2, _translate("MainWindow", "度逍遥"))
        self.comboBox.setItemText(3, _translate("MainWindow", "度博文"))
        self.label.setText(_translate("MainWindow", "文件名"))
    def showmessage(self):#显示消息的函数
            QMessageBox.information(MainWindow,'感谢您的使用','合成完毕,请检查文件,感谢您的使用')
    def showmessage2(self):#显示消息的函数
            QMessageBox.information(MainWindow,'非常抱歉','请检查网络连接和授权')
    def start(self):
        print("绑定函数开始执行")
        global who,filename,yuyinneirong
        who=self.comboBox.currentText()
        filename=self.plainTextEdit_2.toPlainText()
        yuyinneirong=self.plainTextEdit.toPlainText()
        #该函数有疑问,上未找到获取参数的办法
        print("参数获取完毕，请求线程开始")
        self.r.start()
class hc(QThread):#由这个线程去完成请求工作
    signal = pyqtSignal()#定义信号槽
    signal2 = pyqtSignal()
    def __init__(self):
        super(hc,self).__init__()
    def run(self):
        print("子线程启动")
        global who,filename,yuyinneirong#获取的参数
        print("多线程参数共享获取正常")
        filename=str(filename)+".wav"
        text=urllib.parse.quote(yuyinneirong)
        data={"tex":text,"tok":access_token,'cuid':"cuidwangyifan","ctp":"1","lan":"zh","per":"2","vol":"9","aue":"6"}
        #data是传送的表单,向能力接口提交文字内容,声音大小等信息
        if who=="度小宇":
            data['per']=1
            print("度小宇朗读")
        elif who=='度小美':
            data['per']=0
            print("度小美朗读")
        elif who=='度丫丫':
            data['per']=4
            print("度丫丫朗读")
        else:
            data['per']=3
            print("度博文朗读")
        try:
            response=requests.post("http://tsn.baidu.com/text2audio",data=data)
            with open (filename,"wb")as f:#存储文件
                f.write(response.content)
            print("写入完毕,子线程结束")
            self.signal.emit()#正常结束线程前,触发消息1,告知用户正常完成请求并保存
        except:
            print("网络原因或者激活码问题,子线程不需要在运行了,结束子进程")
            self.signal2.emit()#触发消息2，报告异常
            print("子进程正常退出,运行良好")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
