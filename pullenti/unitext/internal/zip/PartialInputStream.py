# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

class PartialInputStream(Stream):
    """ A <see cref="PartialInputStream"/> is an <see cref="InflaterInputStream"/>
    whose data is only a part or subsection of a file. """
    
    def __init__(self, zip_file : 'ZipFile', start : int, length_ : int) -> None:
        """ Initialise a new instance of the <see cref="PartialInputStream"/> class.
        
        Args:
            zip_file(ZipFile): The <see cref="ZipFile"/> containing the underlying stream to use for IO.
            start(int): The start of the partial data.
            length_(int): The length of the partial data.
        """
        super().__init__()
        self.__m_zip_file = None;
        self.__m_base_stream = None;
        self.__m_start = 0
        self.__m_length = 0
        self.__m_read_pos = 0
        self.__m_end = 0
        self.__m_start = start
        self.__m_length = length_
        self.__m_zip_file = zip_file
        self.__m_base_stream = self.__m_zip_file._m_base_stream
        self.__m_read_pos = start
        self.__m_end = (start + length_)
    
    def readbyte(self) -> int:
        """ Read a byte from this stream.
        
        Returns:
            int: Returns the byte read or -1 on end of stream.
        """
        if (self.__m_read_pos >= self.__m_end): 
            return -1
        self.__m_base_stream.seek(self.__m_read_pos, 0)
        self.__m_read_pos += 1
        return self.__m_base_stream.readbyte()
    
    def close(self) -> None:
        """ Close this <see cref="PartialInputStream">partial input stream</see>. """
        pass
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        """ Reads a sequence of bytes from the current stream and advances the position within the stream by the number of bytes read.
        
        Args:
            buffer(bytearray): An array of bytes. When this method returns, the buffer contains the specified byte array with the values between offset and (offset + count - 1) replaced by the bytes read from the current source.
            offset(int): The zero-based byte offset in buffer at which to begin storing the data read from the current stream.
            count(int): The maximum number of bytes to be read from the current stream.
        
        Returns:
            int: The total number of bytes read into the buffer. This can be less than the number of bytes requested if that many bytes are not currently available, or zero (0) if the end of the stream has been reached.
        """
        if (count > (self.__m_end - self.__m_read_pos)): 
            count = ((self.__m_end - self.__m_read_pos))
            if (count == 0): 
                return 0
        self.__m_base_stream.seek(self.__m_read_pos, 0)
        read_count = self.__m_base_stream.read(buffer, offset, count)
        if (read_count > 0): 
            self.__m_read_pos += read_count
        return read_count
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        """ Writes a sequence of bytes to the current stream and advances the current position within this stream by the number of bytes written.
        
        Args:
            buffer(bytearray): An array of bytes. This method copies count bytes from buffer to the current stream.
            offset(int): The zero-based byte offset in buffer at which to begin copying bytes to the current stream.
            count(int): The number of bytes to be written to the current stream.
        """
        raise Exception("Not supported")
    
    def set_length(self, value : int) -> None:
        """ When overridden in a derived class, sets the length of the current stream.
        
        Args:
            value(int): The desired length of the current stream in bytes.
        """
        raise Exception("Not supported")
    
    def seek(self, offset : int, origin : int) -> int:
        """ When overridden in a derived class, sets the position within the current stream.
        
        Args:
            offset(int): A byte offset relative to the origin parameter.
            origin(int): A value of type <see cref="T:System.IO.SeekOrigin"></see> indicating the reference point used to obtain the new position.
        
        Returns:
            int: The new position within the current stream.
        """
        new_pos = self.__m_read_pos
        swichVal = origin
        if (swichVal == 0): 
            new_pos = (self.__m_start + (offset))
        elif (swichVal == 1): 
            new_pos = (self.__m_read_pos + (offset))
        elif (swichVal == 2): 
            new_pos = (self.__m_end + (offset))
        if (new_pos < self.__m_start): 
            raise Exception("Negative position is invalid")
        if (new_pos >= self.__m_end): 
            raise Exception("Cannot seek past end")
        self.__m_read_pos = new_pos
        return self.__m_read_pos
    
    def flush(self) -> None:
        """ Clears all buffers for this stream and causes any buffered data to be written to the underlying device. """
        pass
    
    @property
    def position(self) -> int:
        """ Gets or sets the position within the current stream.
        
        Returns:
            int: The current position within the stream.
        """
        return self.__m_read_pos - self.__m_start
    @position.setter
    def position(self, value) -> int:
        new_pos = self.__m_start + (value)
        if (new_pos < self.__m_start): 
            raise Exception("Negative position is invalid")
        if (new_pos >= self.__m_end): 
            raise Exception("Cannot seek past end")
        self.__m_read_pos = new_pos
        return value
    
    @property
    def length(self) -> int:
        """ Gets the length in bytes of the stream.
        
        Returns:
            int: A long value representing the length of the stream in bytes.
        """
        return self.__m_length
    
    @property
    def can_write(self) -> bool:
        """ Gets a value indicating whether the current stream supports writing.
        
        Returns:
            bool: true if the stream supports writing; otherwise, false.
        """
        return False
    
    @property
    def can_seek(self) -> bool:
        """ Gets a value indicating whether the current stream supports seeking.
        
        Returns:
            bool: true if the stream supports seeking; otherwise, false.
        """
        return True
    
    @property
    def can_read(self) -> bool:
        """ Gets a value indicating whether the current stream supports reading.
        
        Returns:
            bool: true if the stream supports reading; otherwise, false.
        """
        return True