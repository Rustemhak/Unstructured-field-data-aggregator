# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.uni.UnitextGenNumStyleEx import UnitextGenNumStyleEx
from pullenti.unitext.internal.uni.UniTextGenNumType import UniTextGenNumType
from pullenti.unitext.internal.uni.UniTextGenNumLevel import UniTextGenNumLevel
from pullenti.unitext.internal.uni.UnitextGenNumStyle import UnitextGenNumStyle

class DocNumStyles:
    
    def __init__(self) -> None:
        self.__m_num_styles = dict()
    
    def get_style(self, id0_ : str) -> 'UnitextGenNumStyleEx':
        if (id0_ is None): 
            return None
        if (id0_ in self.__m_num_styles): 
            return self.__m_num_styles[id0_]
        return None
    
    @staticmethod
    def __read_attr_val(x : xml.etree.ElementTree.Element, nam : str, nam2 : str=None) -> str:
        if (x.attrib is not None): 
            for a in x.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == nam): 
                    return a[1]
                elif (nam2 is not None and Utils.getXmlAttrLocalName(a) == nam2): 
                    return a[1]
        if (nam == "val"): 
            if (x.attrib is not None): 
                for a in x.attrib.items(): 
                    return a[1]
        return None
    
    def read_all_styles(self, node : xml.etree.ElementTree.Element) -> None:
        abstr = dict()
        for xnum in node: 
            if (Utils.getXmlLocalName(xnum) == "abstractNum" and xnum.attrib is not None and len(xnum.attrib) >= 1): 
                id0_ = DocNumStyles.__read_attr_val(xnum, "abstractNumId", None)
                if (id0_ is None or id0_ in abstr): 
                    continue
                if (id0_ == "14"): 
                    pass
                nsty = UnitextGenNumStyle._new108(id0_)
                abstr[id0_] = nsty
                for xx in xnum: 
                    if (Utils.getXmlLocalName(xx) == "lvl"): 
                        nlev = UniTextGenNumLevel()
                        nsty.levels.append(nlev)
                        for xxx in xx: 
                            if (xxx.attrib is not None): 
                                if (Utils.getXmlLocalName(xxx) == "numFmt"): 
                                    nlev.type0_ = DocNumStyles._get_num_typ(DocNumStyles.__read_attr_val(xxx, "val", None))
                                elif (Utils.getXmlLocalName(xxx) == "lvlText"): 
                                    nlev.format0_ = DocNumStyles.__read_attr_val(xxx, "val", None)
                                elif (Utils.getXmlLocalName(xxx) == "start"): 
                                    ii = 0
                                    wrapii411 = RefOutArgWrapper(0)
                                    inoutres412 = Utils.tryParseInt(Utils.ifNotNull(DocNumStyles.__read_attr_val(xxx, "val", None), ""), wrapii411)
                                    ii = wrapii411.value
                                    if (inoutres412): 
                                        nlev.start = ii
                    elif (Utils.getXmlLocalName(xx) == "numStyleLink"): 
                        lid = DocNumStyles.__read_attr_val(xx, "val", None)
                        if (lid is not None and lid in abstr): 
                            nsty.levels.extend(abstr[lid].levels)
            elif (Utils.getXmlLocalName(xnum) == "num"): 
                id0_ = DocNumStyles.__read_attr_val(xnum, "numId", None)
                int_id = None
                for xx in xnum: 
                    if (Utils.getXmlLocalName(xx) == "abstractNumId"): 
                        int_id = DocNumStyles.__read_attr_val(xx, "val", None)
                if (int_id is None or id0_ is None): 
                    continue
                num0 = None
                wrapnum0418 = RefOutArgWrapper(None)
                inoutres419 = Utils.tryGetValue(abstr, int_id, wrapnum0418)
                num0 = wrapnum0418.value
                if (not inoutres419): 
                    continue
                num = UnitextGenNumStyleEx._new413(num0)
                num.id0_ = id0_
                if (not id0_ in self.__m_num_styles): 
                    self.__m_num_styles[id0_] = num
                for xx in xnum: 
                    if (Utils.getXmlLocalName(xx) == "lvlOverride"): 
                        l_ = 0
                        wrapl416 = RefOutArgWrapper(0)
                        inoutres417 = Utils.tryParseInt(Utils.ifNotNull(DocNumStyles.__read_attr_val(xx, "val", None), ""), wrapl416)
                        l_ = wrapl416.value
                        if (not inoutres417): 
                            continue
                        if ((l_ < 0) or l_ >= len(num.src.levels)): 
                            continue
                        for xxx in xx: 
                            if (Utils.getXmlLocalName(xxx) == "startOverride"): 
                                s = 0
                                wraps414 = RefOutArgWrapper(0)
                                inoutres415 = Utils.tryParseInt(Utils.ifNotNull(DocNumStyles.__read_attr_val(xxx, "val", None), ""), wraps414)
                                s = wraps414.value
                                if (inoutres415): 
                                    if (not l_ in num.override_starts): 
                                        num.override_starts[l_] = s
    
    @staticmethod
    def _read_number_style(xml0_ : xml.etree.ElementTree.Element) -> 'UnitextGenNumStyle':
        res = None
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "ilvl"): 
                res = UnitextGenNumStyle()
                nn = 0
                wrapnn420 = RefOutArgWrapper(0)
                inoutres421 = Utils.tryParseInt(Utils.ifNotNull(DocNumStyles.__read_attr_val(x, "val", None), ""), wrapnn420)
                nn = wrapnn420.value
                if (inoutres421): 
                    res.lvl = nn
            elif (Utils.getXmlLocalName(x) == "ilfo"): 
                vv = DocNumStyles.__read_attr_val(x, "val", None)
                if (vv == "2"): 
                    res.is_bullet = True
            elif (Utils.getXmlLocalName(x) == "t" and res is not None): 
                res.txt = DocNumStyles.__read_attr_val(x, "val", None)
        return res
    
    @staticmethod
    def _get_num_typ(ty : str) -> 'UniTextGenNumType':
        if (ty == "bullet"): 
            return UniTextGenNumType.BULLET
        if ("decimal" in ty): 
            return UniTextGenNumType.DECIMAL
        if (ty == "lowerLetter"): 
            return UniTextGenNumType.LOWERLETTER
        if (ty == "russianLower"): 
            return UniTextGenNumType.LOWERCYRLETTER
        if (ty == "russianUpper"): 
            return UniTextGenNumType.UPPERCYRLETTER
        if (ty == "upperLetter"): 
            return UniTextGenNumType.UPPERLETTER
        if (ty == "lowerRoman"): 
            return UniTextGenNumType.LOWERROMAN
        if ("oman" in ty): 
            return UniTextGenNumType.UPPERROMAN
        return UniTextGenNumType.DECIMAL