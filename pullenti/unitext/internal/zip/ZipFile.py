# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import typing
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.UpdateCommand import UpdateCommand
from pullenti.unitext.internal.zip.IDynamicDataSource import IDynamicDataSource
from pullenti.unitext.internal.zip.DynamicDiskDataSource import DynamicDiskDataSource
from pullenti.unitext.internal.zip.ZipNameTransform import ZipNameTransform
from pullenti.unitext.internal.zip.ZipExtraData import ZipExtraData
from pullenti.unitext.internal.zip.GeneralBitFlags import GeneralBitFlags
from pullenti.unitext.internal.zip.ZipUpdate import ZipUpdate
from pullenti.unitext.internal.zip.StreamUtils import StreamUtils
from pullenti.unitext.internal.zip.Deflater import Deflater
from pullenti.unitext.internal.zip.FileUpdateMode import FileUpdateMode
from pullenti.unitext.internal.zip.DeflaterOutputStream import DeflaterOutputStream
from pullenti.unitext.internal.zip.MemoryArchiveStorage import MemoryArchiveStorage
from pullenti.unitext.internal.zip.DiskArchiveStorage import DiskArchiveStorage
from pullenti.unitext.internal.zip.IArchiveStorage import IArchiveStorage
from pullenti.unitext.internal.zip.UncompressedStream import UncompressedStream
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.internal.zip.ZipString import ZipString
from pullenti.unitext.internal.zip.PartialInputStream import PartialInputStream
from pullenti.unitext.internal.zip.Inflater import Inflater
from pullenti.unitext.internal.zip.CompressionMethod import CompressionMethod
from pullenti.unitext.internal.zip.UseZip64 import UseZip64
from pullenti.unitext.internal.zip.IEntryFactory import IEntryFactory
from pullenti.unitext.internal.zip.ZipEntry import ZipEntry
from pullenti.unitext.internal.zip.ZipEntryFactory import ZipEntryFactory
from pullenti.unitext.internal.zip.ZipHelperStream import ZipHelperStream
from pullenti.unitext.internal.zip.Crc32 import Crc32
from pullenti.unitext.internal.zip.ZipConstants import ZipConstants
from pullenti.unitext.internal.zip.DescriptorData import DescriptorData
from pullenti.unitext.internal.zip.InflaterInputStream import InflaterInputStream
from pullenti.unitext.internal.zip.TestOperation import TestOperation
from pullenti.unitext.internal.zip.TestStrategy import TestStrategy
from pullenti.unitext.internal.zip.TestStatus import TestStatus

