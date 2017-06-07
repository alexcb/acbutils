class SocketReaderWriter(object):
    def __init__(self, sock):
        self.sock = sock
        self.buf = ''

    def read(self, n):
        while len(self.buf) < n:
            x = self.sock.recv(1024)
            if x == '':
                raise EOFError
            self.buf += x
        x = self.buf[:n]
        self.buf = self.buf[n:]
        return x

    def write(self, x):
        self.sock.send(x)
