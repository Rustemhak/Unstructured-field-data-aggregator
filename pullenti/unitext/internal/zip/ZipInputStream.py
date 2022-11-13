# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.CompressionMethod import CompressionMethod
from pullenti.unitext.internal.zip.GeneralBitFlags import GeneralBitFlags
from pullenti.unitext.internal.zip.InflaterInputStream import InflaterInputStream
from pullenti.unitext.internal.zip.ZipConstants import ZipConstants
from pullenti.unitext.internal.zip.Inflater import Inflater
from pullenti.unitext.internal.zip.Crc32 import Crc32
from pullenti.unitext.internal.zip.ZipEntry import ZipEntry

class ZipInputStream(InflaterInputStream):
    # This is an InflaterInputStream that reads the files baseInputStream an zip archive
    # one after another.  It has a special method to get the zip entry of
    # the next file.  The zip entry contains information about the file name
    # size, compressed size, Crc, etc.
    # It includes support for Stored and Deflated entries.
    
    class ReadDataHandler:
        """ Delegate for reading bytes from a stream. """
        
        def call(self, b : bytearray, offset : int, length_ : int) -> int:
            return None
    
    class ReadDataHandler_ReadingNotAvailable(ZipInputStream.ReadDataHandler):
        
        def __init__(self, src : 'ZipInputStream') -> None:
            super().__init__()
            self.__m_source = None;
            self.__m_source = src
        
        def call(self, destination : bytearray, offset : int, count : int) -> int:
            return self.__m_source._reading_not_available(destination, offset, count)
    
    class ReadDataHandler_InitialRead(ZipInputStream.ReadDataHandler):
        
        def __init__(self, src : 'ZipInputStream') -> None:
            super().__init__()
            self.__m_source = None;
            self.__m_source = src
        
        def call(self, destination : bytearray, offset : int, count : int) -> int:
            return self.__m_source._initial_read(destination, offset, count)
    
    class ReadDataHandler_ReadingNotSupported(ZipInputStream.ReadDataHandler):
        
        def __init__(self, src : 'ZipInputStream') -> None:
            super().__init__()
            self.__m_source = None;
            self.__m_source = src
        
        def call(self, destination : bytearray, offset : int, count : int) -> int:
            return self.__m_source._reading_not_supported(destination, offset, count)
    
    class ReadDataHandler_BodyRead(ZipInputStream.ReadDataHandler):
        
        def __init__(self, src : 'ZipInputStream') -> None:
            super().__init__()
            self.__m_source = None;
            self.__m_source = src
        
        def call(self, buffer : bytearray, offset : int, count : int) -> int:
            return self.__m_source._body_read(buffer, offset, count)
    
    def __init__(self, base_input_stream : Stream, buffer_size : int=4096) -> None:
        super().__init__(base_input_stream, Inflater(True), buffer_size)
        self.__internal_reader = None;
        self.__m_crc = Crc32()
        self.__m_entry = None;
        self.__m_size = 0
        self.__m_method = 0
        self.__m_flags = 0
        self.__m_password = None;
        self.__read_data_handler_reading_not_available = ZipInputStream.ReadDataHandler_ReadingNotAvailable(self)
        self.__read_data_handler_initial_read = ZipInputStream.ReadDataHandler_InitialRead(self)
        self.__read_data_handler_reading_not_supported = ZipInputStream.ReadDataHandler_ReadingNotSupported(self)
        self.__read_data_handler_body_read = ZipInputStream.ReadDataHandler_BodyRead(self)
        self.__internal_reader = self.__read_data_handler_reading_not_available
    
    @property
    def password(self) -> str:
        return self.__m_password
    @password.setter
    def password(self, value) -> str:
        self.__m_password = value
        return value
    
    @property
    def can_decompress_entry(self) -> bool:
        return ((self.__m_entry is not None)) and self.__m_entry.can_decompress
    
    def get_next_entry(self) -> 'ZipEntry':
        if (self.__m_crc is None): 
            raise Exception("Closed.")
        if (self.__m_entry is not None): 
            self.close_entry()
        header = self._input_buffer.read_le_int()
        if ((header == ZipConstants.CENTRAL_HEADER_SIGNATURE or header == ZipConstants.END_OF_CENTRAL_DIRECTORY_SIGNATURE or header == ZipConstants.CENTRAL_HEADER_DIGITAL_SIGNATURE) or header == ZipConstants.ARCHIVE_EXTRA_DATA_SIGNATURE or header == ZipConstants.ZIP64CENTRAL_FILE_HEADER_SIGNATURE): 
            self.close()
            return None
        if (((header == ZipConstants.SPANNING_TEMP_SIGNATURE)) or ((header == ZipConstants.SPANNING_SIGNATURE))): 
            header = self._input_buffer.read_le_int()
        if (header != ZipConstants.LOCAL_HEADER_SIGNATURE): 
            raise Utils.newException("Wrong Local header signature: 0x" + "{0}".format("{:X}".format(header)), None)
        version_required_to_extract = self._input_buffer.read_le_short()
        self.__m_flags = self._input_buffer.read_le_short()
        self.__m_method = self._input_buffer.read_le_short()
        dostime = self._input_buffer.read_le_int()
        crc2 = self._input_buffer.read_le_int()
        self._csize = self._input_buffer.read_le_int()
        self.__m_size = self._input_buffer.read_le_int()
        name_len = self._input_buffer.read_le_short()
        extra_len = self._input_buffer.read_le_short()
        is_crypted = ((self.__m_flags & 1)) == 1
        buffer = Utils.newArrayOfBytes(name_len, 0)
        self._input_buffer.read_raw_buffer(buffer)
        name = ZipConstants.convert_to_string_ext0(self.__m_flags, buffer)
        self.__m_entry = ZipEntry(name, version_required_to_extract)
        self.__m_entry.flags = self.__m_flags
        self.__m_entry._compression_method = Utils.valToEnum(self.__m_method, CompressionMethod)
        if (((self.__m_flags & 8)) == 0): 
            self.__m_entry.crc = crc2
            self.__m_entry.size = self.__m_size
            self.__m_entry.compressed_size = self._csize
            self.__m_entry._crypto_check_value = (((crc2 >> 24)) & 0xff)
        else: 
            if (crc2 != 0): 
                self.__m_entry.crc = crc2
            if (self.__m_size != 0): 
                self.__m_entry.size = self.__m_size
            if (self._csize != 0): 
                self.__m_entry.compressed_size = self._csize
            self.__m_entry._crypto_check_value = ((((dostime) >> 8)) & 0xff)
        self.__m_entry.dos_time = dostime
        if (extra_len > 0): 
            extra = Utils.newArrayOfBytes(extra_len, 0)
            self._input_buffer.read_raw_buffer(extra)
            self.__m_entry.extra_data = extra
        self.__m_entry._process_extra_data(True)
        if (self.__m_entry.compressed_size >= 0): 
            self._csize = self.__m_entry.compressed_size
        if (self.__m_entry.size >= 0): 
            self.__m_size = self.__m_entry.size
        if (self.__m_method == (CompressionMethod.STORED) and (((not is_crypted and self._csize != self.__m_size) or ((is_crypted and (self._csize - ZipConstants.CRYPTO_HEADER_SIZE) != self.__m_size))))): 
            raise Utils.newException("Stored, but compressed != uncompressed", None)
        if (self.__m_entry.is_compression_method_supported()): 
            self.__internal_reader = self.__read_data_handler_initial_read
        else: 
            self.__internal_reader = self.__read_data_handler_reading_not_supported
        return self.__m_entry
    
    def __read_data_descriptor(self) -> None:
        if (self._input_buffer.read_le_int() != ZipConstants.DATA_DESCRIPTOR_SIGNATURE): 
            raise Utils.newException("Data descriptor signature not found", None)
        self.__m_entry.crc = self._input_buffer.read_le_int()
        if (self.__m_entry.local_header_requires_zip64): 
            self._csize = (self._input_buffer.read_le_int())
            self._input_buffer.read_le_int()
            self.__m_size = (self._input_buffer.read_le_int())
            self._input_buffer.read_le_int()
        else: 
            self._csize = self._input_buffer.read_le_int()
            self.__m_size = self._input_buffer.read_le_int()
        self.__m_entry.compressed_size = self._csize
        self.__m_entry.size = self.__m_size
    
    def __complete_close_entry(self, test_crc : bool) -> None:
        if (((self.__m_flags & 8)) != 0): 
            self.__read_data_descriptor()
        self.__m_size = 0
        if (test_crc and ((self.__m_crc.value != self.__m_entry.crc))): 
            raise Utils.newException("CRC mismatch", None)
        self.__m_crc.reset()
        if (self.__m_method == (CompressionMethod.DEFLATED)): 
            self._inf.reset()
        self.__m_entry = (None)
    
    def close_entry(self) -> None:
        if (self.__m_crc is None): 
            raise Exception("Closed")
        if (self.__m_entry is None): 
            return
        if (self.__m_method == (CompressionMethod.DEFLATED)): 
            if (((self.__m_flags & 8)) != 0): 
                tmp = Utils.newArrayOfBytes(4096, 0)
                while self.read(tmp, 0, len(tmp)) > 0:
                    pass
                return
            self._csize -= self._inf.total_in
            self._input_buffer.available = self._input_buffer.available + self._inf.remaining_input
        if (((self._input_buffer.available > self._csize)) and ((self._csize >= 0))): 
            self._input_buffer.available = ((self._input_buffer.available) - (self._csize))
        else: 
            self._csize -= self._input_buffer.available
            self._input_buffer.available = 0
            while self._csize != 0:
                skipped = super().skip(self._csize)
                if (skipped <= 0): 
                    raise Utils.newException("Zip archive ends early.", None)
                self._csize -= skipped
        self.__complete_close_entry(False)
    
    @property
    def available(self) -> int:
        return (1 if self.__m_entry is not None else 0)
    
    @property
    def length(self) -> int:
        if (self.__m_entry is not None): 
            if (self.__m_entry.size >= 0): 
                return self.__m_entry.size
            else: 
                return 0
        else: 
            return 0
    
    def readbyte(self) -> int:
        b = Utils.newArrayOfBytes(1, 0)
        if (self.read(b, 0, 1) <= 0): 
            return -1
        return (b[0]) & 0xff
    
    def _reading_not_available(self, destination : bytearray, offset : int, count : int) -> int:
        raise Exception("Unable to read from this stream")
    
    def _reading_not_supported(self, destination : bytearray, offset : int, count : int) -> int:
        raise Utils.newException("The compression method for this entry is not supported", None)
    
    def _initial_read(self, destination : bytearray, offset : int, count : int) -> int:
        if (not self.can_decompress_entry): 
            raise Utils.newException("Library cannot extract this entry. Version required is (" + str(self.__m_entry.version) + ")", None)
        if (((self._csize > 0)) or ((((self.__m_flags & (GeneralBitFlags.DESCRIPTOR))) != 0))): 
            if (((self.__m_method == (CompressionMethod.DEFLATED))) and ((self._input_buffer.available > 0))): 
                self._input_buffer.set_inflater_input(self._inf)
            self.__internal_reader = self.__read_data_handler_body_read
            return self._body_read(destination, offset, count)
        else: 
            self.__internal_reader = self.__read_data_handler_reading_not_available
            return 0
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        if (buffer is None): 
            raise Exception("null buffer")
        if (offset < 0): 
            raise Utils.newException("bad offset", None)
        if (count < 0): 
            raise Utils.newException("bad count", None)
        if (((len(buffer) - offset)) < count): 
            raise Exception("Invalid offset/count combination")
        try: 
            return self.__internal_reader.call(buffer, offset, count)
        except Exception as ex: 
            raise Exception(ex.__str__(), ex)
    
    def _body_read(self, buffer : bytearray, offset : int, count : int) -> int:
        if (self.__m_crc is None): 
            raise Exception("Closed")
        if (((self.__m_entry is None)) or ((count <= 0))): 
            return 0
        if ((offset + count) > len(buffer)): 
            raise Exception("Offset + count exceeds buffer size")
        finished = False
        swichVal = self.__m_method
        if (swichVal == CompressionMethod.DEFLATED): 
            count = super().read(buffer, offset, count)
            if (count <= 0): 
                if (not self._inf.is_finished): 
                    raise Utils.newException("Inflater not finished!", None)
                self._input_buffer.available = self._inf.remaining_input
                if (((self.__m_flags & 8)) == 0 and (((self._inf.total_in != self._csize and self._csize != 0xFFFFFFFF and self._csize != -1) or self._inf.total_out != self.__m_size))): 
                    raise Utils.newException(((("Size mismatch: " + (chr(self._csize)) + ";") + (chr(self.__m_size)) + " <-> ") + (chr(self._inf.total_in)) + ";") + (chr(self._inf.total_out)), None)
                self._inf.reset()
                finished = True
        elif (swichVal == CompressionMethod.STORED): 
            if (((count > self._csize)) and ((self._csize >= 0))): 
                count = (self._csize)
            if (count > 0): 
                count = self._input_buffer.read_clear_text_buffer(buffer, offset, count)
                if (count > 0): 
                    self._csize -= count
                    self.__m_size -= count
            if (self._csize == 0): 
                finished = True
            elif (count < 0): 
                raise Utils.newException("EOF in stored block", None)
        if (count > 0): 
            self.__m_crc.update_by_buf_ex(buffer, offset, count)
        if (finished): 
            self.__complete_close_entry(True)
        return count
    
    def close(self) -> None:
        self.__internal_reader = self.__read_data_handler_reading_not_available
        self.__m_crc = (None)
        self.__m_entry = (None)
        super().close()