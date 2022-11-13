# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.InflaterHuffmanTree import InflaterHuffmanTree

class InflaterDynHeader:
    
    __lnum = 0
    
    __dnum = 1
    
    __blnum = 2
    
    __bllens = 3
    
    __lens = 4
    
    __reps = 5
    
    __rep_min = None
    
    __rep_bits = None
    
    __bl_order = None
    
    def __init__(self) -> None:
        self.__bl_lens = None;
        self.__litdist_lens = None;
        self.__bl_tree = None;
        self.__mode = 0
        self.__m_lnum = 0
        self.__m_dnum = 0
        self.__m_blnum = 0
        self.__m_num = 0
        self.__rep_symbol = 0
        self.__last_len = 0
        self.__ptr = 0
    
    def decode(self, input0_ : 'StreamManipulator') -> bool:
        while True: 
            swichVal = self.__mode
            if (swichVal == InflaterDynHeader.__lnum): 
                self.__m_lnum = input0_.peek_bits(5)
                if (self.__m_lnum < 0): 
                    return False
                self.__m_lnum += 257
                input0_.drop_bits(5)
                self.__mode = InflaterDynHeader.__dnum
            elif (swichVal == InflaterDynHeader.__dnum): 
                self.__m_dnum = input0_.peek_bits(5)
                if (self.__m_dnum < 0): 
                    return False
                self.__m_dnum += 1
                input0_.drop_bits(5)
                self.__m_num = (self.__m_lnum + self.__m_dnum)
                self.__litdist_lens = Utils.newArrayOfBytes(self.__m_num, 0)
                self.__mode = InflaterDynHeader.__blnum
            elif (swichVal == InflaterDynHeader.__blnum): 
                self.__m_blnum = input0_.peek_bits(4)
                if (self.__m_blnum < 0): 
                    return False
                self.__m_blnum += 4
                input0_.drop_bits(4)
                self.__bl_lens = Utils.newArrayOfBytes(19, 0)
                self.__ptr = 0
                self.__mode = InflaterDynHeader.__bllens
            elif (swichVal == InflaterDynHeader.__bllens): 
                while self.__ptr < self.__m_blnum:
                    len0_ = input0_.peek_bits(3)
                    if (len0_ < 0): 
                        return False
                    input0_.drop_bits(3)
                    self.__bl_lens[InflaterDynHeader.__bl_order[self.__ptr]] = (len0_)
                    self.__ptr += 1
                self.__bl_tree = InflaterHuffmanTree(self.__bl_lens)
                self.__bl_lens = (None)
                self.__ptr = 0
                self.__mode = InflaterDynHeader.__lens
            elif (swichVal == InflaterDynHeader.__lens): 
                symbol = 0
                while True:
                    symbol = self.__bl_tree.get_symbol(input0_)
                    if (((((symbol)) & (~ 15))) == 0): pass
                    else: 
                        break
                    self.__last_len = symbol
                    self.__litdist_lens[self.__ptr] = self.__last_len
                    self.__ptr += 1
                    if (self.__ptr == self.__m_num): 
                        return True
                if (symbol < 0): 
                    return False
                if (symbol >= 17): 
                    self.__last_len = (0)
                elif (self.__ptr == 0): 
                    raise Exception()
                self.__rep_symbol = (symbol - 16)
                self.__mode = InflaterDynHeader.__reps
            elif (swichVal == InflaterDynHeader.__reps): 
                bits = InflaterDynHeader.__rep_bits[self.__rep_symbol]
                count = input0_.peek_bits(bits)
                if (count < 0): 
                    return False
                input0_.drop_bits(bits)
                count += InflaterDynHeader.__rep_min[self.__rep_symbol]
                if ((self.__ptr + count) > self.__m_num): 
                    raise Exception()
                while True:
                    if (count > 0): pass
                    else: 
                        break
                    count -= 1
                    
                    self.__litdist_lens[self.__ptr] = self.__last_len
                    self.__ptr += 1
                if (self.__ptr == self.__m_num): 
                    return True
                self.__mode = InflaterDynHeader.__lens
    
    def build_lit_len_tree(self) -> 'InflaterHuffmanTree':
        litlen_lens = Utils.newArrayOfBytes(self.__m_lnum, 0)
        Utils.copyArray(self.__litdist_lens, 0, litlen_lens, 0, self.__m_lnum)
        return InflaterHuffmanTree(litlen_lens)
    
    def build_dist_tree(self) -> 'InflaterHuffmanTree':
        dist_lens = Utils.newArrayOfBytes(self.__m_dnum, 0)
        Utils.copyArray(self.__litdist_lens, self.__m_lnum, dist_lens, 0, self.__m_dnum)
        return InflaterHuffmanTree(dist_lens)
    
    # static constructor for class InflaterDynHeader
    @staticmethod
    def _static_ctor():
        InflaterDynHeader.__rep_min = [3, 3, 11]
        InflaterDynHeader.__rep_bits = [2, 3, 7]
        InflaterDynHeader.__bl_order = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]

InflaterDynHeader._static_ctor()