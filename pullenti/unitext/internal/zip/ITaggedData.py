# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class ITaggedData:
    # ExtraData tagged value interface.
    
    @property
    def tagid(self) -> int:
        return None
    
    def set_data(self, data : bytearray, offset : int, count : int) -> None:
        pass
    
    def get_data(self) -> bytearray:
        return None