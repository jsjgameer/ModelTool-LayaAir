import struct

class Struct(object):
    def __init__(self, fmt):
        self.fmt = fmt

    def unpack(self, *args):
        return struct.unpack(self.fmt, *args)
        pass

    def pack(self, *args):
        return struct.pack(self.fmt, *args)
        pass


pack_Uint8 = Struct('B').pack
pack_Uint16 = Struct('H').pack
pack_Uint32 = Struct('I').pack
pack_Float = Struct('f').pack
pack_Double = Struct('d').pack


def uint8_2_byte(int_):
    return pack_Uint8(int_)
    pass


def uint16_2_byte(int_):
    return pack_Uint16(int_)
    pass


def uint32_2_byte(int_):
    return pack_Uint32(int_)
    pass


def float_2_byte(float_):
    return pack_Float(float_)
    pass


def double_2_byte(float_):
    return pack_Double(float_)
    pass


def str_2_byte(string):
    return bytes(string.encode('utf-8'))
    pass


class ByteUnit(object):

    def __init__(self, url, unicode_errors='strict'):
        self.url = url
        self.file = open(url, "wb")
        self.unicode_errors = unicode_errors
        pass

    def __del__(self):
        if not self.file.closed:
            self.file.flush()
            pass
        pass

    def flush(self):
        self.file.flush()
        pass

    def close(self):
        self.file.close()
        pass

    def write_uint8(self, int_):
        self.file.write(uint8_2_byte(int_))
        pass

    def write_uint16(self, int_):
        self.file.write(uint16_2_byte(int_))
        pass

    def write_uint32(self, int_):
        self.file.write(uint32_2_byte(int_))
        pass

    def write_string(self, string):
        self.write_uint16(len(string))
        self.file.write(str_2_byte(string))
        pass

    def write_float(self, float_):
        self.file.write(float_2_byte(float_))
        pass

    def write_double(self, double_):
        self.file.write(double_2_byte(double_))
        pass

    def write_byte(self, byte):
        self.file.write(byte)
        pass

    def pos(self):
        return self.file.tell()
        pass

    def seek(self, pos):
        self.file.seek(pos, 0)
        pass
