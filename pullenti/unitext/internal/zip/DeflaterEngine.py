# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.zip.DeflaterConstants import DeflaterConstants
from pullenti.unitext.internal.zip.DeflateStrategy import DeflateStrategy
from pullenti.unitext.internal.zip.DeflaterHuffman import DeflaterHuffman
from pullenti.unitext.internal.zip.Adler32 import Adler32

class DeflaterEngine(DeflaterConstants):
    # Low level compression engine for deflate algorithm which uses a 32K sliding window
    # with secondary compression from Huffman/Shannon-Fano codes.
    
    __too_far = 4096
    
    def __init__(self, pending : 'DeflaterPending') -> None:
        super().__init__()
        self.__ins_h = 0
        self.__head = None;
        self.__prev = None;
        self.__match_start = 0
        self.__match_len = 0
        self.__prev_available = False
        self.__block_start = 0
        self.__strstart = 0
        self.__lookahead = 0
        self.__window = None;
        self.__m_strategy = DeflateStrategy.DEFAULT
        self.__max_chain = 0
        self.__max_lazy = 0
        self.__nice_length = 0
        self.__good_length = 0
        self.__compression_function = 0
        self.__input_buf = None;
        self.__m_total_in = 0
        self.__input_off = 0
        self.__input_end = 0
        self.__pending = None;
        self.__huffman = None;
        self.__m_adler = None;
        self.__pending = pending
        self.__huffman = DeflaterHuffman(pending)
        self.__m_adler = Adler32()
        self.__window = Utils.newArrayOfBytes(2 * DeflaterConstants.WSIZE, 0)
        self.__head = Utils.newArray(DeflaterConstants.HASH_SIZE, 0)
        self.__prev = Utils.newArray(DeflaterConstants.WSIZE, 0)
        self.__strstart = 1
        self.__block_start = self.__strstart
    
    def deflate(self, flush : bool, finish : bool) -> bool:
        progress = False
        while True:
            self.fill_window()
            can_flush = flush and ((self.__input_off == self.__input_end))
            swichVal = self.__compression_function
            if (swichVal == DeflaterConstants.DEFLATE_STORED): 
                progress = self.__deflate_stored(can_flush, finish)
            elif (swichVal == DeflaterConstants.DEFLATE_FAST): 
                progress = self.__deflate_fast(can_flush, finish)
            elif (swichVal == DeflaterConstants.DEFLATE_SLOW): 
                progress = self.__deflate_slow(can_flush, finish)
            else: 
                raise Exception("unknown compressionFunction")
            if (self.__pending.is_flushed and progress): 
                pass
            else: 
                break
        return progress
    
    def set_input(self, buffer : bytearray, offset : int, count : int) -> None:
        if (buffer is None): 
            raise Exception("buffer")
        if (offset < 0): 
            raise Exception("offset")
        if (count < 0): 
            raise Exception("count")
        if (self.__input_off < self.__input_end): 
            raise Exception("Old input was not completely processed")
        end = offset + count
        if (((offset > end)) or ((end > len(buffer)))): 
            raise Exception("count")
        self.__input_buf = buffer
        self.__input_off = offset
        self.__input_end = end
    
    def needs_input(self) -> bool:
        return (self.__input_end == self.__input_off)
    
    def set_dictionary(self, buffer : bytearray, offset : int, length : int) -> None:
        self.__m_adler.update_by_buf_ex(buffer, offset, length)
        if (length < DeflaterConstants.MIN_MATCH): 
            return
        if (length > DeflaterConstants.MAX_DIST): 
            offset += (length - DeflaterConstants.MAX_DIST)
            length = DeflaterConstants.MAX_DIST
        Utils.copyArray(buffer, offset, self.__window, self.__strstart, length)
        self.__update_hash()
        length -= 1
        while True:
            length -= 1
            if (length > 0): pass
            else: 
                break
            self.__insert_string()
            self.__strstart += 1
        self.__strstart += 2
        self.__block_start = self.__strstart
    
    def reset(self) -> None:
        self.__huffman.reset()
        self.__m_adler.reset()
        self.__strstart = 1
        self.__block_start = self.__strstart
        self.__lookahead = 0
        self.__m_total_in = 0
        self.__prev_available = False
        self.__match_len = (DeflaterConstants.MIN_MATCH - 1)
        i = 0
        while i < DeflaterConstants.HASH_SIZE: 
            self.__head[i] = (0)
            i += 1
        i = 0
        while i < DeflaterConstants.WSIZE: 
            self.__prev[i] = (0)
            i += 1
    
    def reset_adler(self) -> None:
        self.__m_adler.reset()
    
    @property
    def adler(self) -> int:
        return self.__m_adler.value
    
    @property
    def total_in(self) -> int:
        return self.__m_total_in
    
    @property
    def strategy(self) -> 'DeflateStrategy':
        return self.__m_strategy
    @strategy.setter
    def strategy(self, value) -> 'DeflateStrategy':
        self.__m_strategy = value
        return value
    
    def set_level(self, level : int) -> None:
        if (((level < 0)) or ((level > 9))): 
            raise Exception("level")
        self.__good_length = DeflaterConstants.GOOD_LENGTH[level]
        self.__max_lazy = DeflaterConstants.MAX_LAZY[level]
        self.__nice_length = DeflaterConstants.NICE_LENGTH[level]
        self.__max_chain = DeflaterConstants.MAX_CHAIN[level]
        if (DeflaterConstants.COMPR_FUNC[level] != self.__compression_function): 
            swichVal = self.__compression_function
            if (swichVal == DeflaterConstants.DEFLATE_STORED): 
                if (self.__strstart > self.__block_start): 
                    self.__huffman.flush_stored_block(self.__window, self.__block_start, self.__strstart - self.__block_start, False)
                    self.__block_start = self.__strstart
                self.__update_hash()
            elif (swichVal == DeflaterConstants.DEFLATE_FAST): 
                if (self.__strstart > self.__block_start): 
                    self.__huffman.flush_block(self.__window, self.__block_start, self.__strstart - self.__block_start, False)
                    self.__block_start = self.__strstart
            elif (swichVal == DeflaterConstants.DEFLATE_SLOW): 
                if (self.__prev_available): 
                    self.__huffman.tally_lit((self.__window[self.__strstart - 1]) & 0xff)
                if (self.__strstart > self.__block_start): 
                    self.__huffman.flush_block(self.__window, self.__block_start, self.__strstart - self.__block_start, False)
                    self.__block_start = self.__strstart
                self.__prev_available = False
                self.__match_len = (DeflaterConstants.MIN_MATCH - 1)
            self.__compression_function = DeflaterConstants.COMPR_FUNC[level]
    
    def fill_window(self) -> None:
        if (self.__strstart >= (DeflaterConstants.WSIZE + DeflaterConstants.MAX_DIST)): 
            self.__slide_window()
        while (self.__lookahead < DeflaterConstants.MIN_LOOKAHEAD) and (self.__input_off < self.__input_end):
            more = (2 * DeflaterConstants.WSIZE) - self.__lookahead - self.__strstart
            if (more > (self.__input_end - self.__input_off)): 
                more = (self.__input_end - self.__input_off)
            Utils.copyArray(self.__input_buf, self.__input_off, self.__window, self.__strstart + self.__lookahead, more)
            self.__m_adler.update_by_buf_ex(self.__input_buf, self.__input_off, more)
            self.__input_off += more
            self.__m_total_in += more
            self.__lookahead += more
        if (self.__lookahead >= DeflaterConstants.MIN_MATCH): 
            self.__update_hash()
    
    def __update_hash(self) -> None:
        self.__ins_h = ((((self.__window[self.__strstart]) << DeflaterConstants.HASH_SHIFT)) ^ (self.__window[self.__strstart + 1]))
    
    def __insert_string(self) -> int:
        match = 0
        hash0_ = ((((self.__ins_h << DeflaterConstants.HASH_SHIFT)) ^ (self.__window[self.__strstart + ((DeflaterConstants.MIN_MATCH - 1))]))) & DeflaterConstants.HASH_MASK
        match = self.__head[hash0_]
        self.__prev[self.__strstart & DeflaterConstants.WMASK] = match
        self.__head[hash0_] = (self.__strstart)
        self.__ins_h = hash0_
        return (match) & 0xffff
    
    def __slide_window(self) -> None:
        Utils.copyArray(self.__window, DeflaterConstants.WSIZE, self.__window, 0, DeflaterConstants.WSIZE)
        self.__match_start -= DeflaterConstants.WSIZE
        self.__strstart -= DeflaterConstants.WSIZE
        self.__block_start -= DeflaterConstants.WSIZE
        i = 0
        while i < DeflaterConstants.HASH_SIZE: 
            m = (self.__head[i]) & 0xffff
            self.__head[i] = ((((m - DeflaterConstants.WSIZE) if m >= DeflaterConstants.WSIZE else 0)))
            i += 1
        i = 0
        while i < DeflaterConstants.WSIZE: 
            m = (self.__prev[i]) & 0xffff
            self.__prev[i] = ((((m - DeflaterConstants.WSIZE) if m >= DeflaterConstants.WSIZE else 0)))
            i += 1
    
    def __find_longest_match(self, cur_match : int) -> bool:
        chain_length = self.__max_chain
        nice_length = self.__nice_length
        prev = self.__prev
        scan = self.__strstart
        match = 0
        best_end = self.__strstart + self.__match_len
        best_len = max(self.__match_len, DeflaterConstants.MIN_MATCH - 1)
        limit = max(self.__strstart - DeflaterConstants.MAX_DIST, 0)
        strend = (self.__strstart + DeflaterConstants.MAX_MATCH) - 1
        scan_end1 = self.__window[best_end - 1]
        scan_end = self.__window[best_end]
        if (best_len >= self.__good_length): 
            chain_length >>= 2
        if (nice_length > self.__lookahead): 
            nice_length = self.__lookahead
        while True:
            if ((self.__window[cur_match + best_len] != scan_end or self.__window[(cur_match + best_len) - 1] != scan_end1 or self.__window[cur_match] != self.__window[scan]) or self.__window[cur_match + 1] != self.__window[scan + 1]): 
                cur_match = (((prev[cur_match & DeflaterConstants.WMASK]) & 0xffff))
                chain_length -= 1
                if (cur_match > limit and chain_length != 0): 
                    pass
                else: 
                    break
                continue
            match = (cur_match + 2)
            scan += 2
            while True:
                scan += 1
                match += 1
                scan += 1
                match += 1
                scan += 1
                match += 1
                scan += 1
                match += 1
                scan += 1
                match += 1
                scan += 1
                match += 1
                scan += 1
                match += 1
                scan += 1
                match += 1
                if ((((self.__window[scan] == self.__window[match] and self.__window[scan] == self.__window[match] and self.__window[scan] == self.__window[match]) and self.__window[scan] == self.__window[match] and self.__window[scan] == self.__window[match]) and self.__window[scan] == self.__window[match] and self.__window[scan] == self.__window[match]) and self.__window[scan] == self.__window[match] and ((scan < strend))): pass
                else: 
                    break
            if (scan > best_end): 
                self.__match_start = cur_match
                best_end = scan
                best_len = (scan - self.__strstart)
                if (best_len >= nice_length): 
                    break
                scan_end1 = self.__window[best_end - 1]
                scan_end = self.__window[best_end]
            scan = self.__strstart
            cur_match = (((prev[cur_match & DeflaterConstants.WMASK]) & 0xffff))
            chain_length -= 1
            if (cur_match > limit and chain_length != 0): 
                pass
            else: 
                break
        self.__match_len = min(best_len, self.__lookahead)
        return self.__match_len >= DeflaterConstants.MIN_MATCH
    
    def __deflate_stored(self, flush : bool, finish : bool) -> bool:
        if (not flush and ((self.__lookahead == 0))): 
            return False
        self.__strstart += self.__lookahead
        self.__lookahead = 0
        stored_length = self.__strstart - self.__block_start
        if (((stored_length >= DeflaterConstants.MAX_BLOCK_SIZE)) or (((self.__block_start < DeflaterConstants.WSIZE) and stored_length >= DeflaterConstants.MAX_DIST)) or flush): 
            last_block = finish
            if (stored_length > DeflaterConstants.MAX_BLOCK_SIZE): 
                stored_length = DeflaterConstants.MAX_BLOCK_SIZE
                last_block = False
            self.__huffman.flush_stored_block(self.__window, self.__block_start, stored_length, last_block)
            self.__block_start += stored_length
            return not last_block
        return True
    
    def __deflate_fast(self, flush : bool, finish : bool) -> bool:
        if ((self.__lookahead < DeflaterConstants.MIN_LOOKAHEAD) and not flush): 
            return False
        while self.__lookahead >= DeflaterConstants.MIN_LOOKAHEAD or flush:
            if (self.__lookahead == 0): 
                self.__huffman.flush_block(self.__window, self.__block_start, self.__strstart - self.__block_start, finish)
                self.__block_start = self.__strstart
                return False
            if (self.__strstart > ((2 * DeflaterConstants.WSIZE) - DeflaterConstants.MIN_LOOKAHEAD)): 
                self.__slide_window()
            hash_head = 0
            hash_head = self.__insert_string()
            if ((self.__lookahead >= DeflaterConstants.MIN_MATCH and ((hash_head)) != 0 and self.__m_strategy != DeflateStrategy.HUFFMANONLY) and (self.__strstart - hash_head) <= DeflaterConstants.MAX_DIST and self.__find_longest_match(hash_head)): 
                full = self.__huffman.tally_dist(self.__strstart - self.__match_start, self.__match_len)
                self.__lookahead -= self.__match_len
                if (self.__match_len <= self.__max_lazy and self.__lookahead >= DeflaterConstants.MIN_MATCH): 
                    while True:
                        self.__match_len -= 1
                        if (self.__match_len > 0): pass
                        else: 
                            break
                        self.__strstart += 1
                        self.__insert_string()
                    self.__strstart += 1
                else: 
                    self.__strstart += self.__match_len
                    if (self.__lookahead >= (DeflaterConstants.MIN_MATCH - 1)): 
                        self.__update_hash()
                self.__match_len = (DeflaterConstants.MIN_MATCH - 1)
                if (not full): 
                    continue
            else: 
                self.__huffman.tally_lit((self.__window[self.__strstart]) & 0xff)
                self.__strstart += 1
                self.__lookahead -= 1
            if (self.__huffman.is_full()): 
                last_block = finish and ((self.__lookahead == 0))
                self.__huffman.flush_block(self.__window, self.__block_start, self.__strstart - self.__block_start, last_block)
                self.__block_start = self.__strstart
                return not last_block
        return True
    
    def __deflate_slow(self, flush : bool, finish : bool) -> bool:
        if ((self.__lookahead < DeflaterConstants.MIN_LOOKAHEAD) and not flush): 
            return False
        while self.__lookahead >= DeflaterConstants.MIN_LOOKAHEAD or flush:
            if (self.__lookahead == 0): 
                if (self.__prev_available): 
                    self.__huffman.tally_lit((self.__window[self.__strstart - 1]) & 0xff)
                self.__prev_available = False
                self.__huffman.flush_block(self.__window, self.__block_start, self.__strstart - self.__block_start, finish)
                self.__block_start = self.__strstart
                return False
            if (self.__strstart >= ((2 * DeflaterConstants.WSIZE) - DeflaterConstants.MIN_LOOKAHEAD)): 
                self.__slide_window()
            prev_match = self.__match_start
            prev_len = self.__match_len
            if (self.__lookahead >= DeflaterConstants.MIN_MATCH): 
                hash_head = self.__insert_string()
                if ((self.__m_strategy != DeflateStrategy.HUFFMANONLY and hash_head != 0 and (self.__strstart - hash_head) <= DeflaterConstants.MAX_DIST) and self.__find_longest_match(hash_head)): 
                    if (self.__match_len <= 5 and ((self.__m_strategy == DeflateStrategy.FILTERED or ((self.__match_len == DeflaterConstants.MIN_MATCH and (self.__strstart - self.__match_start) > DeflaterEngine.__too_far))))): 
                        self.__match_len = (DeflaterConstants.MIN_MATCH - 1)
            if (((prev_len >= DeflaterConstants.MIN_MATCH)) and ((self.__match_len <= prev_len))): 
                self.__huffman.tally_dist(self.__strstart - 1 - prev_match, prev_len)
                prev_len -= 2
                first_pass = True
                while first_pass or (prev_len > 0):
                    first_pass = False
                    self.__strstart += 1
                    self.__lookahead -= 1
                    if (self.__lookahead >= DeflaterConstants.MIN_MATCH): 
                        self.__insert_string()
                    prev_len -= 1
                self.__strstart += 1
                self.__lookahead -= 1
                self.__prev_available = False
                self.__match_len = (DeflaterConstants.MIN_MATCH - 1)
            else: 
                if (self.__prev_available): 
                    self.__huffman.tally_lit((self.__window[self.__strstart - 1]) & 0xff)
                self.__prev_available = True
                self.__strstart += 1
                self.__lookahead -= 1
            if (self.__huffman.is_full()): 
                len0_ = self.__strstart - self.__block_start
                if (self.__prev_available): 
                    len0_ -= 1
                last_block = (finish and ((self.__lookahead == 0)) and not self.__prev_available)
                self.__huffman.flush_block(self.__window, self.__block_start, len0_, last_block)
                self.__block_start += len0_
                return not last_block
        return True