import socket
import struct
from sys import exc_info
import traceback
import logging
import time
import numpy as np


class DroneIPC:
    def __init__(self, address, port, maxBufferSize) -> None:
        if maxBufferSize > 0 and maxBufferSize < 10000:
            self.MAX_BUFFER_SIZE = maxBufferSize
        else:
            self.MAX_BUFFER_SIZE = 4000
        self.sock = socket.socket()
        socket.setdefaulttimeout(None)
        self.port = port
        self.addr = address
        self.data = []
        self.sock.bind((self.addr, self.port))
        print("Socket created on ", self.addr, ":", self.port, "!")
        self.sock.listen(10)
        print("Socket Awaiting Connection...")
    
    def update(self):
        # Accept returns when a port connects
        con, addr = self.sock.accept()
        bytesReceived = con.recv(self.MAX_BUFFER_SIZE)

        # We can convert the bytes received into a numpy array where each element
        # is defined by dtype.
        dataReceived = np.frombuffer(bytesReceived, dtype=np.float32)

        # We can convert the array data into a byteBuffer that can be sent over the socket
        byteData = struct.pack('%sf' % len(self.data), *self.data)
        con.sendall(byteData)
        con.close()

    """
    Deconstructor that handles socket closing.
    """
    def __del__(self):
        pass