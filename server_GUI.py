from PySide2.QtWidgets import *
from PySide2.QtGui import *
import socket
import datetime
import threading

server : socket     # 服务器socket对象
clients = []        # 存储客户端socket

# 开始按钮事件
def start():
    startButton.setEnabled(False)               # 开始按钮设置为不可点击
    threading._start_new_thread(myConnect,())   # 开始线程用于连接客户端

# 用于连接客户端
def myConnect():
    infoServer = {}     # 获取服务器配置信息
    for infos in infoEdit.toPlainText().split('\n'):            # 遍历每一行
        info = infos.split(':')
        infoServer[info[0]] = info[1]                           # A:B ==> 'A'='B'
    
    global server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # 服务器socket
    server.bind((infoServer['host'],int(infoServer['port'])))   # 初始化服务器
    server.listen(10)                                           # 开始监听
    history.insertPlainText('等待连接\n')                        # 打印日志

    # 等待连接并开启线程维护
    while True:
        client = server.accept()                            # 连接客户端
        t = threading.Thread(target=myrecv,args=(client,))  # 创建线程
        t.start()                                           # 开始线程

# 用于维护客户端的信息接收
def myrecv(client):
    global clients
    name = client[0].recv(1024).decode()                    # 获取客户端名字
    history.insertPlainText(f'[client]{name}连接成功\n')    # 打印日志
    
    # 告知其他连接上的客户端有人加入
    for other in clients:
        other.send(f'{name}加入聊天室'.encode())
    
    clients.append(client[0])   # 将连接上的客户端存储

    try:
        # 接收消息
        while True:
            msg = client[0].recv(1024).decode()         # 获取消息
            history.insertPlainText(msg+'\n')           # 打印输出
            for other in clients:
                if other == client[0]:                  # 自身不发送
                    continue
                other.send(msg.encode())                # 发送给其他人
    except:
        # 断开连接
        history.insertPlainText(f'{name}退出聊天室\n')  # 打印日志
        clients.remove(client[0])                       # 删除客户端
        client[0].close()                               # 关闭该客户端socket
        
        for other in clients:                           # 告诉其他人退出的消息
            other.send(f'{name}退出聊天室'.encode())

# 发送按钮点击事件
def send():
    msg = textEdit.toPlainText()            # 获取输入框内容
    pre = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'[server]'  # 前缀
    history.insertPlainText(pre+msg+'\n')   # 打印输出到历史记录
    textEdit.setPlainText('')               # 输入框清空
    global clients
    for client in clients:                  # 给所有人发送消息
        client.send((pre+msg).encode())

# 窗口初始化
app = QApplication([])
window = QMainWindow()
window.resize(1000,800)
window.move(300,300)
window.setWindowTitle('聊天室_服务端')

# 文字标签
label1 = QLabel(window)
label1.setText('聊天记录')
label1.move(50,10)
label2 = QLabel(window)
label2.setText('输入框')
label2.move(50,560)
label3 = QLabel(window)
label3.setText('本地信息')
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

# 服务端信息
infoEdit = QPlainTextEdit(window)
infoEdit.move(700,50)
infoEdit.resize(250,400)
infoEdit.insertPlainText('host:127.0.0.1\n')
infoEdit.insertPlainText('port:8888')

# 开始按钮
startButton = QPushButton('开始',window)
startButton.move(700,350)
startButton.resize(250,100)
startButton.clicked.connect(start)

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
palette.setColor(palette.Background,QColor(255,192,203))    # 粉色
window.setPalette(palette)

window.show()
app.exec_()
