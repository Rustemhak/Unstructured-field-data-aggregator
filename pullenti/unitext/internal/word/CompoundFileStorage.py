# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.DirectoryObjectTypes import DirectoryObjectTypes
from pullenti.unitext.internal.word.MiniFATStream import MiniFATStream
from pullenti.unitext.internal.word.FATStream import FATStream
from pullenti.unitext.internal.word.DirectoryStreamIds import DirectoryStreamIds
from pullenti.unitext.internal.word.ExtendedName import ExtendedName
from pullenti.unitext.internal.word.CompoundFileObjectType import CompoundFileObjectType
from pullenti.unitext.internal.word.ReaderUtils import ReaderUtils

class CompoundFileStorage:
    # Compound File Storage.
    
    @property
    def _system(self) -> 'CompoundFileSystem':
        return self.__m_system
    
    @property
    def _entry(self) -> 'CFDirectoryEntry':
        return self.__m_entry
    
    @property
    def name(self) -> 'ExtendedName':
        return ExtendedName(None, self.__m_entry._name, 0, len(self.__m_entry._name) - 1)
    
    @property
    def length(self) -> int:
        return self.__m_entry._stream_size
    
    @property
    def object_type(self) -> 'CompoundFileObjectType':
        return Utils.valToEnum(self.__m_entry._object_type, CompoundFileObjectType)
    
    def __init__(self, system : 'CompoundFileSystem', streamid : int, ancestors : typing.List[int]) -> None:
        self.__m_system = None;
        self.__m_streamid = 0
        self.__m_entry = None;
        self.__m_ancestors = None;
        self.__m_system = system
        self.__m_streamid = streamid
        self.__m_ancestors = ancestors
        self.__initialize()
    
    def __initialize(self) -> None:
        self.__m_entry = ReaderUtils._read_directory_entry(self._system.base_stream, self.__get_stream_offset(), self._system._is_version3)
        ReaderUtils._validate_directory_entry(self.__m_entry)
    
    def __get_stream_offset(self) -> int:
        offset_within_logical_stream = (self.__m_streamid) * ReaderUtils._directory_entry_size
        if (not self._system._is_version3 and ((offset_within_logical_stream >> self._system._header._sector_shift)) >= (self._system._header._directory_sectors_count)): 
            raise Utils.newException("Stream ID out of range", None)
        return self._system._to_physical_stream_offset(self._system._header._first_directory_sector_location, offset_within_logical_stream)
    
    def __append_child(self, collection : typing.List['CompoundFileStorage'], streamid : int, processed : typing.List[tuple], ancestors : typing.List[int]) -> None:
        if (streamid in processed): 
            raise Utils.newException("Circular structure: siblings", None)
        item = CompoundFileStorage(self._system, streamid, ancestors)
        processed[streamid] = item
        if (item._entry._left_siblingid != DirectoryStreamIds._nostream): 
            self.__append_child(collection, item._entry._left_siblingid, processed, ancestors)
        if (item.object_type != CompoundFileObjectType.UNKNOWN): 
            collection.append(item)
        if (item._entry._right_siblingid != DirectoryStreamIds._nostream): 
            self.__append_child(collection, item._entry._right_siblingid, processed, ancestors)
    
    def get_storages(self) -> typing.List['CompoundFileStorage']:
        entries = list()
        processed = dict()
        childid = self.__m_entry._childid
        if (childid != DirectoryStreamIds._nostream): 
            new_ancestors = list()
            new_ancestors.append(self.__m_streamid)
            new_ancestors.extend(self.__m_ancestors)
            if (childid in new_ancestors): 
                raise Utils.newException("Circular structure: ancestors", None)
            self.__append_child(entries, childid, processed, self.__m_ancestors)
        return entries
    
    def find_storage(self, name_ : 'ExtendedName') -> 'CompoundFileStorage':
        for storage in self.get_storages(): 
            if (storage.name == name_): 
                return storage
        return None
    
    def create_stream(self) -> Stream:
        if (self.__m_entry._object_type == DirectoryObjectTypes._stream): 
            if ((self.__m_entry._stream_size) > (self._system.base_stream.length)): 
                raise Utils.newException("Stream length", None)
            if (self.__m_entry._stream_size < self._system._header._mini_stream_cutoff_size): 
                return MiniFATStream(self)
            else: 
                return FATStream(self)
        else: 
            raise Exception()