class ZipFile(object):
    # This class represents a Zip archive.  You can ask for the contained
    # entries, or get an input stream for a file entry.  The entry is
    # automatically decompressed.
    
    class HeaderTest(IntEnum):
        EXTRACT = 0x01
        HEADER = 0x02
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class UpdateComparer(object):
        """ Class used to sort updates. """
        
        def compare(self, x : object, y : object) -> int:
            """ Compares two objects and returns a value indicating whether one is
            less than, equal to or greater than the other.
            
            Args:
                x(object): First object to compare
                y(object): Second object to compare.
            
            Returns:
                int: Compare result.
            """
            from pullenti.unitext.internal.zip.UpdateCommand import UpdateCommand
            from pullenti.unitext.internal.zip.ZipUpdate import ZipUpdate
            zx = Utils.asObjectOrNull(x, ZipUpdate)
            zy = Utils.asObjectOrNull(y, ZipUpdate)
            result = 0
            if (zx is None): 
                if (zy is None): 
                    result = 0
                else: 
                    result = -1
            elif (zy is None): 
                result = 1
            else: 
                xcmd_value = (0 if (((zx.command == UpdateCommand.COPY)) or ((zx.command == UpdateCommand.MODIFY))) else 1)
                ycmd_value = (0 if (((zy.command == UpdateCommand.COPY)) or ((zy.command == UpdateCommand.MODIFY))) else 1)
                result = (xcmd_value - ycmd_value)
                if (result == 0): 
                    offset_diff = zx.entry.offset - zy.entry.offset
                    if (offset_diff < 0): 
                        result = -1
                    elif (offset_diff == 0): 
                        result = 0
                    else: 
                        result = 1
            return result
    
    def __init__(self, name_ : str, stream : Stream) -> None:
        self.__is_disposed_ = False
        self.__name_ = None;
        self.__comment_ = None;
        self._m_base_stream = None;
        self.__m_stream_owner = False
        self.__offset_of_first_entry = 0
        self.__entries_ = None;
        self.__is_new_archive_ = False
        self.__use_zip64_ = UseZip64.DYNAMIC
        self.__m_updates = None;
        self.__update_count_ = 0
        self.__update_index_ = None;
        self.__archive_storage_ = None;
        self.__update_data_source_ = None;
        self.__contents_edited_ = False
        self.__buffer_size_ = ZipFile.DEFAULT_BUFFER_SIZE
        self.__copy_buffer_ = None;
        self.__new_comment_ = None;
        self.__comment_edited_ = False
        self.__update_entry_factory_ = ZipEntryFactory()
        self.__name_ = name_
        if (stream is None): 
            self._m_base_stream = (FileStream(name_, "rb"))
            self.__m_stream_owner = True
        else: 
            self._m_base_stream = stream
            self.__m_stream_owner = False
        try: 
            self.__read_entries()
        except Exception as ex517: 
            self.__dispose_internal(True)
            raise ex517
    
    def close(self) -> None:
        self.__dispose_internal(True)
    
    @staticmethod
    def create_file(file_name : str) -> 'ZipFile':
        if (file_name is None): 
            raise Exception("fileName")
        f = FileStream(file_name, "wb")
        result = ZipFile(None, f)
        result.__name_ = file_name
        result.__m_stream_owner = True
        return result
    
    @staticmethod
    def create_stream(out_stream : Stream) -> 'ZipFile':
        if (out_stream is None): 
            raise Exception("outStream")
        if (not out_stream.writable): 
            raise Exception("Stream is not writeable", "outStream")
        if (not out_stream.seekable): 
            raise Exception("Stream is not seekable", "outStream")
        result = ZipFile(None, out_stream)
        return result
    
    @property
    def is_stream_owner(self) -> bool:
        return self.__m_stream_owner
    @is_stream_owner.setter
    def is_stream_owner(self, value) -> bool:
        self.__m_stream_owner = value
        return value
    
    @property
    def is_embedded_archive(self) -> bool:
        return self.__offset_of_first_entry > 0
    
    @property
    def is_new_archive(self) -> bool:
        return self.__is_new_archive_
    
    @property
    def zip_file_comment(self) -> str:
        return self.__comment_
    
    @property
    def name(self) -> str:
        return self.__name_
    
    @property
    def size(self) -> int:
        return len(self.__entries_)
    
    @property
    def count(self) -> int:
        return len(self.__entries_)
    
    def get_indexer_item(self, index : int) -> 'ZipEntry':
        return self.__entries_[index].clone()
    
    @property
    def zip_entries(self) -> typing.List['ZipEntry']:
        return list(self.__entries_)
    
    def find_entry(self, name_ : str, ignore_case : bool) -> int:
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        i = 0
        while i < len(self.__entries_): 
            if (Utils.compareStrings(name_, self.__entries_[i].name, ignore_case) == 0): 
                return i
            i += 1
        return -1
    
    def get_entry(self, name_ : str) -> 'ZipEntry':
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        index = self.find_entry(name_, True)
        return (self.__entries_[index].clone() if (index >= 0) else None)
    
    def get_input_stream(self, entry : 'ZipEntry') -> Stream:
        if (entry is None): 
            raise Exception("entry")
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        index = entry.zip_file_index
        if (((index < 0)) or ((index >= len(self.__entries_))) or ((self.__entries_[index].name != entry.name))): 
            index = self.find_entry(entry.name, True)
            if (index < 0): 
                raise Utils.newException("Entry cannot be found", None)
        return self.get_input_stream0(index)
    
    def get_input_stream0(self, entry_index : int) -> Stream:
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        start = self.__locate_entry(self.__entries_[entry_index])
        method = self.__entries_[entry_index]._compression_method
        result = PartialInputStream(self, start, self.__entries_[entry_index].compressed_size)
        if (self.__entries_[entry_index].is_crypted == True): 
            raise Utils.newException("Unable to decrypt this entry", None)
        swichVal = method
        if (swichVal == CompressionMethod.STORED): 
            pass
        elif (swichVal == CompressionMethod.DEFLATED): 
            result = (InflaterInputStream(result, Inflater(True)))
        else: 
            raise Utils.newException("Unsupported compression method {0}".format(Utils.enumToString(method)), None)
        return result
    
    def test_archive(self, test_data : bool) -> bool:
        return self.test_archive_ex(test_data, TestStrategy.FINDFIRSTERROR, None)
    
    def test_archive_ex(self, test_data : bool, strategy : 'TestStrategy', result_handler : 'ZipTestResultHandler') -> bool:
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        status = TestStatus(self)
        if (result_handler is not None): 
            result_handler.call(status, None)
        test = Utils.valToEnum((((ZipFile.HeaderTest.HEADER) | (ZipFile.HeaderTest.EXTRACT)) if test_data else ZipFile.HeaderTest.HEADER), ZipFile.HeaderTest)
        testing = True
        try: 
            entry_index = 0
            while testing and ((entry_index < self.count)):
                if (result_handler is not None): 
                    status._set_entry(self.get_indexer_item(entry_index))
                    status._set_operation(TestOperation.ENTRYHEADER)
                    result_handler.call(status, None)
                try: 
                    self.__test_local_header(self.get_indexer_item(entry_index), test)
                except Exception as ex: 
                    status._add_error()
                    if (result_handler is not None): 
                        result_handler.call(status, "Exception during test - '{0}'".format(ex.__str__()))
                    if (strategy == TestStrategy.FINDFIRSTERROR): 
                        testing = False
                if (testing and test_data and self.get_indexer_item(entry_index).is_file): 
                    if (result_handler is not None): 
                        status._set_operation(TestOperation.ENTRYDATA)
                        result_handler.call(status, None)
                    crc = Crc32()
                    with self.get_input_stream(self.get_indexer_item(entry_index)) as entry_stream: 
                        buffer = Utils.newArrayOfBytes(4096, 0)
                        total_bytes = 0
                        bytes_read = 0
                        while True:
                            bytes_read = entry_stream.read(buffer, 0, len(buffer))
                            if (((bytes_read)) > 0): pass
                            else: 
                                break
                            crc.update_by_buf_ex(buffer, 0, bytes_read)
                            if (result_handler is not None): 
                                total_bytes += bytes_read
                                status._set_bytes_tested(total_bytes)
                                result_handler.call(status, None)
                    if (self.get_indexer_item(entry_index).crc != crc.value): 
                        status._add_error()
                        if (result_handler is not None): 
                            result_handler.call(status, "CRC mismatch")
                        if (strategy == TestStrategy.FINDFIRSTERROR): 
                            testing = False
                    if (((self.get_indexer_item(entry_index).flags & (GeneralBitFlags.DESCRIPTOR))) != 0): 
                        with ZipHelperStream(None, self._m_base_stream) as helper: 
                            data = DescriptorData()
                            helper.read_data_descriptor(self.get_indexer_item(entry_index).local_header_requires_zip64, data)
                            if (self.get_indexer_item(entry_index).crc != data.crc): 
                                status._add_error()
                            if (self.get_indexer_item(entry_index).compressed_size != data.compressed_size): 
                                status._add_error()
                            if (self.get_indexer_item(entry_index).size != data.size): 
                                status._add_error()
                if (result_handler is not None): 
                    status._set_operation(TestOperation.ENTRYCOMPLETE)
                    result_handler.call(status, None)
                entry_index += 1
            if (result_handler is not None): 
                status._set_operation(TestOperation.MISCELLANEOUSTESTS)
                result_handler.call(status, None)
        except Exception as ex: 
            status._add_error()
            if (result_handler is not None): 
                result_handler.call(status, "Exception during test - '{0}'".format(ex.__str__()))
        if (result_handler is not None): 
            status._set_operation(TestOperation.COMPLETE)
            status._set_entry(None)
            result_handler.call(status, None)
        return (status.error_count == 0)
    
    def __test_local_header(self, entry : 'ZipEntry', tests : 'HeaderTest') -> int:
        test_header = (((tests) & (ZipFile.HeaderTest.HEADER))) != 0
        test_data = (((tests) & (ZipFile.HeaderTest.EXTRACT))) != 0
        self._m_base_stream.seek(self.__offset_of_first_entry + entry.offset, 0)
        if ((self.__readleuint()) != ZipConstants.LOCAL_HEADER_SIGNATURE): 
            raise Utils.newException("Wrong local header signature @{0}".format("{:X}".format((self.__offset_of_first_entry + entry.offset))), None)
        extract_version = self.__readleushort()
        local_flags = self.__readleushort()
        compression_method = self.__readleushort()
        file_time = self.__readleushort()
        file_date = self.__readleushort()
        crc_value = self.__readleuint()
        compressed_size = self.__readleuint()
        size_ = self.__readleuint()
        stored_name_length = self.__readleushort()
        extra_data_length = self.__readleushort()
        name_data = Utils.newArrayOfBytes(stored_name_length, 0)
        StreamUtils.read_fully(self._m_base_stream, name_data)
        extra_data = Utils.newArrayOfBytes(extra_data_length, 0)
        StreamUtils.read_fully(self._m_base_stream, extra_data)
        local_extra_data = ZipExtraData(extra_data)
        if (local_extra_data.find(1)): 
            size_ = local_extra_data.read_long()
            compressed_size = local_extra_data.read_long()
            if ((((local_flags) & (GeneralBitFlags.DESCRIPTOR))) != 0): 
                if (((size_ != -1)) and ((size_ != entry.size))): 
                    raise Utils.newException("Size invalid for descriptor", None)
                if (((compressed_size != -1)) and ((compressed_size != entry.compressed_size))): 
                    raise Utils.newException("Compressed size invalid for descriptor", None)
        elif (((extract_version >= ZipConstants.VERSION_ZIP64)) and (((((size_) == 4294967295)) or (((compressed_size) == 4294967295))))): 
            raise Utils.newException("Required Zip64 extended information missing", None)
        if (test_data): 
            if (entry.is_file): 
                if (not entry.is_compression_method_supported()): 
                    raise Utils.newException("Compression method not supported", None)
                if (((extract_version > ZipConstants.VERSION_MADE_BY)) or ((((extract_version > (20))) and ((extract_version < ZipConstants.VERSION_ZIP64))))): 
                    raise Utils.newException("Version required to extract this entry not supported ({0})".format(extract_version), None)
                if ((((local_flags) & ((((GeneralBitFlags.PATCHED) | (GeneralBitFlags.STRONGENCRYPTION) | (GeneralBitFlags.ENHANCEDCOMPRESS)) | (GeneralBitFlags.HEADERMASKED))))) != 0): 
                    raise Utils.newException("The library does not support the zip version required to extract this entry", None)
        if (test_header): 
            if (((((((((extract_version <= (63))) and ((extract_version != (10))) and ((extract_version != (11)))) and ((extract_version != (20))) and ((extract_version != (21)))) and ((extract_version != (25))) and ((extract_version != (27)))) and ((extract_version != (45))) and ((extract_version != (46)))) and ((extract_version != (50))) and ((extract_version != (51)))) and ((extract_version != (52))) and ((extract_version != (61)))) and ((extract_version != (62))) and ((extract_version != (63)))): 
                raise Utils.newException("Version required to extract this entry is invalid ({0})".format(extract_version), None)
            if ((((local_flags) & (((GeneralBitFlags.RESERVEDPKWARE4) | (GeneralBitFlags.RESERVEDPKWARE14) | (GeneralBitFlags.RESERVEDPKWARE15))))) != 0): 
                raise Utils.newException("Reserved bit flags cannot be set.", None)
            if ((((((local_flags) & (GeneralBitFlags.ENCRYPTED))) != 0)) and ((extract_version < (20)))): 
                raise Utils.newException("Version required to extract this entry is too low for encryption ({0})".format(extract_version), None)
            if ((((local_flags) & (GeneralBitFlags.STRONGENCRYPTION))) != 0): 
                if ((((local_flags) & (GeneralBitFlags.ENCRYPTED))) == 0): 
                    raise Utils.newException("Strong encryption flag set but encryption flag is not set", None)
                if (extract_version < (50)): 
                    raise Utils.newException("Version required to extract this entry is too low for encryption ({0})".format(extract_version), None)
            if ((((((local_flags) & (GeneralBitFlags.PATCHED))) != 0)) and ((extract_version < (27)))): 
                raise Utils.newException("Patched data requires higher version than ({0})".format(extract_version), None)
            if (local_flags != entry.flags): 
                raise Utils.newException("Central header/local header flags mismatch", None)
            if (entry._compression_method != (Utils.valToEnum(compression_method, CompressionMethod))): 
                raise Utils.newException("Central header/local header compression method mismatch", None)
            if (entry.version != extract_version): 
                raise Utils.newException("Extract version mismatch", None)
            if ((((local_flags) & (GeneralBitFlags.STRONGENCRYPTION))) != 0): 
                if (extract_version < (62)): 
                    raise Utils.newException("Strong encryption flag set but version not high enough", None)
            if ((((local_flags) & (GeneralBitFlags.HEADERMASKED))) != 0): 
                if (((file_time != (0))) or ((file_date != (0)))): 
                    raise Utils.newException("Header masked set but date/time values non-zero", None)
            if ((((local_flags) & (GeneralBitFlags.DESCRIPTOR))) == 0): 
                if (crc_value != entry.crc): 
                    raise Utils.newException("Central header/local header crc mismatch", None)
            if (((size_ == 0)) and ((compressed_size == 0))): 
                if (crc_value != (0)): 
                    raise Utils.newException("Invalid CRC for empty entry", None)
            if (len(entry.name) > stored_name_length): 
                raise Utils.newException("File name length mismatch", None)
            local_name = ZipConstants.convert_to_string_ext0(local_flags, name_data)
            if (local_name != entry.name): 
                raise Utils.newException("Central header and local header file name mismatch", None)
            if (entry.is_directory): 
                if (size_ > 0): 
                    raise Utils.newException("Directory cannot have size", None)
                if (entry.is_crypted): 
                    if (compressed_size > (ZipConstants.CRYPTO_HEADER_SIZE + 2)): 
                        raise Utils.newException("Directory compressed size invalid", None)
                elif (compressed_size > 2): 
                    raise Utils.newException("Directory compressed size invalid", None)
            if (not ZipNameTransform.is_valid_name_ex(local_name, True)): 
                raise Utils.newException("Name is invalid", None)
        if ((((((local_flags) & (GeneralBitFlags.DESCRIPTOR))) == 0)) or ((((size_ > 0)) or ((compressed_size > 0))))): 
            pass
        extra_length = stored_name_length + extra_data_length
        return (self.__offset_of_first_entry + entry.offset + ZipConstants.LOCAL_HEADER_BASE_SIZE) + extra_length
    
    DEFAULT_BUFFER_SIZE = 4096
    
    @property
    def name_transform(self) -> 'INameTransform':
        return self.__update_entry_factory_.name_transform
    @name_transform.setter
    def name_transform(self, value) -> 'INameTransform':
        self.__update_entry_factory_.name_transform = value
        return value
    
    @property
    def entry_factory(self) -> 'IEntryFactory':
        return self.__update_entry_factory_
    @entry_factory.setter
    def entry_factory(self, value) -> 'IEntryFactory':
        if (value is None): 
            self.__update_entry_factory_ = (ZipEntryFactory())
        else: 
            self.__update_entry_factory_ = value
        return value
    
    @property
    def buffer_size(self) -> int:
        return self.__buffer_size_
    @buffer_size.setter
    def buffer_size(self, value) -> int:
        if (value < 1024): 
            raise Exception("value", "cannot be below 1024")
        if (self.__buffer_size_ != value): 
            self.__buffer_size_ = value
            self.__copy_buffer_ = (None)
        return value
    
    @property
    def is_updating(self) -> bool:
        return self.__m_updates is not None
    
    @property
    def use_zip64(self) -> 'UseZip64':
        return self.__use_zip64_
    @use_zip64.setter
    def use_zip64(self, value) -> 'UseZip64':
        self.__use_zip64_ = value
        return value
    
    def begin_update_ex(self, archive_storage : 'IArchiveStorage', data_source : 'IDynamicDataSource') -> None:
        if (archive_storage is None): 
            raise Exception("archiveStorage")
        if (data_source is None): 
            raise Exception("dataSource")
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        if (self.is_embedded_archive): 
            raise Utils.newException("Cannot update embedded/SFX archives", None)
        self.__archive_storage_ = archive_storage
        self.__update_data_source_ = data_source
        self.__update_index_ = dict()
        if (self.__entries_ is None): 
            self.__entries_ = Utils.newArray(0, None)
        self.__m_updates = list()
        for entry in self.__entries_: 
            index = len(self.__m_updates)
            self.__m_updates.append(ZipUpdate(entry, UpdateCommand.COPY))
            self.__update_index_[entry.name] = index
        cmp = ZipFile.UpdateComparer()
        ii = 0
        while ii < len(self.__m_updates): 
            ch = False
            jj = 0
            while jj < (len(self.__m_updates) - 1): 
                if (cmp.compare(self.__m_updates[jj], self.__m_updates[jj + 1]) > 0): 
                    u = self.__m_updates[jj]
                    self.__m_updates[jj] = self.__m_updates[jj + 1]
                    self.__m_updates[jj + 1] = u
                    ch = True
                jj += 1
            if (not ch): 
                break
            ii += 1
        idx = 0
        for up in self.__m_updates: 
            update = Utils.asObjectOrNull(up, ZipUpdate)
            if (up is None): 
                continue
            if (idx == (len(self.__m_updates) - 1)): 
                break
            update.offset_based_size = self.__m_updates[idx + 1].entry.offset - update.entry.offset
            idx += 1
        self.__update_count_ = len(self.__m_updates)
        self.__contents_edited_ = False
        self.__comment_edited_ = False
        self.__new_comment_ = (None)
    
    def begin_update(self, archive_storage : 'IArchiveStorage') -> None:
        self.begin_update_ex(archive_storage, DynamicDiskDataSource())
    
    def begin_update0(self) -> None:
        if (self.name is None): 
            self.begin_update_ex(MemoryArchiveStorage(), DynamicDiskDataSource())
        else: 
            self.begin_update_ex(DiskArchiveStorage(self), DynamicDiskDataSource())
    
    def commit_update(self) -> None:
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        self.__check_updating()
        try: 
            self.__update_index_.clear()
            self.__update_index_ = (None)
            if (self.__contents_edited_): 
                self.__run_updates()
            elif (self.__comment_edited_): 
                self.__update_comment_only()
            elif (len(self.__entries_) == 0): 
                the_comment = (self.__new_comment_.raw_comment if (self.__new_comment_ is not None) else ZipConstants.convert_to_array_str(self.__comment_))
                with ZipHelperStream(None, self._m_base_stream) as zhs: 
                    zhs.write_end_of_central_directory(0, 0, 0, the_comment)
        finally: 
            self.__post_update_cleanup()
    
    def abort_update(self) -> None:
        self.__post_update_cleanup()
    
    def set_comment(self, comment : str) -> None:
        if (self.__is_disposed_): 
            raise Exception("ZipFile")
        self.__check_updating()
        self.__new_comment_ = ZipString(comment)
        if (self.__new_comment_.raw_length > 0xffff): 
            self.__new_comment_ = (None)
            raise Utils.newException("Comment length exceeds maximum - 65535", None)
        self.__comment_edited_ = True
    
    def __add_update(self, update : 'ZipUpdate') -> None:
        self.__contents_edited_ = True
        index = self.__find_existing_update(update.entry.name)
        if (index >= 0): 
            if (self.__m_updates[index] is None): 
                self.__update_count_ += 1
            self.__m_updates[index] = (update)
        else: 
            index = len(self.__m_updates)
            self.__m_updates.append(update)
            self.__update_count_ += 1
            self.__update_index_[update.entry.name] = index
    
    def add(self, file_name : str, entry_name : str) -> None:
        if (file_name is None): 
            raise Exception("fileName")
        if (entry_name is None): 
            raise Exception("entryName")
        self.__check_updating()
        self.__add_update(ZipUpdate(self.entry_factory.make_file_entry_ex(entry_name, False), UpdateCommand.ADD, None, file_name))
    
    def add_stream(self, str0_ : Stream, entry_name : str) -> None:
        if (entry_name is None): 
            raise Exception("entryName")
        self.__check_updating()
        self.__add_update(ZipUpdate(self.entry_factory.make_file_entry_ex(entry_name, False), UpdateCommand.ADD, None, None, str0_))
    
    def add_directory(self, directory_name : str) -> None:
        if (directory_name is None): 
            raise Exception("directoryName")
        self.__check_updating()
        dir_entry = self.entry_factory.make_directory_entry(directory_name)
        self.__add_update(ZipUpdate(dir_entry, UpdateCommand.ADD))
    
    def delete(self, file_name : str) -> bool:
        if (file_name is None): 
            raise Exception("fileName")
        self.__check_updating()
        result = False
        index = self.__find_existing_update(file_name)
        if (((index >= 0)) and ((self.__m_updates[index] is not None))): 
            result = True
            self.__contents_edited_ = True
            self.__m_updates[index] = None
            self.__update_count_ -= 1
        else: 
            raise Utils.newException("Cannot find entry to delete", None)
        return result
    
    def __writeleshort(self, value : int) -> None:
        self._m_base_stream.writebyte((value & 0xff))
        self._m_base_stream.writebyte((((value >> 8)) & 0xff))
    
    def __writeleushort(self, value : int) -> None:
        self._m_base_stream.writebyte(((value) & 0xff))
        self._m_base_stream.writebyte(((value) >> 8))
    
    def __writeleint(self, value : int) -> None:
        self.__writeleshort(value & 0xffff)
        self.__writeleshort(value >> 16)
    
    def __writeleuint(self, value : int) -> None:
        self.__writeleushort(((value) & 0xffff))
        self.__writeleushort(((value) >> 16))
    
    def __write_le_long(self, value1 : int, value2 : int) -> None:
        self.__writeleint(value1)
        self.__writeleint(value2)
    
    def __writeleulong(self, value1 : int, value2 : int) -> None:
        self.__writeleuint(value1)
        self.__writeleuint(value2)
    
    def __write_local_entry_header(self, update : 'ZipUpdate') -> None:
        entry = update.out_entry
        entry.offset = self._m_base_stream.position
        if (update.command != UpdateCommand.COPY): 
            if (entry._compression_method == CompressionMethod.DEFLATED): 
                if (entry.size == 0): 
                    entry.compressed_size = entry.size
                    entry.crc = 0
                    entry._compression_method = CompressionMethod.STORED
            elif (entry._compression_method == CompressionMethod.STORED): 
                entry.flags &= (~ (GeneralBitFlags.DESCRIPTOR))
            entry.is_crypted = False
            swichVal = self.__use_zip64_
            if (swichVal == UseZip64.DYNAMIC): 
                if (entry.size < 0): 
                    entry.force_zip64()
            elif (swichVal == UseZip64.ON): 
                entry.force_zip64()
            elif (swichVal == UseZip64.OFF): 
                pass
        self.__writeleint(ZipConstants.LOCAL_HEADER_SIGNATURE)
        self.__writeleshort(entry.version)
        self.__writeleshort(entry.flags)
        self.__writeleshort(entry._compression_method)
        self.__writeleint(entry.dos_time)
        if (not entry.has_crc): 
            update.crc_patch_offset = self._m_base_stream.position
            self.__writeleint(0)
        else: 
            self.__writeleint(entry.crc)
        if (entry.local_header_requires_zip64): 
            self.__writeleint(-1)
            self.__writeleint(-1)
        else: 
            if (((entry.compressed_size < 0)) or ((entry.size < 0))): 
                update.size_patch_offset = self._m_base_stream.position
            self.__writeleint(entry.compressed_size)
            self.__writeleint(entry.size)
        name_ = ZipConstants.convert_to_array(entry.flags, entry.name)
        if (len(name_) > 0xFFFF): 
            raise Utils.newException("Entry name too long.", None)
        ed = ZipExtraData(entry.extra_data)
        if (entry.local_header_requires_zip64): 
            ed.start_new_entry()
            ed.add_le_long(entry.size, 0)
            ed.add_le_long(entry.compressed_size, 0)
            ed.add_new_entry(1)
        else: 
            ed.delete(1)
        entry.extra_data = ed.get_entry_data()
        self.__writeleshort(len(name_))
        self.__writeleshort(len(entry.extra_data))
        if (len(name_) > 0): 
            self._m_base_stream.write(name_, 0, len(name_))
        if (entry.local_header_requires_zip64): 
            if (not ed.find(1)): 
                raise Utils.newException("Internal error cannot find extra data", None)
            update.size_patch_offset = (self._m_base_stream.position) + ed.current_read_index
        if (len(entry.extra_data) > 0): 
            self._m_base_stream.write(entry.extra_data, 0, len(entry.extra_data))
    
    def __write_central_directory_header(self, entry : 'ZipEntry') -> int:
        if (entry.compressed_size < 0): 
            raise Utils.newException("Attempt to write central directory entry with unknown csize", None)
        if (entry.size < 0): 
            raise Utils.newException("Attempt to write central directory entry with unknown size", None)
        self.__writeleint(ZipConstants.CENTRAL_HEADER_SIGNATURE)
        self.__writeleshort(ZipConstants.VERSION_MADE_BY)
        self.__writeleshort(entry.version)
        self.__writeleshort(entry.flags)
        #begin unchecked C# block !!! 
        
        self.__writeleshort(entry._compression_method)
        self.__writeleint(entry.dos_time)
        self.__writeleint(entry.crc)
        #res unchecked C# block !!! 
        if ((entry.is_zip64forced())): 
            self.__writeleint(-1)
        else: 
            self.__writeleint((entry.compressed_size & 0xffffffff))
        if ((entry.is_zip64forced())): 
            self.__writeleint(-1)
        else: 
            self.__writeleint(entry.size)
        name_ = ZipConstants.convert_to_array(entry.flags, entry.name)
        if (len(name_) > 0xFFFF): 
            raise Utils.newException("Entry name is too long.", None)
        self.__writeleshort(len(name_))
        ed = ZipExtraData(entry.extra_data)
        if (entry.central_header_requires_zip64): 
            ed.start_new_entry()
            if ((self.__use_zip64_ == UseZip64.ON)): 
                ed.add_le_long(entry.size, 0)
            if ((self.__use_zip64_ == UseZip64.ON)): 
                ed.add_le_long(entry.compressed_size, 0)
            ed.add_new_entry(1)
        else: 
            ed.delete(1)
        central_extra_data = ed.get_entry_data()
        self.__writeleshort(len(central_extra_data))
        self.__writeleshort((len(entry.comment) if entry.comment is not None else 0))
        self.__writeleshort(0)
        self.__writeleshort(0)
        if (entry.external_file_attributes != -1): 
            self.__writeleint(entry.external_file_attributes)
        elif (entry.is_directory): 
            self.__writeleuint(16)
        else: 
            self.__writeleuint(0)
        self.__writeleuint(entry.offset)
        if (len(name_) > 0): 
            self._m_base_stream.write(name_, 0, len(name_))
        if (len(central_extra_data) > 0): 
            self._m_base_stream.write(central_extra_data, 0, len(central_extra_data))
        raw_comment = (MiscHelper.encode_string_ascii(entry.comment) if (entry.comment is not None) else Utils.newArrayOfBytes(0, 0))
        if (len(raw_comment) > 0): 
            self._m_base_stream.write(raw_comment, 0, len(raw_comment))
        return (ZipConstants.CENTRAL_HEADER_BASE_SIZE + len(name_) + len(central_extra_data)) + len(raw_comment)
    
    def __post_update_cleanup(self) -> None:
        self.__update_data_source_ = (None)
        self.__m_updates = (None)
        self.__update_index_ = (None)
        if (self.__archive_storage_ is not None): 
            self.__archive_storage_.close()
            self.__archive_storage_ = (None)
    
    def __get_transformed_file_name(self, name_ : str) -> str:
        transform = self.name_transform
        return (transform.transform_file(name_) if (transform is not None) else name_)
    
    def __get_transformed_directory_name(self, name_ : str) -> str:
        transform = self.name_transform
        return (transform.transform_directory(name_) if (transform is not None) else name_)
    
    def __get_buffer(self) -> bytearray:
        if (self.__copy_buffer_ is None): 
            self.__copy_buffer_ = Utils.newArrayOfBytes(self.__buffer_size_, 0)
        return self.__copy_buffer_
    
    def __copy_descriptor_bytes(self, update : 'ZipUpdate', dest : Stream, source : Stream) -> None:
        bytes_to_copy = self.__get_descriptor_size(update)
        if (bytes_to_copy > 0): 
            buffer = self.__get_buffer()
            while bytes_to_copy > 0:
                read_size = min(len(buffer), bytes_to_copy)
                bytes_read = source.read(buffer, 0, read_size)
                if (bytes_read > 0): 
                    dest.write(buffer, 0, bytes_read)
                    bytes_to_copy -= bytes_read
                else: 
                    raise Utils.newException("Unxpected end of stream", None)
    
    def __copy_bytes(self, update : 'ZipUpdate', destination : Stream, source : Stream, bytes_to_copy : int, update_crc : bool) -> None:
        if (destination == source): 
            raise Exception("Destination and source are the same")
        crc = Crc32()
        buffer = self.__get_buffer()
        target_bytes = bytes_to_copy
        total_bytes_read = 0
        bytes_read = 0
        first_pass = True
        while first_pass or (((bytes_read > 0)) and ((bytes_to_copy > 0))):
            first_pass = False
            read_size = len(buffer)
            if (bytes_to_copy < read_size): 
                read_size = (bytes_to_copy)
            bytes_read = source.read(buffer, 0, read_size)
            if (bytes_read > 0): 
                if (update_crc): 
                    crc.update_by_buf_ex(buffer, 0, bytes_read)
                destination.write(buffer, 0, bytes_read)
                bytes_to_copy -= bytes_read
                total_bytes_read += bytes_read
        if (total_bytes_read != target_bytes): 
            raise Utils.newException("Failed to copy bytes expected {0} read {1}".format(target_bytes, total_bytes_read), None)
        if (update_crc): 
            update.out_entry.crc = crc.value
    
    def __get_descriptor_size(self, update : 'ZipUpdate') -> int:
        result = 0
        if (((update.entry.flags & (GeneralBitFlags.DESCRIPTOR))) != 0): 
            result = (ZipConstants.DATA_DESCRIPTOR_SIZE - 4)
            if (update.entry.local_header_requires_zip64): 
                result = (ZipConstants.ZIP64DATA_DESCRIPTOR_SIZE - 4)
        return result
    
    def __copy_descriptor_bytes_direct(self, update : 'ZipUpdate', stream : Stream, destination_position : int, source_position : int) -> None:
        bytes_to_copy = self.__get_descriptor_size(update)
        while bytes_to_copy > 0:
            read_size = bytes_to_copy
            buffer = self.__get_buffer()
            stream.position = source_position
            bytes_read = stream.read(buffer, 0, read_size)
            if (bytes_read > 0): 
                stream.position = destination_position.value
                stream.write(buffer, 0, bytes_read)
                bytes_to_copy -= bytes_read
                destination_position.value += bytes_read
                source_position += bytes_read
            else: 
                raise Utils.newException("Unxpected end of stream", None)
    
    def __copy_entry_data_direct(self, update : 'ZipUpdate', stream : Stream, update_crc : bool, destination_position : int, source_position : int) -> None:
        bytes_to_copy = update.entry.compressed_size
        crc = Crc32()
        buffer = self.__get_buffer()
        target_bytes = bytes_to_copy
        total_bytes_read = 0
        bytes_read = 0
        first_pass = True
        while first_pass or (((bytes_read > 0)) and ((bytes_to_copy > 0))):
            first_pass = False
            read_size = len(buffer)
            if (bytes_to_copy < read_size): 
                read_size = (bytes_to_copy)
            stream.position = source_position.value
            bytes_read = stream.read(buffer, 0, read_size)
            if (bytes_read > 0): 
                if (update_crc): 
                    crc.update_by_buf_ex(buffer, 0, bytes_read)
                stream.position = destination_position.value
                stream.write(buffer, 0, bytes_read)
                destination_position.value += bytes_read
                source_position.value += bytes_read
                bytes_to_copy -= bytes_read
                total_bytes_read += bytes_read
        if (total_bytes_read != target_bytes): 
            raise Utils.newException("Failed to copy bytes expected {0} read {1}".format(target_bytes, total_bytes_read), None)
        if (update_crc): 
            update.out_entry.crc = crc.value
    
    def __find_existing_update(self, file_name : str) -> int:
        result = -1
        converted_name = self.__get_transformed_file_name(file_name)
        if (converted_name in self.__update_index_): 
            result = (self.__update_index_[converted_name])
        return result
    
    def __get_output_stream(self, entry : 'ZipEntry') -> Stream:
        result = self._m_base_stream
        if (entry.is_crypted == True): 
            raise Utils.newException("Encryption not supported", None)
        swichVal = entry._compression_method
        if (swichVal == CompressionMethod.STORED): 
            return UncompressedStream(result)
        elif (swichVal == CompressionMethod.DEFLATED): 
            dos = DeflaterOutputStream(result, Deflater(9, True))
            dos.is_stream_owner = False
            return dos
        else: 
            raise Utils.newException("Unknown compression method {0}".format(Utils.enumToString(entry._compression_method)), None)
    
    def __add_entry(self, work_file : 'ZipFile', update : 'ZipUpdate') -> None:
        source = None
        try: 
            if (update.entry.is_file): 
                source = update.get_source()
                if (source is None): 
                    source = self.__update_data_source_.get_source(update.entry, update.filename)
            if (source is not None): 
                source_stream_length = source.length
                if (update.out_entry.size < 0): 
                    update.out_entry.size = source_stream_length
                elif (update.out_entry.size != source_stream_length): 
                    pass
                work_file.__write_local_entry_header(update)
                data_start = work_file._m_base_stream.position
                with work_file.__get_output_stream(update.out_entry) as output: 
                    self.__copy_bytes(update, output, source, source_stream_length, True)
                data_end = work_file._m_base_stream.position
                update.out_entry.compressed_size = data_end - data_start
                if (((update.out_entry.flags & (GeneralBitFlags.DESCRIPTOR))) == (GeneralBitFlags.DESCRIPTOR)): 
                    with ZipHelperStream(None, work_file._m_base_stream) as helper: 
                        helper.write_data_descriptor(update.out_entry)
            else: 
                work_file.__write_local_entry_header(update)
                update.out_entry.compressed_size = 0
        finally: 
            if (source is not None): 
                source.close()
    
    def __modify_entry(self, work_file : 'ZipFile', update : 'ZipUpdate') -> None:
        work_file.__write_local_entry_header(update)
        data_start = work_file._m_base_stream.position
        if (update.entry.is_file and ((update.filename is not None))): 
            with work_file.__get_output_stream(update.out_entry) as output: 
                with self.get_input_stream(update.entry) as source: 
                    self.__copy_bytes(update, output, source, source.length, True)
        data_end = work_file._m_base_stream.position
        update.entry.compressed_size = data_end - data_start
    
    def __copy_entry_direct(self, work_file : 'ZipFile', update : 'ZipUpdate', destination_position : int) -> None:
        skip_over = False
        if (update.entry.offset == destination_position.value): 
            skip_over = True
        if (not skip_over): 
            self._m_base_stream.position = destination_position.value
            work_file.__write_local_entry_header(update)
            destination_position.value = (self._m_base_stream.position)
        source_position = 0
        name_length_offset = 26
        entry_data_offset = update.entry.offset + name_length_offset
        self._m_base_stream.seek(entry_data_offset, 0)
        name_length = self.__readleushort()
        extra_length = self.__readleushort()
        source_position = ((self._m_base_stream.position) + (name_length) + (extra_length))
        if (skip_over): 
            if (update.offset_based_size != -1): 
                destination_position.value += update.offset_based_size
            else: 
                destination_position.value += ((((source_position - entry_data_offset)) + name_length_offset + update.entry.compressed_size) + self.__get_descriptor_size(update))
        else: 
            if (update.entry.compressed_size > 0): 
                wrapsource_position518 = RefOutArgWrapper(source_position)
                self.__copy_entry_data_direct(update, self._m_base_stream, False, destination_position, wrapsource_position518)
                source_position = wrapsource_position518.value
            self.__copy_descriptor_bytes_direct(update, self._m_base_stream, destination_position, source_position)
    
    def __copy_entry(self, work_file : 'ZipFile', update : 'ZipUpdate') -> None:
        work_file.__write_local_entry_header(update)
        if (update.entry.compressed_size > 0): 
            name_length_offset = 26
            entry_data_offset = (update.entry.offset) + name_length_offset
            self._m_base_stream.seek(entry_data_offset, 0)
            name_length = self.__readleushort()
            extra_length = self.__readleushort()
            self._m_base_stream.seek((name_length) + (extra_length), 1)
            self.__copy_bytes(update, work_file._m_base_stream, self._m_base_stream, update.entry.compressed_size, False)
        self.__copy_descriptor_bytes(update, work_file._m_base_stream, self._m_base_stream)
    
    def __reopen(self, source : Stream) -> None:
        if (source is None): 
            raise Utils.newException("Failed to reopen archive - no source", None)
        self.__is_new_archive_ = False
        self._m_base_stream = source
        self.__read_entries()
    
    def __update_comment_only(self) -> None:
        base_length = self._m_base_stream.length
        update_file = None
        if (self.__archive_storage_.update_mode == FileUpdateMode.SAFE): 
            with self.__archive_storage_.make_temporary_copy(self._m_base_stream) as copy_stream: 
                update_file = ZipHelperStream(None, copy_stream)
                update_file.is_stream_owner = True
                self._m_base_stream.close()
                self._m_base_stream = (None)
        elif (self.__archive_storage_.update_mode == FileUpdateMode.DIRECT): 
            self._m_base_stream = self.__archive_storage_.open_for_direct_update(self._m_base_stream)
            update_file = ZipHelperStream(None, self._m_base_stream)
        else: 
            self._m_base_stream.close()
            self._m_base_stream = (None)
            update_file = ZipHelperStream(self.name)
        try: 
            located_central_dir_offset = update_file.locate_block_with_signature(ZipConstants.END_OF_CENTRAL_DIRECTORY_SIGNATURE, base_length, ZipConstants.END_OF_CENTRAL_RECORD_BASE_SIZE, 0xffff)
            if (located_central_dir_offset < 0): 
                raise Utils.newException("Cannot find central directory", None)
            central_header_comment_size_offset = 16
            update_file.position = update_file.position + (central_header_comment_size_offset)
            raw_comment = self.__new_comment_.raw_comment
            update_file.writeleshort(len(raw_comment))
            update_file.write(raw_comment, 0, len(raw_comment))
            update_file.set_length(update_file.position)
        finally: 
            update_file.close()
        if (self.__archive_storage_.update_mode == FileUpdateMode.SAFE): 
            self.__reopen(self.__archive_storage_.convert_temporary_to_final())
        else: 
            self.__read_entries()
    
    def __run_updates(self) -> None:
        size_entries = 0
        end_of_stream = 0
        direct_update = False
        destination_position = 0
        work_file = None
        if (self.is_new_archive): 
            work_file = self
            work_file._m_base_stream.position = 0
            direct_update = True
        elif (self.__archive_storage_.update_mode == FileUpdateMode.DIRECT): 
            work_file = self
            work_file._m_base_stream.position = 0
            direct_update = True
            cmp = ZipFile.UpdateComparer()
            ii = 0
            while ii < len(self.__m_updates): 
                ch = False
                jj = 0
                while jj < (len(self.__m_updates) - 1): 
                    if (cmp.compare(self.__m_updates[jj], self.__m_updates[jj + 1]) > 0): 
                        u = self.__m_updates[jj]
                        self.__m_updates[jj] = self.__m_updates[jj + 1]
                        self.__m_updates[jj + 1] = u
                        ch = True
                    jj += 1
                if (not ch): 
                    break
                ii += 1
        else: 
            work_file = ZipFile.create_stream(self.__archive_storage_.get_temporary_output())
            work_file.use_zip64 = self.use_zip64
        try: 
            for up in self.__m_updates: 
                update = Utils.asObjectOrNull(up, ZipUpdate)
                if (update is not None): 
                    swichVal = update.command
                    if (swichVal == UpdateCommand.COPY): 
                        if (direct_update): 
                            wrapdestination_position519 = RefOutArgWrapper(destination_position)
                            self.__copy_entry_direct(work_file, update, wrapdestination_position519)
                            destination_position = wrapdestination_position519.value
                        else: 
                            self.__copy_entry(work_file, update)
                    elif (swichVal == UpdateCommand.MODIFY): 
                        self.__modify_entry(work_file, update)
                    elif (swichVal == UpdateCommand.ADD): 
                        if (not self.is_new_archive and direct_update): 
                            work_file._m_base_stream.position = destination_position
                        self.__add_entry(work_file, update)
                        if (direct_update): 
                            destination_position = (work_file._m_base_stream.position)
            if (not self.is_new_archive and direct_update): 
                work_file._m_base_stream.position = destination_position
            central_dir_offset = work_file._m_base_stream.position
            for up in self.__m_updates: 
                update = Utils.asObjectOrNull(up, ZipUpdate)
                if (update is not None): 
                    size_entries += work_file.__write_central_directory_header(update.out_entry)
            the_comment = (self.__new_comment_.raw_comment if (self.__new_comment_ is not None) else ZipConstants.convert_to_array_str(self.__comment_))
            with ZipHelperStream(None, work_file._m_base_stream) as zhs: 
                zhs.write_end_of_central_directory(self.__update_count_, size_entries, central_dir_offset, the_comment)
            end_of_stream = (work_file._m_base_stream.position)
            for up in self.__m_updates: 
                update = Utils.asObjectOrNull(up, ZipUpdate)
                if (update is not None): 
                    if (((update.crc_patch_offset > 0)) and ((update.out_entry.compressed_size > 0))): 
                        work_file._m_base_stream.position = update.crc_patch_offset
                        work_file.__writeleint(update.out_entry.crc)
                    if (update.size_patch_offset > 0): 
                        work_file._m_base_stream.position = update.size_patch_offset
                        if (update.out_entry.local_header_requires_zip64): 
                            work_file.__write_le_long(update.out_entry.size, 0)
                            work_file.__write_le_long(update.out_entry.compressed_size, 0)
                        else: 
                            work_file.__writeleint(update.out_entry.compressed_size)
                            work_file.__writeleint(update.out_entry.size)
        except Exception as ex520: 
            if (not direct_update and ((work_file.name is not None))): 
                pathlib.Path(work_file.name).unlink()
            raise ex520
        finally: 
            if (work_file is not None): 
                work_file.close()
            work_file = (None)
        if (direct_update): 
            if (work_file is not None): 
                work_file._m_base_stream.length = end_of_stream
                work_file._m_base_stream.flush()
            self.__is_new_archive_ = False
            self.__read_entries()
        else: 
            self._m_base_stream.close()
            self.__reopen(self.__archive_storage_.convert_temporary_to_final())
    
    def __check_updating(self) -> None:
        if (self.__m_updates is None): 
            raise Exception("BeginUpdate has not been called")
    
    def __dispose_internal(self, disposing : bool) -> None:
        if (not self.__is_disposed_): 
            self.__is_disposed_ = True
            self.__entries_ = Utils.newArray(0, None)
            if (self.is_stream_owner and ((self._m_base_stream is not None))): 
                self._m_base_stream.close()
                self._m_base_stream = (None)
            self.__post_update_cleanup()
    
    def _dispose(self, disposing : bool) -> None:
        self.__dispose_internal(disposing)
    
    def __readleushort(self) -> int:
        data1 = self._m_base_stream.readbyte()
        if (data1 < 0): 
            raise Exception("End of stream")
        data2 = self._m_base_stream.readbyte()
        if (data2 < 0): 
            raise Exception("End of stream")
        return ((data1) | ((data2 << 8)))
    
    def __readleuint(self) -> int:
        return ((self.__readleushort()) | (((self.__readleushort()) << 16)))
    
    def __locate_block_with_signature(self, signature : int, end_location : int, minimum_block_size : int, maximum_variable_data : int) -> int:
        with ZipHelperStream(None, self._m_base_stream) as les: 
            return les.locate_block_with_signature(signature, end_location, minimum_block_size, maximum_variable_data)
    
    def __read_entries(self) -> None:
        if (self._m_base_stream is None): 
            return
        if (self._m_base_stream.length == (0)): 
            return
        if (self._m_base_stream.seekable == False): 
            raise Utils.newException("ZipFile stream must be seekable", None)
        located_end_of_central_dir = self.__locate_block_with_signature(ZipConstants.END_OF_CENTRAL_DIRECTORY_SIGNATURE, self._m_base_stream.length, ZipConstants.END_OF_CENTRAL_RECORD_BASE_SIZE, 0xffff)
        if (located_end_of_central_dir < 0): 
            raise Utils.newException("Cannot find central directory", None)
        this_disk_number = self.__readleushort()
        start_central_dir_disk = self.__readleushort()
        entries_for_this_disk = self.__readleushort()
        entries_for_whole_central_dir = self.__readleushort()
        central_dir_size = self.__readleuint()
        offset_of_central_dir = self.__readleuint()
        comment_size = self.__readleushort()
        if (comment_size > (0)): 
            comment = Utils.newArrayOfBytes(comment_size, 0)
            StreamUtils.read_fully(self._m_base_stream, comment)
            self.__comment_ = ZipConstants.convert_to_string0(comment)
        else: 
            self.__comment_ = ""
        is_zip64 = False
        if ((this_disk_number == (0xffff))): 
            is_zip64 = True
            offset = self.__locate_block_with_signature(ZipConstants.ZIP64CENTRAL_DIR_LOCATOR_SIGNATURE, located_end_of_central_dir, 0, 0x1000)
            if (offset < 0): 
                raise Utils.newException("Cannot find Zip64 locator", None)
            self.__readleuint()
            offset64 = self.__readleuint()
            self.__readleuint()
            total_disks = self.__readleuint()
            self._m_base_stream.position = offset64
            sig64 = self.__readleuint()
            if (sig64 != ZipConstants.ZIP64CENTRAL_FILE_HEADER_SIGNATURE): 
                raise Utils.newException("Invalid Zip64 Central directory signature at {0}".format("{:X}".format(offset64)), None)
            record_size = self.__readleuint()
            self.__readleuint()
            version_made_by = self.__readleushort()
            version_to_extract = self.__readleushort()
            this_disk = self.__readleuint()
            central_dir_disk = self.__readleuint()
            entries_for_this_disk = (self.__readleuint())
            self.__readleuint()
            entries_for_whole_central_dir = (self.__readleuint())
            self.__readleuint()
            central_dir_size = (self.__readleuint())
            self.__readleuint()
            offset_of_central_dir = (self.__readleuint())
            self.__readleuint()
        self.__entries_ = Utils.newArray(entries_for_this_disk, None)
        if (not is_zip64 and ((offset_of_central_dir < ((located_end_of_central_dir) - (((4) + (central_dir_size))))))): 
            self.__offset_of_first_entry = (located_end_of_central_dir - ((4 + central_dir_size + offset_of_central_dir)))
            if (self.__offset_of_first_entry <= 0): 
                raise Utils.newException("Invalid embedded zip archive", None)
        self._m_base_stream.seek(self.__offset_of_first_entry + offset_of_central_dir, 0)
        i = 0
        while i < entries_for_this_disk: 
            if ((self.__readleuint()) != ZipConstants.CENTRAL_HEADER_SIGNATURE): 
                raise Utils.newException("Wrong Central Directory signature", None)
            version_made_by = self.__readleushort()
            version_to_extract = self.__readleushort()
            bit_flags = self.__readleushort()
            method = self.__readleushort()
            dostime = self.__readleuint()
            crc = self.__readleuint()
            csize = self.__readleuint()
            size_ = self.__readleuint()
            name_len = self.__readleushort()
            extra_len = self.__readleushort()
            comment_len = self.__readleushort()
            disk_start_no = self.__readleushort()
            internal_attributes = self.__readleushort()
            external_attributes = self.__readleuint()
            offset = self.__readleuint()
            buffer = Utils.newArrayOfBytes(max(name_len, comment_len), 0)
            StreamUtils.read_fully_ex(self._m_base_stream, buffer, 0, name_len)
            name_ = ZipConstants.convert_to_string_ext(bit_flags, buffer, name_len)
            entry = ZipEntry(name_, version_to_extract, version_made_by, Utils.valToEnum(method, CompressionMethod))
            entry.crc = crc
            entry.size = size_
            entry.compressed_size = csize
            entry.flags = bit_flags
            entry.dos_time = dostime
            entry.zip_file_index = i
            entry.offset = offset
            entry.external_file_attributes = external_attributes
            if (((bit_flags & 8)) == 0): 
                entry._crypto_check_value = ((crc) >> 24)
            else: 
                entry._crypto_check_value = ((((dostime) >> 8)) & 0xff)
            if (extra_len > 0): 
                extra = Utils.newArrayOfBytes(extra_len, 0)
                StreamUtils.read_fully(self._m_base_stream, extra)
                entry.extra_data = extra
            entry._process_extra_data(False)
            if (comment_len > 0): 
                StreamUtils.read_fully_ex(self._m_base_stream, buffer, 0, comment_len)
                entry.comment = ZipConstants.convert_to_string_ext(bit_flags, buffer, comment_len)
            self.__entries_[i] = entry
            i += 1
    
    def __locate_entry(self, entry : 'ZipEntry') -> int:
        return self.__test_local_header(entry, ZipFile.HeaderTest.EXTRACT)
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()