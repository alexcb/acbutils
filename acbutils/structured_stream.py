import struct
import cStringIO

class StructuredStream(object):
    def __init__(self, stream, endian):
        if isinstance(stream, basestring):
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

    def get_sint8(self):
        return self._read(self.endian + 'b')[0]

    def get_uint8(self):
        return ord(self.stream.read(1))

    def get_sint16(self):
        return self._read(self.endian + 'h')[0]

    def get_uint16(self):
        return self._read(self.endian + 'H')[0]

    def get_sint32(self):
        return self._read(self.endian + 'i')[0]

    def get_uint32(self):
        return self._read(self.endian + 'I')[0]

    def get_sint64(self):
        return self._read(self.endian + 'q')[0]

    def get_uint64(self):
        return self._read(self.endian + 'Q')[0]

    def get_float32(self):
        return self._read(self.endian + 'f')[0]

    def get_float64(self):
        return self._read(self.endian + 'd')[0]

    def get_char(self):
        return chr(self.get_uint8())
