# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class IChecksum:
    # A data checksum can be updated by one byte or with a byte array. After each
    # update the value of the current checksum can be returned by calling
    # <code>getValue</code>. The complete checksum object can also be reset
    # so it can be used again with new data.
    
    @property
    def value(self) -> int:
        return None
    
    def reset(self) -> None:
        pass
    
    def update_by_val(self, value_ : int) -> None:
        pass
    
    def update_by_buf(self, buffer : bytearray) -> None:
        pass
    
    def update_by_buf_ex(self, buffer : bytearray, offset : int, count : int) -> None:
        pass