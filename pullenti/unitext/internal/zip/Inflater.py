# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.InflaterHuffmanTree import InflaterHuffmanTree
from pullenti.unitext.internal.zip.DeflaterConstants import DeflaterConstants
from pullenti.unitext.internal.zip.Adler32 import Adler32
from pullenti.unitext.internal.zip.InflaterDynHeader import InflaterDynHeader
from pullenti.unitext.internal.zip.StreamManipulator import StreamManipulator
from pullenti.unitext.internal.zip.OutputWindow import OutputWindow
from pullenti.unitext.internal.zip.Deflater import Deflater

class Inflater:
    # Inflater is used to decompress data that has been compressed according
    # to the "deflate" standard described in rfc1951.
    # By default Zlib (rfc1950) headers and footers are expected in the input.
    # You can use constructor <code> public Inflater(bool noHeader)</code> passing true
    # if there is no Zlib header information
    # The usage is as following.  First you have to set some input with
    # <code>SetInput()</code>, then Inflate() it.  If inflate doesn't
    # inflate any bytes there may be three reasons:
    # <ul>
    # <li>IsNeedingInput() returns true because the input buffer is empty.
    # You have to provide more input with <code>SetInput()</code>.
    # NOTE: IsNeedingInput() also returns true when, the stream is finished.
    # </li>
    # <li>IsNeedingDictionary() returns true, you have to provide a preset
    # dictionary with <code>SetDictionary()</code>.</li>
    # <li>IsFinished returns true, the inflater has finished.</li>
    # </ul>
    # Once the first output byte is produced, a dictionary will not be
    # needed at a later stage.
    
    __cplens = None
    
    __cplext = None
    
    __cpdist = None
    
    __cpdext = None
    
    __decode_header = 0
    
    __decode_dict = 1
    
    __decode_blocks = 2
    
    __decode_stored_len1 = 3
    
    __decode_stored_len2 = 4
    
    __decode_stored = 5
    
    __decode_dyn_header = 6
    
    __decode_huffman = 7
    
    __decode_huffman_lenbits = 8
    
    __decode_huffman_dist = 9
    
    __decode_huffman_distbits = 10
    
    __decode_chksum = 11
    
    __finished = 12
    
    def __init__(self, no_header : bool=False) -> None:
        self.__mode = 0
        self.__read_adler = 0
        self.__needed_bits = 0
        self.__rep_length = 0
        self.__rep_dist = 0
        self.__uncompr_len = 0
        self.__is_last_block = False
        self.__m_total_out = 0
        self.__m_total_in = 0
        self.__no_header = False
        self.__input0_ = None;
        self.__output_window = None;
        self.__dyn_header = None;
        self.__litlen_tree = None;
        self.__dist_tree = None;
        self.__m_adler = None;
        self.__no_header = no_header
        self.__m_adler = Adler32()
        self.__input0_ = StreamManipulator()
        self.__output_window = OutputWindow()
        self.__mode = (Inflater.__decode_blocks if no_header else Inflater.__decode_header)
    
    def reset(self) -> None:
        self.__mode = (Inflater.__decode_blocks if self.__no_header else Inflater.__decode_header)
        self.__m_total_in = 0
        self.__m_total_out = 0
        self.__input0_.reset()
        self.__output_window.reset()
        self.__dyn_header = (None)
        self.__litlen_tree = (None)
        self.__dist_tree = (None)
        self.__is_last_block = False
        self.__m_adler.reset()
    
    def __decode_header_ex(self) -> bool:
        header = self.__input0_.peek_bits(16)
        if (header < 0): 
            return False
        self.__input0_.drop_bits(16)
        header = (((((header << 8)) | ((header >> 8)))) & 0xffff)
        if ((header % 31) != 0): 
            raise Utils.newException("Header checksum illegal", None)
        if (((header & 0x0f00)) != ((Deflater.DEFLATED << 8))): 
            raise Utils.newException("Compression Method unknown", None)
        if (((header & 0x0020)) == 0): 
            self.__mode = Inflater.__decode_blocks
        else: 
            self.__mode = Inflater.__decode_dict
            self.__needed_bits = 32
        return True
    
    def __decode_dict_ex(self) -> bool:
        while self.__needed_bits > 0:
            dict_byte = self.__input0_.peek_bits(8)
            if (dict_byte < 0): 
                return False
            self.__input0_.drop_bits(8)
            self.__read_adler = (((self.__read_adler << 8)) | dict_byte)
            self.__needed_bits -= 8
        return False
    
    def __decode_huffman_ex(self) -> bool:
        free = self.__output_window.get_free_space()
        mode0 = self.__mode
        while free >= 258:
            symbol = 0
            swichVal = mode0
            if (swichVal == Inflater.__decode_huffman): 
                while True:
                    symbol = self.__litlen_tree.get_symbol(self.__input0_)
                    if (((symbol & (~ 0xff))) != 0): 
                        break
                    self.__output_window.write0_(symbol)
                    free -= 1
                    if (free < 258): 
                        return True
                if (symbol < 257): 
                    if (symbol < 0): 
                        return False
                    else: 
                        self.__dist_tree = (None)
                        self.__litlen_tree = (None)
                        mode0 = Inflater.__decode_blocks
                        self.__mode = mode0
                        return True
                try: 
                    self.__rep_length = Inflater.__cplens[symbol - 257]
                    self.__needed_bits = Inflater.__cplext[symbol - 257]
                except Exception as ex513: 
                    raise Utils.newException("Illegal rep length code", None)
                mode0 = Inflater.__decode_huffman_lenbits
            elif (swichVal == Inflater.__decode_huffman_lenbits): 
                if (self.__needed_bits > 0): 
                    mode0 = Inflater.__decode_huffman_lenbits
                    self.__mode = mode0
                    i = self.__input0_.peek_bits(self.__needed_bits)
                    if (i < 0): 
                        return False
                    self.__input0_.drop_bits(self.__needed_bits)
                    self.__rep_length += i
                mode0 = Inflater.__decode_huffman_dist
                self.__mode = mode0
            elif (swichVal == Inflater.__decode_huffman_dist): 
                symbol = self.__dist_tree.get_symbol(self.__input0_)
                if (symbol < 0): 
                    return False
                try: 
                    self.__rep_dist = Inflater.__cpdist[symbol]
                    self.__needed_bits = Inflater.__cpdext[symbol]
                except Exception as ex514: 
                    raise Utils.newException("Illegal rep dist code", None)
                mode0 = Inflater.__decode_huffman_distbits
            elif (swichVal == Inflater.__decode_huffman_distbits): 
                if (self.__needed_bits > 0): 
                    mode0 = Inflater.__decode_huffman_distbits
                    self.__mode = mode0
                    i = self.__input0_.peek_bits(self.__needed_bits)
                    if (i < 0): 
                        return False
                    self.__input0_.drop_bits(self.__needed_bits)
                    self.__rep_dist += i
                self.__output_window.repeat(self.__rep_length, self.__rep_dist)
                free -= self.__rep_length
                mode0 = Inflater.__decode_huffman
                self.__mode = mode0
            else: 
                raise Utils.newException("Inflater unknown mode", None)
        return True
    
    def __decode_chksum_ex(self) -> bool:
        while self.__needed_bits > 0:
            chk_byte = self.__input0_.peek_bits(8)
            if (chk_byte < 0): 
                return False
            self.__input0_.drop_bits(8)
            self.__read_adler = (((self.__read_adler << 8)) | chk_byte)
            self.__needed_bits -= 8
        if ((self.__m_adler.value) != self.__read_adler): 
            raise Utils.newException(("Adler chksum doesn't match: " + (chr(self.__m_adler.value)) + " vs. ") + (chr(self.__read_adler)), None)
        self.__mode = Inflater.__finished
        return False
    
    def __decode(self) -> bool:
        while True:
            swichVal = self.__mode
            if (swichVal == Inflater.__decode_header): 
                return self.__decode_header_ex()
            elif (swichVal == Inflater.__decode_dict): 
                return self.__decode_dict_ex()
            elif (swichVal == Inflater.__decode_chksum): 
                return self.__decode_chksum_ex()
            elif (swichVal == Inflater.__decode_blocks): 
                if (self.__is_last_block): 
                    if (self.__no_header): 
                        self.__mode = Inflater.__finished
                        return False
                    else: 
                        self.__input0_.skip_to_byte_boundary()
                        self.__needed_bits = 32
                        self.__mode = Inflater.__decode_chksum
                        return True
                type0_ = self.__input0_.peek_bits(3)
                if (type0_ < 0): 
                    return False
                self.__input0_.drop_bits(3)
                if (((type0_ & 1)) != 0): 
                    self.__is_last_block = True
                swichVal = type0_ >> 1
                if (swichVal == DeflaterConstants.STORED_BLOCK): 
                    self.__input0_.skip_to_byte_boundary()
                    self.__mode = Inflater.__decode_stored_len1
                elif (swichVal == DeflaterConstants.STATIC_TREES): 
                    self.__litlen_tree = InflaterHuffmanTree.DEF_LIT_LEN_TREE
                    self.__dist_tree = InflaterHuffmanTree.DEF_DIST_TREE
                    self.__mode = Inflater.__decode_huffman
                elif (swichVal == DeflaterConstants.DYN_TREES): 
                    self.__dyn_header = InflaterDynHeader()
                    self.__mode = Inflater.__decode_dyn_header
                else: 
                    raise Utils.newException("Unknown block type " + (chr(type0_)), None)
                return True
            elif (swichVal == Inflater.__decode_stored_len1): 
                self.__uncompr_len = self.__input0_.peek_bits(16)
                if (((self.__uncompr_len)) < 0): 
                    return False
                self.__input0_.drop_bits(16)
                self.__mode = Inflater.__decode_stored_len2
            elif (swichVal == Inflater.__decode_stored_len2): 
                nlen = self.__input0_.peek_bits(16)
                if (nlen < 0): 
                    return False
                self.__input0_.drop_bits(16)
                if (nlen != ((self.__uncompr_len ^ 0xffff))): 
                    raise Utils.newException("broken uncompressed block", None)
                self.__mode = Inflater.__decode_stored
            elif (swichVal == Inflater.__decode_stored): 
                more = self.__output_window.copy_stored(self.__input0_, self.__uncompr_len)
                self.__uncompr_len -= more
                if (self.__uncompr_len == 0): 
                    self.__mode = Inflater.__decode_blocks
                    return True
                return not self.__input0_.is_needing_input
            elif (swichVal == Inflater.__decode_dyn_header): 
                if (not self.__dyn_header.decode(self.__input0_)): 
                    return False
                self.__litlen_tree = self.__dyn_header.build_lit_len_tree()
                self.__dist_tree = self.__dyn_header.build_dist_tree()
                self.__mode = Inflater.__decode_huffman
            elif (swichVal == Inflater.__decode_huffman or swichVal == Inflater.__decode_huffman_lenbits or swichVal == Inflater.__decode_huffman_dist or swichVal == Inflater.__decode_huffman_distbits): 
                return self.__decode_huffman_ex()
            elif (swichVal == Inflater.__finished): 
                return False
            else: 
                raise Utils.newException("Inflater.Decode unknown mode", None)
    
    def set_dictionary(self, buffer : bytearray) -> None:
        self.set_dictionary_ex(buffer, 0, len(buffer))
    
    def set_dictionary_ex(self, buffer : bytearray, index : int, count : int) -> None:
        if (buffer is None): 
            raise Exception("buffer")
        if (index < 0): 
            raise Exception("index")
        if (count < 0): 
            raise Exception("count")
        if (not self.is_needing_dictionary): 
            raise Exception("Dictionary is not needed")
        self.__m_adler.update_by_buf_ex(buffer, index, count)
        if ((self.__m_adler.value) != self.__read_adler): 
            raise Utils.newException("Wrong adler checksum", None)
        self.__m_adler.reset()
        self.__output_window.copy_dict(buffer, index, count)
        self.__mode = Inflater.__decode_blocks
    
    def set_input(self, buffer : bytearray) -> None:
        self.set_input_ex(buffer, 0, len(buffer))
    
    def set_input_ex(self, buffer : bytearray, index : int, count : int) -> None:
        self.__input0_.set_input(buffer, index, count)
        self.__m_total_in += count
    
    def inflate(self, buffer : bytearray) -> int:
        if (buffer is None): 
            raise Exception("buffer")
        return self.inflate_ex(buffer, 0, len(buffer))
    
    def inflate_ex(self, buffer : bytearray, offset : int, count : int) -> int:
        if (buffer is None): 
            raise Exception("buffer")
        if (count < 0): 
            raise Exception("count", "count cannot be negative")
        if (offset < 0): 
            raise Exception("offset", "offset cannot be negative")
        if ((offset + count) > len(buffer)): 
            raise Exception("count exceeds buffer bounds")
        if (count == 0): 
            if (not self.is_finished): 
                self.__decode()
            return 0
        bytes_copied = 0
        first_pass = True
        while first_pass or (self.__decode() or ((((self.__output_window.get_available() > 0)) and ((self.__mode != Inflater.__decode_chksum))))):
            first_pass = False
            if (self.__mode != Inflater.__decode_chksum): 
                more = self.__output_window.copy_output(buffer, offset, count)
                if (more > 0): 
                    self.__m_adler.update_by_buf_ex(buffer, offset, more)
                    offset += more
                    bytes_copied += more
                    self.__m_total_out += more
                    count -= more
                    if (count == 0): 
                        return bytes_copied
        return bytes_copied
    
    @property
    def is_needing_input(self) -> bool:
        return self.__input0_.is_needing_input
    
    @property
    def is_needing_dictionary(self) -> bool:
        return self.__mode == Inflater.__decode_dict and self.__needed_bits == 0
    
    @property
    def is_finished(self) -> bool:
        return self.__mode == Inflater.__finished and self.__output_window.get_available() == 0
    
    @property
    def adler(self) -> int:
        return (self.__read_adler if self.is_needing_dictionary else self.__m_adler.value)
    
    @property
    def total_out(self) -> int:
        return self.__m_total_out
    
    @property
    def total_in(self) -> int:
        return self.__m_total_in - self.remaining_input
    
    @property
    def remaining_input(self) -> int:
        return self.__input0_.available_bytes
    
    # static constructor for class Inflater
    @staticmethod
    def _static_ctor():
        Inflater.__cplens = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258]
        Inflater.__cplext = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0]
        Inflater.__cpdist = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577]
        Inflater.__cpdext = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13]

Inflater._static_ctor()