#coding=utf-8
# import socket
# def IsOpen(ip,port):
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     try:
#         s.connect((ip,int(port)))
#         s.shutdown(2)
#         print '%d is open' % port
#         return True
#     except:
#         print '%d is down' % port
#         return False
# if __name__ == '__main__':
#     IsOpen('127.0.0.1',12121)
import datetime
import time
ago = datetime.datetime.now()
time.sleep(10)
now = datetime.datetime.now()
print now - ago