# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.internal.html.HtmlSectionItem import HtmlSectionItem
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocblock import UnitextDocblock
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen

class HtmlSection:
    
    def __init__(self) -> None:
        self.nodes = list()
        self.title = None;
        self.level = 0
        self.children = list()
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("H{0}: ".format(self.level), end="", file=tmp, flush=True)
        if (len(self.children) > 0): 
            print("Childs={0} ".format(len(self.children)), end="", file=tmp, flush=True)
        if (len(self.nodes) > 0): 
            print("Nodes={0} ".format(len(self.nodes)), end="", file=tmp, flush=True)
        if (self.title is not None): 
            print(self.title, end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    def _generate(self, blk : 'UnitextDocblock', lev : int, hg : 'UnitextHtmlGen') -> None:
        gen = None
        if (self.title is not None): 
            blk.head = UnitextContainer()
            gen = UnitextGen()
            hg.get_uni_text(self.title, gen, None, 0)
            hh = gen.finish(True, None)
            if (isinstance(hh, UnitextContainer)): 
                blk.head = (Utils.asObjectOrNull(hh, UnitextContainer))
            elif (hh is not None): 
                blk.head.children.append(hh)
            blk.head.children.append(UnitextNewline())
            blk.head.typ = UnitextContainerType.HEAD
        blk.body = (UnitextContainer())
        if (len(self.nodes) > 0): 
            gen = UnitextGen()
            for ch in self.nodes: 
                hg.get_uni_text(ch, gen, None, 0)
            hh = gen.finish(True, None)
            if (hh is not None and len(self.children) > 0): 
                pr = UnitextDocblock._new32("Preamble")
                pr.body = hh
                blk.body.children.append(pr)
            elif (isinstance(hh, UnitextContainer)): 
                blk.body = (Utils.asObjectOrNull(hh, UnitextContainer))
            elif (hh is not None): 
                blk.body.children.append(hh)
        for ch in self.children: 
            chblk = UnitextDocblock()
            blk.body.children.append(chblk)
            if (lev == 0): 
                chblk.typname = "Section"
            elif (lev == 1): 
                chblk.typname = "Subsection"
            else: 
                chblk.typname = "Chapter"
            ch._generate(chblk, lev + 1, hg)
    
    @staticmethod
    def create(n : 'HtmlNode') -> 'HtmlSectionItem':
        ttt = HtmlSectionItem()
        ttt.stack.append(HtmlSection())
        HtmlSection.__create(n, ttt)
        if (len(ttt.stack) > 1): 
            del ttt.stack[0:0+len(ttt.stack) - 1]
        if (len(ttt.stack[0].children) == 0): 
            return None
        if (len(ttt.stack[0].children) == 1): 
            if (len(ttt.stack[0].nodes) > 0): 
                ttt.head.extend(ttt.stack[0].nodes)
            ttt.stack[0] = ttt.stack[0].children[0]
        if (len(ttt.stack[0].children) < 2): 
            return None
        return ttt
    
    @staticmethod
    def __create(n : 'HtmlNode', st : 'HtmlSectionItem') -> None:
        cur_lev = len(st.stack)
        for ch in n.children: 
            if (not Utils.isNullOrEmpty(ch.tag_name) and ch.tag_name[0] == 'H'): 
                le = 0
                wraple34 = RefOutArgWrapper(0)
                inoutres35 = Utils.tryParseInt(ch.tag_name[1:], wraple34)
                le = wraple34.value
                if (inoutres35): 
                    if (le > 0): 
                        if (le < len(st.stack)): 
                            del st.stack[0:0+len(st.stack) - le]
                        while le > len(st.stack):
                            if (len(st.stack[0].children) == 0): 
                                break
                            al = st.stack[0].children[len(st.stack[0].children) - 1]
                            st.stack.insert(0, al)
                        if (le == len(st.stack)): 
                            s = HtmlSection._new33(le, ch)
                            st.stack[0].children.append(s)
                            st.stack.insert(0, s)
                            st.has_body = True
                            p = n
                            while p is not None: 
                                p.misc = (p)
                                p = p.parent
                            continue
                        else: 
                            pass
            if (ch.text is not None and ch.text.startswith("Автор:")): 
                pass
            HtmlSection.__create(ch, st)
            if (ch.misc is not None): 
                continue
            if (n.misc is not None): 
                if (len(st.stack) > 1): 
                    st.stack[0].nodes.append(ch)
                elif (st.has_body): 
                    st.tail.append(ch)
                else: 
                    st.head.append(ch)
        if (cur_lev < len(st.stack)): 
            del st.stack[0:0+len(st.stack) - cur_lev]
    
    @staticmethod
    def _new33(_arg1 : int, _arg2 : 'HtmlNode') -> 'HtmlSection':
        res = HtmlSection()
        res.level = _arg1
        res.title = _arg2
        return res