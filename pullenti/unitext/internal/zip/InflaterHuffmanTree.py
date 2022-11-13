# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.DeflaterHuffman import DeflaterHuffman

class InflaterHuffmanTree:
    # Huffman tree used for inflation
    
    __max_bitlen = 15
    
    DEF_LIT_LEN_TREE = None
    
    DEF_DIST_TREE = None
    
    def __init__(self, code_lengths : bytearray) -> None:
        self.__tree = None;
        self.__build_tree(code_lengths)
    
    def __build_tree(self, code_lengths : bytearray) -> None:
        bl_count = Utils.newArray(InflaterHuffmanTree.__max_bitlen + 1, 0)
        next_code = Utils.newArray(InflaterHuffmanTree.__max_bitlen + 1, 0)
        i = 0
        while i < len(code_lengths): 
            bits = code_lengths[i]
            if (bits > 0): 
                bl_count[bits] += 1
            i += 1
        code = 0
        tree_size = 512
        bits = 1
        while bits <= InflaterHuffmanTree.__max_bitlen: 
            next_code[bits] = code
            code += bl_count[bits] << ((16 - bits))
            if (bits >= 10): 
                start = next_code[bits] & 0x1ff80
                end = code & 0x1ff80
                tree_size += (((end - start)) >> ((16 - bits)))
            bits += 1
        self.__tree = Utils.newArray(tree_size, 0)
        tree_ptr = 512
        for bits in range(InflaterHuffmanTree.__max_bitlen, 9, -1):
            end = code & 0x1ff80
            code -= bl_count[bits] << ((16 - bits))
            start = code & 0x1ff80
            i = start
            while i < end: 
                self.__tree[DeflaterHuffman.bit_reverse(i)] = (((((- tree_ptr) << 4)) | bits))
                tree_ptr += 1 << ((bits - 9))
                i += 1 << 7
        i = 0
        first_pass703 = True
        while True:
            if first_pass703: first_pass703 = False
            else: i += 1
            if (not (i < len(code_lengths))): break
            bits = code_lengths[i]
            if (bits == 0): 
                continue
            code = next_code[bits]
            revcode = DeflaterHuffman.bit_reverse(code)
            if (bits <= 9): 
                first_pass = True
                while first_pass or (revcode < 512):
                    first_pass = False
                    self.__tree[revcode] = ((((i << 4)) | bits))
                    revcode += 1 << bits
            else: 
                sub_tree = self.__tree[revcode & 511]
                tree_len = 1 << ((sub_tree & 15))
                sub_tree = (- ((sub_tree >> 4)))
                first_pass = True
                while first_pass or (revcode < tree_len):
                    first_pass = False
                    self.__tree[sub_tree | ((revcode >> 9))] = ((((i << 4)) | bits))
                    revcode += 1 << bits
            next_code[bits] = (code + ((1 << ((16 - bits)))))
    
    def get_symbol(self, input0_ : 'StreamManipulator') -> int:
        lookahead = 0
        symbol = 0
        lookahead = input0_.peek_bits(9)
        if (((lookahead)) >= 0): 
            symbol = self.__tree[lookahead]
            if (((symbol)) >= 0): 
                input0_.drop_bits(symbol & 15)
                return symbol >> 4
            subtree = - ((symbol >> 4))
            bitlen = symbol & 15
            lookahead = input0_.peek_bits(bitlen)
            if (((lookahead)) >= 0): 
                symbol = (self.__tree[subtree | ((lookahead >> 9))])
                input0_.drop_bits(symbol & 15)
                return symbol >> 4
            else: 
                bits = input0_.available_bits
                lookahead = input0_.peek_bits(bits)
                symbol = (self.__tree[subtree | ((lookahead >> 9))])
                if (((symbol & 15)) <= bits): 
                    input0_.drop_bits(symbol & 15)
                    return symbol >> 4
                else: 
                    return -1
        else: 
            bits = input0_.available_bits
            lookahead = input0_.peek_bits(bits)
            symbol = (self.__tree[lookahead])
            if (symbol >= 0 and ((symbol & 15)) <= bits): 
                input0_.drop_bits(symbol & 15)
                return symbol >> 4
            else: 
                return -1
    
    # static constructor for class InflaterHuffmanTree
    @staticmethod
    def _static_ctor():
        try: 
            code_lengths = Utils.newArrayOfBytes(288, 0)
            i = 0
            while i < 144:
                code_lengths[i] = (8)
                i += 1
            while i < 256:
                code_lengths[i] = (9)
                i += 1
            while i < 280:
                code_lengths[i] = (7)
                i += 1
            while i < 288:
                code_lengths[i] = (8)
                i += 1
            InflaterHuffmanTree.DEF_LIT_LEN_TREE = InflaterHuffmanTree(code_lengths)
            code_lengths = Utils.newArrayOfBytes(32, 0)
            i = 0
            while i < 32:
                code_lengths[i] = (5)
                i += 1
            InflaterHuffmanTree.DEF_DIST_TREE = InflaterHuffmanTree(code_lengths)
        except Exception as ex: 
            pass

InflaterHuffmanTree._static_ctor()