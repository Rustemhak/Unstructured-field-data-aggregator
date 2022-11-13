# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.InflaterInputBuffer import InflaterInputBuffer
from pullenti.unitext.internal.zip.Inflater import Inflater

class InflaterInputStream(Stream):
    # This filter stream is used to decompress data compressed using the "deflate"
    # format. The "deflate" format is described in RFC 1951.
    # This stream may form the basis for other decompression filters, such
    # as the <see cref="ICSharpCode.SharpZipLib.GZip.GZipInputStream">GZipInputStream</see>.
    
    def __init__(self, base_input_stream : Stream, inflater : 'Inflater'=None, buffer_size : int=4096) -> None:
        super().__init__()
        self._inf = None;
        self._input_buffer = None;
        self.__base_input_stream = None;
        self._csize = 0
        self.__is_closed = False
        self.__m_is_stream_owner = True
        if (inflater is None): 
            inflater = Inflater()
        if (base_input_stream is None): 
            raise Exception("baseInputStream")
        if (inflater is None): 
            raise Exception("inflater")
        if (buffer_size <= 0): 
            raise Exception("bufferSize")
        self.__base_input_stream = base_input_stream
        self._inf = inflater
        self._input_buffer = InflaterInputBuffer(base_input_stream, buffer_size)
    
    @property
    def is_stream_owner(self) -> bool:
        return self.__m_is_stream_owner
    @is_stream_owner.setter
    def is_stream_owner(self, value) -> bool:
        self.__m_is_stream_owner = value
        return value
    
    def skip(self, count : int) -> int:
        if (count <= 0): 
            raise Exception("count")
        if (self.__base_input_stream.seekable): 
            self.__base_input_stream.seek(count, 1)
            return count
        else: 
            length_ = 2048
            if (count < length_): 
                length_ = (count)
            tmp = Utils.newArrayOfBytes(length_, 0)
            read_count = 1
            to_skip = count
            while ((to_skip > 0)) and ((read_count > 0)):
                if (to_skip < length_): 
                    length_ = (to_skip)
                read_count = self.__base_input_stream.read(tmp, 0, length_)
                to_skip -= read_count
            return count - to_skip
    
    @property
    def available(self) -> int:
        return (0 if self._inf.is_finished else 1)
    
    def _fill(self) -> None:
        if (self._input_buffer.available <= 0): 
            self._input_buffer.fill()
            if (self._input_buffer.available <= 0): 
                raise Utils.newException("Unexpected EOF", None)
        self._input_buffer.set_inflater_input(self._inf)
    
    @property
    def can_read(self) -> bool:
        return self.__base_input_stream.readable
    
    @property
    def can_seek(self) -> bool:
        return False
    
    @property
    def can_write(self) -> bool:
        return False
    
    @property
    def length(self) -> int:
        return self._input_buffer.raw_length
    
    @property
    def position(self) -> int:
        return self.__base_input_stream.position
    @position.setter
    def position(self, value) -> int:
        return value
    
    def flush(self) -> None:
        self.__base_input_stream.flush()
    
    def seek(self, offset : int, origin : int) -> int:
        return 0
    
    def set_length(self, value : int) -> None:
        raise Exception("InflaterInputStream SetLength not supported")
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        raise Exception("InflaterInputStream Write not supported")
    
    def writebyte(self, value : int) -> None:
        raise Exception("InflaterInputStream WriteByte not supported")
    
    def close(self) -> None:
        if (not self.__is_closed): 
            self.__is_closed = True
            if (self.__m_is_stream_owner): 
                self.__base_input_stream.close()
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        if (self._inf.is_needing_dictionary): 
            raise Exception("Need a dictionary")
        remaining_bytes = count
        while True:
            bytes_read = 0
            try: 
                bytes_read = self._inf.inflate_ex(buffer, offset, remaining_bytes)
            except Exception as ex: 
                raise Exception(ex.__str__(), ex)
            offset += bytes_read
            remaining_bytes -= bytes_read
            if (remaining_bytes == 0 or self._inf.is_finished): 
                break
            if (self._inf.is_needing_input): 
                try: 
                    self._fill()
                except Exception as ex: 
                    raise Exception(ex.__str__(), ex)
            elif (bytes_read == 0): 
                raise Exception("Dont know what to do")
        return count - remaining_bytes