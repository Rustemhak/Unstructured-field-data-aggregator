# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import io
from pullenti.unisharp.Utils import Utils

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextService import UnitextService
from pullenti.unitext.internal.word.CompoundFileSystem import CompoundFileSystem
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.UnitextDocument import UnitextDocument

class MSOfficeHelper:
    
    @staticmethod
    def check_extension(file_name : str) -> bool:
        ext = pathlib.PurePath(file_name).suffix.upper()
        return (ext == ".DOC" or ext == ".DOCX" or ext == ".PPTX") or ext == ".XLSX"
    
    @staticmethod
    def __uni_from_word97(cf : 'CompoundFileSystem') -> 'UnitextDocument':
        from pullenti.unitext.internal.word.WordDocument import WordDocument
        word_ = WordDocument()
        doc = UnitextDocument._new41(FileFormat.DOC)
        word_.load(cf, doc)
        return doc
    
    @staticmethod
    def _uni_from_word97arr(data : bytearray) -> 'UnitextDocument':
        if (len(data) > 0x300 and data[0] == (0xD0) and data[1] == (0xCF)): 
            i0 = 0x50
            while i0 < len(data): 
                if (data[i0] != (0xFF)): 
                    break
                i0 += 1
            if ((i0 + 0x200) <= len(data) and data[i0 + 1] == (0xA5)): 
                buf = Utils.newArrayOfBytes(len(data) - i0, 0)
                i = 0
                while i < len(buf): 
                    buf[i] = data[i0 + i]
                    i += 1
                doc = MSOfficeHelper._uni_from_word6or_early(buf)
                if (doc is not None): 
                    doc.source_format = FileFormat.DOC
                    doc.attrs["word"] = "6"
                return doc
        with CompoundFileSystem(None, data) as cf: 
            return MSOfficeHelper.__uni_from_word97(cf)
    
    @staticmethod
    def _uni_from_word6or_early(buf : bytearray) -> 'UnitextDocument':
        pos0 = int.from_bytes(buf[0x18:0x18+4], byteorder="little")
        pos1 = int.from_bytes(buf[0x1C:0x1C+4], byteorder="little")
        if (pos1 <= len(buf) and pos0 >= 0x20 and pos1 > pos0): 
            pass
        else: 
            return None
        v0 = 0
        v1 = 0
        i = pos0
        while i < pos1: 
            if (buf[i] == (0) or buf[i] == (4)): 
                if (((((i - pos0)) & 1)) == 0): 
                    v1 += 1
                else: 
                    v0 += 1
            i += 1
        str0_ = None
        if (v0 > (v1 * 3)): 
            str0_ = MiscHelper.decode_string_unicode(buf, pos0, pos1 - pos0)
        else: 
            str0_ = MiscHelper.decode_string1251(buf, pos0, pos1 - pos0)
        ddd = UnitextService.create_document_from_text(str0_)
        return ddd
    
    @staticmethod
    def _uni_from_word97file(file_name : str) -> 'UnitextDocument':
        with CompoundFileSystem(file_name, None) as cf: 
            return MSOfficeHelper.__uni_from_word97(cf)
    
    @staticmethod
    def __correct_content(txt : io.StringIO) -> str:
        res = io.StringIO()
        off = 0
        lf = 0
        off_tmp = io.StringIO()
        j = 0
        first_pass692 = True
        while True:
            if first_pass692: first_pass692 = False
            else: j += 1
            if (not (j < txt.tell())): break
            ch = Utils.getCharAtStringIO(txt, j)
            if (ch == ':'): 
                pass
            if ((ord(ch)) == 127): 
                ch = ' '
            if (off > 0): 
                if ((ord(ch)) == 0x15): 
                    off -= 1
                    if (off == 0): 
                        ttt = MSOfficeHelper._extract_spec_text(Utils.toStringStringIO(off_tmp).strip())
                        if (ttt is not None): 
                            print(ttt, end="", file=res)
                        Utils.setLengthStringIO(off_tmp, 0)
                    else: 
                        print(ch, end="", file=off_tmp)
                else: 
                    print(ch, end="", file=off_tmp)
                    if ((ord(ch)) == 0x13): 
                        off += 1
                continue
            if ((ord(ch)) == 0x13): 
                if (off == 0): 
                    Utils.setLengthStringIO(off_tmp, 0)
                off += 1
            elif ((ord(ch)) == 0xD or ch == '\v'): 
                print("\r\n", end="", file=res)
                lf += 1
            elif ((ord(ch)) == 0xC): 
                print("\r\n\r\n\r\n", end="", file=res)
                lf += 3
            elif (Utils.isWhitespace(ch) or (ord(ch)) > 0x20 or (ord(ch)) == 7): 
                if (ch == '\n'): 
                    if (res.tell() == 0 or Utils.getCharAtStringIO(res, res.tell() - 1) != '\r'): 
                        print('\r', end="", file=res)
                print(ch, end="", file=res)
                if (not Utils.isWhitespace(ch)): 
                    lf = 0
            elif ((ord(ch)) == 3 or (ord(ch)) == 4): 
                break
            else: 
                pass
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _extract_spec_text(txt : str) -> str:
        txt = Utils.trimStartString(txt)
        if (txt.startswith("HYPERLINK")): 
            i1 = txt.find("PAGEREF")
            if (i1 > 0): 
                for ii in range(i1 - 1, -1, -1):
                    if ((ord(txt[ii])) == 0x14 or (ord(txt[ii])) == 0x1): 
                        txt = txt[ii + 1:ii + 1+i1 - ii - 1].strip()
                        return txt + "\n"
            i = txt.rfind(chr(0x14))
            if (i < 0): 
                i = txt.rfind(chr(0x1))
            if (i > 0 and (i < len(txt))): 
                txt = txt[i + 1:]
                return txt
            return None
        if (txt.startswith("TOC")): 
            ii = txt.find("HYPERLINK")
            if (ii > 0): 
                return MSOfficeHelper._extract_spec_text(txt[ii:])
            res = io.StringIO()
            treg = False
            for ch in txt: 
                if ((ord(ch)) == 0x14 or (ord(ch)) == 0x15): 
                    treg = True
                elif ((ord(ch)) == 0x13): 
                    treg = False
                elif (treg): 
                    if ((ord(ch)) == 0xD): 
                        print("\r\n", end="", file=res)
                    elif (ch == '\v' or (ord(ch)) == 7): 
                        print("  ", end="", file=res)
                    else: 
                        print(ch, end="", file=res)
            return Utils.toStringStringIO(res)
        return None