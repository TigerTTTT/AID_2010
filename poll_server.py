from socket import *
from select import *

HOST = "0.0.0.0"
PORT = 4321
ADDR = (HOST, PORT)
# 创建tcp套接字连接客户端，处理请求
tcp_socket = socket()
tcp_socket.bind(ADDR)
tcp_socket.listen(4)

# 设置为非阻塞IO
tcp_socket.setblocking(False)
# 设置监控列表
p = poll()
p.register(tcp_socket, POLLIN)
map = {tcp_socket.fileno(): tcp_socket, }
# 循环的监控发生的IO事件
while True:
    events = p.poll()
    # 遍历就绪的IO对象
    for fd, event in events:
        # 分情况处理
        if fd is tcp_socket.fileno():
            # 处理客户端连接
            connfd, addr = map[fd].accept()
            print("Connect From:", addr)
            # 添加客户端连接套接字到监控列表
            connfd.setblocking(False)
            map[connfd.fileno()] = connfd
            p.register(connfd, POLLIN)
        else:
            # 处理一个客户端的消息
            data = map[fd].recv(1024)
            if not data:
                map[fd].close()
                p.unregister(fd)
                del map[fd]
                continue
            print(data.decode())
            map[fd].send(b"OK")
