from PySide2.QtWidgets import *
from PySide2.QtGui import *
import socket
import datetime
import threading

global server       # 连接到的服务器
infoServer = {}     # 存储连接服务器的信息

# 连接按钮连接的事件
def conn():
    global infoServer
    global server
    if connectButton.text() == '连接':      # 连接服务器
        # 获取用于连接服务器的消息
        for infos in infoEdit.toPlainText().split('\n'):                # 遍历每一行
            info = infos.split(':')
            infoServer[info[0]] = info[1]                               # A:B ==> 'A'='B'
        # 连接服务器
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       # 初始化连接方式
        server.connect((infoServer['host'],int(infoServer['port'])))    # 连接服务器
        connectButton.setText('关闭')                                   # 按钮改变文字
        threading._start_new_thread(myrevc,())                          # 开启线程维护连接接收消息
    elif connectButton.text() == '关闭':    # 断开服务器
        server.close()                      # 关闭连接
        connectButton.setText('连接')       # 按钮改变文字

# 用于线程获取消息
def myrevc():
    global infoServer
    server.send(f'{infoServer["name"]}'.encode())       # 告诉服务器自己的名字
    history.insertPlainText('成功连接服务器\n')          # 成功连接服务器的消息打印
    # 收消息
    while True:
        msg = server.recv(1024).decode()                # 接收消息
        history.insertPlainText(msg+'\n')               # 消息打印到文本框

# 发送按钮发送消息
def send():
    global infoServer
    msg = textEdit.toPlainText()                    # 获取输入框的内容
    pre = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+f'[{infoServer["name"]}]'   # 消息前缀
    server.send((pre+msg).encode())                 # 发送消息
    history.insertPlainText(pre+msg+'\n')           # 历史信息
    textEdit.setPlainText('')                       # 输入框清空

# 窗口初始化
app = QApplication([])
window = QMainWindow()
window.resize(1000,800)
window.move(300,300)
window.setWindowTitle('聊天室_客户端')

# 文字标签
label1 = QLabel(window)
label1.setText('聊天记录')
label1.move(50,10)
label2 = QLabel(window)
label2.setText('输入框')
label2.move(50,560)
label3 = QLabel(window)
label3.setText('服务端信息')
label3.move(700,10)

# 聊天记录
history = QPlainTextEdit(window)
history.move(50,50)
history.resize(650,500)
history.setReadOnly(True)

# 输入框
textEdit = QPlainTextEdit(window)
textEdit.move(50,600)
textEdit.resize(650,100)

# 连接信息
infoEdit = QPlainTextEdit(window)
infoEdit.move(700,50)
infoEdit.resize(250,300)
infoEdit.insertPlainText('name:client\n')
infoEdit.insertPlainText('host:127.0.0.1\n')
infoEdit.insertPlainText('port:8888')

# 连接按钮
connectButton = QPushButton('连接',window)
connectButton.move(700,350)
connectButton.resize(250,100)
connectButton.clicked.connect(conn)

# 清空按钮
clearButton = QPushButton('清空聊天框',window)
clearButton.move(700,450)
clearButton.resize(250,100)
clearButton.clicked.connect(lambda : history.setPlainText(''))

# 发送按钮
sendButton = QPushButton('发送',window)
sendButton.move(700,600)
sendButton.resize(250,100)
sendButton.clicked.connect(send)

# 主题
palette = window.palette()
palette.setColor(palette.Background,QColor(150,255,150))    # 绿色
window.setPalette(palette)

window.show()
app.exec_()
