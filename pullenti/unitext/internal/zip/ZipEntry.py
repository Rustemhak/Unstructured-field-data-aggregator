# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.HostSystemID import HostSystemID
from pullenti.unitext.internal.zip.ZipExtraData import ZipExtraData
from pullenti.unitext.internal.zip.GeneralBitFlags import GeneralBitFlags
from pullenti.unitext.internal.zip.CompressionMethod import CompressionMethod
from pullenti.unitext.internal.zip.ZipConstants import ZipConstants

class ZipEntry:
    # This class represents an entry in a zip archive.  This can be a file
    # or a directory
    # ZipFile and ZipInputStream will give you instances of this class as
    # information about the members in an archive.  ZipOutputStream
    # uses an instance of this class when creating an entry in a Zip file.
    
    class Known(IntEnum):
        NONE = 0
        SIZE = 0x01
        COMPRESSEDSIZE = 0x02
        CRC = 0x04
        TIME = 0x08
        EXTERNALATTRIBUTES = 0x10
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, name_ : str, version_required_to_extract : int=0, made_by_info : int=ZipConstants.VERSION_MADE_BY, method : 'CompressionMethod'=CompressionMethod.DEFLATED) -> None:
        self.__m_known = ZipEntry.Known.NONE
        self.__m_external_file_attributes = -1
        self.__m_version_made_by = 0
        self.__m_name = None;
        self.__m_size = 0
        self.__m_compressed_size = 0
        self.__version_to_extract = 0
        self.__m_crc = 0
        self.__m_dos_time = 0
        self.__m_method = CompressionMethod.DEFLATED
        self.__m_extra = None;
        self.__m_comment = None;
        self.flags = 0
        self.__m_zip_file_index = -1
        self.__m_ooffset = 0
        self.__force_zip64_ = False
        self.__m_crypto_check_value = 0
        self.__aes_ver = 0
        self.__aes_encryption_strength = 0
        if (name_ is None): 
            raise Exception("name")
        if (len(name_) > 0xffff): 
            raise Exception("Name is too long", "name")
        if (((version_required_to_extract != 0)) and ((version_required_to_extract < 10))): 
            raise Exception("versionRequiredToExtract")
        self.date_time = datetime.datetime.now()
        self.__m_name = name_
        self.__m_version_made_by = (made_by_info)
        self.__version_to_extract = (version_required_to_extract)
        self.__m_method = method
    
    @property
    def has_crc(self) -> bool:
        return ((self.__m_known) & (ZipEntry.Known.CRC)) != (0)
    
    @property
    def is_crypted(self) -> bool:
        return ((self.flags & 1)) != 0
    @is_crypted.setter
    def is_crypted(self, value) -> bool:
        if (value): 
            self.flags |= 1
        else: 
            self.flags &= (~ 1)
        return value
    
    @property
    def is_unicode_text(self) -> bool:
        return ((self.flags & (GeneralBitFlags.UNICODETEXT))) != 0
    @is_unicode_text.setter
    def is_unicode_text(self, value) -> bool:
        if (value): 
            self.flags |= (GeneralBitFlags.UNICODETEXT)
        else: 
            self.flags &= (~ (GeneralBitFlags.UNICODETEXT))
        return value
    
    @property
    def _crypto_check_value(self) -> int:
        return self.__m_crypto_check_value
    @_crypto_check_value.setter
    def _crypto_check_value(self, value) -> int:
        self.__m_crypto_check_value = value
        return value
    
    @property
    def zip_file_index(self) -> int:
        return self.__m_zip_file_index
    @zip_file_index.setter
    def zip_file_index(self, value) -> int:
        self.__m_zip_file_index = value
        return value
    
    @property
    def offset(self) -> int:
        return self.__m_ooffset
    @offset.setter
    def offset(self, value) -> int:
        self.__m_ooffset = value
        return value
    
    @property
    def external_file_attributes(self) -> int:
        if (((self.__m_known) & (ZipEntry.Known.EXTERNALATTRIBUTES)) == (0)): 
            return -1
        else: 
            return self.__m_external_file_attributes
    @external_file_attributes.setter
    def external_file_attributes(self, value) -> int:
        self.__m_external_file_attributes = value
        self.__m_known = (Utils.valToEnum((self.__m_known) | (ZipEntry.Known.EXTERNALATTRIBUTES), ZipEntry.Known))
        return value
    
    @property
    def version_made_by(self) -> int:
        return ((self.__m_version_made_by) & 0xff)
    
    @property
    def isdosentry(self) -> bool:
        return (((self.host_system == (HostSystemID.MSDOS))) or ((self.host_system == (HostSystemID.WINDOWSNT))))
    
    def __has_dos_attributes(self, attributes : int) -> bool:
        result = False
        if (((self.__m_known) & (ZipEntry.Known.EXTERNALATTRIBUTES)) != (0)): 
            if (((((self.host_system == (HostSystemID.MSDOS))) or ((self.host_system == (HostSystemID.WINDOWSNT))))) and ((self.external_file_attributes & attributes)) == attributes): 
                result = True
        return result
    
    @property
    def host_system(self) -> int:
        return (((self.__m_version_made_by) >> 8)) & 0xff
    @host_system.setter
    def host_system(self, value) -> int:
        self.__m_version_made_by &= (0xff)
        self.__m_version_made_by |= ((((value & 0xff)) << 8))
        return value
    
    @property
    def version(self) -> int:
        if (self.__version_to_extract != (0)): 
            return self.__version_to_extract
        else: 
            result = 10
            if (self.aeskey_size > 0): 
                result = ZipConstants.VERSION_AES
            elif (self.central_header_requires_zip64): 
                result = ZipConstants.VERSION_ZIP64
            elif (CompressionMethod.DEFLATED == self.__m_method): 
                result = 20
            elif (self.is_directory == True): 
                result = 20
            elif (self.is_crypted == True): 
                result = 20
            elif (self.__has_dos_attributes(0x08)): 
                result = 11
            return result
    
    @property
    def can_decompress(self) -> bool:
        return ((self.version <= ZipConstants.VERSION_MADE_BY)) and (((((self.version == 10)) or ((self.version == 11)) or ((self.version == 20))) or ((self.version == 45)) or ((self.version == 51)))) and self.is_compression_method_supported()
    
    def force_zip64(self) -> None:
        self.__force_zip64_ = True
    
    def is_zip64forced(self) -> bool:
        return self.__force_zip64_
    
    @property
    def local_header_requires_zip64(self) -> bool:
        result = self.__force_zip64_
        if (not result): 
            true_compressed_size = self.__m_compressed_size
            if (((self.__version_to_extract == (0))) and self.is_crypted): 
                true_compressed_size += ZipConstants.CRYPTO_HEADER_SIZE
            result = ((((self.__version_to_extract == (0))) or (((self.__version_to_extract) >= ZipConstants.VERSION_ZIP64))))
        return result
    
    @property
    def central_header_requires_zip64(self) -> bool:
        return self.local_header_requires_zip64
    
    @property
    def dos_time(self) -> int:
        if (((self.__m_known) & (ZipEntry.Known.TIME)) == (0)): 
            return 0
        else: 
            return self.__m_dos_time
    @dos_time.setter
    def dos_time(self, value) -> int:
        self.__m_dos_time = (value)
        self.__m_known = (Utils.valToEnum((self.__m_known) | (ZipEntry.Known.TIME), ZipEntry.Known))
        return value
    
    @property
    def date_time(self) -> datetime.datetime:
        sec = min(59, 2 * (((self.__m_dos_time) & 0x1f)))
        min0_ = min(59, (((self.__m_dos_time) >> 5)) & 0x3f)
        hrs = min(23, (((self.__m_dos_time) >> 11)) & 0x1f)
        mon = max(1, min(12, ((((self.__m_dos_time) >> 21)) & 0xf)))
        year = (((((self.__m_dos_time) >> 25)) & 0x7f)) + 1980
        day = max(1, min(Utils.lastDayOfMonth(year, mon), ((((self.__m_dos_time) >> 16)) & 0x1f)))
        return datetime.datetime(year, mon, day, hrs, min0_, sec)
    @date_time.setter
    def date_time(self, value) -> datetime.datetime:
        year = value.year
        month = value.month
        day = value.day
        hour = value.hour
        minute = value.minute
        second = value.second
        if (year < (1980)): 
            year = (1980)
            month = (1)
            day = (1)
            hour = (0)
            minute = (0)
            second = (0)
        elif (year > (2107)): 
            year = (2107)
            month = (12)
            day = (31)
            hour = (23)
            minute = (59)
            second = (59)
        self.dos_time = (((((((year) - 1980)) & 0x7f)) << 25 | (((month) << 21)) | (((day) << 16))) | (((hour) << 11)) | (((minute) << 5))) | (((second) >> 1))
        return value
    
    @property
    def name(self) -> str:
        return self.__m_name
    
    @property
    def size(self) -> int:
        return (self.__m_size if ((self.__m_known) & (ZipEntry.Known.SIZE)) != (0) else -1)
    @size.setter
    def size(self, value) -> int:
        self.__m_size = value
        self.__m_known = (Utils.valToEnum((self.__m_known) | (ZipEntry.Known.SIZE), ZipEntry.Known))
        return value
    
    @property
    def compressed_size(self) -> int:
        return (self.__m_compressed_size if ((self.__m_known) & (ZipEntry.Known.COMPRESSEDSIZE)) != (0) else -1)
    @compressed_size.setter
    def compressed_size(self, value) -> int:
        self.__m_compressed_size = value
        self.__m_known = (Utils.valToEnum((self.__m_known) | (ZipEntry.Known.COMPRESSEDSIZE), ZipEntry.Known))
        return value
    
    @property
    def crc(self) -> int:
        return (self.__m_crc if ((self.__m_known) & (ZipEntry.Known.CRC)) != (0) else 0)
    @crc.setter
    def crc(self, value) -> int:
        self.__m_crc = value
        self.__m_known = (Utils.valToEnum((self.__m_known) | (ZipEntry.Known.CRC), ZipEntry.Known))
        return value
    
    @property
    def crc_ok(self) -> bool:
        return ((self.__m_known) & (ZipEntry.Known.CRC)) != (0)
    
    @property
    def _compression_method(self) -> 'CompressionMethod':
        return self.__m_method
    @_compression_method.setter
    def _compression_method(self, value) -> 'CompressionMethod':
        if (not ZipEntry.is_compression_method_supported_ex(value)): 
            raise Exception("Compression method not supported")
        self.__m_method = value
        return value
    
    @property
    def _compression_method_for_header(self) -> 'CompressionMethod':
        return (CompressionMethod.WINZIPAES if (self.aeskey_size > 0) else self.__m_method)
    
    @property
    def extra_data(self) -> bytearray:
        return self.__m_extra
    @extra_data.setter
    def extra_data(self, value) -> bytearray:
        if (value is None): 
            self.__m_extra = (None)
        else: 
            if (len(value) > 0xffff): 
                raise Exception("value")
            self.__m_extra = Utils.newArrayOfBytes(len(value), 0)
            Utils.copyArray(value, 0, self.__m_extra, 0, len(value))
        return value
    
    @property
    def aeskey_size(self) -> int:
        swichVal = self.__aes_encryption_strength
        if (swichVal == 0): 
            return 0
        elif (swichVal == 1): 
            return 128
        elif (swichVal == 2): 
            return 192
        elif (swichVal == 3): 
            return 256
        else: 
            raise Utils.newException("Invalid AESEncryptionStrength " + (chr(self.__aes_encryption_strength)), None)
    @aeskey_size.setter
    def aeskey_size(self, value) -> int:
        swichVal = value
        if (swichVal == 0): 
            self.__aes_encryption_strength = 0
        elif (swichVal == 128): 
            self.__aes_encryption_strength = 1
        elif (swichVal == 256): 
            self.__aes_encryption_strength = 3
        else: 
            raise Utils.newException("AESKeySize must be 0, 128 or 256: " + (chr(value)), None)
        return value
    
    @property
    def _aesencryption_strength(self) -> int:
        return self.__aes_encryption_strength
    
    @property
    def _aessalt_len(self) -> int:
        return math.floor(self.aeskey_size / 16)
    
    @property
    def _aesoverhead_size(self) -> int:
        return 12 + self._aessalt_len
    
    def _process_extra_data(self, local_header : bool) -> None:
        extra_data_ = ZipExtraData(self.__m_extra)
        if (extra_data_.find(0x0001)): 
            self.__force_zip64_ = True
            if (extra_data_.value_length < 4): 
                return
            if (local_header or ((self.__m_size == 2147483647))): 
                self.__m_size = (extra_data_.read_long())
            if (local_header or ((self.__m_compressed_size == 2147483647))): 
                self.__m_compressed_size = (extra_data_.read_long())
            if (not local_header and ((self.__m_ooffset == 2147483647))): 
                self.__m_ooffset = (extra_data_.read_long())
        elif ((((((self.__version_to_extract) & 0xff)) >= ZipConstants.VERSION_ZIP64)) and ((((self.__m_size == 2147483647)) or ((self.__m_compressed_size == 2147483647))))): 
            raise Utils.newException("Zip64 Extended information required but is missing.", None)
        if (extra_data_.find(10)): 
            if (extra_data_.value_length < 4): 
                raise Utils.newException("NTFS Extra data invalid", None)
            extra_data_.read_int()
            while extra_data_.unread_count >= 4:
                ntfs_tag = extra_data_.read_short()
                ntfs_length = extra_data_.read_short()
                if (ntfs_tag == 1): 
                    if (ntfs_length >= 24): 
                        last_modification = extra_data_.read_long()
                        last_access = extra_data_.read_long()
                        create_time = extra_data_.read_long()
                    break
                else: 
                    extra_data_.skip(ntfs_length)
        elif (extra_data_.find(0x5455)): 
            length = extra_data_.value_length
            flags_ = extra_data_.read_byte()
            if (((((flags_ & 1)) != 0)) and ((length >= 5))): 
                itime = extra_data_.read_int()
                self.date_time = ((datetime.datetime(1970, 1, 1, 0, 0, 0)) + datetime.timedelta(seconds=itime))
        if (self.__m_method == CompressionMethod.WINZIPAES): 
            self.__processaesextra_data(extra_data_)
    
    def __processaesextra_data(self, extra_data_ : 'ZipExtraData') -> None:
        if (extra_data_.find(0x9901)): 
            self.__version_to_extract = (ZipConstants.VERSION_AES)
            self.flags = (self.flags | (GeneralBitFlags.STRONGENCRYPTION))
            length = extra_data_.value_length
            if (length < 7): 
                raise Utils.newException("AES Extra Data Length " + (chr(length)) + " invalid.", None)
            ver = extra_data_.read_short()
            vendor_id = extra_data_.read_short()
            encr_strength = extra_data_.read_byte()
            actual_compress = extra_data_.read_short()
            self.__aes_ver = ver
            self.__aes_encryption_strength = encr_strength
            self.__m_method = (Utils.valToEnum(actual_compress, CompressionMethod))
        else: 
            raise Utils.newException("AES Extra Data missing", None)
    
    @property
    def comment(self) -> str:
        return self.__m_comment
    @comment.setter
    def comment(self, value) -> str:
        if (((value is not None)) and ((len(value) > 0xffff))): 
            raise Exception("value", "cannot exceed 65535")
        self.__m_comment = value
        return value
    
    @property
    def is_directory(self) -> bool:
        name_length = len(self.__m_name)
        result = ((((name_length > 0)) and ((((self.__m_name[name_length - 1] == '/')) or ((self.__m_name[name_length - 1] == '\\')))))) or self.__has_dos_attributes(16)
        return result
    
    @property
    def is_file(self) -> bool:
        return not self.is_directory and not self.__has_dos_attributes(8)
    
    def is_compression_method_supported(self) -> bool:
        return ZipEntry.is_compression_method_supported_ex(self._compression_method)
    
    def clone(self) -> object:
        return self
    
    def __str__(self) -> str:
        return "{0}: {1}".format(self.__m_name, self.__m_compressed_size)
    
    @staticmethod
    def is_compression_method_supported_ex(method : 'CompressionMethod') -> bool:
        return ((method == CompressionMethod.DEFLATED)) or ((method == CompressionMethod.STORED))