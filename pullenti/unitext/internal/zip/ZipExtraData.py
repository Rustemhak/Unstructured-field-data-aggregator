# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.ITaggedData import ITaggedData
from pullenti.unitext.internal.zip.RawTaggedData import RawTaggedData
from pullenti.unitext.internal.zip.ExtendedUnixData import ExtendedUnixData
from pullenti.unitext.internal.zip.NTTaggedData import NTTaggedData

class ZipExtraData:
    # A class to handle the extra data field for Zip entries
    
    def __init__(self, data : bytearray=None) -> None:
        self.__index = 0
        self.__read_value_start = 0
        self.__read_value_length = 0
        self.__new_entry = None;
        self.__m_data = None;
        if (data is None): 
            self.__m_data = Utils.newArrayOfBytes(0, 0)
        else: 
            self.__m_data = data
    
    def get_entry_data(self) -> bytearray:
        if ((self.length) > (65535)): 
            raise Utils.newException("Data exceeds maximum length", None)
        if (self.__m_data is None): 
            return None
        res = Utils.newArrayOfBytes(len(self.__m_data), 0)
        Utils.copyArray(self.__m_data, 0, res, 0, len(self.__m_data))
        return res
    
    def clear(self) -> None:
        if (((self.__m_data is None)) or ((len(self.__m_data) != 0))): 
            self.__m_data = Utils.newArrayOfBytes(0, 0)
    
    @property
    def length(self) -> int:
        return len(self.__m_data)
    
    def get_stream_for_tag(self, tag : int) -> Stream:
        result = None
        if (self.find(tag)): 
            result = (MemoryStream(self.__m_data[self.__index : (self.__index + self.__read_value_length)]))
        return result
    
    def __get_data(self, tag : int) -> 'ITaggedData':
        result = None
        if (self.find(tag)): 
            result = ZipExtraData.__create(tag, self.__m_data, self.__read_value_start, self.__read_value_length)
        return result
    
    @staticmethod
    def __create(tag : int, data : bytearray, offset : int, count : int) -> 'ITaggedData':
        result = None
        swichVal = tag
        if (swichVal == 0x000A): 
            result = (NTTaggedData())
        elif (swichVal == 0x5455): 
            result = (ExtendedUnixData())
        else: 
            result = (RawTaggedData(tag))
        result.set_data(data, offset, count)
        return result
    
    @property
    def value_length(self) -> int:
        return self.__read_value_length
    
    @property
    def current_read_index(self) -> int:
        return self.__index
    
    @property
    def unread_count(self) -> int:
        if (((self.__read_value_start > len(self.__m_data))) or ((self.__read_value_start < 4))): 
            raise Utils.newException("Find must be called before calling a Read method", None)
        return (self.__read_value_start + self.__read_value_length) - self.__index
    
    def find(self, headerid : int) -> bool:
        self.__read_value_start = len(self.__m_data)
        self.__read_value_length = 0
        self.__index = 0
        local_length = self.__read_value_start
        local_tag = headerid - 1
        while ((local_tag != headerid)) and ((self.__index < (len(self.__m_data) - 3))):
            local_tag = self.__read_short_internal()
            local_length = self.__read_short_internal()
            if (local_tag != headerid): 
                self.__index += local_length
        result = ((local_tag == headerid)) and ((((self.__index + local_length)) <= len(self.__m_data)))
        if (result): 
            self.__read_value_start = self.__index
            self.__read_value_length = local_length
        return result
    
    def add_entry(self, tagged_data : 'ITaggedData') -> None:
        if (tagged_data is None): 
            raise Exception("taggedData")
        self.add_entry2(tagged_data.tagid, tagged_data.get_data())
    
    def add_entry2(self, headerid : int, field_data : bytearray) -> None:
        if ((((headerid) > (65535))) or ((headerid < 0))): 
            raise Exception("headerID")
        add_length = (0 if (field_data is None) else len(field_data))
        if ((add_length) > (65535)): 
            raise Exception("fieldData", "exceeds maximum length")
        new_length = len(self.__m_data) + add_length + 4
        if (self.find(headerid)): 
            new_length -= ((self.value_length + 4))
        if ((new_length) > (65535)): 
            raise Utils.newException("Data exceeds maximum length", None)
        self.delete(headerid)
        new_data = Utils.newArrayOfBytes(new_length, 0)
        Utils.copyArray(self.__m_data, 0, new_data, 0, len(self.__m_data))
        index = len(self.__m_data)
        self.__m_data = new_data
        wrapindex516 = RefOutArgWrapper(index)
        self.__set_short(wrapindex516, headerid)
        index = wrapindex516.value
        wrapindex515 = RefOutArgWrapper(index)
        self.__set_short(wrapindex515, add_length)
        index = wrapindex515.value
        if (field_data is not None): 
            Utils.copyArray(field_data, 0, new_data, index, len(field_data))
    
    def start_new_entry(self) -> None:
        self.__new_entry = MemoryStream()
    
    def add_new_entry(self, headerid : int) -> None:
        new_data = self.__new_entry.toarray()
        self.__new_entry = (None)
        self.add_entry2(headerid, new_data)
    
    def add_data0(self, data : int) -> None:
        self.__new_entry.writebyte(data)
    
    def add_data(self, data : bytearray) -> None:
        if (data is None): 
            raise Exception("data")
        self.__new_entry.write(data, 0, len(data))
    
    def add_le_short(self, to_add : int) -> None:
        #begin unchecked C# block !!! 
        
        self.__new_entry.writebyte(to_add)
        self.__new_entry.writebyte((to_add >> 8))
        #res unchecked C# block !!! 
    
    def add_le_int(self, to_add : int) -> None:
        #begin unchecked C# block !!! 
        
        self.add_le_short(to_add)
        self.add_le_short((to_add >> 16))
        #res unchecked C# block !!! 
    
    def add_le_long(self, to_add1 : int, to_add2 : int) -> None:
        self.add_le_int(to_add1)
        self.add_le_int(to_add2)
    
    def delete(self, headerid : int) -> bool:
        result = False
        if (self.find(headerid)): 
            result = True
            true_start = self.__read_value_start - 4
            new_data = Utils.newArrayOfBytes(len(self.__m_data) - ((self.value_length + 4)), 0)
            Utils.copyArray(self.__m_data, 0, new_data, 0, true_start)
            true_end = true_start + self.value_length + 4
            Utils.copyArray(self.__m_data, true_end, new_data, true_start, len(self.__m_data) - true_end)
            self.__m_data = new_data
        return result
    
    def read_long(self) -> int:
        self.__read_check(8)
        res = self.read_int()
        self.read_int()
        return res
    
    def read_int(self) -> int:
        self.__read_check(4)
        result = ((self.__m_data[self.__index]) + (((self.__m_data[self.__index + 1]) << 8)) + (((self.__m_data[self.__index + 2]) << 16))) + (((self.__m_data[self.__index + 3]) << 24))
        self.__index += 4
        return result
    
    def read_short(self) -> int:
        self.__read_check(2)
        result = (self.__m_data[self.__index]) + (((self.__m_data[self.__index + 1]) << 8))
        self.__index += 2
        return result
    
    def read_byte(self) -> int:
        result = -1
        if (((self.__index < len(self.__m_data))) and (((self.__read_value_start + self.__read_value_length) > self.__index))): 
            result = (self.__m_data[self.__index])
            self.__index += 1
        return result
    
    def skip(self, amount : int) -> None:
        self.__read_check(amount)
        self.__index += amount
    
    def __read_check(self, length_ : int) -> None:
        if (((self.__read_value_start > len(self.__m_data))) or ((self.__read_value_start < 4))): 
            raise Utils.newException("Find must be called before calling a Read method", None)
        if (self.__index > ((self.__read_value_start + self.__read_value_length) - length_)): 
            raise Utils.newException("End of extra data", None)
        if ((self.__index + length_) < 4): 
            raise Utils.newException("Cannot read before start of tag", None)
    
    def __read_short_internal(self) -> int:
        if (self.__index > (len(self.__m_data) - 2)): 
            raise Utils.newException("End of extra data", None)
        result = (self.__m_data[self.__index]) + (((self.__m_data[self.__index + 1]) << 8))
        self.__index += 2
        return result
    
    def __set_short(self, index : int, source : int) -> None:
        self.__m_data[index.value] = (source)
        self.__m_data[index.value + 1] = ((source >> 8))
        index.value += 2
    
    def dispose(self) -> None:
        try: 
            if (self.__new_entry is not None): 
                self.__new_entry.close()
        except Exception as ex: 
            pass