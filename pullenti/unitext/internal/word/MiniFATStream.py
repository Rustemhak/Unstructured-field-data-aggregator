# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.CompoundFileStream import CompoundFileStream
from pullenti.unitext.internal.word.ReaderUtils import ReaderUtils

class MiniFATStream(CompoundFileStream):
    
    def __init__(self, storage : 'CompoundFileStorage') -> None:
        super().__init__(storage, storage._system._get_mini_sector_size())
    
    def _get_page_data(self, page_index : int) -> bytearray:
        page = Utils.newArrayOfBytes(self._page_size, 0)
        sector = self._system._get_mini_stream_next_sector(self._storage._entry._starting_sector_location, page_index)
        return ReaderUtils._read_fragment(self._system.base_stream, self._system._get_mini_sector_offset(sector), self._page_size)