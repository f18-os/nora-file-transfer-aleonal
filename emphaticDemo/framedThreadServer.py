#! /usr/bin/env python3
import sys, os, socket, params, time
from threading import Thread
from threading import Lock
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
        lock = threading.lock()

    def run(self):
        while True:
            lock.acquire()

            payload = self.fsock.receivemsg()

            if not payload:
                if self.debug: print(self.fsock, "server thread done")
                else print("client disconnected unexpectedly")
                lock.release()
                return

            if "sdsf" in payload.decode():
                print("Client in port %s exiting..." % addr[1])
                sys.exit(0)

            data = re.split(" ", payload.decode())

            if "put" in data[0]:
                if not open(data[1], "rb"):
                    f = open(data[1], "wb")
                    f.write(data[2])
                    f.close()
                    print("File received.")
                else:
                    #addcode here
                    print("File already exists in server!")
                    self.fsock.sendmsg(sock, b"sdsf", 1)

            elif "get" in data[0]:
                print("File request received.")

                try:
                    f = open(data[1], "rb")
                except FileNotFoundError:
                    print("File not found.")
                    self.fsock.sendmsg(sock, b"sdsf", 1)
                    continue

                if os.stat(data[1]).st_size == 0:
                    framedSend(sock, b"empty", -1)
                    f.close()
                    print("Error, file is empty.")
                    continue

                    self.fsock.sendmsg(sock, f.read(), -1)
                f.close()
                print("File sent.")

            if debug: print("rec'd: ", payload)
            lock.release()


while True:
    sock, addr = lsock.accept()
    ServerThread(sock, debug)
