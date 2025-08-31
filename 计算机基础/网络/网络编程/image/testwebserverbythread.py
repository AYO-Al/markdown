import random
import socket
import threading
import time

response="""\
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {}
X-Server: testwebserverbythread
Connection: keep-alive

"""

def get_response():
    with open("index.html","rb") as f:
        response_body = f.read()
        html = response_body.replace(b"{{}}",str(random.randint(1,100)).encode())
        return response.format(len(html)).replace("\n","\r\n").encode()+html

def fn3(conn: socket.socket):
    try:
        data  = conn.recv(1024)
        if not data:
            print(conn.getpeername(),"closed")
            return
        print(str(data))
        conn.sendall(get_response())
    except Exception as e:
        print(e)
    finally:
        conn.close()


def fn2(s: socket.socket):
    while True:

        conn, raddr = s.accept()

        threading.Thread(target=fn3,args=(conn,),daemon=True,name="recv").start()


if __name__ == '__main__':
    server = socket.socket()
    server.bind(('127.0.0.1',8088))
    server.listen()

    threading.Thread(target=fn2,args=(server,),name="accept").start()


    while True:
        time.sleep(20)
        print([ t.name for t in threading.enumerate() ])