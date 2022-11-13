# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

class UnitextStyle:
    """ Представление стилей. Реализовано пока только для формата DOCX.
    Стиль
    """
    
    def __init__(self) -> None:
        self.attrs = dict()
        self.id0_ = 0
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        for at in self.attrs.items(): 
            if (tmp.tell() > 0): 
                print(" ", end="", file=tmp)
            print("{0}:{1}".format(at[0], at[1]), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def get_attr(self, name : str) -> str:
        """ Получить значение атрибута
        
        Args:
            name(str): имя
        
        Returns:
            str: значение
        """
        res = None
        wrapres573 = RefOutArgWrapper(None)
        inoutres574 = Utils.tryGetValue(self.attrs, name, wrapres573)
        res = wrapres573.value
        if (inoutres574): 
            return res
        return None
    
    def add_attr(self, name : str, val : str, append_val : bool=False) -> None:
        if (Utils.isNullOrEmpty(val)): 
            return
        val0 = None
        wrapval0575 = RefOutArgWrapper(None)
        inoutres576 = Utils.tryGetValue(self.attrs, name, wrapval0575)
        val0 = wrapval0575.value
        if (not inoutres576): 
            self.attrs[name] = val
        elif (not append_val or val0 is None): 
            self.attrs[name] = val
        elif (val0.find(';') < 0): 
            self.attrs[name] = "{0};{1}".format(val0, val)
        else: 
            vals = Utils.splitString(val0, ';', False)
            i = 0
            while i < len(vals): 
                if (vals[i] == val): 
                    return
                i += 1
            self.attrs[name] = "{0};{1}".format(val0, val)
    
    def remove_inherit_attrs(self, fr : 'UnitextStyledFragment') -> None:
        dels = None
        for kp in self.attrs.items(): 
            val = None
            p = fr
            while p is not None: 
                if (p.style_id >= 0 and p.style is not None): 
                    val = p.style.get_attr(kp[0])
                    if ((val) is not None): 
                        break
                p = p.parent
            if (val is None or val != kp[1]): 
                continue
            if (dels is None): 
                dels = list()
            dels.append(kp[0])
        if (dels is not None): 
            for k in dels: 
                del self.attrs[k]
    
    def clone(self, ignore_block_attrs : bool=False) -> 'UnitextStyle':
        res = UnitextStyle()
        self.copy_to(res)
        return res
    
    def copy_to(self, res : 'UnitextStyle') -> None:
        res.id0_ = self.id0_
        for kp in self.attrs.items(): 
            res.add_attr(kp[0], kp[1], False)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("style")
        xml0_.write_attribute_string("id", str(self.id0_))
        for kp in self.attrs.items(): 
            xml0_.write_attribute_string(kp[0], kp[1])
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "id"): 
                    self.id0_ = int(a[1])
                else: 
                    self.add_attr(Utils.getXmlAttrLocalName(a), a[1], False)
    
    def get_html(self, res : io.StringIO) -> None:
        """ Вывести в Html значение атрибута style="..."
        
        Args:
            res(io.StringIO): 
        """
        for kp in self.attrs.items(): 
            if (kp[0] == "heading-level"): 
                continue
            print("{0}:{1};".format(kp[0], kp[1]), end="", file=res, flush=True)