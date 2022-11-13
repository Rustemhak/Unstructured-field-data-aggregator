# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class EncodingStandard(IntEnum):
    """ Подерживаемые стандартные кодировки для EncodingWrapper. Введены, чтобы избежать зависимости от
    платформы и языка программирования.
    Подерживаемые стандартные кодировки
    """
    UNDEFINED = 0
    """ Неизвестная """
    ACSII = 1
    """ Ascii """
    UTF8 = 2
    """ Utf-8, может быть префикс EF BB BF. """
    UTF16LE = 3
    """ Utf-16, двухбайтовая, младший байт первый. Может быть префикс FF FE. """
    UTF16BE = 4
    """ Utf-16, двухбайтовая, старшый байт первый (BigEndianUnicode). Может быть префикс FE FF. """
    CP1251 = 5
    """ Windows-1251 """
    CP1252 = 6
    """ Windows-1252 """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)