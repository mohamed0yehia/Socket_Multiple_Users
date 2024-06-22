
class SocketServer:

    sockets = []
    threads = []
    ips = []
    i = 0
    runflag = True

    def _init_(self):
        print("Welcome..")

    def sockactive(self,soc,socip):
        try:
            soc.send('0'.encode())
        except:
            self.sockets.remove(soc)
            self.threads.pop(self.i-1)
            self.i-=1
            self.ips.remove(socip)
            return False
        else:
            return True


    def sockhandle(self,sock,ip):
        sock.settimeout(3000)
        while self.sockactive(sock,ip):
            try:
                y = sock.recv(1024).decode()
                if y != '':
                    print(f"From {ip} recieved: {y}")
                else:
                    print(f"Nothing recieved from {ip}")
            except:
                print('Nothing recieved')
        print(f"Thread ended for {ip}")

    def listening(self,s):
        s.settimeout(3)
        while self.runflag:
            try:
                x,y = s.accept()
                self.ips.append(y)
                self.sockets.append(x)
                newthread = threading.Thread(target=self.sockhandle,args=(x,y))
                self.threads.append(newthread)
                newthread.start()
                self.i = self.i + 1
            except:
                pass

    def main(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)
        print(hostip)
        s.bind(('',8888))
        s.listen(5)
        listeningthread = threading.Thread(target=self.listening,args=(s,))
        listeningthread.start()
        while True:
            x = input()
            if x == 'exit':
  
                self.runflag = False
                break