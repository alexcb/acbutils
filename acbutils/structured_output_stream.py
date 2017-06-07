import struct
import cStringIO

class StructuredOutputStream(object):
    def __init__(self, endian):
        self.stream = cStringIO.StringIO()
        if endian == 'little':
            endian = '<'
        if endian == 'big':
            endian = '>'
        assert endian in ('<', '>')
        self.endian = endian

    def _write(self, format, *values):
        x = struct.Struct(format)
        self.stream.write(x.pack(*values))

    def getvalue(self):
        return self.stream.getvalue()

    def put_sint8(self, x):
        self._write(self.endian + 'b', x)

    def put_uint8(self, x):
        self._write(self.endian + 'B', x)

    def put_sint16(self, x):
        self._write(self.endian + 'h', x)

    def put_uint16(self, x):
        self._write(self.endian + 'H', x)

    def put_sint32(self, x):
        self._write(self.endian + 'i', x)

    def put_uint32(self, x):
        self._write(self.endian + 'I', x)

    def put_sint64(self, x):
        self._write(self.endian + 'q', x)

    def put_uint64(self, x):
        self._write(self.endian + 'Q', x)

    def put_float32(self, x):
        self._write(self.endian + 'f', x)

    def put_float64(self, x):
        self._write(self.endian + 'd', x)

    def put_char(self, x):
        self.put_uint8(ord(x))

    def put_bytes(self, x):
        self.stream.write(x)

    def put_uint8_bytes(self, x):
        self.put_uint8(len(x))
        self.put_bytes(x)

    def put_uint16_bytes(self, x):
        self.put_uint16(len(x))
        self.put_bytes(x)

    def put_uint32_bytes(self, x):
        self.put_uint32(len(x))
        self.put_bytes(x)

    def put_uint64_bytes(self, x):
        self.put_uint64(len(x))
        self.put_bytes(x)


if __name__ == '__main__':
    sos = StructuredOutputStream('little')
    sos.put_uint32_bytes('aaaab')
    print repr(sos.getvalue())
