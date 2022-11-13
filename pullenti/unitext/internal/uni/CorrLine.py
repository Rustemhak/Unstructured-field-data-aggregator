# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.UnitextNewline import UnitextNewline

class CorrLine:
    
    def __init__(self) -> None:
        self.length = 0
        self.is_pure_text = False
        self.first_ind = 0
        self.last_ind = 0
        self.__m_text = None;
        self.new_lines = 0
        self.page_break_after = False
        self.merge = False
        self.cant_follow_any = False
        self.__m_can_be_empty_line_of_table = -1
        self.__m_can_has_hor_line_of_table = -1
    
    @property
    def text(self) -> str:
        return self.__m_text
    @text.setter
    def text(self, value) -> str:
        self.__m_text = Utils.trimEndString(value)
        self.length = len(value)
        self.__m_can_be_empty_line_of_table = -1
        self.__m_can_has_hor_line_of_table = -1
        return value
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.merge): 
            print("<-Merge ", end="", file=res)
        print("[{0}{1}]".format(self.length, (" txt" if self.is_pure_text else "")), end="", file=res, flush=True)
        if (self.page_break_after): 
            print(" PageBreak".format(), end="", file=res, flush=True)
        else: 
            print(" {0}nls".format(self.new_lines), end="", file=res, flush=True)
        if (len(self.text) < 100): 
            print(" '{0}'".format(self.text), end="", file=res, flush=True)
        else: 
            print(" '{0}...".format(self.text[0:0+100]), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def parse_list(cnt : 'UnitextContainer') -> typing.List['CorrLine']:
        res = list()
        line = None
        tmp = io.StringIO()
        i = 0
        first_pass665 = True
        while True:
            if first_pass665: first_pass665 = False
            else: i += 1
            if (not (i < len(cnt.children))): break
            ch = cnt.children[i]
            if (isinstance(ch, UnitextPagebreak)): 
                if (line is not None): 
                    line.page_break_after = True
                continue
            if (isinstance(ch, UnitextNewline)): 
                if (line is not None): 
                    if (ch.tag is not None): 
                        line.cant_follow_any = True
                    line.new_lines += ch.count
                    continue
            if (line is None or line.new_lines > 0 or line.page_break_after): 
                if (line is not None): 
                    line.text = Utils.toStringStringIO(tmp)
                    Utils.setLengthStringIO(tmp, 0)
                line = (None)
            if (line is None): 
                line = CorrLine._new319(True)
                Utils.setLengthStringIO(tmp, 0)
                res.append(line)
                line.first_ind = i
            line.last_ind = i
            if (isinstance(ch, UnitextPlaintext)): 
                print(ch.text, end="", file=tmp)
                continue
            if (isinstance(ch, UnitextFootnote)): 
                pass
            else: 
                line.is_pure_text = False
        if (line is not None): 
            line.text = Utils.toStringStringIO(tmp)
        return res
    
    @staticmethod
    def is_hiphen(ch : 'char') -> bool:
        if ((ch == '-' or ch == '–' or ch == '¬') or ch == '-'): 
            return True
        if (ch == (chr(0x00AD))): 
            return True
        if ((ch == '-' or ch == '—' or ch == '–') or ch == '−' or ch == '-'): 
            return True
        return False
    
    @staticmethod
    def is_table_char(ch : 'char') -> bool:
        if (CorrLine.is_hiphen(ch)): 
            return True
        if (ch == '|' or ch == '_'): 
            return True
        cod = ord(ch)
        if (cod >= 0x2500 and cod <= 0x2595): 
            return True
        return False
    
    def can_followed(self, li : 'CorrLine') -> bool:
        if (not li.is_pure_text or not self.is_pure_text): 
            return False
        if (self.cant_follow_any): 
            return False
        if (self.new_lines > 2): 
            return False
        if (Utils.isNullOrEmpty(self.text) or Utils.isNullOrEmpty(li.text)): 
            return False
        last_ch = self.text[len(self.text) - 1]
        first_ch = chr(0)
        ws_before = 0
        for ch in li.text: 
            if (not Utils.isWhitespace(ch)): 
                first_ch = ch
                break
            else: 
                ws_before += 1
        if ((ord(first_ch)) == 0): 
            return False
        if (ws_before > 10): 
            wsb = 0
            for ch in self.text: 
                if (not Utils.isWhitespace(ch)): 
                    break
                else: 
                    wsb += 1
            if (wsb < (math.floor((0.8 * (ws_before))))): 
                return False
        if (last_ch == '.' or last_ch == ';' or last_ch == ':'): 
            if (self.new_lines > 1 or self.page_break_after): 
                return False
            if (not str.isalpha(first_ch)): 
                return False
            if (not str.islower(first_ch)): 
                return False
            if (last_ch != '.'): 
                return False
            return True
        if (str.isalpha(first_ch)): 
            if (str.islower(first_ch)): 
                return True
        if (self.new_lines > 1 or self.page_break_after): 
            return False
        if (CorrLine.is_hiphen(last_ch) or last_ch == ','): 
            if (not str.isalnum(first_ch)): 
                return False
            return True
        if (str.isalpha(last_ch) and str.islower(last_ch)): 
            ws_before0 = 0
            for ch in self.text: 
                if (not Utils.isWhitespace(ch)): 
                    break
                else: 
                    ws_before0 += 1
            if (ws_before == ws_before0): 
                if (li.text[len(li.text) - 1] == '.'): 
                    if (str.islower(first_ch) and str.islower(first_ch)): 
                        return True
        return False
    
    @property
    def can_be_empty_line_of_table(self) -> bool:
        if (not self.is_pure_text): 
            return False
        if (self.__m_can_be_empty_line_of_table >= 0): 
            return self.__m_can_be_empty_line_of_table > 0
        cou = 0
        for ch in self.text: 
            if (CorrLine.is_table_char(ch)): 
                cou += 1
            elif (not Utils.isWhitespace(ch)): 
                self.__m_can_be_empty_line_of_table = 0
                return False
        self.__m_can_be_empty_line_of_table = (1 if cou > 1 else 0)
        return self.__m_can_be_empty_line_of_table > 0
    
    @property
    def can_has_hor_line_of_table(self) -> bool:
        if (not self.is_pure_text): 
            return False
        if (self.__m_can_has_hor_line_of_table >= 0): 
            return self.__m_can_has_hor_line_of_table > 0
        i = 0
        while i < (len(self.text) - 2): 
            if (CorrLine.is_table_char(self.text[i]) and self.text[i + 1] == self.text[i] and self.text[i + 2] == self.text[i]): 
                self.__m_can_has_hor_line_of_table = 1
                return True
            i += 1
        self.__m_can_has_hor_line_of_table = 0
        return False
    
    @staticmethod
    def _new319(_arg1 : bool) -> 'CorrLine':
        res = CorrLine()
        res.is_pure_text = _arg1
        return res