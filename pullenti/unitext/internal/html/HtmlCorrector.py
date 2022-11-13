# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.unitext.internal.html.HtmlNode import HtmlNode
from pullenti.unitext.internal.html.HtmlParser import HtmlParser

class HtmlCorrector:
    # Используется для встраивания узлов в HTML-тексты
    
    def __init__(self, html_ : str) -> None:
        self.__m_html = None;
        self.__m_root = None;
        self.__m_impls = None;
        self.__m_text = None;
        self.__m_html = html_
        self.__m_impls = dict()
        self.__parse()
        if (self.__m_text is None): 
            self.__m_text = ""
    
    def __parse(self) -> None:
        tmp = Utils.newStringIO(self.__m_html)
        self.__m_root = HtmlParser.parse(tmp, True)
        if (self.__m_root is not None): 
            if (self.__m_root.tag_name == "HTML"): 
                self.__m_root.tag_name = "DIV"
            if (not Utils.isNullOrEmpty(self.__m_root.text) and self.__m_root.tag_name is None): 
                hh = HtmlNode._new1("span")
                hh.children.append(self.__m_root)
                self.__m_root.parent = hh
                self.__m_root = hh
            self.__create_text()
    
    def __create_text(self) -> None:
        pars = GetPlaintextParam._new2("\n", "  ", "\n\n")
        self.__m_text = self.__m_root.get_plaintext(pars)
    
    @property
    def plain_text(self) -> str:
        return self.__m_text
    
    @property
    def html_text(self) -> str:
        if (self.__m_root is None): 
            return ""
        res = io.StringIO()
        self.__m_root.get_html(res)
        return Utils.toStringStringIO(res)
    
    def set_text(self, begin_char : int, end_char : int, new_text : str) -> bool:
        if (self.__m_root is None or self.__m_text is None): 
            return False
        if (begin_char > len(self.__m_text) or end_char > len(self.__m_text) or begin_char > end_char): 
            return False
        nod = self.__m_root.implantate_node(begin_char, end_char, "span")
        if (nod is None): 
            return False
        if (Utils.isNullOrEmpty(new_text)): 
            if (nod.parent is not None and nod in nod.parent.children): 
                nod.parent.children.remove(nod)
                self.__create_text()
                return True
            return False
        if (nod.children is not None and len(nod.children) > 0): 
            nod.children.clear()
        nod.text = new_text
        nod.tag_name = (None)
        self.__create_text()
        return True
    
    def implantate_node(self, begin_char : int, end_char : int, tag_name : str, id0_ : str, attrs : typing.List[tuple]) -> bool:
        if ((self.__m_root is None or Utils.isNullOrEmpty(tag_name) or (begin_char < 0)) or begin_char > end_char or end_char >= len(self.__m_text)): 
            return False
        if (id0_ is None): 
            return False
        if (id0_ in self.__m_impls): 
            self.remove_node(id0_)
        while (begin_char < end_char) and (begin_char < len(self.__m_text)): 
            if (not Utils.isWhitespace(self.__m_text[begin_char])): 
                break
            begin_char += 1
        while end_char > begin_char: 
            if (not Utils.isWhitespace(self.__m_text[end_char])): 
                break
            end_char -= 1
        nod = self.__m_root.implantate_node(begin_char, end_char, tag_name)
        if (nod is None): 
            return False
        nod.attrs = dict()
        nod.attrs["ID"] = id0_
        if (attrs is not None): 
            for kp in attrs.items(): 
                if (not kp[0].upper() in nod.attrs): 
                    nod.attrs[kp[0].upper()] = kp[1]
        self.__m_impls[id0_] = nod
        return True
    
    def remove_node(self, id0_ : str) -> bool:
        if (id0_ in self.__m_impls): 
            self.__m_impls[id0_].remove()
            del self.__m_impls[id0_]
            if (len(self.__m_impls) == 0): 
                self.__parse()
            return True
        else: 
            return False
    
    def find_node(self, tag_name : str, attr_name : str, attr_value : str) -> 'HtmlNode':
        if (self.__m_root is None): 
            return None
        return self.__m_root.find_subnode(tag_name, attr_name, attr_value)
    
    def clear_all(self) -> None:
        for kp in self.__m_impls.items(): 
            kp[1].remove()
        self.__m_impls.clear()
        self.__parse()