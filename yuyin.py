#encoding:utf-8
#请购买百度的AI接口
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import requests,urllib.parse
from PyQt5.QtWidgets import QMessageBox

global who,filename,yuyinneirong
try:
    #这是获取利用AK和SK获取access_token的
    host = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=4E1BG9lTnlSeIf1NQFlrSq6h&client_secret=544ca4657ba8002e3dea3ac2f5fdd241'
    response = requests.get(host)
    r=response.json()
    access_token=r['access_token']
    print(r)
except:
    access_token='24.2577dd33801a349ca9e57a1cf2fd93c3.2592000.1625470688.282335-10854623'
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(447, 276)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 80, 54, 12))
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(100, 30, 291, 111))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 220, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 170, 54, 12))
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 170, 113, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(100, 220, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 220, 61, 16))
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.r=hc()#定义一个线程
        self.r.signal.connect(self.showmessage)
        self.r.signal2.connect(self.showmessage2)
        self.pushButton.clicked.connect(self.start)#绑定执行函数块
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def showmessage(self):
        QMessageBox.information(MainWindow,'感谢您的使用','合成完毕,请检查文件,感谢您的使用')
    def showmessage2(self):
        QMessageBox.information(MainWindow,'非常抱歉','请检查网络连接和授权')
    def start(self):
        print("绑定函数开始执行")
        global who,filename,yuyinneirong
        who=self.comboBox.currentText()
        filename=self.lineEdit.text()
        yuyinneirong=self.textEdit.toPlainText()
        print("参数获取完毕，请求线程开始")
        self.r.start()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "语音合成界面版"))
        self.label.setText(_translate("MainWindow", "输入文字"))
        self.pushButton.setText(_translate("MainWindow", "合成语音"))
        self.label_2.setText(_translate("MainWindow", "文件名"))
        self.comboBox.setItemText(0, _translate("MainWindow", "度小宇"))
        self.comboBox.setItemText(1, _translate("MainWindow", "度小美"))
        self.comboBox.setItemText(2, _translate("MainWindow", "度丫丫"))
        self.comboBox.setItemText(3, _translate("MainWindow", "度逍遥"))
        self.label_3.setText(_translate("MainWindow", "声音设置"))
class hc(QThread):
    signal = pyqtSignal()
    signal2 = pyqtSignal()
    def __init__(self):
        super(hc,self).__init__()
    def run(self):
        print("子线程启动")
        global who,filename,yuyinneirong
        print("多线程参数共享获取正常")
        filename=str(filename)+".wav"
        text=urllib.parse.quote(yuyinneirong)
        data={"tex":text,"tok":access_token,'cuid':"cuidwangyifan","ctp":"1","lan":"zh","per":"2","vol":"9","aue":"6"}
        print(data)
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
            with open (filename,"wb")as f:
                f.write(response.content)
            print("写入完毕,子线程结束")
            self.signal.emit()#触发消息1
        except:
            print("网络原因或者激活码问题,子线程不需要在运行了,结束子进程")
            self.signal2.emit()#触发消息2
            print("子进程正常退出,运行良好")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
