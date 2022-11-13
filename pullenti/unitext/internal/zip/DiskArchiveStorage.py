# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import shutil
import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.FileUpdateMode import FileUpdateMode
from pullenti.unitext.internal.zip.BaseArchiveStorage import BaseArchiveStorage

class DiskArchiveStorage(BaseArchiveStorage):
    """ An <see cref="IArchiveStorage"/> implementation suitable for hard disks. """
    
    def __init__(self, file : 'ZipFile', update_mode_ : 'FileUpdateMode'=FileUpdateMode.SAFE) -> None:
        """ Initializes a new instance of the <see cref="DiskArchiveStorage"/> class.
        
        Args:
            file(ZipFile): The file.
            update_mode_(FileUpdateMode): The update mode.
        """
        super().__init__(update_mode_)
        self.__temporary_stream_ = None;
        self.__file_name_ = None;
        self.__temporary_name_ = None;
        if (file.name is None): 
            raise Utils.newException("Cant handle non file archives", None)
        self.__file_name_ = file.name
    
    def get_temporary_output(self) -> Stream:
        """ Gets a temporary output <see cref="Stream"/> for performing updates on.
        
        Returns:
            Stream: Returns the temporary output stream.
        """
        if (self.__temporary_name_ is not None): 
            self.__temporary_name_ = DiskArchiveStorage.__get_temp_file_name(self.__temporary_name_, True)
            self.__temporary_stream_ = (FileStream(self.__temporary_name_, "r+b"))
        else: 
            self.__temporary_name_ = "temp.bin"
            self.__temporary_stream_ = (FileStream(self.__temporary_name_, "r+b"))
        return self.__temporary_stream_
    
    def convert_temporary_to_final(self) -> Stream:
        """ Converts a temporary <see cref="Stream"/> to its final form.
        
        Returns:
            Stream: Returns a <see cref="Stream"/> that can be used to read
        the final storage for the archive.
        """
        if (self.__temporary_stream_ is None): 
            raise Utils.newException("No temporary stream has been created", None)
        result = None
        move_temp_name = DiskArchiveStorage.__get_temp_file_name(self.__file_name_, False)
        new_file_created = False
        try: 
            self.__temporary_stream_.close()
            shutil.move(self.__file_name_, move_temp_name)
            shutil.move(self.__temporary_name_, self.__file_name_)
            new_file_created = True
            pathlib.Path(move_temp_name).unlink()
            result = (FileStream(self.__file_name_, "rb"))
        except Exception as ex511: 
            result = (None)
            if (not new_file_created): 
                shutil.move(move_temp_name, self.__file_name_)
                pathlib.Path(self.__temporary_name_).unlink()
            raise ex511
        return result
    
    def make_temporary_copy(self, stream : Stream) -> Stream:
        """ Make a temporary copy of a stream.
        
        Args:
            stream(Stream): The <see cref="Stream"/> to copy.
        
        Returns:
            Stream: Returns a temporary output <see cref="Stream"/> that is a copy of the input.
        """
        stream.close()
        self.__temporary_name_ = DiskArchiveStorage.__get_temp_file_name(self.__file_name_, True)
        shutil.copy(self.__file_name_, self.__temporary_name_)
        self.__temporary_stream_ = (FileStream(self.__temporary_name_, "r+b"))
        return self.__temporary_stream_
    
    def open_for_direct_update(self, stream : Stream) -> Stream:
        """ Return a stream suitable for performing direct updates on the original source.
        
        Args:
            stream(Stream): The current stream.
        
        Returns:
            Stream: Returns a stream suitable for direct updating.
        """
        result = None
        if (((stream is None)) or not stream.writable): 
            if (stream is not None): 
                stream.close()
            return FileStream(self.__file_name_, "r+b")
        else: 
            result = stream
        return result
    
    def close(self) -> None:
        """ Disposes this instance. """
        if (self.__temporary_stream_ is not None): 
            self.__temporary_stream_.close()
            self.__temporary_stream_ = (None)
    
    @staticmethod
    def __get_temp_file_name(original : str, make_temp_file : bool) -> str:
        result = None
        if (original is None): 
            result = "temp.bin"
        else: 
            counter = 0
            suffix_seed = datetime.datetime.now().second
            while result is None:
                counter += 1
                new_name = "{0}.{1}{2}.tmp".format(original, suffix_seed, counter)
                if (not pathlib.Path(new_name).is_file()): 
                    if (make_temp_file): 
                        try: 
                            with FileStream(new_name, "wb") as stream: 
                                pass
                            result = new_name
                        except Exception as ex512: 
                            suffix_seed = datetime.datetime.now().second
                    else: 
                        result = new_name
        return result