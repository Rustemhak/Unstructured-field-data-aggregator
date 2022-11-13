# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.MiscHelper import MiscHelper
from pullenti.util.EncodingStandard import EncodingStandard

class EncodingWrapper:
    """ Реализация кодировщика строк, замена системного Encoding.
    Введена из-за того, что в .NET Core не поддержаны разные 1251 и пр.
    Да и для кросспрограммности и кроссплатформенности это необходимо.
    Кодировщик строк
    """
    
    def __init__(self, typ : 'EncodingStandard', str0_ : str=None, cp : int=0) -> None:
        """ Создать обёртку
        
        Args:
            typ(EncodingStandard): Стандартная кодировка, для которой есть собственная реализация
            str0_(str): Строковое название, например, windows-1251, utf-8 и пр.
            cp(int): Кодовая страница Windows, например, 1251
        """
        self.std_typ = EncodingStandard.UNDEFINED
        self.code_page = 0
        self.code_page = cp
        self.std_typ = typ
        if (cp == 1251): 
            self.std_typ = EncodingStandard.CP1251
        elif (cp == 1252): 
            self.std_typ = EncodingStandard.CP1252
        if (Utils.isNullOrEmpty(str0_)): 
            return
        ss = str0_.replace("-", "").upper()
        if (ss.endswith("ASCII")): 
            self.std_typ = EncodingStandard.ACSII
            return
        if (ss.startswith("WINDOWS")): 
            cod = 0
            wrapcod590 = RefOutArgWrapper(0)
            inoutres591 = Utils.tryParseInt(ss[7:], wrapcod590)
            cod = wrapcod590.value
            if (inoutres591): 
                self.code_page = cod
                if (cod == 1251): 
                    self.std_typ = EncodingStandard.CP1251
                elif (cod == 1252): 
                    self.std_typ = EncodingStandard.CP1252
                return
        if (ss.startswith("CP")): 
            cod = 0
            wrapcod592 = RefOutArgWrapper(0)
            inoutres593 = Utils.tryParseInt(ss[2:], wrapcod592)
            cod = wrapcod592.value
            if (inoutres593): 
                self.code_page = cod
                if (cod == 1251): 
                    self.std_typ = EncodingStandard.CP1251
                elif (cod == 1252): 
                    self.std_typ = EncodingStandard.CP1252
                return
        if (ss == "UTF8"): 
            self.std_typ = EncodingStandard.UTF8
            return
        if (ss == "UNICODE" or ss == "UTF16" or ss == "UTF16LE"): 
            self.std_typ = EncodingStandard.UTF16LE
            return
        if (ss == "UTF16BE"): 
            self.std_typ = EncodingStandard.UTF16BE
            return
    
    def __str__(self) -> str:
        if (self.std_typ != EncodingStandard.UNDEFINED): 
            return Utils.enumToString(self.std_typ)
        if (self.code_page > 0): 
            return "CodePage={0}".format(self.code_page)
        return "?"
    
    def get_bytes(self, str0_ : str) -> bytearray:
        """ Закодировать строку
        
        Args:
            str0_(str): кодируемая строка
        
        Returns:
            bytearray: массив файт
        """
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        if (self.std_typ == EncodingStandard.ACSII): 
            return MiscHelper.encode_string_ascii(str0_)
        if (self.std_typ == EncodingStandard.UTF8): 
            return MiscHelper.encode_string_utf8(str0_, False)
        if (self.std_typ == EncodingStandard.CP1251): 
            return MiscHelper.encode_string1251(str0_)
        if (self.std_typ == EncodingStandard.CP1252): 
            return MiscHelper.encode_string1252(str0_)
        if (self.std_typ == EncodingStandard.UTF16LE): 
            return MiscHelper.encode_string_unicode(str0_)
        if (self.std_typ == EncodingStandard.UTF16BE): 
            return MiscHelper.encode_string_unicodebe(str0_)
        return MiscHelper.encode_string1252(str0_)
    
    def get_string(self, dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Раскодировать строку
        
        Args:
            dat(bytearray): массив байт
            len0_(int): начальная позиция в массиве
            pos(int): длина
        
        """
        if (dat is None or (pos < 0)): 
            return None
        if (len(dat) == 0): 
            return ""
        if (len0_ < 0): 
            len0_ = (len(dat) - pos)
        if (self.std_typ == EncodingStandard.ACSII): 
            return MiscHelper.decode_string_ascii(dat, pos, len0_)
        if (self.std_typ == EncodingStandard.UTF8): 
            return MiscHelper.decode_string_utf8(dat, pos, len0_)
        if (self.std_typ == EncodingStandard.CP1251): 
            return MiscHelper.decode_string1251(dat, pos, len0_)
        if (self.std_typ == EncodingStandard.CP1252): 
            return MiscHelper.decode_string1252(dat, pos, len0_)
        if (self.std_typ == EncodingStandard.UTF16LE): 
            return MiscHelper.decode_string_unicode(dat, pos, len0_)
        if (self.std_typ == EncodingStandard.UTF16BE): 
            return MiscHelper.decode_string_unicodebe(dat, pos, len0_)
        return MiscHelper.decode_string1252(dat, pos, len0_)
    
    @staticmethod
    def check_encoding(data : bytearray, head_len : int) -> 'EncodingWrapper':
        """ Определение кодировки по байтовому массиву
        
        Args:
            data(bytearray): кодированный массив
            head_len(int): размер префикса, если он есть
        
        Returns:
            EncodingWrapper: результирующая кодировка
        """
        head_len.value = 0
        if ((len(data) >= 3 and data[0] == (0xEF) and data[1] == (0xBB)) and data[2] == (0xBF)): 
            if (len(data) == 3): 
                return None
            head_len.value = 3
            return EncodingWrapper(EncodingStandard.UTF8)
        if (len(data) >= 2 and data[0] == (0xFF) and data[1] == (0xFE)): 
            if (len(data) == 2): 
                return None
            head_len.value = 2
            return EncodingWrapper(EncodingStandard.UTF16LE)
        if (len(data) >= 2 and data[0] == (0xFE) and data[1] == (0xFF)): 
            if (len(data) == 2): 
                return None
            head_len.value = 2
            return EncodingWrapper(EncodingStandard.UTF16BE)
        i = 0
        j = 0
        dos = 0
        win = 0
        utf8 = 0
        d0 = 0
        rus = 0
        i = 0
        first_pass726 = True
        while True:
            if first_pass726: first_pass726 = False
            else: i += 1
            if (not (i < len(data))): break
            j = (data[i])
            if (j == 0xE2 and ((i + 2) < len(data))): 
                if (data[i + 1] == (0x80) and data[i + 2] == (0x99)): 
                    utf8 += 1
                    i += 2
                    continue
            if (j >= 0xC0): 
                win += 1
            if ((j >= 0x80 and j <= 0xAF)): 
                dos += 1
            elif (j >= 0xE0 and j <= 0xEF): 
                dos += 1
            if (j >= 0x80): 
                rus += 1
                if (j == 0xD0 or j == 0xD1): 
                    d0 += 1
        if (dos > win and utf8 == 0): 
            data2 = Utils.newArrayOfBytes(len(data), 0)
            i = 0
            while i < len(data): 
                data2[i] = data[i]
                j = (data[i])
                if (j >= 0xE0 and j <= 0xEF): 
                    j -= 0x30
                if (j >= 0x80 and j <= 0xDF): 
                    data2[i] = ((j + 0x40))
                if (j == 0xF1): 
                    data2[i] = (0xB8)
                if (j == 0xF0): 
                    data2[i] = (0xA8)
                i += 1
            data = data2
        enc = None
        txt = None
        if (d0 > ((math.floor(rus / 5))) or utf8 > 0): 
            try: 
                txt = MiscHelper.decode_string_utf8(data, 0, -1)
                enc = EncodingWrapper(EncodingStandard.UTF8)
                if (utf8 > 0): 
                    return enc
            except Exception as ex594: 
                pass
        if (txt is None or enc is None): 
            return EncodingWrapper(EncodingStandard.CP1251)
        try: 
            txt2 = MiscHelper.decode_string1251(data, 0, -1)
            ru = 0
            ru2 = 0
            for ch in txt: 
                if ((ord(ch)) >= 0x400 and ((ord(ch)) < 0x500)): 
                    if (str.isalpha(ch)): 
                        ru += 1
            for ch in txt2: 
                if ((ord(ch)) >= 0x400 and ((ord(ch)) < 0x500)): 
                    if (str.isalpha(ch)): 
                        ru2 += 1
            if (ru2 > ((ru * 2))): 
                return EncodingWrapper(EncodingStandard.CP1251)
            return enc
        except Exception as ex: 
            pass
        return EncodingWrapper(EncodingStandard.UTF8)