# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class WebdingsHelper:
    
    __m_convert = None
    
    @staticmethod
    def get_unicode(code : int) -> 'char':
        res = '\x00'
        wrapres170 = RefOutArgWrapper(None)
        inoutres171 = Utils.tryGetValue(WebdingsHelper.__m_convert, code, wrapres170)
        res = wrapres170.value
        if (inoutres171): 
            return res
        else: 
            return chr(0)
    
    @staticmethod
    def get_unicode_string(str0_ : str) -> str:
        res = io.StringIO()
        for c in str0_: 
            ch = WebdingsHelper.get_unicode(ord(c))
            if (ch != (chr(0))): 
                print(ch, end="", file=res)
            else: 
                print("?", end="", file=res)
        return Utils.toStringStringIO(res)
    
    # static constructor for class WebdingsHelper
    @staticmethod
    def _static_ctor():
        WebdingsHelper.__m_convert = dict()
        data = [0x33, 9204, 0x34, 9205, 0x35, 9206, 0x36, 9207, 0x37, 9194, 0x38, 9193, 0x39, 9198, 0x3A, 9197, 0x3B, 9208, 0x3C, 9209, 0x3D, 9210, 0x60, 11156, 0x61, 10004, 0x63, 9633, 0x67, 9632, 0x6E, 9899, 0x73, 10067, 0x77, 9971, 0x79, 8854, 0x7C, 124, 0x87, 9975, 0x98, 10031, 0xD9, 9729, 0xE8, 9413, 0xE9, 9855]
        i = 0
        while i < (len(data) - 1): 
            if (data[i] < 0xFFFF): 
                if (not data[i] in WebdingsHelper.__m_convert): 
                    cod = data[i + 1] & 0xFFFF
                    WebdingsHelper.__m_convert[data[i]] = chr(cod)
            i += 2

WebdingsHelper._static_ctor()