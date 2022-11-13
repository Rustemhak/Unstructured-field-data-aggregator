# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class StreamUtils:
    # Provides simple <see cref="Stream"/>" utilities.
    
    @staticmethod
    def read_fully(stream : Stream, buffer : bytearray) -> None:
        StreamUtils.read_fully_ex(stream, buffer, 0, len(buffer))
    
    @staticmethod
    def read_fully_ex(stream : Stream, buffer : bytearray, offset : int, count : int) -> None:
        if (stream is None): 
            raise Exception("stream")
        if (buffer is None): 
            raise Exception("buffer")
        if (((offset < 0)) or ((offset > len(buffer)))): 
            raise Exception("offset")
        if (((count < 0)) or (((offset + count) > len(buffer)))): 
            raise Exception("count")
        while count > 0:
            read_count = stream.read(buffer, offset, count)
            if (read_count <= 0): 
                raise Exception()
            offset += read_count
            count -= read_count
    
    @staticmethod
    def copy(source : Stream, destination : Stream, buffer : bytearray) -> None:
        if (source is None): 
            raise Exception("source")
        if (destination is None): 
            raise Exception("destination")
        if (buffer is None): 
            raise Exception("buffer")
        if (len(buffer) < 128): 
            raise Exception("Buffer is too small", "buffer")
        copying = True
        while copying:
            bytes_read = source.read(buffer, 0, len(buffer))
            if (bytes_read > 0): 
                destination.write(buffer, 0, bytes_read)
            else: 
                destination.flush()
                copying = False
    
    def __init__(self) -> None:
        pass