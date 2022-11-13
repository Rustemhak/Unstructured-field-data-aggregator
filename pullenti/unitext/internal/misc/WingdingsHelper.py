# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class WingdingsHelper:
    
    __m_convert = None
    
    @staticmethod
    def get_unicode(code : int) -> 'char':
        res = '\x00'
        wrapres172 = RefOutArgWrapper(None)
        inoutres173 = Utils.tryGetValue(WingdingsHelper.__m_convert, code, wrapres172)
        res = wrapres172.value
        if (inoutres173): 
            return res
        else: 
            return chr(0)
    
    @staticmethod
    def get_unicode_string(str0_ : str) -> str:
        res = io.StringIO()
        for c in str0_: 
            ch = WingdingsHelper.get_unicode(ord(c))
            if (ch != (chr(0))): 
                print(ch, end="", file=res)
            else: 
                print("?", end="", file=res)
        return Utils.toStringStringIO(res)
    
    # static constructor for class WingdingsHelper
    @staticmethod
    def _static_ctor():
        WingdingsHelper.__m_convert = dict()
        data = [0x21, 128393, 0x22, 9986, 0x23, 9985, 0x24, 128083, 0x25, 128365, 0x26, 128366, 0x27, 128367, 0x28, 128383, 0x29, 9990, 0x2A, 128386, 0x2B, 128387, 0x2C, 128234, 0x2D, 128235, 0x2E, 128236, 0x2F, 128237, 0x30, 128193, 0x31, 128194, 0x32, 128196, 0x33, 128463, 0x34, 128464, 0x35, 128452, 0x36, 8987, 0x37, 128430, 0x38, 128432, 0x39, 128434, 0x3A, 128435, 0x3B, 128436, 0x3C, 128427, 0x3D, 128428, 0x3E, 9991, 0x3F, 9997, 0x40, 128398, 0x41, 9996, 0x42, 128076, 0x43, 128077, 0x44, 128078, 0x45, 9756, 0x46, 9758, 0x47, 9757, 0x48, 9759, 0x49, 128400, 0x4A, 9786, 0x4B, 128528, 0x4C, 9785, 0x4D, 128163, 0x4E, 9760, 0x4F, 127987, 0x50, 127985, 0x51, 9992, 0x52, 9788, 0x53, 128167, 0x54, 10052, 0x55, 128326, 0x56, 10014, 0x57, 128328, 0x58, 10016, 0x59, 10017, 0x5A, 9770, 0x5B, 9775, 0x5C, 2384, 0x5D, 9784, 0x5E, 9800, 0x5F, 9801, 0x60, 9802, 0x61, 9803, 0x62, 9804, 0x63, 9805, 0x64, 9806, 0x65, 9807, 0x66, 9808, 0x67, 9809, 0x68, 9810, 0x69, 9811, 0x6A, 128624, 0x6B, 128629, 0x6C, 9679, 0x6D, 128318, 0x6E, 9632, 0x6F, 9633, 0x70, 128912, 0x71, 10065, 0x72, 10066, 0x73, 11047, 0x74, 10731, 0x75, 9670, 0x76, 10070, 0x77, 11045, 0x78, 8999, 0x79, 11193, 0x7A, 8984, 0x7B, 127989, 0x7C, 127990, 0x7D, 128630, 0x7E, 128631, 0x80, 9450, 0x81, 9312, 0x82, 9313, 0x83, 9314, 0x84, 9315, 0x85, 9316, 0x86, 9317, 0x87, 9318, 0x88, 9319, 0x89, 9320, 0x8A, 9321, 0x8B, 9471, 0x8C, 10102, 0x8D, 10103, 0x8E, 10104, 0x8F, 10105, 0x90, 10106, 0x91, 10107, 0x92, 10108, 0x93, 10109, 0x94, 10110, 0x95, 10111, 0x96, 128610, 0x97, 128608, 0x98, 128609, 0x99, 128611, 0x9A, 128606, 0x9B, 128604, 0x9B, 128605, 0x9B, 128607, 0x9E, 183, 0x9F, 8226, 0xA0, 9642, 0xA1, 9898, 0xA2, 128902, 0xA3, 128904, 0xA4, 9673, 0xA5, 9678, 0xA6, 128319, 0xA7, 9642, 0xA8, 9723, 0xA9, 128962, 0xAA, 10022, 0xAB, 9733, 0xAC, 10038, 0xAD, 10036, 0xAE, 10041, 0xAF, 10037, 0xB0, 11216, 0xB1, 8982, 0xB2, 10209, 0xB3, 8977, 0xB4, 11217, 0xB5, 10026, 0xB6, 10032, 0xB7, 128336, 0xB8, 128337, 0xB9, 128338, 0xBA, 128339, 0xBB, 128340, 0xBC, 128341, 0xBD, 128342, 0xBE, 128343, 0xBF, 128344, 0xC0, 128345, 0xC1, 128346, 0xC2, 128347, 0xC3, 11184, 0xC4, 11185, 0xC5, 11186, 0xC6, 11187, 0xC7, 11188, 0xC8, 11189, 0xC9, 11190, 0xCA, 11191, 0xCB, 128618, 0xCB, 128619, 0xCD, 128597, 0xCE, 128596, 0xCF, 128599, 0xD0, 128598, 0xD1, 128592, 0xD2, 128593, 0xD3, 128594, 0xD4, 128595, 0xD5, 9003, 0xD6, 8998, 0xD7, 11160, 0xD8, 11162, 0xD9, 11161, 0xDA, 11163, 0xDB, 11144, 0xDC, 11146, 0xDD, 11145, 0xDE, 11147, 0xDF, 129128, 0xE0, 129130, 0xE1, 129129, 0xE2, 129131, 0xE3, 129132, 0xE4, 129133, 0xE5, 129135, 0xE6, 129134, 0xE7, 129144, 0xE8, 129146, 0xE9, 129145, 0xEA, 129147, 0xEB, 129148, 0xEC, 129149, 0xED, 129151, 0xEE, 129150, 0xEF, 8678, 0xF0, 8680, 0xF1, 8679, 0xF2, 8681, 0xF3, 11012, 0xF4, 8691, 0xF5, 11008, 0xF6, 11009, 0xF7, 11011, 0xF8, 11010, 0xF9, 129196, 0xFA, 129197, 0xFB, 128502, 0xFC, 10004, 0xFD, 128503, 0xFE, 128505]
        i = 0
        while i < (len(data) - 1): 
            if (data[i] < 0xFFFF): 
                if (not data[i] in WingdingsHelper.__m_convert): 
                    cod = data[i + 1] & 0xFFFF
                    WingdingsHelper.__m_convert[data[i]] = chr(cod)
            i += 2

WingdingsHelper._static_ctor()