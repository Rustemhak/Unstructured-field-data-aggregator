# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class FileFormat(IntEnum):
    """ Формат файла """
    UNKNOWN = 0
    """ Неизвестный формат """
    DOC = 1
    """ Двоичный формат документа MsWord """
    DOCX = 2
    """ Открытый формат документа MsWord """
    DOCXML = 3
    """ Специфический формат документа MsWord в Xml """
    PPTX = 4
    """ Открытый формат MsPowerPoint """
    PDF = 5
    """ Portable Document Format (Adobe) """
    TXT = 6
    """ Текстовой файл в разных кодировках """
    HTML = 7
    """ Hypertext Markup Language """
    MHT = 8
    """ Mime HtmFile """
    RTF = 9
    """ Rich Text Format """
    XLS = 10
    """ Двоичный формат таблицы MsExcel """
    XLSX = 11
    """ Открытый формат таблицы MsExcel """
    XLSXML = 12
    """ Специфический формат таблицы MsExcel в Xml """
    CSV = 13
    """ Comma-Separated Values, текстовое представление таблицы """
    ODT = 14
    """ OpenOffice Document """
    ODS = 15
    """ OpenOffice Spreadsheet """
    DJVU = 16
    """ Дежавю-формат """
    FB2 = 17
    """ FictionBook (FeedBook) версии 2 """
    FB3 = 18
    """ FictionBook (FeedBook) версии 3 """
    EPUB = 19
    """ Electronic Publication """
    MSG = 20
    """ Письмо формата MsOutlook """
    EML = 21
    """ Почтовый формат """
    ZIP = 22
    """ Zip-архив """
    RAR = 23
    """ Rar-архив """
    TAR = 24
    """ Tar-архив """
    GZIP = 25
    """ Gzip-архив """
    ZIP7 = 26
    """ Zip7-архив """
    BMP = 27
    """ Картинка Bmp """
    JPG = 28
    """ Картинка Jpeg """
    JPG2000 = 29
    """ Картинка Jpeg2000 """
    TIF = 30
    """ Картинка Tiff """
    PNG = 31
    """ Картинка Pgn """
    GIF = 32
    """ Картинка Gif """
    EMF = 33
    """ Картинка Enhanced Windows Metafile """
    XML = 34
    """ Xml-формат """
    XPS = 35
    """ XML Paper Specification File """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)