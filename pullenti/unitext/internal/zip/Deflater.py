# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.zip.DeflateStrategy import DeflateStrategy
from pullenti.unitext.internal.zip.DeflaterConstants import DeflaterConstants
from pullenti.unitext.internal.zip.DeflaterPending import DeflaterPending
from pullenti.unitext.internal.zip.DeflaterEngine import DeflaterEngine

class Deflater:
    # This is the Deflater class.  The deflater class compresses input
    # with the deflate algorithm described in RFC 1951.  It has several
    # compression levels and three different strategies described below.
    # This class is <i>not</i> thread safe.  This is inherent in the API, due
    # to the split of deflate and setInput.
    
    BEST_COMPRESSION = 9
    
    BEST_SPEED = 1
    
    DEFAULT_COMPRESSION = -1
    
    NO_COMPRESSION = 0
    
    DEFLATED = 8
    
    __is_setdict = 0x01
    
    __is_flushing = 0x04
    
    __is_finishing = 0x08
    
    __init_state = 0x00
    
    __setdict_state = 0x01
    
    __busy_state = 0x10
    
    __flushing_state = 0x14
    
    __finishing_state = 0x1c
    
    __finished_state = 0x1e
    
    __closed_state = 0x7f
    
    def __init__(self, level : int=DEFAULT_COMPRESSION, no_zlib_header_or_footer : bool=False) -> None:
        self.__level = 0
        self.__no_zlib_header_or_footer = False
        self.__state = 0
        self.__m_total_out = 0
        self.__pending = None;
        self.__engine = None;
        try: 
            if (level == Deflater.DEFAULT_COMPRESSION): 
                level = 6
            elif ((level < Deflater.NO_COMPRESSION) or level > Deflater.BEST_COMPRESSION): 
                raise Exception("level")
            self.__pending = DeflaterPending()
            self.__engine = DeflaterEngine(self.__pending)
            self.__no_zlib_header_or_footer = no_zlib_header_or_footer
            self.set_strategy(DeflateStrategy.DEFAULT)
            self.set_level(level)
            self.reset()
        except Exception as ex: 
            pass
    
    def reset(self) -> None:
        self.__state = (((Deflater.__busy_state if self.__no_zlib_header_or_footer else Deflater.__init_state)))
        self.__m_total_out = 0
        self.__pending.reset()
        self.__engine.reset()
    
    @property
    def adler(self) -> int:
        return self.__engine.adler
    
    @property
    def total_in(self) -> int:
        return self.__engine.total_in
    
    @property
    def total_out(self) -> int:
        return self.__m_total_out
    
    def flush(self) -> None:
        self.__state |= Deflater.__is_flushing
    
    def finish(self) -> None:
        self.__state |= ((Deflater.__is_flushing | Deflater.__is_finishing))
    
    @property
    def is_finished(self) -> bool:
        return ((self.__state == Deflater.__finished_state)) and self.__pending.is_flushed
    
    @property
    def is_needing_input(self) -> bool:
        return self.__engine.needs_input()
    
    def set_input(self, input0_ : bytearray) -> None:
        self.set_input_ex(input0_, 0, len(input0_))
    
    def set_input_ex(self, input0_ : bytearray, offset : int, count : int) -> None:
        if (((self.__state & Deflater.__is_finishing)) != 0): 
            raise Exception("Finish() already called")
        self.__engine.set_input(input0_, offset, count)
    
    def set_level(self, level : int) -> None:
        if (level == Deflater.DEFAULT_COMPRESSION): 
            level = 6
        elif ((level < Deflater.NO_COMPRESSION) or level > Deflater.BEST_COMPRESSION): 
            raise Exception("level")
        if (self.__level != level): 
            self.__level = level
            self.__engine.set_level(level)
    
    def get_level(self) -> int:
        return self.__level
    
    def set_strategy(self, strategy : 'DeflateStrategy') -> None:
        self.__engine.strategy = strategy
    
    def deflate(self, output : bytearray) -> int:
        return self.deflate_ex(output, 0, len(output))
    
    def deflate_ex(self, output : bytearray, offset : int, length : int) -> int:
        orig_length = length
        if (self.__state == Deflater.__closed_state): 
            raise Exception("Deflater closed")
        if (self.__state < Deflater.__busy_state): 
            header = ((Deflater.DEFLATED + ((((DeflaterConstants.MAX_WBITS - 8)) << 4)))) << 8
            level_flags = ((self.__level - 1)) >> 1
            if ((level_flags < 0) or level_flags > 3): 
                level_flags = 3
            header |= level_flags << 6
            if (((self.__state & Deflater.__is_setdict)) != 0): 
                header |= DeflaterConstants.PRESET_DICT
            header += (31 - ((header % 31)))
            self.__pending.write_shortmsb(header)
            if (((self.__state & Deflater.__is_setdict)) != 0): 
                chksum = self.__engine.adler
                self.__engine.reset_adler()
                self.__pending.write_shortmsb(chksum >> 16)
                self.__pending.write_shortmsb(chksum & 0xffff)
            self.__state = (Deflater.__busy_state | ((self.__state & ((Deflater.__is_flushing | Deflater.__is_finishing)))))
        while True: 
            count = self.__pending.flush(output, offset, length)
            offset += count
            self.__m_total_out += count
            length -= count
            if (length == 0 or self.__state == Deflater.__finished_state): 
                break
            if (not self.__engine.deflate(((self.__state & Deflater.__is_flushing)) != 0, ((self.__state & Deflater.__is_finishing)) != 0)): 
                if (self.__state == Deflater.__busy_state): 
                    return orig_length - length
                elif (self.__state == Deflater.__flushing_state): 
                    if (self.__level != Deflater.NO_COMPRESSION): 
                        neededbits = 8 + ((((- self.__pending.bit_count)) & 7))
                        while neededbits > 0:
                            self.__pending.write_bits(2, 10)
                            neededbits -= 10
                    self.__state = Deflater.__busy_state
                elif (self.__state == Deflater.__finishing_state): 
                    self.__pending.align_to_byte()
                    if (not self.__no_zlib_header_or_footer): 
                        adler_ = self.__engine.adler
                        self.__pending.write_shortmsb(adler_ >> 16)
                        self.__pending.write_shortmsb(adler_ & 0xffff)
                    self.__state = Deflater.__finished_state
        return orig_length - length
    
    def set_dictionary(self, dictionary : bytearray) -> None:
        self.set_dictionary_ex(dictionary, 0, len(dictionary))
    
    def set_dictionary_ex(self, dictionary : bytearray, index : int, count : int) -> None:
        if (self.__state != Deflater.__init_state): 
            raise Exception()
        self.__state = Deflater.__setdict_state
        self.__engine.set_dictionary(dictionary, index, count)