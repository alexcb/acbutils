import struct
import cStringIO

class StructuredStream(object):
    def __init__(self, stream=None, endian='little'):
        if stream is None:
            self.stream = cStringIO.StringIO()
        elif isinstance(stream, basestring):
            self.stream = cStringIO.StringIO(stream)
        else:
            self.stream = stream
        if endian == 'little':
            endian = '<'
        if endian == 'big':
            endian = '>'
        assert endian in ('<', '>')
        self.endian = endian

    def _read(self, format):
        x = struct.Struct(format)
        try:
            return x.unpack(self.stream.read(x.size))
        except struct.error:
            raise EOFError

    def _write(self, format, *values):
        x = struct.Struct(format)
        self.stream.write(x.pack(*values))

    def get_value(self):
        return self.stream.getvalue()

    def get_sint8(self):
        return self._read(self.endian + 'b')[0]

    def put_sint8(self, x):
        self._write(self.endian + 'b', x)

    def get_uint8(self):
        return ord(self.stream.read(1))

    def put_uint8(self, x):
        self._write(self.endian + 'B', x)

    def get_sint16(self):
        return self._read(self.endian + 'h')[0]

    def put_sint16(self, x):
        self._write(self.endian + 'h', x)

    def get_uint16(self):
        return self._read(self.endian + 'H')[0]

    def put_uint16(self, x):
        self._write(self.endian + 'H', x)

    def get_sint32(self):
        return self._read(self.endian + 'i')[0]

    def put_sint32(self, x):
        self._write(self.endian + 'i', x)

    def get_uint32(self):
        return self._read(self.endian + 'I')[0]

    def put_uint32(self, x):
        self._write(self.endian + 'I', x)

    def get_sint64(self):
        return self._read(self.endian + 'q')[0]

    def put_sint64(self, x):
        self._write(self.endian + 'q', x)

    def get_uint64(self):
        return self._read(self.endian + 'Q')[0]

    def put_uint64(self, x):
        self._write(self.endian + 'Q', x)

    def get_float32(self):
        return self._read(self.endian + 'f')[0]

    def put_float32(self, x):
        self._write(self.endian + 'f', x)

    def get_float64(self):
        return self._read(self.endian + 'd')[0]

    def put_float64(self, x):
        self._write(self.endian + 'd', x)

    def get_char(self):
        return chr(self.get_uint8())

    def put_char(self, x):
        self.put_uint8(ord(x))

    def get_bytes(self, n):
        x = self.stream.read(n)
        if len(x) != n:
            raise EOFError('wanted %d bytes; got %d' % (n, len(x)))
        return x

    def put_bytes(self, x):
        self.stream.write(x)

    def get_uint8_bytes(self):
        n = self.get_uint8()
        return self.get_bytes(n)

    def put_uint8_bytes(self, x):
        self.put_uint8(len(x))
        self.put_bytes(x)

    def get_uint16_bytes(self):
        n = self.get_uint16()
        return self.get_bytes(n)

    def put_uint16_bytes(self, x):
        self.put_uint16(len(x))
        self.put_bytes(x)

    def get_uint32_bytes(self):
        n = self.get_uint32()
        return self.get_bytes(n)

    def put_uint32_bytes(self, x):
        self.put_uint32(len(x))
        self.put_bytes(x)

    def get_uint64_bytes(self):
        n = self.get_uint64()
        return self.get_bytes(n)

    def put_uint64_bytes(self, x):
        self.put_uint64(len(x))
        self.put_bytes(x)


if __name__ == '__main__':
    ss = StructuredStream('\xFE\x00\x00\x00')
    print repr(ss.get_uint32())

    ss = StructuredStream()
    ss.put_uint64(12)
    print repr(ss.get_value())
