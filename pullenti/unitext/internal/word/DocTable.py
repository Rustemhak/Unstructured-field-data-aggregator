# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import xml.etree
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.UnitextStyledFragment import UnitextStyledFragment
from pullenti.unitext.UnitextStyle import UnitextStyle
from pullenti.unitext.internal.word.DocTableRow import DocTableRow
from pullenti.unitext.internal.word.DocTableCell import DocTableCell
from pullenti.unitext.UnitextContainer import UnitextContainer

class DocTable:
    
    def __init__(self) -> None:
        self.cols = 0
        self.rows = list()
        self.col_width = list()
        self.hide_borders = False
        self.__m_style = None;
    
    def read(self, own : 'DocxToText', sfrag : 'UnitextStyledFragment', stack_nodes : typing.List[xml.etree.ElementTree.Element]) -> None:
        if (sfrag is not None): 
            self.__m_style = UnitextStyledFragment._new424(UnitextStyledFragmentType.TABLE, sfrag)
            sfrag.children.append(self.__m_style)
        xml0_ = stack_nodes[len(stack_nodes) - 1]
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "tblGrid"): 
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "gridCol"): 
                        self.cols += 1
                        if (xx.attrib is not None): 
                            for a in xx.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "w"): 
                                    n = 0
                                    wrapn425 = RefOutArgWrapper(0)
                                    inoutres426 = Utils.tryParseInt(Utils.ifNotNull(a[1], ""), wrapn425)
                                    n = wrapn425.value
                                    if (inoutres426): 
                                        self.col_width.append(n)
            elif (Utils.getXmlLocalName(x) == "tblPr"): 
                if (self.__m_style is not None): 
                    st0 = UnitextStyle()
                    own.m_styles.read_unitext_style(x, st0)
                    st0.remove_inherit_attrs(self.__m_style)
                    self.__m_style.style = own.m_styles.register_style(st0)
                cou = 0
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "tblBorders"): 
                        for xxx in xx: 
                            if (((Utils.getXmlLocalName(xxx) == "top" or Utils.getXmlLocalName(xxx) == "left" or Utils.getXmlLocalName(xxx) == "right") or Utils.getXmlLocalName(xxx) == "bottom" or Utils.getXmlLocalName(xxx) == "start") or Utils.getXmlLocalName(xxx) == "end"): 
                                if (xxx.attrib is not None): 
                                    for a in xxx.attrib.items(): 
                                        if (Utils.getXmlAttrLocalName(a) == "color"): 
                                            if (a[1] == "FFFFFF"): 
                                                cou += 1
                if (cou == 4): 
                    self.hide_borders = True
            elif (Utils.getXmlLocalName(x) == "tr"): 
                tr = DocTableRow()
                self.rows.append(tr)
                first_span = 0
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "tc"): 
                        tc = DocTableCell()
                        tr.cells.append(tc)
                        stack_nodes.append(xx)
                        tc.read(own, self.__m_style, stack_nodes)
                        del stack_nodes[len(stack_nodes) - 1]
                        if (first_span > 0): 
                            tc.col_span += first_span
                            first_span = 0
                    elif (Utils.getXmlLocalName(xx) == "sdt"): 
                        for xxx in xx: 
                            if (Utils.getXmlLocalName(xxx) == "sdtContent"): 
                                for xxxx in xxx: 
                                    if (Utils.getXmlLocalName(xxxx) == "tc"): 
                                        tc = DocTableCell()
                                        tr.cells.append(tc)
                                        stack_nodes.append(xxxx)
                                        tc.read(own, self.__m_style, stack_nodes)
                                        del stack_nodes[len(stack_nodes) - 1]
                                        if (first_span > 0): 
                                            tc.col_span += first_span
                                            first_span = 0
                                        if (isinstance(tc.uni, UnitextContainer)): 
                                            tc.uni.typ = UnitextContainerType.CONTENTCONTROL
                                        else: 
                                            ccc = UnitextContainer._new427(UnitextContainerType.CONTENTCONTROL, self.__m_style)
                                            ccc.children.append(tc.uni)
                                            tc.uni.parent = (ccc)
                                            tc.uni = (ccc)
                    elif (Utils.getXmlLocalName(xx) == "trPr"): 
                        for xxx in xx: 
                            if (Utils.getXmlLocalName(xxx) == "gridBefore" and xxx.attrib is not None and len(xxx.attrib) == 1): 
                                cou = 0
                                wrapcou428 = RefOutArgWrapper(0)
                                inoutres429 = Utils.tryParseInt(Utils.getXmlAttrByIndex(xxx.attrib, 0)[1], wrapcou428)
                                cou = wrapcou428.value
                                if (inoutres429): 
                                    if (cou > 0): 
                                        first_span = cou
        if (len(self.col_width) == self.cols): 
            nn = 0
            for w in self.col_width: 
                nn += w
            if (nn > 0): 
                ii = 0
                while ii < len(self.col_width): 
                    self.col_width[ii] = (math.floor((self.col_width[ii] * 100) / nn))
                    if (self.col_width[ii] == 0): 
                        self.col_width[ii] = 1
                    ii += 1
            else: 
                self.col_width.clear()
        else: 
            self.col_width.clear()
        i = 0
        while i < len(self.rows): 
            r = self.rows[i]
            gr_num = 1
            j = 0
            first_pass689 = True
            while True:
                if first_pass689: first_pass689 = False
                else: j += 1
                if (not (j < len(r.cells))): break
                c = r.cells[j]
                c.grid_num = gr_num
                gr_num += c.col_span
                if (c.merge_vert != 1): 
                    continue
                span_cell = None
                for ii in range(i - 1, -1, -1):
                    rr = self.rows[ii]
                    grr_num = 1
                    jj = 0
                    while jj < len(rr.cells): 
                        cc = rr.cells[jj]
                        if (cc.merge_vert == 2 and ((c.grid_num == cc.grid_num or c.grid_num == grr_num))): 
                            cc.row_span += 1
                            span_cell = cc
                            break
                        grr_num += cc.col_span
                        jj += 1
                    if (span_cell is not None): 
                        break
                if (span_cell is None): 
                    pass
            i += 1
    
    def create_uni(self) -> 'UnitextTable':
        if (len(self.rows) == 0): 
            return None
        tab = UnitextTable()
        tab._m_styled_frag = self.__m_style
        tab.hide_borders = self.hide_borders
        ii = 0
        while ii < len(self.col_width): 
            tab.set_col_width(ii, "{0}%".format(self.col_width[ii]))
            ii += 1
        rn = 0
        for r in self.rows: 
            cn = 0
            for c in r.cells: 
                if (c.merge_vert == 1): 
                    continue
                while True: 
                    if (tab.get_cell(rn, cn) is None): 
                        break
                    cn += 1
                cel = tab.add_cell(rn, (rn + c.row_span) - 1, cn, (cn + c.col_span) - 1, c.uni)
                cel._m_styled_frag = c.frag
                if (c.uni is not None and c.uni._m_styled_frag == c.frag): 
                    c.uni._m_styled_frag = (None)
            rn += 1
        return tab