# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math

class DeflaterConstants:
    # This class contains constants used for deflation.
    
    DEBUGGING = False
    
    STORED_BLOCK = 0
    
    STATIC_TREES = 1
    
    DYN_TREES = 2
    
    PRESET_DICT = 0x20
    
    DEFAULT_MEM_LEVEL = 8
    
    MAX_MATCH = 258
    
    MIN_MATCH = 3
    
    MAX_WBITS = 15
    
    WSIZE = 1 << MAX_WBITS
    
    WMASK = WSIZE - 1
    
    HASH_BITS = DEFAULT_MEM_LEVEL + 7
    
    HASH_SIZE = 1 << HASH_BITS
    
    HASH_MASK = HASH_SIZE - 1
    
    HASH_SHIFT = math.floor((((HASH_BITS + MIN_MATCH) - 1)) / MIN_MATCH)
    
    MIN_LOOKAHEAD = MAX_MATCH + MIN_MATCH + 1
    
    MAX_DIST = WSIZE - MIN_LOOKAHEAD
    
    PENDING_BUF_SIZE = 1 << ((DEFAULT_MEM_LEVEL + 8))
    
    MAX_BLOCK_SIZE = min(65535, PENDING_BUF_SIZE - 5)
    
    DEFLATE_STORED = 0
    
    DEFLATE_FAST = 1
    
    DEFLATE_SLOW = 2
    
    GOOD_LENGTH = None
    
    MAX_LAZY = None
    
    NICE_LENGTH = None
    
    MAX_CHAIN = None
    
    COMPR_FUNC = None
    
    # static constructor for class DeflaterConstants
    @staticmethod
    def _static_ctor():
        DeflaterConstants.GOOD_LENGTH = [0, 4, 4, 4, 4, 8, 8, 8, 32, 32]
        DeflaterConstants.MAX_LAZY = [0, 4, 5, 6, 4, 16, 16, 32, 128, 258]
        DeflaterConstants.NICE_LENGTH = [0, 8, 16, 32, 16, 32, 128, 128, 258, 258]
        DeflaterConstants.MAX_CHAIN = [0, 4, 8, 32, 16, 32, 128, 256, 1024, 4096]
        DeflaterConstants.COMPR_FUNC = [0, 1, 1, 1, 1, 2, 2, 2, 2, 2]

DeflaterConstants._static_ctor()