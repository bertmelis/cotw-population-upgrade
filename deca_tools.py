import zlib
import os
import struct
from deca.file import ArchiveFile
from deca.ff_adf import Adf

def read_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
        file.close()
        return data


def save_file(filename, data_bytes):
    with open(filename, "wb") as file:
        file.write(data_bytes)
        file.close()


def decompress(data_bytes):
    decompress = zlib.decompressobj()
    decompressed = decompress.decompress(data_bytes)
    decompressed = decompressed + decompress.flush()
    return decompressed


def compress(data_bytes):
    compress = zlib.compressobj()
    compressed = compress.compress(data_bytes)
    compressed = compressed + compress.flush()
    return compressed


def modify_uint8_data_by_absaddr(data_bytes, addr, value):
    value_byte = value.to_bytes(4, byteorder='little')
    for i in range(0, len(value_byte)):
        data_bytes[addr + i] = value_byte[i]


def modify_f32_data_by_absaddr(data_bytes, abs_addr, value):
    hex_float = struct.pack("f", value)
    for i in range(0, 4):
        data_bytes[abs_addr + i] = hex_float[i]

class FakeVfs:
    def hash_string_match(self, hash32=None, hash48=None, hash64=None):
        return []

    def lookup_equipment_from_hash(self, name_hash):
        return None

def parse_adf(adf_file):
    obj = Adf()
    with ArchiveFile(open(adf_file, 'rb')) as f:
        obj.deserialize(f)
    content = obj.dump_to_string(FakeVfs())
    save_file(adf_file + ".txt", bytearray(content, 'utf-8'))
    return obj
