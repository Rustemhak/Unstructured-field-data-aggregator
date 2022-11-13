# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.FileFormatClass import FileFormatClass
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.FileFormat import FileFormat

class FileFormatsHelper:
    """ Хелпер работы с форматами файлов """
    
    @staticmethod
    def analize_format(file_ext : str, file_context : bytearray) -> 'FileFormat':
        """ Проанализировать формат файла по расширению и небольшому начальному фрагменту
        
        Args:
            file_ext(str): расширение файла (может быть null)
            file_context(bytearray): начальный фрагмент файла (может быть null), но можно и весь файл целиком, если он уже в памяти.
        
        Returns:
            FileFormat: формат
        """
        from pullenti.util.TextHelper import TextHelper
        if (file_ext is not None): 
            file_ext = file_ext.lower()
            if (not file_ext.startswith(".")): 
                file_ext = ("." + file_ext)
        if (file_context is not None and len(file_context) > 6): 
            if (file_context[0] == (0xD0) and file_context[1] == (0xCF)): 
                if ((file_ext == ".doc" or file_ext == ".docx" or file_ext == ".rtf") or file_ext == ".txt" or file_ext == ".dot"): 
                    return FileFormat.DOC
                if (file_ext == ".xls" or file_ext == ".xlsx"): 
                    return FileFormat.XLS
                if (file_ext == ".msg"): 
                    return FileFormat.MSG
                if (file_ext is None or file_ext == "."): 
                    return FileFormat.DOC
            if (((chr(file_context[0])) == '0' and (chr(file_context[1])) == 'M' and (chr(file_context[2])) == '8') and (chr(file_context[3])) == 'R'): 
                if (file_ext == ".msg"): 
                    return FileFormat.MSG
            if (file_context[0] == (1) and file_context[1] == (0) and len(file_context) > 0x30): 
                if (((chr(file_context[0x28])) == ' ' and (chr(file_context[0x29])) == 'E' and (chr(file_context[0x2A])) == 'M') and (chr(file_context[0x2B])) == 'F'): 
                    return FileFormat.EMF
            if (file_context[0] == (0x50) and file_context[1] == (0x4B)): 
                if ((file_ext == ".doc" or file_ext == ".docx" or file_ext == ".rtf") or file_ext == ".dotm"): 
                    return FileFormat.DOCX
                elif (file_ext == ".pptx"): 
                    return FileFormat.PPTX
                elif (file_ext == ".vsdx"): 
                    return FileFormat.UNKNOWN
                elif (file_ext == ".xls" or file_ext == ".xlsx" or file_ext == ".xlsb"): 
                    return FileFormat.XLSX
                elif (file_ext == ".odt"): 
                    return FileFormat.ODT
                elif (file_ext == ".ods"): 
                    return FileFormat.ODS
                elif (file_ext == ".epub"): 
                    return FileFormat.EPUB
                elif (file_ext == ".fb3"): 
                    return FileFormat.FB3
                elif (file_ext == ".xps"): 
                    return FileFormat.XPS
                else: 
                    for k in range(3):
                        tag = ("[Content_Types].xml" if k == 0 else ("word/document.xml" if k == 1 else "word/"))
                        i = 0
                        while i < (len(file_context) - len(tag)): 
                            j = 0
                            j = 0
                            while j < len(tag): 
                                if (file_context[i + j] != (ord(tag[j]))): 
                                    break
                                j += 1
                            if (j >= len(tag)): 
                                return FileFormat.DOCX
                            i += 1
                    odt_tag = "oasis.opendocument.text"
                    i = 0
                    while i < (len(file_context) - len(odt_tag)): 
                        j = 0
                        j = 0
                        while j < len(odt_tag): 
                            if (file_context[i + j] != (ord(odt_tag[j]))): 
                                break
                            j += 1
                        if (j >= len(odt_tag)): 
                            return FileFormat.ODT
                        i += 1
                    return FileFormat.ZIP
            if (file_context[0] == (0x52) and file_context[1] == (0x61) and file_context[2] == (0x72)): 
                return FileFormat.RAR
            if (file_context[0] == (0x37) and file_context[1] == (0x7A) and file_context[2] == (0xDC)): 
                return FileFormat.ZIP7
            if ((file_context[0] == (0x25) and file_context[1] == (0x50) and file_context[2] == (0x44)) and file_context[3] == (0x46) and file_context[4] == (0x2D)): 
                return FileFormat.PDF
            if ((file_context[0] == (0x7B) and file_context[1] == (0x5C) and file_context[2] == (0x72)) and file_context[3] == (0x74) and file_context[4] == (0x66)): 
                return FileFormat.RTF
            if ((chr(file_context[0])) == 'B' and (chr(file_context[1])) == 'M'): 
                if (file_ext == ".bmp" or file_ext == "." or file_ext is None): 
                    return FileFormat.BMP
            if ((chr(file_context[0])) == 'I' and (chr(file_context[1])) == 'I'): 
                if ((file_ext == ".tif" or file_ext == ".tiff" or file_ext == ".") or file_ext is None): 
                    return FileFormat.TIF
            if ((chr(file_context[1])) == 'P' and (chr(file_context[2])) == 'N' and (chr(file_context[3])) == 'G'): 
                if (file_ext == ".png" or file_ext == "." or file_ext is None): 
                    return FileFormat.PNG
            if ((chr(file_context[0])) == 'G' and (chr(file_context[1])) == 'I' and (chr(file_context[2])) == 'F'): 
                if (file_ext == ".gif" or file_ext == "." or file_ext is None): 
                    return FileFormat.GIF
            if ((len(file_context) > 20 and (chr(file_context[6])) == 'J' and (chr(file_context[7])) == 'F') and (chr(file_context[8])) == 'I'): 
                if ((file_ext == ".jpg" or file_ext == ".jpeg" or file_ext == ".") or file_ext is None): 
                    return FileFormat.JPG
            if (((len(file_context) > 10 and file_context[0] == (0) and file_context[1] == (0)) and file_context[2] == (0) and file_context[3] == (0xC)) and file_context[4] == (0x6A) and file_context[5] == (0x50)): 
                return FileFormat.JPG2000
            enc = MiscHelper.decode_string_ascii(file_context, 0, (len(file_context) if len(file_context) < 1000 else 1000))
            if (file_context[0] == (0xEF) and file_context[1] == (0xBB) and file_context[2] == (0xBF)): 
                enc = enc[3:]
            enc = enc.upper().strip()
            if (enc.startswith("<HTML") or enc.startswith("<!DOCTYPE HTML") or enc.startswith("<DIV>")): 
                return FileFormat.HTML
            if (enc.startswith("AT&TFORM")): 
                return FileFormat.DJVU
            if (Utils.startsWithString(enc, "<?xml", True)): 
                if ("<FUNCTIONBOOK" in enc or "<FICTIONBOOK" in enc): 
                    return FileFormat.FB2
                if ("<WORKBOOK " in enc or "<?mso-application progid=\"Excel.Sheet\"".upper() in enc): 
                    return FileFormat.XLSXML
                if ("<?mso-application progid=\"Word.Document\"".upper() in enc): 
                    return FileFormat.DOCXML
                if ("<HTML" in enc): 
                    return FileFormat.HTML
            if ((enc.startswith("DELIVERED-TO:") or enc.startswith("RECEIVED:") or enc.startswith("RECEIVED-FROM:")) or enc.startswith("DELIVERED:")): 
                return FileFormat.EML
            ii = enc.find("CONTENT-TYPE:")
            if (ii > 0): 
                if (file_ext == ".eml"): 
                    return FileFormat.EML
                if (enc.find("MULTIPART/RELATED") > ii): 
                    return FileFormat.MHT
            if (file_context[0] == (0xFF) and file_context[1] == (0xFE)): 
                txt = MiscHelper.decode_string_unicode(file_context, 0, -1)
                if ("<htm" in txt): 
                    return FileFormat.HTML
                return FileFormat.TXT
            if (file_context[0] == (0xFE) and file_context[1] == (0xFF)): 
                txt = MiscHelper.decode_string_unicodebe(file_context, 0, -1)
                if ("<htm" in txt): 
                    return FileFormat.HTML
                return FileFormat.TXT
            if (Utils.startsWithString(enc, "<?xml", True)): 
                return FileFormat.XML
            if (file_ext == "."): 
                txt = TextHelper.read_string_from_bytes(file_context, False)
                if (txt is not None): 
                    return FileFormat.TXT
        else: 
            if (file_ext == ".doc" or file_ext == ".dot"): 
                return FileFormat.DOC
            if (file_ext == ".odt"): 
                return FileFormat.ODT
            if (file_ext == ".docx" or file_ext == ".dotx"): 
                return FileFormat.DOCX
            if (file_ext == ".pptx"): 
                return FileFormat.PPTX
            if (file_ext == ".zip"): 
                return FileFormat.ZIP
            if (file_ext == ".rar"): 
                return FileFormat.RAR
            if (file_ext == ".xlsx" or file_ext == ".xlsb"): 
                return FileFormat.XLSX
            if (file_ext == ".xls"): 
                return FileFormat.XLS
            if (file_ext == ".msg"): 
                return FileFormat.MSG
            if (file_ext == ".eml"): 
                return FileFormat.EML
            if (file_ext == ".djvu"): 
                return FileFormat.DJVU
        if (file_ext == ".tar"): 
            return FileFormat.TAR
        if (file_ext == ".gzip" or file_ext == ".gz"): 
            return FileFormat.GZIP
        if (file_ext == ".7z"): 
            return FileFormat.ZIP7
        if (file_ext == ".xml"): 
            return FileFormat.XML
        if (file_ext == ".pdf"): 
            return FileFormat.PDF
        if (file_ext == ".djvu"): 
            return FileFormat.DJVU
        if (file_ext == ".xls"): 
            return FileFormat.XLS
        if (file_ext == ".txt"): 
            return FileFormat.TXT
        if (file_ext == ".csv"): 
            return FileFormat.CSV
        if (file_ext == ".rtf"): 
            return FileFormat.RTF
        if (file_ext == ".htm" or file_ext == ".html"): 
            return FileFormat.HTML
        if (file_ext == ".doc"): 
            return FileFormat.TXT
        if (file_ext == ".mht" or file_ext == ".mhtml"): 
            return FileFormat.MHT
        if (file_ext == ".fb2"): 
            return FileFormat.FB2
        if (file_ext == ".fb3"): 
            return FileFormat.FB3
        if (file_ext == ".epub"): 
            return FileFormat.EPUB
        if (file_ext == ".bmp"): 
            return FileFormat.BMP
        if (file_ext == ".jpg" or file_ext == ".jpeg"): 
            return FileFormat.JPG
        if (file_ext == ".jp2"): 
            return FileFormat.JPG2000
        if (file_ext == ".gif"): 
            return FileFormat.GIF
        if (file_ext == ".png"): 
            return FileFormat.PNG
        if (file_ext == ".emf"): 
            return FileFormat.EMF
        if (file_ext == ".tif" or file_ext == ".tiff"): 
            return FileFormat.TIF
        return FileFormat.UNKNOWN
    
    @staticmethod
    def get_format_class(frm : 'FileFormat') -> 'FileFormatClass':
        """ Получить класс формата. Пригодится для определения типа файла.
        
        Args:
            frm(FileFormat): формат
        
        Returns:
            FileFormatClass: класс формата
        """
        if ((frm == FileFormat.ZIP or frm == FileFormat.ZIP7 or frm == FileFormat.RAR) or frm == FileFormat.TAR or frm == FileFormat.GZIP): 
            return FileFormatClass.ARCHIVE
        if (((frm == FileFormat.BMP or frm == FileFormat.JPG or frm == FileFormat.JPG2000) or frm == FileFormat.PNG or frm == FileFormat.TIF) or frm == FileFormat.GIF or frm == FileFormat.EMF): 
            return FileFormatClass.IMAGE
        if ((((frm == FileFormat.DOC or frm == FileFormat.DOCX or frm == FileFormat.XLS) or frm == FileFormat.XLSX or frm == FileFormat.PPTX) or frm == FileFormat.RTF or frm == FileFormat.ODT) or frm == FileFormat.DOCXML or frm == FileFormat.XLSXML): 
            return FileFormatClass.OFFICE
        if (frm == FileFormat.PDF or frm == FileFormat.DJVU or frm == FileFormat.XPS): 
            return FileFormatClass.PAGELAYOUT
        return FileFormatClass.UNDEFINED
    
    @staticmethod
    def get_format_ext(frm : 'FileFormat') -> str:
        """ Получить расширение для формата
        
        Args:
            frm(FileFormat): формат
        
        Returns:
            str: расширение с точкой (null - если не знает)
        """
        if (frm == FileFormat.DOC): 
            return ".doc"
        if (frm == FileFormat.DOCX): 
            return ".docx"
        if (frm == FileFormat.DOCXML): 
            return ".doc"
        if (frm == FileFormat.PPTX): 
            return ".pptx"
        if (frm == FileFormat.HTML): 
            return ".htm"
        if (frm == FileFormat.PDF): 
            return ".pdf"
        if (frm == FileFormat.RTF): 
            return ".rtf"
        if (frm == FileFormat.TXT): 
            return ".txt"
        if (frm == FileFormat.XLS or frm == FileFormat.XLSXML): 
            return ".xls"
        if (frm == FileFormat.XLSX): 
            return ".xlsx"
        if (frm == FileFormat.EPUB): 
            return ".epub"
        if (frm == FileFormat.FB2): 
            return ".fb2"
        if (frm == FileFormat.FB3): 
            return ".fb3"
        if (frm == FileFormat.CSV): 
            return ".csv"
        if (frm == FileFormat.MSG): 
            return ".msg"
        if (frm == FileFormat.EML): 
            return ".eml"
        if (frm == FileFormat.JPG): 
            return ".jpg"
        if (frm == FileFormat.JPG2000): 
            return ".jp2"
        if (frm == FileFormat.BMP): 
            return ".bmp"
        if (frm == FileFormat.GIF): 
            return ".gif"
        if (frm == FileFormat.TIF): 
            return ".tif"
        if (frm == FileFormat.PNG): 
            return ".png"
        if (frm == FileFormat.EMF): 
            return ".emf"
        if (frm == FileFormat.XML): 
            return ".xml"
        if (frm == FileFormat.ZIP): 
            return ".zip"
        if (frm == FileFormat.RAR): 
            return ".rar"
        if (frm == FileFormat.TAR): 
            return ".tar"
        if (frm == FileFormat.GZIP): 
            return ".gz"
        if (frm == FileFormat.ZIP7): 
            return ".7z"
        if (frm == FileFormat.XPS): 
            return ".xps"
        if (frm == FileFormat.DJVU): 
            return ".djvu"
        return None
    
    @staticmethod
    def analize_file_format(file_name : str, content : bytearray=None) -> 'FileFormat':
        """ Проанализировать формат файла или байтового потока.
        
        Args:
            file_name(str): имя файла, может быть null, если есть содержимое
            content(bytearray): содержимое, может быть null, тогда файл указывает на файл локальной файловой системы
        
        """
        head = Utils.newArrayOfBytes(2048, 0)
        if (content is not None): 
            if (len(content) < 2): 
                return FileFormat.UNKNOWN
            i = 0
            while ((i < len(head)) and (i < len(content))): 
                head[i] = content[i]
                i += 1
        else: 
            if (not pathlib.Path(file_name).is_file()): 
                return FileFormat.UNKNOWN
            with FileStream(file_name, "rb") as f: 
                if (f.read(head, 0, len(head)) < 2): 
                    return FileFormat.UNKNOWN
        ext = None
        try: 
            ext = ("." if file_name is None else pathlib.PurePath(file_name).suffix)
        except Exception as ex: 
            ext = "."
        return FileFormatsHelper.analize_format(ext, head)