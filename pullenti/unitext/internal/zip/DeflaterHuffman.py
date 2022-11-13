# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.zip.DeflaterConstants import DeflaterConstants

class DeflaterHuffman:
    # This is the DeflaterHuffman class.
    # This class is <i>not</i> thread safe.  This is inherent in the API, due
    # to the split of Deflate and SetInput.
    
    class Tree:
        
        def __init__(self, dh : 'DeflaterHuffman', elems : int, min_codes : int, max_length : int) -> None:
            self.freqs = None;
            self.length = None;
            self.min_num_codes = 0
            self.num_codes = 0
            self.__codes = None;
            self.__bl_counts = None;
            self.__max_length = 0
            self.__dh = None;
            self.__dh = dh
            self.min_num_codes = min_codes
            self.__max_length = max_length
            self.freqs = Utils.newArray(elems, 0)
            self.__bl_counts = Utils.newArray(max_length, 0)
        
        def reset(self) -> None:
            i = 0
            while i < len(self.freqs): 
                self.freqs[i] = (0)
                i += 1
            self.__codes = (None)
            self.length = (None)
        
        def write_symbol(self, code : int) -> None:
            self.__dh.pending.write_bits((self.__codes[code]) & 0xffff, self.length[code])
        
        def check_empty(self) -> None:
            empty = True
            i = 0
            while i < len(self.freqs): 
                if (self.freqs[i] != (0)): 
                    empty = False
                i += 1
            if (not empty): 
                raise Utils.newException("!Empty", None)
        
        def set_static_codes(self, static_codes : typing.List[int], static_lengths : bytearray) -> None:
            self.__codes = static_codes
            self.length = static_lengths
        
        def build_codes(self) -> None:
            num_symbols = len(self.freqs)
            next_code = Utils.newArray(self.__max_length, 0)
            code = 0
            self.__codes = Utils.newArray(len(self.freqs), 0)
            bits = 0
            while bits < self.__max_length: 
                next_code[bits] = code
                code += self.__bl_counts[bits] << ((15 - bits))
                bits += 1
            i = 0
            while i < self.num_codes: 
                bits = self.length[i]
                if (bits > 0): 
                    self.__codes[i] = DeflaterHuffman.bit_reverse(next_code[bits - 1])
                    next_code[bits - 1] += 1 << ((16 - bits))
                i += 1
        
        def build_tree(self) -> None:
            num_symbols = len(self.freqs)
            heap = Utils.newArray(num_symbols, 0)
            heap_len = 0
            max_code = 0
            n = 0
            while n < num_symbols: 
                freq = self.freqs[n]
                if (freq != 0): 
                    pos = heap_len
                    heap_len += 1
                    ppos = 0
                    while True:
                        ppos = math.floor(((pos - 1)) / 2)
                        if (pos > 0 and self.freqs[heap[ppos]] > freq): pass
                        else: 
                            break
                        heap[pos] = heap[ppos]
                        pos = ppos
                    heap[pos] = n
                    max_code = n
                n += 1
            while heap_len < 2:
                max_code += 1
                node = (max_code if max_code < 2 else 0)
                heap[heap_len] = node
                heap_len += 1
            self.num_codes = max(max_code + 1, self.min_num_codes)
            num_leafs = heap_len
            childs = Utils.newArray((4 * heap_len) - 2, 0)
            values = Utils.newArray((2 * heap_len) - 1, 0)
            num_nodes = num_leafs
            i = 0
            while i < heap_len: 
                node = heap[i]
                childs[2 * i] = node
                childs[(2 * i) + 1] = -1
                values[i] = (self.freqs[node]) << 8
                heap[i] = i
                i += 1
            first_pass = True
            while first_pass or (heap_len > 1):
                first_pass = False
                first = heap[0]
                heap_len -= 1
                last = heap[heap_len]
                ppos = 0
                path = 1
                while path < heap_len:
                    if (((path + 1) < heap_len) and values[heap[path]] > values[heap[path + 1]]): 
                        path += 1
                    heap[ppos] = heap[path]
                    ppos = path
                    path = ((path * 2) + 1)
                last_val = values[last]
                while True:
                    path = ppos
                    ppos = math.floor(((path - 1)) / 2)
                    if (((path)) > 0 and values[heap[ppos]] > last_val): pass
                    else: 
                        break
                    heap[path] = heap[ppos]
                heap[path] = last
                second = heap[0]
                last = num_nodes
                num_nodes += 1
                childs[2 * last] = first
                childs[(2 * last) + 1] = second
                mindepth = min(values[first] & 0xff, values[second] & 0xff)
                last_val = ((values[first] + values[second]) - mindepth) + 1
                values[last] = last_val
                ppos = 0
                path = 1
                while path < heap_len:
                    if (((path + 1) < heap_len) and values[heap[path]] > values[heap[path + 1]]): 
                        path += 1
                    heap[ppos] = heap[path]
                    ppos = path
                    path = ((ppos * 2) + 1)
                while True:
                    path = ppos
                    ppos = math.floor(((path - 1)) / 2)
                    if (((path)) > 0 and values[heap[ppos]] > last_val): pass
                    else: 
                        break
                    heap[path] = heap[ppos]
                heap[path] = last
            if (heap[0] != ((math.floor(len(childs) / 2)) - 1)): 
                raise Utils.newException("Heap invariant violated", None)
            self.__build_length(childs)
        
        def get_encoded_length(self) -> int:
            len0_ = 0
            i = 0
            while i < len(self.freqs): 
                len0_ += ((self.freqs[i]) * (self.length[i]))
                i += 1
            return len0_
        
        def calcblfreq(self, bl_tree : 'Tree') -> None:
            max_count = 0
            min_count = 0
            count = 0
            curlen = -1
            i = 0
            while i < self.num_codes:
                count = 1
                nextlen = self.length[i]
                if (nextlen == 0): 
                    max_count = 138
                    min_count = 3
                else: 
                    max_count = 6
                    min_count = 3
                    if (curlen != nextlen): 
                        bl_tree.freqs[nextlen] += 1
                        count = 0
                curlen = nextlen
                i += 1
                while (i < self.num_codes) and curlen == (self.length[i]):
                    i += 1
                    count += 1
                    if (count >= max_count): 
                        break
                if (count < min_count): 
                    bl_tree.freqs[curlen] += (count)
                elif (curlen != 0): 
                    bl_tree.freqs[DeflaterHuffman.REP_3_6] += 1
                elif (count <= 10): 
                    bl_tree.freqs[DeflaterHuffman.REP_3_10] += 1
                else: 
                    bl_tree.freqs[DeflaterHuffman.REP_11_138] += 1
        
        def write_tree(self, bl_tree : 'Tree') -> None:
            max_count = 0
            min_count = 0
            count = 0
            curlen = -1
            i = 0
            while i < self.num_codes:
                count = 1
                nextlen = self.length[i]
                if (nextlen == 0): 
                    max_count = 138
                    min_count = 3
                else: 
                    max_count = 6
                    min_count = 3
                    if (curlen != nextlen): 
                        bl_tree.write_symbol(nextlen)
                        count = 0
                curlen = nextlen
                i += 1
                while (i < self.num_codes) and curlen == (self.length[i]):
                    i += 1
                    count += 1
                    if (count >= max_count): 
                        break
                if (count < min_count): 
                    while True:
                        if (count > 0): pass
                        else: 
                            break
                        count -= 1
                        
                        bl_tree.write_symbol(curlen)
                elif (curlen != 0): 
                    bl_tree.write_symbol(DeflaterHuffman.REP_3_6)
                    self.__dh.pending.write_bits(count - 3, 2)
                elif (count <= 10): 
                    bl_tree.write_symbol(DeflaterHuffman.REP_3_10)
                    self.__dh.pending.write_bits(count - 3, 3)
                else: 
                    bl_tree.write_symbol(DeflaterHuffman.REP_11_138)
                    self.__dh.pending.write_bits(count - 11, 7)
        
        def __build_length(self, childs : typing.List[int]) -> None:
            self.length = Utils.newArrayOfBytes(len(self.freqs), 0)
            num_nodes = math.floor(len(childs) / 2)
            num_leafs = math.floor(((num_nodes + 1)) / 2)
            overflow = 0
            i = 0
            while i < self.__max_length: 
                self.__bl_counts[i] = 0
                i += 1
            lengths = Utils.newArray(num_nodes, 0)
            lengths[num_nodes - 1] = 0
            for i in range(num_nodes - 1, -1, -1):
                if (childs[(2 * i) + 1] != -1): 
                    bit_length = lengths[i] + 1
                    if (bit_length > self.__max_length): 
                        bit_length = self.__max_length
                        overflow += 1
                    lengths[childs[(2 * i) + 1]] = bit_length
                    lengths[childs[2 * i]] = lengths[childs[(2 * i) + 1]]
                else: 
                    bit_length = lengths[i]
                    self.__bl_counts[bit_length - 1] += 1
                    self.length[childs[2 * i]] = (lengths[i])
            if (overflow == 0): 
                return
            incr_bit_len = self.__max_length - 1
            first_pass = True
            while first_pass or (overflow > 0):
                first_pass = False
                while True:
                    incr_bit_len -= 1
                    if (self.__bl_counts[incr_bit_len] == 0): pass
                    else: 
                        break
                first_pass = True
                while first_pass or (overflow > 0 and (incr_bit_len < (self.__max_length - 1))):
                    first_pass = False
                    self.__bl_counts[incr_bit_len] -= 1
                    incr_bit_len += 1
                    self.__bl_counts[incr_bit_len] += 1
                    overflow -= 1 << ((self.__max_length - 1 - incr_bit_len))
            self.__bl_counts[self.__max_length - 1] += overflow
            self.__bl_counts[self.__max_length - 2] -= overflow
            node_ptr = 2 * num_leafs
            bits = self.__max_length
            while bits != 0: 
                n = self.__bl_counts[bits - 1]
                while n > 0:
                    child_ptr = 2 * childs[node_ptr]
                    node_ptr += 1
                    if (childs[child_ptr + 1] == -1): 
                        self.length[childs[child_ptr]] = (bits)
                        n -= 1
                bits -= 1
    
    BUFSIZE = 1 << ((DeflaterConstants.DEFAULT_MEM_LEVEL + 6))
    
    LITERAL_NUM = 286
    
    DIST_NUM = 30
    
    BITLEN_NUM = 19
    
    REP_3_6 = 16
    
    REP_3_10 = 17
    
    REP_11_138 = 18
    
    EOF_SYMBOL = 256
    
    BL_ORDER = None
    
    BIT4REVERSE = None
    
    STATICLCODES = None
    
    STATICLLENGTH = None
    
    STATICDCODES = None
    
    STATICDLENGTH = None
    
    def __init__(self, pending_ : 'DeflaterPending') -> None:
        self.pending = None;
        self.__literal_tree = None;
        self.__dist_tree = None;
        self.__bl_tree = None;
        self.__d_buf = None;
        self.__l_buf = None;
        self.__last_lit = 0
        self.__extra_bits = 0
        self.pending = pending_
        self.__literal_tree = DeflaterHuffman.Tree(self, DeflaterHuffman.LITERAL_NUM, 257, 15)
        self.__dist_tree = DeflaterHuffman.Tree(self, DeflaterHuffman.DIST_NUM, 1, 15)
        self.__bl_tree = DeflaterHuffman.Tree(self, DeflaterHuffman.BITLEN_NUM, 4, 7)
        self.__d_buf = Utils.newArray(DeflaterHuffman.BUFSIZE, 0)
        self.__l_buf = Utils.newArrayOfBytes(DeflaterHuffman.BUFSIZE, 0)
    
    def reset(self) -> None:
        self.__last_lit = 0
        self.__extra_bits = 0
        self.__literal_tree.reset()
        self.__dist_tree.reset()
        self.__bl_tree.reset()
    
    def send_all_trees(self, bl_tree_codes : int) -> None:
        self.__bl_tree.build_codes()
        self.__literal_tree.build_codes()
        self.__dist_tree.build_codes()
        self.pending.write_bits(self.__literal_tree.num_codes - 257, 5)
        self.pending.write_bits(self.__dist_tree.num_codes - 1, 5)
        self.pending.write_bits(bl_tree_codes - 4, 4)
        rank = 0
        while rank < bl_tree_codes: 
            self.pending.write_bits(self.__bl_tree.length[DeflaterHuffman.BL_ORDER[rank]], 3)
            rank += 1
        self.__literal_tree.write_tree(self.__bl_tree)
        self.__dist_tree.write_tree(self.__bl_tree)
    
    def compress_block(self) -> None:
        i = 0
        while i < self.__last_lit: 
            litlen = (self.__l_buf[i]) & 0xff
            dist = (self.__d_buf[i]) - 1
            if (dist != -1): 
                lc = DeflaterHuffman.__lcode(litlen)
                self.__literal_tree.write_symbol(lc)
                bits = math.floor(((lc - 261)) / 4)
                if (bits > 0 and bits <= 5): 
                    self.pending.write_bits(litlen & ((((1 << bits)) - 1)), bits)
                dc = DeflaterHuffman.__dcode(dist)
                self.__dist_tree.write_symbol(dc)
                bits = ((math.floor(dc / 2)) - 1)
                if (bits > 0): 
                    self.pending.write_bits(dist & ((((1 << bits)) - 1)), bits)
            else: 
                self.__literal_tree.write_symbol(litlen)
            i += 1
        self.__literal_tree.write_symbol(DeflaterHuffman.EOF_SYMBOL)
    
    def flush_stored_block(self, stored : bytearray, stored_offset : int, stored_length : int, last_block : bool) -> None:
        self.pending.write_bits(((DeflaterConstants.STORED_BLOCK << 1)) + (((1 if last_block else 0))), 3)
        self.pending.align_to_byte()
        self.pending.write_short(stored_length)
        self.pending.write_short(~ stored_length)
        self.pending.write_block(stored, stored_offset, stored_length)
        self.reset()
    
    def flush_block(self, stored : bytearray, stored_offset : int, stored_length : int, last_block : bool) -> None:
        self.__literal_tree.freqs[DeflaterHuffman.EOF_SYMBOL] += 1
        self.__literal_tree.build_tree()
        self.__dist_tree.build_tree()
        self.__literal_tree.calcblfreq(self.__bl_tree)
        self.__dist_tree.calcblfreq(self.__bl_tree)
        self.__bl_tree.build_tree()
        bl_tree_codes = 4
        for i in range(18, bl_tree_codes, -1):
            if (self.__bl_tree.length[DeflaterHuffman.BL_ORDER[i]] > (0)): 
                bl_tree_codes = (i + 1)
        opt_len = ((14 + (bl_tree_codes * 3) + self.__bl_tree.get_encoded_length()) + self.__literal_tree.get_encoded_length() + self.__dist_tree.get_encoded_length()) + self.__extra_bits
        static_len = self.__extra_bits
        i = 0
        while i < DeflaterHuffman.LITERAL_NUM: 
            static_len += ((self.__literal_tree.freqs[i]) * (DeflaterHuffman.STATICLLENGTH[i]))
            i += 1
        i = 0
        while i < DeflaterHuffman.DIST_NUM: 
            static_len += ((self.__dist_tree.freqs[i]) * (DeflaterHuffman.STATICDLENGTH[i]))
            i += 1
        if (opt_len >= static_len): 
            opt_len = static_len
        if (stored_offset >= 0 and ((stored_length + 4) < (opt_len >> 3))): 
            self.flush_stored_block(stored, stored_offset, stored_length, last_block)
        elif (opt_len == static_len): 
            self.pending.write_bits(((DeflaterConstants.STATIC_TREES << 1)) + (((1 if last_block else 0))), 3)
            self.__literal_tree.set_static_codes(DeflaterHuffman.STATICLCODES, DeflaterHuffman.STATICLLENGTH)
            self.__dist_tree.set_static_codes(DeflaterHuffman.STATICDCODES, DeflaterHuffman.STATICDLENGTH)
            self.compress_block()
            self.reset()
        else: 
            self.pending.write_bits(((DeflaterConstants.DYN_TREES << 1)) + (((1 if last_block else 0))), 3)
            self.send_all_trees(bl_tree_codes)
            self.compress_block()
            self.reset()
    
    def is_full(self) -> bool:
        return self.__last_lit >= DeflaterHuffman.BUFSIZE
    
    def tally_lit(self, literal : int) -> bool:
        self.__d_buf[self.__last_lit] = (0)
        self.__l_buf[self.__last_lit] = (literal)
        self.__last_lit += 1
        self.__literal_tree.freqs[literal] += 1
        return self.is_full()
    
    def tally_dist(self, distance : int, length : int) -> bool:
        self.__d_buf[self.__last_lit] = (distance)
        self.__l_buf[self.__last_lit] = ((length - 3))
        self.__last_lit += 1
        lc = DeflaterHuffman.__lcode(length - 3)
        self.__literal_tree.freqs[lc] += 1
        if (lc >= 265 and (lc < 285)): 
            self.__extra_bits += (math.floor(((lc - 261)) / 4))
        dc = DeflaterHuffman.__dcode(distance - 1)
        self.__dist_tree.freqs[dc] += 1
        if (dc >= 4): 
            self.__extra_bits += ((math.floor(dc / 2)) - 1)
        return self.is_full()
    
    @staticmethod
    def bit_reverse(to_reverse : int) -> int:
        return (((((DeflaterHuffman.BIT4REVERSE[to_reverse & 0xF]) << 12)) | (((DeflaterHuffman.BIT4REVERSE[((to_reverse >> 4)) & 0xF]) << 8)) | (((DeflaterHuffman.BIT4REVERSE[((to_reverse >> 8)) & 0xF]) << 4))) | (DeflaterHuffman.BIT4REVERSE[((to_reverse >> 12)) & 0xF]))
    
    @staticmethod
    def __lcode(length : int) -> int:
        if (length == 255): 
            return 285
        code = 257
        while length >= 8:
            code += 4
            length >>= 1
        return code + length
    
    @staticmethod
    def __dcode(distance : int) -> int:
        code = 0
        while distance >= 4:
            code += 2
            distance >>= 1
        return code + distance
    
    # static constructor for class DeflaterHuffman
    @staticmethod
    def _static_ctor():
        DeflaterHuffman.BL_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
        DeflaterHuffman.BIT4REVERSE = bytearray([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])
        DeflaterHuffman.STATICLCODES = Utils.newArray(DeflaterHuffman.LITERAL_NUM, 0)
        DeflaterHuffman.STATICLLENGTH = Utils.newArrayOfBytes(DeflaterHuffman.LITERAL_NUM, 0)
        i = 0
        while i < 144:
            DeflaterHuffman.STATICLCODES[i] = DeflaterHuffman.bit_reverse(((0x030 + i)) << 8)
            DeflaterHuffman.STATICLLENGTH[i] = (8)
            i += 1
        while i < 256:
            DeflaterHuffman.STATICLCODES[i] = DeflaterHuffman.bit_reverse((((0x190 - 144) + i)) << 7)
            DeflaterHuffman.STATICLLENGTH[i] = (9)
            i += 1
        while i < 280:
            DeflaterHuffman.STATICLCODES[i] = DeflaterHuffman.bit_reverse((((0x000 - 256) + i)) << 9)
            DeflaterHuffman.STATICLLENGTH[i] = (7)
            i += 1
        while i < DeflaterHuffman.LITERAL_NUM:
            DeflaterHuffman.STATICLCODES[i] = DeflaterHuffman.bit_reverse((((0x0c0 - 280) + i)) << 8)
            DeflaterHuffman.STATICLLENGTH[i] = (8)
            i += 1
        DeflaterHuffman.STATICDCODES = Utils.newArray(DeflaterHuffman.DIST_NUM, 0)
        DeflaterHuffman.STATICDLENGTH = Utils.newArrayOfBytes(DeflaterHuffman.DIST_NUM, 0)
        i = 0
        while i < DeflaterHuffman.DIST_NUM: 
            DeflaterHuffman.STATICDCODES[i] = DeflaterHuffman.bit_reverse(i << 11)
            DeflaterHuffman.STATICDLENGTH[i] = (5)
            i += 1

DeflaterHuffman._static_ctor()