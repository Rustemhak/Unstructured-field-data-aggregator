# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.ZipConstants import ZipConstants
from pullenti.unitext.internal.zip.ZipExtraData import ZipExtraData
from pullenti.unitext.internal.zip.GeneralBitFlags import GeneralBitFlags

class ZipHelperStream(Stream):
    # This class assists with writing/reading from Zip files.
    
    def __init__(self, name : str, stream : Stream=None) -> None:
        super().__init__()
        self.__is_owner_ = False
        self.__stream_ = None;
        if (stream is None): 
            self.__stream_ = (FileStream(name, "r+b"))
            self.__is_owner_ = True
        else: 
            self.__stream_ = stream
    
    @property
    def is_stream_owner(self) -> bool:
        return self.__is_owner_
    @is_stream_owner.setter
    def is_stream_owner(self, value) -> bool:
        self.__is_owner_ = value
        return value
    
    @property
    def can_read(self) -> bool:
        return self.__stream_.readable
    
    @property
    def can_seek(self) -> bool:
        return self.__stream_.seekable
    
    @property
    def length(self) -> int:
        return self.__stream_.length
    
    @property
    def position(self) -> int:
        return self.__stream_.position
    @position.setter
    def position(self, value) -> int:
        self.__stream_.position = value
        return value
    
    @property
    def can_write(self) -> bool:
        return self.__stream_.writable
    
    def flush(self) -> None:
        self.__stream_.flush()
    
    def seek(self, offset : int, origin : int) -> int:
        return self.__stream_.seek(offset, origin)
    
    def set_length(self, value : int) -> None:
        self.__stream_.length = value
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        return self.__stream_.read(buffer, offset, count)
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        self.__stream_.write(buffer, offset, count)
    
    def close(self) -> None:
        to_close = self.__stream_
        self.__stream_ = (None)
        if (self.__is_owner_ and ((to_close is not None))): 
            self.__is_owner_ = False
            to_close.close()
    
    def __write_local_header(self, entry : 'ZipEntry', patch_data : 'EntryPatchData') -> None:
        method = entry._compression_method
        header_info_available = True
        patch_entry_header = False
        self.writeleint(ZipConstants.LOCAL_HEADER_SIGNATURE)
        self.writeleshort(entry.version)
        self.writeleshort(entry.flags)
        self.writeleshort(method)
        self.writeleint(entry.dos_time)
        if (header_info_available == True): 
            self.writeleint(entry.crc)
            if (entry.local_header_requires_zip64): 
                self.writeleint(-1)
                self.writeleint(-1)
            else: 
                self.writeleint(((entry.compressed_size) + ZipConstants.CRYPTO_HEADER_SIZE if entry.is_crypted else entry.compressed_size))
                self.writeleint(entry.size)
        else: 
            if (patch_data is not None): 
                patch_data.crc_patch_offset = self.__stream_.position
            self.writeleint(0)
            if (patch_data is not None): 
                patch_data.size_patch_offset = self.__stream_.position
            if (entry.local_header_requires_zip64 and patch_entry_header): 
                self.writeleint(-1)
                self.writeleint(-1)
            else: 
                self.writeleint(0)
                self.writeleint(0)
        name = ZipConstants.convert_to_array(entry.flags, entry.name)
        if (len(name) > 0xFFFF): 
            raise Utils.newException("Entry name too long.", None)
        ed = ZipExtraData(entry.extra_data)
        if (entry.local_header_requires_zip64 and ((header_info_available or patch_entry_header))): 
            ed.start_new_entry()
            if (header_info_available): 
                ed.add_le_long(entry.size, 0)
                ed.add_le_long(entry.compressed_size, 0)
            else: 
                ed.add_le_long(-1, -1)
                ed.add_le_long(-1, -1)
            ed.add_new_entry(1)
            if (not ed.find(1)): 
                raise Utils.newException("Internal error cant find extra data", None)
            if (patch_data is not None): 
                patch_data.size_patch_offset = ed.current_read_index
        else: 
            ed.delete(1)
        extra = ed.get_entry_data()
        self.writeleshort(len(name))
        self.writeleshort(len(extra))
        if (len(name) > 0): 
            self.__stream_.write(name, 0, len(name))
        if (entry.local_header_requires_zip64 and patch_entry_header): 
            patch_data.size_patch_offset = patch_data.size_patch_offset + (self.__stream_.position)
        if (len(extra) > 0): 
            self.__stream_.write(extra, 0, len(extra))
    
    def locate_block_with_signature(self, signature : int, end_location : int, minimum_block_size : int, maximum_variable_data : int) -> int:
        pos = end_location - minimum_block_size
        if (pos < 0): 
            return -1
        give_up_marker = max(pos - maximum_variable_data, 0)
        first_pass = True
        while first_pass or (self.readleint() != signature):
            first_pass = False
            if (pos < give_up_marker): 
                return -1
            self.seek(pos, 0)
            pos -= 1
        return self.position
    
    def write_zip64end_of_central_directory(self, no_of_entries : int, size_entries : int, central_dir_offset : int) -> None:
        central_signature_offset = self.__stream_.position
        self.writeleint(ZipConstants.ZIP64CENTRAL_FILE_HEADER_SIGNATURE)
        self.writelelong(44)
        self.writeleshort(ZipConstants.VERSION_MADE_BY)
        self.writeleshort(ZipConstants.VERSION_ZIP64)
        self.writeleint(0)
        self.writeleint(0)
        self.writelelong(no_of_entries)
        self.writelelong(no_of_entries)
        self.writelelong(size_entries)
        self.writelelong(central_dir_offset)
        self.writeleint(ZipConstants.ZIP64CENTRAL_DIR_LOCATOR_SIGNATURE)
        self.writeleint(0)
        self.writelelong(central_signature_offset)
        self.writeleint(1)
    
    def write_end_of_central_directory(self, no_of_entries : int, size_entries : int, start_of_central_directory : int, comment : bytearray) -> None:
        self.writeleint(ZipConstants.END_OF_CENTRAL_DIRECTORY_SIGNATURE)
        self.writeleshort(0)
        self.writeleshort(0)
        if (no_of_entries >= 0xffff): 
            self.writeleushort(0xffff)
            self.writeleushort(0xffff)
        else: 
            self.writeleshort(no_of_entries)
            self.writeleshort(no_of_entries)
        self.writeleint(size_entries)
        self.writeleint(start_of_central_directory)
        comment_length = (len(comment) if (comment is not None) else 0)
        if (comment_length > 0xffff): 
            raise Utils.newException("Comment length({0}) is too long can only be 64K".format(comment_length), None)
        self.writeleshort(comment_length)
        if (comment_length > 0): 
            self.write(comment, 0, len(comment))
    
    def readleshort(self) -> int:
        byte_value1 = self.__stream_.readbyte()
        if (byte_value1 < 0): 
            raise Exception()
        byte_value2 = self.__stream_.readbyte()
        if (byte_value2 < 0): 
            raise Exception()
        return byte_value1 | ((byte_value2 << 8))
    
    def readleint(self) -> int:
        return self.readleshort() | ((self.readleshort() << 16))
    
    def writeleshort(self, value : int) -> None:
        self.__stream_.writebyte((value & 0xff))
        self.__stream_.writebyte((((value >> 8)) & 0xff))
    
    def writeleushort(self, value : int) -> None:
        self.__stream_.writebyte(((value) & 0xff))
        self.__stream_.writebyte(((value) >> 8))
    
    def writeleint(self, value : int) -> None:
        self.writeleshort(value)
        self.writeleshort(value >> 16)
    
    def writeleuint(self, value : int) -> None:
        self.writeleushort(((value) & 0xffff))
        self.writeleushort(((value) >> 16))
    
    def writelelong(self, value : int) -> None:
        self.writeleint(value)
        self.writeleint((value >> 32))
    
    def writeleulong(self, value : int) -> None:
        self.writeleuint(((value) & (0xffffffff)))
        self.writeleuint(((value) >> 32))
    
    def write_data_descriptor(self, entry : 'ZipEntry') -> int:
        if (entry is None): 
            raise Exception("entry")
        result = 0
        if (((entry.flags & (GeneralBitFlags.DESCRIPTOR))) != 0): 
            self.writeleint(ZipConstants.DATA_DESCRIPTOR_SIGNATURE)
            self.writeleint(entry.crc)
            result += 8
            if (entry.local_header_requires_zip64): 
                self.writelelong(entry.compressed_size)
                self.writelelong(entry.size)
                result += 16
            else: 
                self.writeleint(entry.compressed_size)
                self.writeleint(entry.size)
                result += 8
        return result
    
    def read_data_descriptor(self, zip64 : bool, data : 'DescriptorData') -> None:
        int_value = self.readleint()
        if (int_value != ZipConstants.DATA_DESCRIPTOR_SIGNATURE): 
            raise Utils.newException("Data descriptor signature not found", None)
        data.crc = self.readleint()
        if (zip64): 
            data.compressed_size = self.readleint()
            self.readleint()
            data.size = self.readleint()
            self.readleint()
        else: 
            data.compressed_size = self.readleint()
            data.size = self.readleint()