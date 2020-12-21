from threading import Thread
from socket import *
import sys, os
from time import sleep

FTP = "/home/tarena/FTP/"


# 具体处理客户端事务
class Handle:
    def __init__(self, connfd):
        self.connfd = connfd

    def __do_list(self):
        files = os.listdir(FTP)
        if files:
            self.connfd.send(b"OK")
            sleep(0.2)
            msg = "\n".join(files)
            self.connfd.send(msg.encode())
        else:
            self.connfd.send(b"FAIL")

    def __do_get(self, filename):
        if os.path.exists(FTP + filename):
            self.connfd.send(b"OK")
            sleep(0.2)
            file = open(FTP + filename, "rb")
            while True:
                data = file.read(1024)
                if not data:
                    sleep(0.2)
                    self.connfd.send(b"FINISH")
                    break
                else:
                    self.connfd.send(data)
            file.close()
        else:
            self.connfd.send(b"FAIL")

    def __do_put(self):
        pass


    def request(self, data):
        tmp = data.decode().split(" ")
        if tmp[0] == "LIST":
            self.__do_list()
        elif tmp[0] == "GET":
            filename = tmp[1]
            self.__do_get(filename)
        elif tmp[0] == "PUT":
            self.__do_put()
        elif tmp[0] == "EXIT":
            pass


# 为每个客户端创建线程
class ClientThread(Thread):
    def __init__(self, connfd):
        super().__init__(daemon=True)
        self.connfd = connfd
        self.handle = Handle(connfd)

    def run(self) -> None:
        while True:
            data = self.connfd.recv(1024)
            if not data:
                break
            self.handle.request(data)
        self.connfd.close()


# 并发服务类
class ConcurrentServer:
    def __init__(self, host="0.0.0.0", port=0):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.__sock = self.__create_socket()

    # 创建套接字
    def __create_socket(self):
        tcp_socket = socket()
        tcp_socket.bind(self.address)
        return tcp_socket

    # 启动服务
    def serve_forever(self):
        print("Listen the port %d" % self.port)
        self.__sock.listen(5)
        while True:
            try:
                connfd, addr = self.__sock.accept()
                print("Connect from", addr)
            except KeyboardInterrupt:
                self.__sock.close()
                sys.exit("Server exit!")
            # 为客户端创建线程
            t = ClientThread(connfd)
            t.start()


if __name__ == '__main__':
    server = ConcurrentServer("0.0.0.0", 4321)
    server.serve_forever()
