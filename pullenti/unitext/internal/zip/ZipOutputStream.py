# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.GeneralBitFlags import GeneralBitFlags
from pullenti.unitext.internal.zip.ZipConstants import ZipConstants
from pullenti.unitext.internal.zip.DeflaterOutputStream import DeflaterOutputStream
from pullenti.unitext.internal.zip.ZipExtraData import ZipExtraData
from pullenti.unitext.internal.zip.ZipEntry import ZipEntry
from pullenti.unitext.internal.zip.ZipHelperStream import ZipHelperStream
from pullenti.unitext.internal.zip.Deflater import Deflater
from pullenti.unitext.internal.zip.UseZip64 import UseZip64
from pullenti.unitext.internal.zip.CompressionMethod import CompressionMethod
from pullenti.unitext.internal.zip.Crc32 import Crc32

class ZipOutputStream(DeflaterOutputStream):
    # This is a DeflaterOutputStream that writes the files into a zip
    # archive one after another.  It has a special method to start a new
    # zip entry.  The zip entries contains information about the file name
    # size, compressed size, CRC, etc.
    # It includes support for Stored and Deflated entries.
    # This class is not thread safe.
    
    def __init__(self, base_output_stream : Stream, buffer_size : int=512) -> None:
        super().__init__(base_output_stream, Deflater(Deflater.DEFAULT_COMPRESSION, True), buffer_size)
        self.__entries = list()
        self.__crc = Crc32()
        self.__cur_entry = None;
        self.__default_compression_level = Deflater.DEFAULT_COMPRESSION
        self.__cur_method = CompressionMethod.DEFLATED
        self.__size = 0
        self.__offset = 0
        self.__zip_comment = Utils.newArrayOfBytes(0, 0)
        self.__patch_entry_header = False
        self.__crc_patch_pos = -1
        self.__size_patch_pos = -1
        self.__use_zip64_ = UseZip64.DYNAMIC
    
    @property
    def is_finished(self) -> bool:
        return self.__entries is None
    
    def set_comment(self, comment : str) -> None:
        comment_bytes = ZipConstants.convert_to_array_str(comment)
        if (len(comment_bytes) > 0xffff): 
            raise Exception("comment")
        self.__zip_comment = comment_bytes
    
    def set_level(self, level : int) -> None:
        self._deflater_.set_level(level)
        self.__default_compression_level = level
    
    def get_level(self) -> int:
        return self._deflater_.get_level()
    
    @property
    def use_zip64(self) -> 'UseZip64':
        return self.__use_zip64_
    @use_zip64.setter
    def use_zip64(self, value) -> 'UseZip64':
        self.__use_zip64_ = value
        return value
    
    def __write_le_short(self, value : int) -> None:
        #begin unchecked C# block !!! 
        
        self._base_output_stream_.writebyte((value & 0xff))
        self._base_output_stream_.writebyte((((value >> 8)) & 0xff))
        #res unchecked C# block !!! 
    
    def __write_le_int(self, value : int) -> None:
        #begin unchecked C# block !!! 
        
        self.__write_le_short(value)
        self.__write_le_short(value >> 16)
        #res unchecked C# block !!! 
    
    def __write_le_long(self, value : int) -> None:
        #begin unchecked C# block !!! 
        
        self.__write_le_int(value)
        self.__write_le_int((value >> 32))
        #res unchecked C# block !!! 
    
    def put_next_entry(self, entry : 'ZipEntry') -> None:
        if (entry is None): 
            raise Exception("entry")
        if (self.__entries is None): 
            raise Exception("ZipOutputStream was finished")
        if (self.__cur_entry is not None): 
            self.close_entry()
        if (len(self.__entries) == 2147483647): 
            raise Utils.newException("Too many entries for Zip file", None)
        method = entry._compression_method
        compression_level = self.__default_compression_level
        entry.flags &= (GeneralBitFlags.UNICODETEXT)
        self.__patch_entry_header = False
        header_info_available = False
        if (entry.size == 0): 
            entry.compressed_size = entry.size
            entry.crc = 0
            method = CompressionMethod.STORED
            header_info_available = True
        else: 
            header_info_available = (((entry.size >= 0)) and entry.has_crc)
            if (method == CompressionMethod.STORED): 
                if (not header_info_available): 
                    if (not self.can_patch_entries): 
                        method = CompressionMethod.DEFLATED
                        compression_level = 0
                else: 
                    entry.compressed_size = entry.size
                    header_info_available = entry.has_crc
        if (header_info_available == False): 
            if (self.can_patch_entries == False): 
                entry.flags |= 8
            else: 
                self.__patch_entry_header = True
        entry.offset = self.__offset
        entry._compression_method = method
        self.__cur_method = method
        self.__size_patch_pos = (-1)
        if (((self.__use_zip64_ == UseZip64.ON)) or ((((entry.size < 0)) and ((self.__use_zip64_ == UseZip64.DYNAMIC))))): 
            entry.force_zip64()
        self.__write_le_int(ZipConstants.LOCAL_HEADER_SIGNATURE)
        self.__write_le_short(entry.version)
        self.__write_le_short(entry.flags)
        self.__write_le_short(entry._compression_method_for_header)
        self.__write_le_int(entry.dos_time)
        if (header_info_available == True): 
            self.__write_le_int(entry.crc)
            if (entry.local_header_requires_zip64): 
                self.__write_le_int(-1)
                self.__write_le_int(-1)
            else: 
                self.__write_le_int(((entry.compressed_size) + ZipConstants.CRYPTO_HEADER_SIZE if entry.is_crypted else entry.compressed_size))
                self.__write_le_int(entry.size)
        else: 
            if (self.__patch_entry_header): 
                self.__crc_patch_pos = self._base_output_stream_.position
            self.__write_le_int(0)
            if (self.__patch_entry_header): 
                self.__size_patch_pos = self._base_output_stream_.position
            if (entry.local_header_requires_zip64 or self.__patch_entry_header): 
                self.__write_le_int(-1)
                self.__write_le_int(-1)
            else: 
                self.__write_le_int(0)
                self.__write_le_int(0)
        name = ZipConstants.convert_to_array(entry.flags, entry.name)
        if (len(name) > 0xFFFF): 
            raise Utils.newException("Entry name too long.", None)
        ed = ZipExtraData(entry.extra_data)
        if (entry.local_header_requires_zip64): 
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
            if (self.__patch_entry_header): 
                self.__size_patch_pos = (ed.current_read_index)
        else: 
            ed.delete(1)
        extra = ed.get_entry_data()
        self.__write_le_short(len(name))
        self.__write_le_short(len(extra))
        if (len(name) > 0): 
            self._base_output_stream_.write(name, 0, len(name))
        if (entry.local_header_requires_zip64 and self.__patch_entry_header): 
            self.__size_patch_pos += self._base_output_stream_.position
        if (len(extra) > 0): 
            self._base_output_stream_.write(extra, 0, len(extra))
        self.__offset += (ZipConstants.LOCAL_HEADER_BASE_SIZE + len(name) + len(extra))
        if (entry.aeskey_size > 0): 
            self.__offset += entry._aesoverhead_size
        self.__cur_entry = entry
        self.__crc.reset()
        if (method == CompressionMethod.DEFLATED): 
            self._deflater_.reset()
            self._deflater_.set_level(compression_level)
        self.__size = 0
    
    def close_entry(self) -> None:
        if (self.__cur_entry is None): 
            raise Exception("No open entry")
        csize = self.__size
        if (self.__cur_method == CompressionMethod.DEFLATED): 
            if (self.__size >= 0): 
                super().finish()
                csize = self._deflater_.total_out
            else: 
                self._deflater_.reset()
        if (self.__cur_entry.size < 0): 
            self.__cur_entry.size = self.__size
        elif (self.__cur_entry.size != self.__size): 
            raise Utils.newException(("size was " + (chr(self.__size)) + ", but I expected ") + (chr(self.__cur_entry.size)), None)
        if (self.__cur_entry.compressed_size < 0): 
            self.__cur_entry.compressed_size = csize
        elif (self.__cur_entry.compressed_size != csize): 
            raise Utils.newException(("compressed size was " + (chr(csize)) + ", but I expected ") + (chr(self.__cur_entry.compressed_size)), None)
        if (not self.__cur_entry.crc_ok): 
            self.__cur_entry.crc = self.__crc.value
        elif (self.__cur_entry.crc != self.__crc.value): 
            raise Utils.newException(("crc was " + (chr(self.__crc.value)) + ", but I expected ") + (chr(self.__cur_entry.crc)), None)
        self.__offset += csize
        if (self.__cur_entry.is_crypted): 
            if (self.__cur_entry.aeskey_size > 0): 
                self.__cur_entry.compressed_size = self.__cur_entry.compressed_size + self.__cur_entry._aesoverhead_size
            else: 
                self.__cur_entry.compressed_size = self.__cur_entry.compressed_size + ZipConstants.CRYPTO_HEADER_SIZE
        if (self.__patch_entry_header): 
            self.__patch_entry_header = False
            cur_pos = self._base_output_stream_.position
            self._base_output_stream_.seek(self.__crc_patch_pos, 0)
            self.__write_le_int(self.__cur_entry.crc)
            if (self.__cur_entry.local_header_requires_zip64): 
                if (self.__size_patch_pos == (-1)): 
                    raise Utils.newException("Entry requires zip64 but this has been turned off", None)
                self._base_output_stream_.seek(self.__size_patch_pos, 0)
                self.__write_le_long(self.__cur_entry.size)
                self.__write_le_long(self.__cur_entry.compressed_size)
            else: 
                self.__write_le_int(self.__cur_entry.compressed_size)
                self.__write_le_int(self.__cur_entry.size)
            self._base_output_stream_.seek(cur_pos, 0)
        if (((self.__cur_entry.flags & 8)) != 0): 
            self.__write_le_int(ZipConstants.DATA_DESCRIPTOR_SIGNATURE)
            self.__write_le_int(self.__cur_entry.crc)
            if (self.__cur_entry.local_header_requires_zip64): 
                self.__write_le_long(self.__cur_entry.compressed_size)
                self.__write_le_long(self.__cur_entry.size)
                self.__offset += ZipConstants.ZIP64DATA_DESCRIPTOR_SIZE
            else: 
                self.__write_le_int(self.__cur_entry.compressed_size)
                self.__write_le_int(self.__cur_entry.size)
                self.__offset += ZipConstants.DATA_DESCRIPTOR_SIZE
        self.__entries.append(self.__cur_entry)
        self.__cur_entry = (None)
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        if (self.__cur_entry is None): 
            raise Exception("No open entry.")
        if (buffer is None): 
            raise Exception("null buffer")
        if (offset < 0): 
            raise Utils.newException("offset out of range", None)
        if (count < 0): 
            raise Utils.newException("bad count", None)
        if (((len(buffer) - offset)) < count): 
            raise Exception("Invalid offset/count combination")
        try: 
            self.__crc.update_by_buf_ex(buffer, offset, count)
        except Exception as ex: 
            raise Exception(ex.__str__(), ex)
        self.__size += count
        try: 
            swichVal = self.__cur_method
            if (swichVal == CompressionMethod.DEFLATED): 
                super().write(buffer, offset, count)
            elif (swichVal == CompressionMethod.STORED): 
                self._base_output_stream_.write(buffer, offset, count)
        except Exception as ex: 
            raise Exception(ex.__str__(), ex)
    
    def finish(self) -> None:
        if (self.__entries is None): 
            return
        if (self.__cur_entry is not None): 
            self.close_entry()
        num_entries = len(self.__entries)
        size_entries = 0
        for en in self.__entries: 
            entry = Utils.asObjectOrNull(en, ZipEntry)
            if (entry is None): 
                continue
            self.__write_le_int(ZipConstants.CENTRAL_HEADER_SIGNATURE)
            self.__write_le_short(ZipConstants.VERSION_MADE_BY)
            self.__write_le_short(entry.version)
            self.__write_le_short(entry.flags)
            self.__write_le_short(entry._compression_method_for_header)
            self.__write_le_int(entry.dos_time)
            self.__write_le_int(entry.crc)
            if (entry.is_zip64forced() or (((entry.compressed_size) >= 4294967295))): 
                self.__write_le_int(-1)
            else: 
                self.__write_le_int(entry.compressed_size)
            if (entry.is_zip64forced() or (((entry.size) >= 4294967295))): 
                self.__write_le_int(-1)
            else: 
                self.__write_le_int(entry.size)
            name = ZipConstants.convert_to_array(entry.flags, entry.name)
            if (len(name) > 0xffff): 
                raise Utils.newException("Name too long.", None)
            ed = ZipExtraData(entry.extra_data)
            if (entry.central_header_requires_zip64): 
                ed.start_new_entry()
                if (entry.is_zip64forced()): 
                    ed.add_le_long(entry.size, 0)
                if (entry.is_zip64forced()): 
                    ed.add_le_long(entry.compressed_size, 0)
                ed.add_new_entry(1)
            else: 
                ed.delete(1)
            extra = ed.get_entry_data()
            entry_comment = (ZipConstants.convert_to_array(entry.flags, entry.comment) if (entry.comment is not None) else Utils.newArrayOfBytes(0, 0))
            if (len(entry_comment) > 0xffff): 
                raise Utils.newException("Comment too long.", None)
            self.__write_le_short(len(name))
            self.__write_le_short(len(extra))
            self.__write_le_short(len(entry_comment))
            self.__write_le_short(0)
            self.__write_le_short(0)
            if (entry.external_file_attributes != -1): 
                self.__write_le_int(entry.external_file_attributes)
            elif (entry.is_directory): 
                self.__write_le_int(16)
            else: 
                self.__write_le_int(0)
            if ((entry.offset) >= 4294967295): 
                self.__write_le_int(-1)
            else: 
                self.__write_le_int(entry.offset)
            if (len(name) > 0): 
                self._base_output_stream_.write(name, 0, len(name))
            if (len(extra) > 0): 
                self._base_output_stream_.write(extra, 0, len(extra))
            if (len(entry_comment) > 0): 
                self._base_output_stream_.write(entry_comment, 0, len(entry_comment))
            size_entries += ((ZipConstants.CENTRAL_HEADER_BASE_SIZE + len(name) + len(extra)) + len(entry_comment))
        with ZipHelperStream(None, self._base_output_stream_) as zhs: 
            zhs.write_end_of_central_directory(num_entries, size_entries, self.__offset, self.__zip_comment)
        self.__entries = (None)