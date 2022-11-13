# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.Deflater import Deflater

class DeflaterOutputStream(Stream):
    # A special stream deflating or compressing the bytes that are
    # written to it.  It uses a Deflater to perform actual deflating.<br/>
    
    def __init__(self, base_output_stream : Stream, deflater : 'Deflater'=None, buffer_size : int=512) -> None:
        super().__init__()
        self.__password = None;
        self.__buffer_ = None;
        self._deflater_ = None;
        self._base_output_stream_ = None;
        self.__is_closed_ = False
        self.__is_stream_owner_ = True
        if (deflater is None): 
            deflater = Deflater()
        self._base_output_stream_ = base_output_stream
        self.__buffer_ = Utils.newArrayOfBytes(buffer_size, 0)
        self._deflater_ = deflater
    
    def finish(self) -> None:
        self._deflater_.finish()
        while not self._deflater_.is_finished:
            len0_ = self._deflater_.deflate_ex(self.__buffer_, 0, len(self.__buffer_))
            if (len0_ <= 0): 
                break
            self._base_output_stream_.write(self.__buffer_, 0, len0_)
        if (not self._deflater_.is_finished): 
            raise Utils.newException("Can't deflate all input?", None)
        self._base_output_stream_.flush()
    
    @property
    def is_stream_owner(self) -> bool:
        return self.__is_stream_owner_
    @is_stream_owner.setter
    def is_stream_owner(self, value) -> bool:
        self.__is_stream_owner_ = value
        return value
    
    @property
    def can_patch_entries(self) -> bool:
        return self._base_output_stream_.seekable
    
    def _deflate(self) -> None:
        while not self._deflater_.is_needing_input:
            deflate_count = self._deflater_.deflate_ex(self.__buffer_, 0, len(self.__buffer_))
            if (deflate_count <= 0): 
                break
            self._base_output_stream_.write(self.__buffer_, 0, deflate_count)
        if (not self._deflater_.is_needing_input): 
            raise Utils.newException("DeflaterOutputStream can't deflate all input?", None)
    
    @property
    def can_read(self) -> bool:
        return False
    
    @property
    def can_seek(self) -> bool:
        return False
    
    @property
    def can_write(self) -> bool:
        try: 
            return self._base_output_stream_.writable
        except Exception as ex: 
            return False
    
    @property
    def length(self) -> int:
        try: 
            return self._base_output_stream_.length
        except Exception as ex: 
            return -1
    
    @property
    def position(self) -> int:
        try: 
            return self._base_output_stream_.position
        except Exception as ex: 
            return 0
    @position.setter
    def position(self, value) -> int:
        return value
    
    def seek(self, offset : int, origin : int) -> int:
        return 0
    
    def set_length(self, value : int) -> None:
        pass
    
    def readbyte(self) -> int:
        return -1
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        return -1
    
    def flush(self) -> None:
        try: 
            self._deflater_.flush()
            self._deflate()
            self._base_output_stream_.flush()
        except Exception as ex: 
            raise Exception(ex.__str__(), ex)
    
    def close(self) -> None:
        if (not self.__is_closed_): 
            self.__is_closed_ = True
            try: 
                self.finish()
            except Exception as ex: 
                raise Exception(ex.__str__(), ex)
            finally: 
                if (self.__is_stream_owner_): 
                    try: 
                        self._base_output_stream_.close()
                    except Exception as ex: 
                        pass
    
    def writebyte(self, value : int) -> None:
        b = Utils.newArrayOfBytes(1, 0)
        b[0] = value
        self.write(b, 0, 1)
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        try: 
            self._deflater_.set_input_ex(buffer, offset, count)
            self._deflate()
        except Exception as ex: 
            raise Exception(ex.__str__(), ex)