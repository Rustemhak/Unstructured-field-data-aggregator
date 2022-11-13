# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext

class StyleHelper:
    
    @staticmethod
    def process_doc(doc : 'UnitextDocument') -> None:
        StyleHelper.__process_content(doc.content)
        for s in doc.sections: 
            for it in s.items: 
                if (it.content is not None): 
                    StyleHelper.__process_content(it.content)
    
    @staticmethod
    def __process_content(cnt : 'UnitextItem') -> None:
        if (cnt is None or cnt._m_styled_frag is None): 
            return
        def_txt = io.StringIO()
        cp = 0
        wrapcp330 = RefOutArgWrapper(cp)
        cnt._set_default_text_pos(wrapcp330, def_txt)
        cp = wrapcp330.value
        its = list()
        cnt.get_all_items(its, 0)
        i = 0
        while i < (len(its) - 1): 
            if ((isinstance(its[i], UnitextPlaintext)) and its[i].typ == UnitextPlaintextType.GENERATED): 
                if (its[i].parent == its[i + 1].parent and its[i]._m_styled_frag is None): 
                    its[i]._m_styled_frag = its[i + 1]._m_styled_frag
            i += 1
        for it in its: 
            if (it._m_styled_frag is not None): 
                fr = it._m_styled_frag
                if (fr.begin_char < 0): 
                    fr.begin_char = it.begin_char
                if (it.end_char > fr.end_char): 
                    fr.end_char = it.end_char
        StyleHelper.__corr_cp(cnt._m_styled_frag)
        StyleHelper.__set_text(cnt._m_styled_frag, Utils.toStringStringIO(def_txt))
        cnt._m_styled_frag = StyleHelper.__optimize(cnt._m_styled_frag)
        for it in its: 
            if (it._m_styled_frag is not None): 
                if (it._m_styled_frag.tag is not None): 
                    it._m_styled_frag = (None)
    
    @staticmethod
    def __corr_cp(fr : 'UnitextStyledFragment') -> None:
        fr.tag = None
        i = 0
        while i < len(fr.children): 
            ch = fr.children[i]
            ch.parent = fr
            StyleHelper.__corr_cp(ch)
            if (fr.begin_char < 0): 
                fr.begin_char = ch.begin_char
            if (ch.end_char > fr.end_char): 
                fr.end_char = ch.end_char
            i += 1
    
    @staticmethod
    def __set_text(fr : 'UnitextStyledFragment', txt : str) -> None:
        out_text = True
        for ch in fr.children: 
            StyleHelper.__set_text(ch, txt)
            if (ch.typ != UnitextStyledFragmentType.INLINE and ch.typ != UnitextStyledFragmentType.UNDEFINED): 
                out_text = False
        if (out_text and fr.end_char >= 0 and (fr.end_char < len(txt))): 
            fr.text = txt[fr.begin_char:fr.begin_char+(fr.end_char + 1) - fr.begin_char]
    
    @staticmethod
    def __optimize(fr : 'UnitextStyledFragment') -> 'UnitextStyledFragment':
        if (fr.parent is not None and fr.style == fr.parent.style): 
            fr.style = None
        i = 0
        first_pass672 = True
        while True:
            if first_pass672: first_pass672 = False
            else: i += 1
            if (not (i < len(fr.children))): break
            ch = fr.children[i]
            ch = StyleHelper.__optimize(ch)
            if (ch is None): 
                del fr.children[i]
                i -= 1
                continue
            fr.children[i] = ch
            if (i > 0): 
                ch0 = fr.children[i - 1]
                if (ch0.style == ch.style and ch0.typ == ch.typ and (ch0.end_char + 1) == ch.begin_char): 
                    ch0.children.extend(ch.children)
                    for ccc in ch.children: 
                        ccc.parent = ch0
                    ch0.end_char = ch.end_char
                    del fr.children[i]
                    i -= 1
                    ch.tag = (ch0)
                    continue
        if (len(fr.children) == 0 and (fr.begin_char < 0)): 
            return None
        return fr