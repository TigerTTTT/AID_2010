from socket import *
import sys, os


class FTPHandle:
    server_address = ("127.0.0.1", 4321)

    def __init__(self):
        self.socket = self.connect_server()

    def connect_server(self):
        tcp_socket = socket()
        tcp_socket.connect(FTPHandle.server_address)
        return tcp_socket

    def do_list(self):
        self.socket.send(b"LIST")
        data = self.socket.recv(20)
        if data == b"OK":
            files = self.socket.recv(1024 * 1024)
            print(files.decode())
        else:
            print("\n文件库没有文件！\n")

    def do_get(self, filename):
        if os.path.exists(filename):
            print("\n文件已存在！\n")
        else:
            msg = "GET " + filename
            self.socket.send(msg.encode())
            result = self.socket.recv(20)
            if result == b'OK':
                file = open(filename, 'wb')
                while True:
                    data = self.socket.recv(1024)
                    if data == b"FINISH":
                        print("\n文件下载完毕！\n")
                        break
                    file.write(data)
                file.close()
            else:
                print("\n要下载的文件不存在\n")

    def do_put(self, filename):
        try:
            file = open(filename,'rb')
        except Exception:
            print("没有该文件")
            return
        filename = filename.split("/")[-1]
        data = "PUT " + filename
        self.socket.send(data.encode())


    def do_exit(self):
        self.socket.send(b"EXIT")
        self.socket.close()
        sys.exit("FTP退出")


class FTPView:
    def __init__(self):
        self.__handle = FTPHandle()

    def __display_menu(self):
        print("--------------------")
        print("1) 查看文件")
        print("2) 下载文件")
        print("3) 上传文件")
        print("4) 退   出")
        print("--------------------")

    def __select_menu(self):
        try:
            item = input("请选择功能：")

        except KeyboardInterrupt:
            sys.exit("客户端已退出！")
        else:
            if item == "1":
                self.__handle.do_list()
            elif item == "2":
                filename = input("请输入要下载的文件名：")
                self.__handle.do_get(filename)
            elif item == "3":
                filename = input("请输入要上传的文件名：")
                self.__handle.do_put(filename)
            elif item == "4":
                self.__handle.do_exit()
            else:
                print("输入有误，请重新输入！")

    def main(self):
        while True:
            self.__display_menu()
            self.__select_menu()


if __name__ == '__main__':
    my = FTPView()
    my.main()
