# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
import uuid
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.TreeColors import TreeColors
from pullenti.unitext.internal.word.DirectoryStreamIds import DirectoryStreamIds
from pullenti.unitext.internal.word.DirectoryObjectTypes import DirectoryObjectTypes
from pullenti.unitext.internal.word.CFHeader import CFHeader
from pullenti.unitext.internal.word.CFDirectoryEntry import CFDirectoryEntry

class ReaderUtils:
    
    _headerdifatsectors_count = 109
    
    _directory_entry_size = 128
    
    _header_size = 512
    
    @staticmethod
    def _read_header(s : Stream) -> 'CFHeader':
        s.position = 0
        header_bytes = Utils.newArrayOfBytes(ReaderUtils._header_size, 0)
        header_read = s.read(header_bytes, 0, ReaderUtils._header_size)
        if (header_read != ReaderUtils._header_size): 
            raise Utils.newException("Invalid header: eof of file", None)
        header = CFHeader()
        header._signature1 = int.from_bytes(header_bytes[0:0+4], byteorder="little")
        header._signature2 = int.from_bytes(header_bytes[4:4+4], byteorder="little")
        header._minor_version = int.from_bytes(header_bytes[24:24+2], byteorder="little")
        header._major_version = int.from_bytes(header_bytes[26:26+2], byteorder="little")
        header._byte_order = int.from_bytes(header_bytes[28:28+2], byteorder="little")
        header._sector_shift = int.from_bytes(header_bytes[30:30+2], byteorder="little")
        header._mini_sector_shift = int.from_bytes(header_bytes[32:32+2], byteorder="little")
        header._reserved = ReaderUtils.__get_byte_array_portion(header_bytes, 34, 6)
        header._directory_sectors_count = int.from_bytes(header_bytes[40:40+4], byteorder="little")
        header._fatsectors_count = int.from_bytes(header_bytes[44:44+4], byteorder="little")
        header._first_directory_sector_location = int.from_bytes(header_bytes[48:48+4], byteorder="little")
        header._transaction_signature_number = int.from_bytes(header_bytes[52:52+4], byteorder="little")
        header._mini_stream_cutoff_size = int.from_bytes(header_bytes[56:56+4], byteorder="little")
        header._first_minifatsector_location = int.from_bytes(header_bytes[60:60+4], byteorder="little")
        header._minifatsectors_count = int.from_bytes(header_bytes[64:64+4], byteorder="little")
        header._firstdifatsector_location = int.from_bytes(header_bytes[68:68+4], byteorder="little")
        header._difatsectors_count = int.from_bytes(header_bytes[72:72+4], byteorder="little")
        header._difat = Utils.newArray(ReaderUtils._headerdifatsectors_count, 0)
        i = 0
        while i < ReaderUtils._headerdifatsectors_count: 
            header._difat[i] = int.from_bytes(header_bytes[76 + (i * 4):76 + (i * 4)+4], byteorder="little")
            i += 1
        return header
    
    @staticmethod
    def _read_fragment(s : Stream, stream_offset : int, length : int) -> bytearray:
        data = Utils.newArrayOfBytes(length, 0)
        s.position = stream_offset
        read = s.read(data, 0, length)
        if (read <= 0): 
            raise Utils.newException("Unexcpected eof of file", None)
        return data
    
    @staticmethod
    def _read_uint32(s : Stream, stream_offset : int) -> int:
        return int.from_bytes(ReaderUtils._read_fragment(s, stream_offset, 4)[0:0+4], byteorder="little")
    
    @staticmethod
    def _read_array_of_uint32(s : Stream, stream_offset : int, count : int) -> typing.List[int]:
        array0_ = Utils.newArray(count, 0)
        data = ReaderUtils._read_fragment(s, stream_offset, 4 * count)
        i = 0
        while i < count: 
            array0_[i] = int.from_bytes(data[4 * i:4 * i+4], byteorder="little")
            i += 1
        return array0_
    
    @staticmethod
    def _read_directory_entry(s : Stream, stream_offset : int, is_version3 : bool) -> 'CFDirectoryEntry':
        data = ReaderUtils._read_fragment(s, stream_offset, ReaderUtils._directory_entry_size)
        entry = CFDirectoryEntry()
        entry._name_length = int.from_bytes(data[64:64+2], byteorder="little")
        name_length = min(32, math.floor((entry._name_length) / 2))
        entry._name = Utils.newArray(name_length, None)
        i = 0
        while i < name_length: 
            entry._name[i] = (chr(int.from_bytes(data[2 * i:2 * i+2], byteorder="little")))
            i += 1
        entry._object_type = data[66]
        entry._color_flag = data[67]
        entry._left_siblingid = int.from_bytes(data[68:68+4], byteorder="little")
        entry._right_siblingid = int.from_bytes(data[72:72+4], byteorder="little")
        entry._childid = int.from_bytes(data[76:76+4], byteorder="little")
        entry._state_bits = int.from_bytes(data[96:96+4], byteorder="little")
        entry._starting_sector_location = int.from_bytes(data[116:116+4], byteorder="little")
        entry._stream_size = int.from_bytes(data[120:120+4], byteorder="little")
        if (is_version3): 
            entry._stream_size &= (0xFFFFFFFF)
        return entry
    
    @staticmethod
    def _validate_header(header : 'CFHeader') -> None:
        if (header._signature1 != CFHeader._default_signature1 or header._signature2 != CFHeader._default_signature2): 
            raise Utils.newException("Invalid header: signature", None)
        if (header._clsid != Utils.EMPTYUUID): 
            pass
        if (header._minor_version != (0x3E)): 
            pass
        if (header._major_version != (3) and header._major_version != (4)): 
            raise Utils.newException("Invalid header: Major version", None)
        if (header._byte_order != (0xFFFE)): 
            raise Utils.newException("Invalid header: Byte order", None)
        if (header._major_version == (3) and header._sector_shift != (0x0009)): 
            raise Utils.newException("Invalid header: Sector shirt for v3", None)
        if (header._major_version == (4) and header._sector_shift != (0x000c)): 
            raise Utils.newException("Invalid header: Sector shirt for v4", None)
        if (header._mini_sector_shift != (0x0006)): 
            raise Utils.newException("Invalid header: Mini sector shirt", None)
        if (((header._reserved[0] != (0) or header._reserved[1] != (0) or header._reserved[2] != (0)) or header._reserved[3] != (0) or header._reserved[4] != (0)) or header._reserved[5] != (0)): 
            raise Utils.newException("Invalid header: Reserved", None)
        if (header._major_version == (3) and header._directory_sectors_count != (0)): 
            raise Utils.newException("Invalid header: Directory sectors for v3", None)
        if (header._mini_stream_cutoff_size != (0x1000)): 
            raise Utils.newException("Invalid header: Mini stream cutoff size", None)
    
    @staticmethod
    def _validate_directory_entry(entry : 'CFDirectoryEntry') -> None:
        len0_ = entry._name_length
        if ((len(entry._name) * 2) != len0_ or len0_ == 0): 
            raise Utils.newException("Invalid directory entry: name length", None)
        if ((ord(entry._name[len(entry._name) - 1])) != 0): 
            raise Utils.newException("Invalid directory entry: name null termination", None)
        for ch in entry._name: 
            if ((ch == '/' or ch == '\\' or ch == ':') or ch == '!'): 
                raise Utils.newException("Invalid directory entry: illegal char in name", None)
        if ((entry._object_type != DirectoryObjectTypes._unknown and entry._object_type != DirectoryObjectTypes._storage and entry._object_type != DirectoryObjectTypes._stream) and entry._object_type != DirectoryObjectTypes._root_storage): 
            raise Utils.newException("Invalid directory entry: object type", None)
        if (entry._color_flag != TreeColors._red and entry._color_flag != TreeColors._black): 
            raise Utils.newException("Invalid directory entry: color flag", None)
        if (entry._left_siblingid > DirectoryStreamIds._maxregsid and entry._left_siblingid != DirectoryStreamIds._nostream): 
            raise Utils.newException("Invalid directory entry: left sibling", None)
        if (entry._right_siblingid > DirectoryStreamIds._maxregsid and entry._right_siblingid != DirectoryStreamIds._nostream): 
            raise Utils.newException("Invalid directory entry: right sibling", None)
        if (entry._childid > DirectoryStreamIds._maxregsid and entry._childid != DirectoryStreamIds._nostream): 
            raise Utils.newException("Invalid directory entry: child", None)
    
    @staticmethod
    def __get_byte_array_portion(source : bytearray, offset : int, length : int) -> bytearray:
        bytes0_ = Utils.newArrayOfBytes(length, 0)
        Utils.copyArray(source, offset, bytes0_, 0, length)
        return bytes0_