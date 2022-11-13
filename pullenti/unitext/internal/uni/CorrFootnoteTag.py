# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.uni.CorrFootnoteTyps import CorrFootnoteTyps

class CorrFootnoteTag:
    
    def __init__(self) -> None:
        self.typ = CorrFootnoteTyps.DIGIT
        self.number = 0
    
    @staticmethod
    def try_parse(text : str, i : int, for_contaiter : bool, robust : bool=False) -> 'CorrFootnoteTag':
        while i.value < len(text): 
            if (not Utils.isWhitespace(text[i.value])): 
                break
            i.value += 1
        if (i.value >= len(text)): 
            return None
        if (text[i.value] != '<'): 
            if (robust and text[i.value] == '*'): 
                res1 = CorrFootnoteTag._new315(CorrFootnoteTyps.STARS)
                while i.value < len(text): 
                    if (text[i.value] != '*'): 
                        i.value -= 1
                        break
                    else: 
                        res1.number += 1
                    i.value += 1
                return res1
            if (((((i.value + 10) < len(text)) and text[i.value] == 'С' and text[i.value + 1] == 'н') and text[i.value + 2] == 'о' and text[i.value + 3] == 'с') and text[i.value + 4] == 'к' and text[i.value + 5] == 'а'): 
                j = 0
                num = 0
                j = (i.value + 7)
                while j < len(text): 
                    if (text[j] == ':' and num > 0): 
                        res1 = CorrFootnoteTag._new316(CorrFootnoteTyps.DIGIT, num)
                        i.value = j
                        return res1
                    elif (str.isdigit(text[j])): 
                        num = ((num * 10) + (((ord(text[j])) - (ord('0')))))
                    else: 
                        break
                    j += 1
            if (str.isdigit(text[i.value]) and for_contaiter): 
                j = 0
                num = 0
                j = i.value
                while j < len(text): 
                    if (str.isdigit(text[j])): 
                        num = ((num * 10) + (((ord(text[j])) - (ord('0')))))
                    elif (text[j] == ')'): 
                        res1 = CorrFootnoteTag._new316(CorrFootnoteTyps.VERYDOUBT, num)
                        i.value = j
                        return res1
                    else: 
                        break
                    j += 1
            return None
        if ((i.value + 2) >= len(text)): 
            return None
        ii = i.value + 1
        if (text[ii] != '*' and not str.isdigit(text[ii])): 
            return None
        res = CorrFootnoteTag._new315((CorrFootnoteTyps.STARS if text[ii] == '*' else CorrFootnoteTyps.DIGIT))
        while ii < len(text): 
            if (text[ii] == '*' and res.typ == CorrFootnoteTyps.STARS): 
                res.number += 1
            elif (str.isdigit(text[ii]) and res.typ == CorrFootnoteTyps.DIGIT): 
                res.number = ((res.number * 10) + (((ord(text[ii])) - (ord('0')))))
            elif (text[ii] == '>'): 
                i.value = ii
                return res
            else: 
                break
            ii += 1
        return None
    
    @staticmethod
    def _new293(_arg1 : int, _arg2 : 'CorrFootnoteTyps') -> 'CorrFootnoteTag':
        res = CorrFootnoteTag()
        res.number = _arg1
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new315(_arg1 : 'CorrFootnoteTyps') -> 'CorrFootnoteTag':
        res = CorrFootnoteTag()
        res.typ = _arg1
        return res
    
    @staticmethod
    def _new316(_arg1 : 'CorrFootnoteTyps', _arg2 : int) -> 'CorrFootnoteTag':
        res = CorrFootnoteTag()
        res.typ = _arg1
        res.number = _arg2
        return res