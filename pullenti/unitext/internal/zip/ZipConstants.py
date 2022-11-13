# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.util.TextHelper import TextHelper
from pullenti.unitext.internal.zip.GeneralBitFlags import GeneralBitFlags
from pullenti.util.MiscHelper import MiscHelper

class ZipConstants:
    # This class contains constants used for Zip format files
    
    VERSION_MADE_BY = 51
    
    VERSION_STRONG_ENCRYPTION = 50
    
    VERSION_AES = 51
    
    VERSION_ZIP64 = 45
    
    LOCAL_HEADER_BASE_SIZE = 30
    
    ZIP64DATA_DESCRIPTOR_SIZE = 24
    
    DATA_DESCRIPTOR_SIZE = 16
    
    CENTRAL_HEADER_BASE_SIZE = 46
    
    END_OF_CENTRAL_RECORD_BASE_SIZE = 22
    
    CRYPTO_HEADER_SIZE = 12
    
    LOCAL_HEADER_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((3 << 16))) | ((4 << 24))
    
    LOCSIG = ((ord('P')) | (((ord('K')) << 8)) | ((3 << 16))) | ((4 << 24))
    
    SPANNING_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((7 << 16))) | ((8 << 24))
    
    SPANNINGSIG = ((ord('P')) | (((ord('K')) << 8)) | ((7 << 16))) | ((8 << 24))
    
    SPANNING_TEMP_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | (((ord('0')) << 16))) | (((ord('0')) << 24))
    
    SPANTEMPSIG = ((ord('P')) | (((ord('K')) << 8)) | (((ord('0')) << 16))) | (((ord('0')) << 24))
    
    DATA_DESCRIPTOR_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((7 << 16))) | ((8 << 24))
    
    EXTSIG = ((ord('P')) | (((ord('K')) << 8)) | ((7 << 16))) | ((8 << 24))
    
    CENSIG = ((ord('P')) | (((ord('K')) << 8)) | ((1 << 16))) | ((2 << 24))
    
    CENTRAL_HEADER_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((1 << 16))) | ((2 << 24))
    
    ZIP64CENTRAL_FILE_HEADER_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((6 << 16))) | ((6 << 24))
    
    CENSIG64 = ((ord('P')) | (((ord('K')) << 8)) | ((6 << 16))) | ((6 << 24))
    
    ZIP64CENTRAL_DIR_LOCATOR_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((6 << 16))) | ((7 << 24))
    
    ARCHIVE_EXTRA_DATA_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((6 << 16))) | ((7 << 24))
    
    CENTRAL_HEADER_DIGITAL_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((5 << 16))) | ((5 << 24))
    
    CENDIGITALSIG = ((ord('P')) | (((ord('K')) << 8)) | ((5 << 16))) | ((5 << 24))
    
    END_OF_CENTRAL_DIRECTORY_SIGNATURE = ((ord('P')) | (((ord('K')) << 8)) | ((5 << 16))) | ((6 << 24))
    
    ENDSIG = ((ord('P')) | (((ord('K')) << 8)) | ((5 << 16))) | ((6 << 24))
    
    @staticmethod
    def convert_to_string(data : bytearray, count : int) -> str:
        if (data is None): 
            return ""
        tmp = TextHelper.read_string_from_bytes(data, False)
        return tmp
    
    @staticmethod
    def convert_to_string0(data : bytearray) -> str:
        if (data is None): 
            return ""
        return ZipConstants.convert_to_string(data, len(data))
    
    @staticmethod
    def convert_to_string_ext(flags : int, data : bytearray, count : int) -> str:
        if (data is None): 
            return ""
        if (((flags & (GeneralBitFlags.UNICODETEXT))) != 0): 
            return MiscHelper.decode_string_utf8(data, 0, count)
        else: 
            return ZipConstants.convert_to_string(data, count)
    
    @staticmethod
    def convert_to_string_ext0(flags : int, data : bytearray) -> str:
        if (data is None): 
            return ""
        if (((flags & (GeneralBitFlags.UNICODETEXT))) != 0): 
            return MiscHelper.decode_string_utf8(data, 0, len(data))
        else: 
            return ZipConstants.convert_to_string(data, len(data))
    
    @staticmethod
    def convert_to_array_str(str0_ : str) -> bytearray:
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        return MiscHelper.encode_string_utf8(str0_, False)
    
    @staticmethod
    def convert_to_array(flags : int, str0_ : str) -> bytearray:
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        if (((flags & (GeneralBitFlags.UNICODETEXT))) != 0): 
            return MiscHelper.encode_string_utf8(str0_, False)
        else: 
            return ZipConstants.convert_to_array_str(str0_)
    
    def __init__(self) -> None:
        pass