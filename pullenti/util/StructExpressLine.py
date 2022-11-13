# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class StructExpressLine:
    
    def __init__(self) -> None:
        self.begin_char = 0
        self.end_char = 0
        self.text = None;
        self.keyword = None;
        self.number = None;
        self.is_start_of_app = False
        self.illegal_chars = 0
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.is_start_of_app): 
            print("StartOfApp ", end="", file=res)
        if (self.keyword is not None): 
            print("[{0}] ".format(self.keyword), end="", file=res, flush=True)
        if (self.number is not None): 
            print("N{0} ".format(self.number), end="", file=res, flush=True)
        if (self.illegal_chars > 0): 
            print("(illegals={0}) ".format(self.illegal_chars), end="", file=res, flush=True)
        len0_ = (self.end_char + 1) - self.begin_char
        if (len0_ > 100): 
            len0_ = 100
        print("\"{0}\"".format(self.text[self.begin_char:self.begin_char+len0_]), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse(txt : str, i : int) -> 'StructExpressLine':
        while i.value < len(txt): 
            if (txt[i.value] != '\n' and txt[i.value] != '\r'): 
                break
            i.value += 1
        if (i.value >= len(txt)): 
            return None
        res = StructExpressLine()
        res.end_char = i.value
        res.begin_char = res.end_char
        res.text = txt
        while i.value < len(txt): 
            if (txt[i.value] == '\n' or txt[i.value] == '\r'): 
                break
            else: 
                res.end_char = i.value
            i.value += 1
        res.__analyze()
        return res
    
    def __analyze(self) -> None:
        i = 0
        i = self.begin_char
        while i <= self.end_char: 
            if (not Utils.isWhitespace(self.text[i])): 
                break
            i += 1
        if ((i < self.end_char) and str.isupper(self.text[i])): 
            for kw in StructExpressLine.__m_keywords: 
                if (StructExpressLine.__check_word(self.text, i, kw)): 
                    self.keyword = kw
                    i += len(kw)
                    break
        while i <= self.end_char: 
            if (not Utils.isWhitespace(self.text[i])): 
                break
            i += 1
        if (i <= self.end_char): 
            if (self.text[i] == 'N' or self.text[i] == '№'): 
                i = (i + 1)
                while i <= self.end_char: 
                    if (not Utils.isWhitespace(self.text[i])): 
                        break
                    i += 1
        if (i <= self.end_char): 
            j = 0
            j = i
            first_pass728 = True
            while True:
                if first_pass728: first_pass728 = False
                else: j += 1
                if (not (j <= self.end_char)): break
                ch = self.text[j]
                if (str.isdigit(ch)): 
                    continue
                if (ch == ')' or ch == '.'): 
                    continue
                if (str.isalpha(ch)): 
                    if (j > self.begin_char and str.isdigit(self.text[j - 1])): 
                        continue
                    if ((j + 1) <= self.end_char and self.text[j + 1] == ')'): 
                        continue
                break
            if (j > i): 
                self.number = self.text[i:i+j - i]
                i = j
        if (self.keyword == "ПРИЛОЖЕНИЕ" or self.keyword == "ДОДАТОК"): 
            if (i > self.end_char): 
                self.is_start_of_app = True
        self.illegal_chars = 0
        first_pass729 = True
        while True:
            if first_pass729: first_pass729 = False
            else: i += 1
            if (not (i <= self.end_char)): break
            ch = self.text[i]
            if (Utils.isWhitespace(ch) or str.isalnum(ch)): 
                continue
            if (ch == '_' or ch == '|'): 
                self.illegal_chars += 1
                continue
            if ((ord(ch)) <= 0x80 or ch == '№'): 
                continue
            self.illegal_chars += 1
    
    __m_keywords = None
    
    @staticmethod
    def __check_word(txt : str, i : int, sub : str) -> bool:
        j = 0
        j = 0
        while (j < len(sub)) and ((i + j) < len(txt)): 
            if (str.upper(txt[i + j]) != str.upper(sub[j])): 
                return False
            j += 1
        if (j >= len(sub)): 
            return True
        return False
    
    # static constructor for class StructExpressLine
    @staticmethod
    def _static_ctor():
        StructExpressLine.__m_keywords = ["СТАТЬЯ", "СТАТТЯ", "ПРИЛОЖЕНИЕ", "ДОДАТОК"]

StructExpressLine._static_ctor()