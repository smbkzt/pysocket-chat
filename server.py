from socketserver import ThreadingTCPServer, BaseRequestHandler
from threading import Thread
import pickle
import datetime
import os


messages = []
temp = []


class Echo(BaseRequestHandler):

    def handle(self):
        self.temp = []
        Thread(target=self.send).start()
        self.username = self.request.recv(8192).decode()

        while True:
            msg = self.request.recv(8192)
            msg = "[{} {}]: {}".format(datetime.datetime.now().strftime("%H:%M:%S"),
                                       self.username,
                                       msg.decode())

            messages.append(msg)
            if not msg:
                break

                
    def send(self):

        global temp, messages
        while 1:

            if len(self.temp) != len(messages):

                data_string = pickle.dumps(messages)
                self.request.send(data_string)
                self.temp = [item for item in messages]


if __name__ == "__main__":
    serv = ThreadingTCPServer(("127.0.0.1", 4446), Echo)
    serv.serve_forever()
