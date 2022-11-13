# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.internal.word.Sprm import Sprm
from pullenti.unitext.internal.word.StyleDefinition import StyleDefinition
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.internal.uni.IUnitextGenNumStyle import IUnitextGenNumStyle
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.internal.uni.UnitextGenNumStyle import UnitextGenNumStyle
from pullenti.unitext.internal.word.StyleCollection import StyleCollection
from pullenti.unitext.internal.uni.UniTextGenNumType import UniTextGenNumType
from pullenti.unitext.internal.uni.UniTextGenNumLevel import UniTextGenNumLevel
from pullenti.unitext.internal.word.DocNumStyles import DocNumStyles
from pullenti.unitext.internal.word.CharacterFormatting import CharacterFormatting
from pullenti.unitext.internal.word.Prl import Prl
from pullenti.unitext.internal.word.Paragraph import Paragraph
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.internal.word.FcCompressedMapping import FcCompressedMapping
from pullenti.unitext.internal.uni.UniTextGenCell import UniTextGenCell
from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
from pullenti.unitext.internal.word.BasicTypesReader import BasicTypesReader
from pullenti.unitext.internal.misc.WingdingsHelper import WingdingsHelper
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.internal.word.FibRbFcLcb97 import FibRbFcLcb97
from pullenti.unitext.internal.word.FibStructuresReader import FibStructuresReader
from pullenti.unitext.internal.word.ExtendedName import ExtendedName
from pullenti.unitext.internal.word.MSOfficeHelper import MSOfficeHelper
from pullenti.unitext.internal.word.FibRgLw97 import FibRgLw97
from pullenti.unitext.internal.word.FormattingLevel import FormattingLevel
from pullenti.unitext.UnitextPagesection import UnitextPagesection
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.internal.uni.UnitextGenTable import UnitextGenTable
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.internal.word.ReadUtils import ReadUtils
from pullenti.unitext.UnitextContainerType import UnitextContainerType

class WordDocument:
    # Word document model.
    # See specification for explanations.
    # [MS-DOC]: Word Binary File Format (.doc) Structure Specification
    # Release: Thursday, August 27, 2009
    
    class FileCharacterPosition:
        
        def __init__(self) -> None:
            self._offset = 0
            self._length = 0
            self._character_index = 0
            self._bytes_per_character = 0
            self._prls = None;
        
        def __str__(self) -> str:
            from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
            res = io.StringIO()
            print("CharIndex:{0} Offset:{1} Len:{2}".format(self._character_index, self._offset, self._length), end="", file=res, flush=True)
            if (self._prls is not None): 
                for prl in self._prls: 
                    print(" {0}".format(Utils.ifNotNull(SinglePropertyModifiers.get_sprm_name(prl._sprm._sprm), "?")), end="", file=res, flush=True)
            return Utils.toStringStringIO(res)
        
        def _contains(self, position : int) -> bool:
            return self._character_index <= position and (position < (self._character_index + self._length))
    
    class LFO:
        
        def __init__(self) -> None:
            self.lsid = 0
            self.dat_count = 0
            self.ibst_flt_auto_num = 0
            self.__lvls = list()
    
    class LFOData: pass
    
    class LFOLVL:
        
        def __init__(self) -> None:
            self.istart_at = 0
    
    class LSTF:
        
        def __init__(self) -> None:
            self.lsid = 0
            self.istds = Utils.newArrayOfBytes(18, 0)
            self.fsimple_list = False
            self.fauto_num = False
            self.lvls = list()
    
    class LVL:
        
        def __init__(self) -> None:
            self.istart_at = 0
            self.nfc = 0
            self.rgbxch_nums = Utils.newArrayOfBytes(9, 0)
            self.ixch_follow = 0
            self.dxa_indent_sav = 0
            self.cb_grpprl_chpx = 0
            self.cb_grpprl_papx = 0
            self.ilvl_restart_lim = 0
            self.xstname = None;
    
    def __init__(self) -> None:
        self.text = io.StringIO()
        self.__file_character_positions = None;
        self.__m_paragraphs = list()
        self.__m_formattings = None;
        self.__m_style_definitions_map = None;
        self.__default_prls = None;
        self.__m_num_styles = dict()
        self.comment = None;
        self.__m_error = False
        self.__m_footnotes = dict()
        self.__m_comments = dict()
        self.__m_super_texts = dict()
        self.__m_sub_texts = dict()
        self.__m_shapes = dict()
        self.__m_dels = None;
        self.__lfos = list()
        self.__lstfs = list()
    
    @property
    def paragraphs(self) -> typing.List['Paragraph']:
        return self.__m_paragraphs
    
    @property
    def formattings(self) -> typing.List['CharacterFormatting']:
        return self.__m_formattings
    
    @property
    def style_definitions(self) -> typing.List['StyleDefinition']:
        return self.__m_style_definitions_map.values()
    
    @property
    def style_definitions_map(self) -> typing.List[tuple]:
        return self.__m_style_definitions_map
    
    def load(self, system : 'CompoundFileSystem', doc : 'UnitextDocument'=None) -> None:
        word_document_stream_name = "WordDocument"
        word_document_storage = system.get_root_storage().find_storage(ExtendedName.from_string(word_document_stream_name))
        with word_document_storage.create_stream() as word_document_stream: 
            fib = None
            fib = FibStructuresReader._read_fib(word_document_stream)
            if (fib is not None): 
                table_stream_name = WordDocument.__get_table_stream_name(fib)
                table_storage = system.get_root_storage().find_storage(ExtendedName.from_string(table_stream_name))
                if (table_storage is not None): 
                    with table_storage.create_stream() as table_stream: 
                        self.__load_content(word_document_stream, table_stream, fib, doc)
            else: 
                word_document_stream.position = 0
                buf = Utils.newArrayOfBytes(word_document_stream.length, 0)
                i = word_document_stream.read(buf, 0, len(buf))
                if (i < 0x20): 
                    return
                ddd = MSOfficeHelper._uni_from_word6or_early(buf)
                if (ddd is not None): 
                    doc.content = ddd.content
    
    @staticmethod
    def __get_table_stream_name(fib : 'Fib') -> str:
        return ("1Table" if fib._base._fwhich_tbl_stm else "0Table")
    
    def __load_content(self, word_document_stream : Stream, table_stream : Stream, fib : 'Fib', doc : 'UnitextDocument') -> None:
        fib97 = Utils.asObjectOrNull(fib._fib_rg_lw, FibRgLw97)
        if (fib97 is None): 
            return
        fib_lc97 = Utils.asObjectOrNull(fib._fib_rg_fc_lcb_blob, FibRbFcLcb97)
        if (fib_lc97 is None): 
            return
        pos = fib_lc97._fc_clx
        table_stream.position = pos
        iii = fib_lc97._lcb_clx
        clx = BasicTypesReader._read_clx(table_stream, iii)
        self.__load_characters(word_document_stream, clx)
        try: 
            plcf_bte_papx_offset = fib._fib_rg_fc_lcb_blob._fc_plcf_bte_papx
            table_stream.position = plcf_bte_papx_offset
            plcf_bte_papx_length = fib._fib_rg_fc_lcb_blob._lcb_plcf_bte_papx
            plcf_bte_papx = BasicTypesReader._read_plcf_bte_papx(table_stream, plcf_bte_papx_length)
            self.__load_paragraphs(word_document_stream, clx, plcf_bte_papx)
            plcf_bte_chpx_offset = fib._fib_rg_fc_lcb_blob._fc_plcf_bte_chpx
            table_stream.position = plcf_bte_chpx_offset
            plcf_bte_chpx_length = fib._fib_rg_fc_lcb_blob._lcb_plcf_bte_chpx
            plc_bte_chpx = BasicTypesReader._read_plc_bte_chpx(table_stream, plcf_bte_chpx_length)
            self.__load_character_formatting(word_document_stream, plc_bte_chpx)
            stsh_offset = fib._fib_rg_fc_lcb_blob._fc_stshf
            table_stream.position = stsh_offset
            stsh_length = fib._fib_rg_fc_lcb_blob._lcb_stshf
            stsh = BasicTypesReader._read_stsh(table_stream, stsh_length)
            self.__load_stsh(word_document_stream, stsh)
            table_stream.position = fib_lc97._fc_plf_lfo
            self.__loadlfos(table_stream, fib_lc97._lcb_plf_lfo)
            table_stream.position = fib_lc97._fc_plf_lst
            self.__loadlstfs(table_stream, fib_lc97._lcb_plf_lst)
        except Exception as ex: 
            pass
        if (doc is not None): 
            self.__m_dels = Utils.newArrayOfBytes(self.text.tell(), 0)
            if (self.__m_formattings is not None): 
                for f in self.__m_formattings: 
                    if (f.length == 1): 
                        dat = f.get_property(SinglePropertyModifiers._sprm_csymbol)
                        if (dat is not None and len(dat) == 4): 
                            nnn = dat[3]
                            nnn <<= (8)
                            nnn |= (dat[2])
                            if (nnn > (0xF000)): 
                                nnn -= (0xF000)
                            if (f.pos >= 0 and (f.pos < self.text.tell())): 
                                ch0 = Utils.getCharAtStringIO(self.text, f.pos)
                                Utils.setCharAtStringIO(self.text, f.pos, WingdingsHelper.get_unicode(nnn))
                                if (Utils.getCharAtStringIO(self.text, f.pos) == (chr(0))): 
                                    Utils.setCharAtStringIO(self.text, f.pos, chr(nnn))
                    sty = f.get_styles(FormattingLevel.CHARACTER)
                    if (sty is not None): 
                        if ("CFRMarkDel" in str(sty)): 
                            ii = f.pos
                            while ii < (f.pos + f.length): 
                                self.__m_dels[ii] = (1)
                                ii += 1
            total_text = Utils.toStringStringIO(self.text)
            gen = UnitextGen()
            if (self.__m_paragraphs is None or len(self.__m_paragraphs) == 0): 
                gen.append_text(total_text, False)
                doc.content = gen.finish(True, None)
                return
            if (self.__m_formattings is not None): 
                i = 0
                while i < len(self.__m_formattings): 
                    f = self.__m_formattings[i]
                    dat = f.get_property(SinglePropertyModifiers._sprm_ciss)
                    if (f.pos > (84223 - 10) and (f.pos < (84223 + 10))): 
                        pass
                    if ((dat is not None and len(dat) == 1 and dat[0] == (1)) and (f.length < 10)): 
                        tmp = total_text[f.pos:f.pos+f.length]
                        if (not f.pos in self.__m_super_texts): 
                            self.__m_super_texts[f.pos] = tmp
                    if ((dat is not None and len(dat) == 1 and dat[0] == (2)) and (f.length < 10)): 
                        tmp = total_text[f.pos:f.pos+f.length]
                        if (not f.pos in self.__m_sub_texts): 
                            self.__m_sub_texts[f.pos] = tmp
                    i += 1
            for k in range(2):
                table_stream.position = (fib_lc97._fc_plcffnd_ref if k == 0 else fib_lc97._fc_plcfend_ref)
                cps = BasicTypesReader._read_cps(table_stream, ((fib_lc97._lcb_plcffnd_ref if k == 0 else fib_lc97._lcb_plcfend_ref)))
                table_stream.position = (fib_lc97._fc_plcffnd_txt if k == 0 else fib_lc97._fc_plcfend_txt)
                cps2 = BasicTypesReader._read_cps(table_stream, ((fib_lc97._lcb_plcffnd_txt if k == 0 else fib_lc97._lcb_plcfend_txt)))
                if (len(cps) > 2 and gen is not None): 
                    pos0 = fib97._ccp_text
                    len0_ = fib97._ccp_ftn
                    if (k == 1): 
                        pos0 += (((fib97._ccp_ftn) + (fib97._ccp_hdd) + (fib97._ccp_atn)))
                        len0_ = (fib97._ccp_edn)
                    ttt = total_text[pos0:pos0+len0_]
                    i = 0
                    first_pass693 = True
                    while True:
                        if first_pass693: first_pass693 = False
                        else: i += 1
                        if (not ((i < (len(cps) - 2)) and (i < len(cps2)))): break
                        cp = cps[i]
                        if ((cp < 0) or cp >= pos0): 
                            continue
                        ge = UnitextGen()
                        max0_ = (cps2[i + 1] if (i + 1) < (len(cps2) - 2) else len0_)
                        self.__create_uni(ge, None, 0, pos0 + cps2[i], pos0 + max0_, total_text, 0)
                        if (not cp in self.__m_footnotes): 
                            fn = UnitextFootnote._new471(k == 1, ge.finish(True, None))
                            self.__m_footnotes[cp] = fn
            table_stream.position = fib_lc97._fc_plcfand_txt
            cpsat2 = BasicTypesReader._read_cps(table_stream, fib_lc97._lcb_plcfand_txt)
            table_stream.position = fib_lc97._fc_plcfand_ref
            cpsat = BasicTypesReader._read_cps(table_stream, len(cpsat2) * 4)
            if (len(cpsat) == len(cpsat2)): 
                pos0 = ((fib97._ccp_text) + (fib97._ccp_ftn) + (fib97._ccp_hdd))
                len0_ = fib97._ccp_atn
                ttt = total_text[pos0:pos0+len0_]
                i = 0
                first_pass694 = True
                while True:
                    if first_pass694: first_pass694 = False
                    else: i += 1
                    if (not (i < (len(cpsat) - 2))): break
                    cp = cpsat[i]
                    if ((cp < 0) or cp >= pos0): 
                        continue
                    ge = UnitextGen()
                    max0_ = (cpsat2[i + 1] if (i + 1) < (len(cpsat) - 2) else len0_)
                    self.__create_uni(ge, None, 0, pos0 + cpsat2[i], pos0 + max0_, total_text, 0)
                    cc = ge.finish(True, None)
                    if (cc is None): 
                        continue
                    tmp = io.StringIO()
                    cc.get_plaintext(tmp, None)
                    if (tmp.tell() < 1): 
                        continue
                    cmt = UnitextComment._new44(Utils.toStringStringIO(tmp))
                    self.__m_comments[cp] = cmt
            if (fib97._ccp_txbx > (0)): 
                pos0 = ((fib97._ccp_text) + (fib97._ccp_ftn) + (fib97._ccp_hdd)) + (fib97._ccp_atn) + (fib97._ccp_edn)
                len0_ = fib97._ccp_txbx
                ttt = total_text[pos0:pos0+len0_]
                if (fib_lc97._lcb_plcf_txbx_bkd > (0) and fib_lc97._lcb_plcftxbx_txt > (0)): 
                    table_stream.position = fib_lc97._fc_plcftxbx_txt
                    k2 = (math.floor((((fib_lc97._lcb_plcftxbx_txt) - 4)) / 26))
                    cps2 = BasicTypesReader._read_cps(table_stream, ((k2 + 1)) * 4)
                    texts2 = list()
                    ii = 0
                    while ii < (len(cps2) - 2): 
                        ge = UnitextGen()
                        max0_ = (cps2[ii + 1] if (ii + 1) < (len(cps2) - 2) else len0_)
                        self.__create_uni(ge, None, 0, pos0 + cps2[ii], pos0 + max0_, total_text, 0)
                        cc = ge.finish(True, None)
                        cnt = UnitextContainer._new92(UnitextContainerType.SHAPE)
                        if (cc is not None): 
                            cnt.children.append(cc)
                        texts2.append(cnt)
                        ii += 1
                    lids = list()
                    ii = 0
                    while ii < k2: 
                        table_stream.position = table_stream.position + (14)
                        lids.append(ReadUtils._read_int(table_stream))
                        table_stream.position = table_stream.position + (4)
                        ii += 1
                    table_stream.position = fib_lc97._fc_plc_spa_mom
                    kk = (math.floor((((fib_lc97._lcb_plc_spa_mom) - 4)) / 30))
                    cps3 = BasicTypesReader._read_cps(table_stream, ((kk + 1)) * 4)
                    lids2 = list()
                    ii = 0
                    while ii < kk: 
                        lids2.append(ReadUtils._read_int(table_stream))
                        table_stream.position = table_stream.position + (22)
                        ii += 1
                    for ii in range(len(lids2) - 1, -1, -1):
                        j = Utils.indexOfList(lids, lids2[ii], 0)
                        if (j >= 0): 
                            self.__m_shapes[cps3[ii]] = texts2[j]
                            del texts2[j]
                            del lids[j]
                            del lids2[ii]
                            del cps3[ii]
                    for ii in range(len(lids2) - 1, -1, -1):
                        cnt = UnitextContainer()
                        for j in range(len(lids) - 1, -1, -1):
                            if (lids[j] > lids2[ii]): 
                                cnt.children.insert(0, texts2[j])
                                del lids[j]
                                del texts2[j]
                        if (len(cnt.children) > 0): 
                            self.__m_shapes[cps3[ii]] = cnt
            self.__create_uni(gen, None, 0, 0, fib97._ccp_text, total_text, 0)
            doc.content = gen.finish(True, None)
            if (fib_lc97._lcb_plcf_hdd != (0)): 
                table_stream.position = fib_lc97._fc_plcf_hdd
                strs = BasicTypesReader._read_cps(table_stream, fib_lc97._lcb_plcf_hdd)
                if (len(strs) > 7): 
                    pos0 = (fib97._ccp_text) + (fib97._ccp_ftn)
                    len0_ = fib97._ccp_hdd
                    sub = total_text[pos0:pos0+len0_]
                    sect = UnitextPagesection()
                    for k in range(2):
                        gg = UnitextGen()
                        for ii in range(2):
                            jj = 7 + ii
                            if (k > 0): 
                                jj += 2
                            if ((jj < len(strs)) and (strs[jj] < strs[jj + 1])): 
                                self.__create_uni(gg, None, 0, pos0 + strs[jj], (pos0 + strs[jj + 1]) - 1, total_text, 0)
                        fi = gg.finish(True, None)
                        if (fi is not None): 
                            sect.items.append(UnitextPagesectionItem._new259(fi, k > 0))
                    if (len(sect.items) > 0): 
                        doc.sections.append(sect)
            return
    
    def __create_uni(self, gen : 'UnitextGen', blk : 'UnitextItem', i0 : int, p0 : int, p1 : int, txt : str, level : int) -> None:
        if (level > 30): 
            return
        if (i0 == 32): 
            pass
        tmp = io.StringIO()
        i = i0
        first_pass695 = True
        while True:
            if first_pass695: first_pass695 = False
            else: i += 1
            if (not (i < len(self.__m_paragraphs))): break
            p = self.__m_paragraphs[i]
            if (p.pos == 496): 
                pass
            if (p.pos >= p1): 
                break
            if ((p.pos < p0) or (p.pos + p.length) > p1): 
                continue
            if (gen is not None): 
                pass
            data = [ ]
            if (p.is_in_table and gen is not None and blk is None): 
                tab = UnitextGenTable()
                ro = list()
                allids = list()
                has_huge_papx_rows = list()
                cgen = UnitextGen()
                first_pass696 = True
                while True:
                    if first_pass696: first_pass696 = False
                    else: i += 1
                    if (not (i < len(self.__m_paragraphs))): break
                    pp = self.__m_paragraphs[i]
                    if (not pp.is_in_table and pp.is_table_cell_end and pp.length <= 2): 
                        if (len(ro) > 0): 
                            data = pp.get_property(SinglePropertyModifiers._sprm_phuge_papx)
                            if (data is not None): 
                                has_huge_papx_rows.append(len(tab.cells))
                            tab.cells.append(ro)
                        ro = list()
                        continue
                    if (not pp.is_in_table): 
                        i -= 1
                        break
                    if (pp.table_depth < p.table_depth): 
                        i -= 1
                        break
                    if (pp.table_depth > p.table_depth): 
                        i1 = 0
                        i1 = (i + 1)
                        while i1 < len(self.__m_paragraphs): 
                            if (pp.table_depth > self.__m_paragraphs[i1].table_depth and self.__m_paragraphs[i1].table_depth == p.table_depth): 
                                break
                            i1 += 1
                        gt = UnitextGen()
                        self.__create_uni(cgen, None, i, pp.pos, self.__m_paragraphs[i1 - 1].pos + self.__m_paragraphs[i1 - 1].length, txt, level + 1)
                        i = i1
                        if (i1 < len(self.__m_paragraphs)): 
                            pp = self.__m_paragraphs[i1]
                    if (pp.is_table_row_end): 
                        data = pp.get_property(SinglePropertyModifiers._sprm_tdef_table)
                        if (data is not None and len(data) > 0): 
                            cou = data[0]
                            if (cou == len(ro)): 
                                ii = 1; cc = 0
                                while (ii < len(data)) and (cc < len(ro)): 
                                    iid = data[ii + 1]
                                    iid <<= (8)
                                    iid |= (data[ii])
                                    ro[cc].tag = (iid)
                                    if (not iid in allids): 
                                        allids.append(iid)
                                    ii += 2; cc += 1
                        if (len(ro) > 0): 
                            tab.cells.append(ro)
                        ro = list()
                        continue
                    self.__create_uni(cgen, UnitextTable(), i, pp.pos, pp.pos + pp.length, txt, level + 1)
                    if (pp.is_table_cell_end): 
                        cel = UniTextGenCell()
                        ro.append(cel)
                        cel.content = cgen.finish(True, None)
                        cgen = UnitextGen()
                if (len(ro) > 0): 
                    tab.cells.append(ro)
                ii = 0
                first_pass697 = True
                while True:
                    if first_pass697: first_pass697 = False
                    else: ii += 1
                    if (not (ii < len(tab.cells))): break
                    has_col_span = False
                    jj = 0
                    first_pass698 = True
                    while True:
                        if first_pass698: first_pass698 = False
                        else: jj += 1
                        if (not (jj < len(tab.cells[ii]))): break
                        cel = tab.cells[ii][jj]
                        cid = Utils.indexOfList(allids, cel.tag, 0)
                        if (cid < 0): 
                            continue
                        if ((jj + 1) == len(tab.cells[ii])): 
                            if (((cid + 1) < len(allids)) and not cid in has_huge_papx_rows): 
                                has_col_span = True
                                cel.col_span = (len(allids) - cid)
                        else: 
                            cel2 = tab.cells[ii][jj + 1]
                            cid2 = Utils.indexOfList(allids, cel2.tag, 0)
                            if (cid2 < 0): 
                                continue
                            if ((cid + 1) < cid2): 
                                has_col_span = True
                                cel.col_span = (cid2 - cid)
                    if (has_col_span or not ii in has_huge_papx_rows or (ii + 1) == len(tab.cells)): 
                        continue
                    row0 = tab.cells[ii]
                    row1 = tab.cells[ii + 1]
                    if (len(row0) < len(row1)): 
                        emp = 0
                        for vv in row1: 
                            if (vv.content is None): 
                                emp += 1
                        if ((emp + 1) == len(row0)): 
                            fne = 0
                            while fne < len(row1): 
                                if (row1[fne].content is not None): 
                                    break
                                fne += 1
                            row0[fne].col_span = (len(row1) - emp)
                        else: 
                            tab.may_has_error = True
                    elif (len(row0) > len(row1)): 
                        tab.may_has_error = True
                if (gen is not None): 
                    utab = tab.convert()
                    if (utab is not None): 
                        gen.append(utab, None, -1, False)
                        gen.append_newline(False)
                continue
            if (p.is_list and gen is not None and not (isinstance(blk, UnitextList))): 
                data = p.get_property(SinglePropertyModifiers._sprm_pilfo)
                num = None
                if (data is not None and len(data) > 1): 
                    ilfo = data[1]
                    ilfo <<= 8
                    ilfo |= (data[0])
                    ilfo -= 1
                    if (ilfo >= 0 and (ilfo < len(self.__lfos))): 
                        wrapnum497 = RefOutArgWrapper(None)
                        Utils.tryGetValue(self.__m_num_styles, self.__lfos[ilfo].lsid, wrapnum497)
                        num = wrapnum497.value
                if (self.__m_dels[p.pos] != (0)): 
                    continue
                gg = UnitextGen()
                self.__create_uni(gg, UnitextList(), i, p.pos, p.pos + p.length, txt, level + 1)
                gg1 = gg.finish(num is not None, None)
                gen.append(gg1, num, p.list_level, False)
                continue
            if (gen is None): 
                continue
            Utils.setLengthStringIO(tmp, 0)
            print(txt[p.pos:p.pos+p.length], end="", file=tmp)
            cp = p.pos
            ii = 0
            first_pass699 = True
            while True:
                if first_pass699: first_pass699 = False
                else: ii += 1; cp += 1
                if (not (ii < tmp.tell())): break
                ch = Utils.getCharAtStringIO(tmp, ii)
                if (self.__m_dels[cp] != (0)): 
                    if (ii > 0): 
                        gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                    while ii < tmp.tell(): 
                        if (self.__m_dels[cp] == (0)): 
                            break
                        ii += 1; cp += 1
                    if (ii < tmp.tell()): 
                        Utils.removeStringIO(tmp, 0, ii)
                    else: 
                        Utils.setLengthStringIO(tmp, 0)
                    ii = -1
                    cp -= 1
                    continue
                sup = None
                is_sub = False
                wrapsup503 = RefOutArgWrapper(None)
                inoutres504 = Utils.tryGetValue(self.__m_super_texts, cp, wrapsup503)
                sup = wrapsup503.value
                if (inoutres504): 
                    pass
                else: 
                    wrapsup498 = RefOutArgWrapper(None)
                    inoutres499 = Utils.tryGetValue(self.__m_sub_texts, cp, wrapsup498)
                    sup = wrapsup498.value
                    if (inoutres499): 
                        is_sub = True
                if (sup is not None): 
                    if (cp == 84223): 
                        pass
                    if (ii > 0): 
                        gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                    stxt = sup.strip()
                    if (not Utils.isNullOrEmpty(stxt)): 
                        gen.append(UnitextPlaintext._new52(stxt, (UnitextPlaintextType.SUB if is_sub else UnitextPlaintextType.SUP)), None, -1, False)
                    else: 
                        pass
                    ii += len(sup)
                    if (len(sup) > 0): 
                        cp += (len(sup) - 1)
                    if (ii < tmp.tell()): 
                        Utils.removeStringIO(tmp, 0, ii)
                    else: 
                        Utils.setLengthStringIO(tmp, 0)
                    ii = -1
                    continue
                if ((ord(ch)) < 0x15): 
                    pass
                if ((ord(ch)) == 0x13): 
                    tmp2 = io.StringIO()
                    tmp3 = None
                    shape = None
                    lev = 1
                    ii0 = ii
                    cp += 1
                    ii += 1
                    while ii < tmp.tell(): 
                        ch = Utils.getCharAtStringIO(tmp, ii)
                        if ((ord(ch)) == 0x13): 
                            lev += 1
                        elif ((ord(ch)) == 0x15): 
                            lev -= 1
                            if (lev <= 0): 
                                break
                        elif ((ord(ch)) == 0x14 and lev == 1): 
                            if (tmp3 is None): 
                                tmp3 = io.StringIO()
                        print(ch, end="", file=tmp2)
                        if (tmp3 is not None): 
                            print(ch, end="", file=tmp3)
                        if (cp in self.__m_shapes): 
                            shape = self.__m_shapes[cp]
                        ii += 1; cp += 1
                    str0 = Utils.trimStartString(Utils.toStringStringIO(tmp2))
                    if (lev == 0 or ((lev == 1 and str0.startswith("TOC")))): 
                        str0_ = MSOfficeHelper._extract_spec_text(str0)
                        if (ii0 > 0): 
                            gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii0], False)
                        if (str0_ is not None): 
                            hyperlink = None
                            if (str0.startswith("HYPERLINK") and (str0.find("PAGEREF") < 0)): 
                                jj0 = str0.find('"')
                                jj1 = Utils.indexOfList(str0, '"', jj0 + 1)
                                if (jj0 > 0 and jj1 > (jj0 + 1)): 
                                    hyperlink = str0[jj0 + 1:jj0 + 1+jj1 - jj0 - 1]
                            if (hyperlink is not None): 
                                hr = UnitextHyperlink._new53(hyperlink)
                                hr.content = (UnitextPlaintext._new51(str0_))
                                gen.append(hr, None, -1, False)
                            else: 
                                gen.append_text(str0_, False)
                        elif (tmp3 is not None): 
                            tt = Utils.toStringStringIO(tmp3)
                            if (not gen.last_text.endswith(tt)): 
                                gen.append_text(tt, False)
                        if (shape is not None): 
                            gen.append(shape, None, -1, False)
                        if ((ii + 1) >= tmp.tell()): 
                            Utils.setLengthStringIO(tmp, 0)
                        else: 
                            Utils.removeStringIO(tmp, 0, ii + 1)
                        ii = -1
                        continue
                if (self.__m_footnotes is not None): 
                    if (cp in self.__m_footnotes): 
                        if ((ord(ch)) != 0x2): 
                            self.__m_footnotes[cp].custom_mark = "{0}".format(ch)
                        if (ii > 0): 
                            gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                        gen.append(self.__m_footnotes[cp], None, -1, False)
                        Utils.removeStringIO(tmp, 0, ii + 1)
                        ii = -1
                        continue
                if ((ord(ch)) == 0xB): 
                    if (ii > 0): 
                        gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                    gen.append_newline(False)
                    Utils.removeStringIO(tmp, 0, ii + 1)
                    ii = -1
                    continue
                if ((ord(ch)) == 0xC): 
                    if (ii > 0): 
                        gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                    gen.append_pagebreak()
                    Utils.removeStringIO(tmp, 0, ii + 1)
                    ii = -1
                    continue
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                    pass
                if ((ord(ch)) == 5 and self.__m_comments is not None and cp in self.__m_comments): 
                    if (ii > 0): 
                        gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                    gen.append(self.__m_comments[cp], None, -1, False)
                    Utils.removeStringIO(tmp, 0, ii + 1)
                    ii = -1
                    continue
                if ((((ord(ch)) == 7 or (ord(ch)) == 2 or (ord(ch)) == 5) or (ord(ch)) == 3 or (ord(ch)) == 4) or (ord(ch)) == 0x1F): 
                    Utils.removeStringIO(tmp, ii, 1)
                    ii -= 1
                    continue
                if ((ord(ch)) == 1 or (ord(ch)) == 8): 
                    if (ii > 0): 
                        gen.append_text(Utils.toStringStringIO(tmp)[0:0+ii], False)
                    if (cp in self.__m_shapes): 
                        gen.append(self.__m_shapes[cp], None, -1, False)
                    else: 
                        gen.append(UnitextImage(), None, -1, False)
                    Utils.removeStringIO(tmp, 0, ii + 1)
                    ii = -1
                    continue
                if ((ord(ch)) != 6 and (ord(ch)) != 0xD and ((ord(ch)) < 0x20)): 
                    if (ii >= 0 and (ii < tmp.tell())): 
                        Utils.setCharAtStringIO(tmp, ii, ' ')
            if (tmp.tell() > 0): 
                gen.append_text(Utils.toStringStringIO(tmp), False)
    
    def __load_stsh(self, word_document_stream : Stream, stsh : 'STSH') -> None:
        self.__m_style_definitions_map = dict()
        istd = 0
        first_pass700 = True
        while True:
            if first_pass700: first_pass700 = False
            else: istd += 1
            if (not (istd < len(stsh._rglpstd))): break
            std = stsh._rglpstd[istd]
            if (std is None): 
                continue
            def0_ = StyleDefinition(self, std)
            self.__m_style_definitions_map[istd] = def0_
        default_prls = list()
        ftc_bi = stsh._stshi._ftc_bi
        default_prls.append(Prl(Sprm(SinglePropertyModifiers._sprm_cftc_bi), (ftc_bi).to_bytes(2, byteorder="little")))
        ftc_asci = stsh._stshi._stshif._ftc_asci
        default_prls.append(Prl(Sprm(SinglePropertyModifiers._sprm_crg_ftc0), (ftc_asci).to_bytes(2, byteorder="little")))
        ftcfe = stsh._stshi._stshif._ftcfe
        default_prls.append(Prl(Sprm(SinglePropertyModifiers._sprm_crg_ftc1), (ftcfe).to_bytes(2, byteorder="little")))
        ftc_other = stsh._stshi._stshif._ftc_other
        default_prls.append(Prl(Sprm(SinglePropertyModifiers._sprm_crg_ftc2), (ftc_other).to_bytes(2, byteorder="little")))
        self.__default_prls = list(default_prls)
    
    def __load_character_formatting(self, word_document_stream : Stream, plcf_bte_chpx : 'PlcBteChpx') -> None:
        formattings_ = list()
        i = 0
        while i < len(plcf_bte_chpx._apn_bte_chpx): 
            word_document_stream.position = (plcf_bte_chpx._apn_bte_chpx[i]) * 512
            try: 
                papx_fkp = BasicTypesReader._read_chpx_fkp(word_document_stream)
                j = 0
                first_pass701 = True
                while True:
                    if first_pass701: first_pass701 = False
                    else: j += 1
                    if (not (j < len(papx_fkp._rgb))): break
                    start_fc = papx_fkp._rgfc[j]
                    end_fc = papx_fkp._rgfc[j + 1]
                    fc = WordDocument.__find_pos123(self.__file_character_positions, start_fc, end_fc)
                    if (fc is None): 
                        continue
                    if (start_fc < fc._offset): 
                        start_fc = fc._offset
                    if (end_fc > (fc._offset + (fc._bytes_per_character * fc._length))): 
                        end_fc = (fc._offset + (fc._bytes_per_character * fc._length))
                    para = CharacterFormatting(self, math.floor(((start_fc - fc._offset)) / fc._bytes_per_character), math.floor(((end_fc - start_fc)) / fc._bytes_per_character), fc, papx_fkp._rgb[j][1])
                    formattings_.append(para)
            except Exception as ex505: 
                pass
            i += 1
        ii = 0
        while ii < len(formattings_): 
            ch = False
            jj = 0
            while jj < (len(formattings_) - 1): 
                if (formattings_[jj].offset > formattings_[jj + 1].offset): 
                    f = formattings_[jj]
                    formattings_[jj] = formattings_[jj + 1]
                    formattings_[jj + 1] = f
                    ch = True
                jj += 1
            if (not ch): 
                break
            ii += 1
        self.__m_formattings = list(formattings_)
    
    @staticmethod
    def __find_pos123(arr : typing.List['FileCharacterPosition'], start_fc : int, end_fc : int) -> 'FileCharacterPosition':
        for f in arr: 
            if (not ((end_fc <= f._offset or ((f._offset + (f._bytes_per_character * f._length)) < start_fc)))): 
                return f
        return None
    
    def __load_paragraphs(self, word_document_stream : Stream, clx : 'Clx', plcf_bte_papx : 'PlcBtePapx') -> None:
        self.__m_paragraphs = list()
        i = 0
        while i < len(plcf_bte_papx._apn_bte_papx): 
            word_document_stream.position = (plcf_bte_papx._apn_bte_papx[i]) * 512
            er = False
            wraper506 = RefOutArgWrapper(False)
            papx_fkp = BasicTypesReader._read_papx_fkp(word_document_stream, wraper506)
            er = wraper506.value
            if (er): 
                self.__m_error = True
            j = 0
            first_pass702 = True
            while True:
                if first_pass702: first_pass702 = False
                else: j += 1
                if (not (j < len(papx_fkp._rgbx))): break
                start_fc = papx_fkp._rgfc[j]
                end_fc = papx_fkp._rgfc[j + 1]
                fc = WordDocument.__find_pos123(self.__file_character_positions, start_fc, end_fc)
                if (fc is None): 
                    continue
                if (start_fc < fc._offset): 
                    start_fc = fc._offset
                if (end_fc > (fc._offset + (fc._bytes_per_character * fc._length))): 
                    end_fc = (fc._offset + (fc._bytes_per_character * fc._length))
                para = Paragraph(self, math.floor(((start_fc - fc._offset)) / fc._bytes_per_character), math.floor(((end_fc - start_fc)) / fc._bytes_per_character), fc, papx_fkp._rgbx[j][1])
                self.__m_paragraphs.append(para)
            i += 1
        ii = 0
        while ii < len(self.__m_paragraphs): 
            ch = False
            jj = 0
            while jj < (len(self.__m_paragraphs) - 1): 
                if (self.__m_paragraphs[jj].compareTo(self.__m_paragraphs[jj + 1]) > 0): 
                    p = self.__m_paragraphs[jj]
                    self.__m_paragraphs[jj] = self.__m_paragraphs[jj + 1]
                    self.__m_paragraphs[jj + 1] = p
                    ch = True
                jj += 1
            if (not ch): 
                break
            ii += 1
        i = 0
        while i < (len(self.__m_paragraphs) - 1): 
            if ((self.__m_paragraphs[i].pos + self.__m_paragraphs[i].length) < self.__m_paragraphs[i + 1].pos): 
                self.__m_paragraphs[i].length = (self.__m_paragraphs[i + 1].pos - self.__m_paragraphs[i].pos)
            i += 1
    
    def __load_characters(self, word_document_stream : Stream, clx : 'Clx') -> None:
        if (clx is None): 
            return
        plc_pcd = clx._pcdt._plc_pcd
        file_characters = Utils.newArray(len(plc_pcd._pcds), None)
        position = 0
        i = 0
        while i < len(plc_pcd._pcds): 
            length = ((plc_pcd._cps[i + 1]) - (plc_pcd._cps[i]))
            offset = plc_pcd._pcds[i]._fc._fc
            compressed = plc_pcd._pcds[i]._fc._fcompressed
            if (compressed): 
                txt = Utils.newArray(length, None)
                word_document_stream.position = math.floor(offset / 2)
                data = ReadUtils._read_exact(word_document_stream, length)
                FcCompressedMapping._get_chars(data, 0, length, txt, 0)
                print(txt, end="", file=self.text)
            else: 
                word_document_stream.position = offset
                data = ReadUtils._read_exact(word_document_stream, length * 2)
                txt = MiscHelper.decode_string_unicode(data, 0, -1)
                print(txt, end="", file=self.text)
            fc = WordDocument.FileCharacterPosition()
            fc._offset = (math.floor(offset / 2) if compressed else offset)
            fc._bytes_per_character = (1 if compressed else 2)
            fc._length = length
            fc._character_index = position
            fc._prls = self.__expand_prm(plc_pcd._pcds[i]._prm, clx)
            file_characters[i] = fc
            position += length
            i += 1
        li = list(file_characters)
        ii = 0
        while ii < len(li): 
            ch = False
            jj = 0
            while jj < (len(li) - 1): 
                if (li[jj]._offset > li[jj + 1]._offset): 
                    f = li[jj]
                    li[jj] = li[jj + 1]
                    li[jj + 1] = f
                    ch = True
                jj += 1
            if (not ch): 
                break
            ii += 1
        file_characters = list(li)
        self.__file_character_positions = file_characters
    
    def __expand_prm(self, prm : 'Prm', clx : 'Clx') -> typing.List['Prl']:
        if (prm._fcomplex): 
            index = prm._igrpprl
            return clx._rg_prc[index]._grp_prl
        elif (prm._prm != (0x0000)): 
            sprm = 0
            wrapsprm507 = RefOutArgWrapper(0)
            inoutres508 = Utils.tryGetValue(SinglePropertyModifiers._prm0map, prm._isprm, wrapsprm507)
            sprm = wrapsprm507.value
            if (not inoutres508): 
                raise Utils.newException("Invalid Prm: isprm", None)
            value = prm._val
            prl = Prl(Sprm(sprm), bytearray([value]))
            return [prl]
        else: 
            return Utils.newArray(0, None)
    
    def get_defaults(self) -> 'StyleCollection':
        li = list()
        li.append(self.__default_prls)
        return StyleCollection(li)
    
    def get_style(self, character_position : int, level : 'FormattingLevel') -> 'StyleCollection':
        prls = list()
        if ((level) >= (FormattingLevel.CHARACTER)): 
            for formatting in self.__m_formattings: 
                if (formatting._file_character_position._contains(character_position)): 
                    if ((level) >= (FormattingLevel.CHARACTERSTYLE)): 
                        definition = formatting.style
                        if (definition is not None): 
                            definition._expand_styles(prls)
        if ((level) >= (FormattingLevel.PARAGRAPH)): 
            for paragraph in self.__m_paragraphs: 
                if (paragraph._file_character_position._contains(character_position)): 
                    if ((level) >= (FormattingLevel.PARAGRAPHSTYLE)): 
                        definition = paragraph.style
                        definition._expand_styles(prls)
        if ((level) >= (FormattingLevel.PART)): 
            for fcp in self.__file_character_positions: 
                if (fcp._contains(character_position)): 
                    prls.append(fcp._prls)
        if ((level) >= (FormattingLevel.GLOBAL)): 
            prls.append(self.__default_prls)
        return StyleCollection(prls)
    
    def __loadlfos(self, word_document_stream : Stream, length : int) -> None:
        if (length < 10): 
            return
        cou = ReadUtils._read_int(word_document_stream)
        length -= 4
        i = 0
        while i < cou: 
            lfo = WordDocument.LFO()
            self.__lfos.append(lfo)
            lfo.lsid = ReadUtils._read_int(word_document_stream)
            length -= 4
            word_document_stream.position = word_document_stream.position + (8)
            length -= 8
            lfo.dat_count = (word_document_stream.readbyte())
            length -= 1
            lfo.ibst_flt_auto_num = (word_document_stream.readbyte())
            length -= 1
            word_document_stream.position = word_document_stream.position + (2)
            length -= 2
            i += 1
        i = 0
        while i < cou: 
            if (length < 4): 
                break
            cp = ReadUtils._read_int(word_document_stream)
            length -= 4
            j = 0
            while j < self.__lfos[i].dat_count: 
                if (length < 10): 
                    break
                j += 1
            i += 1
    
    def __loadlstfs(self, word_document_stream : Stream, length : int) -> None:
        cou = ReadUtils._read_short(word_document_stream)
        length -= 2
        i = 0
        while i < cou: 
            lstf = WordDocument.LSTF()
            self.__lstfs.append(lstf)
            lstf.lsid = ReadUtils._read_int(word_document_stream)
            length -= 4
            num = UnitextGenNumStyle()
            num.id0_ = str(lstf.lsid)
            if (not lstf.lsid in self.__m_num_styles): 
                self.__m_num_styles[lstf.lsid] = num
            ReadUtils._read_int(word_document_stream)
            length -= 4
            word_document_stream.read(lstf.istds, 0, 18)
            length -= 18
            b = word_document_stream.readbyte()
            word_document_stream.readbyte()
            length -= 2
            if ((((b) & 1)) != 0): 
                lstf.fsimple_list = True
            if ((((b) & 4)) != 0): 
                lstf.fauto_num = True
            i += 1
        i = 0
        while i < cou: 
            lstf = self.__lstfs[i]
            num = self.__m_num_styles[lstf.lsid]
            j = 0
            while j < (((1 if lstf.fsimple_list else 9))): 
                lvl = WordDocument.LVL()
                lstf.lvls.append(lvl)
                lvl.istart_at = ReadUtils._read_int(word_document_stream)
                length -= 4
                lvl.nfc = (word_document_stream.readbyte())
                length -= 1
                bb = word_document_stream.readbyte()
                length -= 1
                word_document_stream.read(lvl.rgbxch_nums, 0, 9)
                length -= 9
                lvl.ixch_follow = (word_document_stream.readbyte())
                length -= 1
                lvl.dxa_indent_sav = ReadUtils._read_int(word_document_stream)
                length -= 4
                ReadUtils._read_int(word_document_stream)
                length -= 4
                lvl.cb_grpprl_chpx = (word_document_stream.readbyte())
                length -= 1
                lvl.cb_grpprl_papx = (word_document_stream.readbyte())
                length -= 1
                lvl.ilvl_restart_lim = (word_document_stream.readbyte())
                length -= 1
                word_document_stream.readbyte()
                length -= 1
                word_document_stream.position = word_document_stream.position + ((lvl.cb_grpprl_chpx) + (lvl.cb_grpprl_papx))
                length -= ((lvl.cb_grpprl_chpx) + (lvl.cb_grpprl_papx))
                tmp = io.StringIO()
                slen = ReadUtils._read_short(word_document_stream)
                length -= 2
                k = 0
                while k < slen: 
                    cod = ReadUtils._read_short(word_document_stream)
                    ch = chr(cod)
                    if (cod >= (0x20)): 
                        if (cod >= (0xF000)): 
                            chh = WingdingsHelper.get_unicode((cod) - 0xF000)
                            if ((ord(chh)) != 0): 
                                ch = chh
                        print(ch, end="", file=tmp)
                    else: 
                        print("%{0}".format(((ord(ch)) + 1)), end="", file=tmp, flush=True)
                    length -= 2
                    k += 1
                lvl.xstname = Utils.toStringStringIO(tmp)
                nl = UniTextGenNumLevel()
                num.levels.append(nl)
                nl.format0_ = lvl.xstname
                nl.start = lvl.istart_at
                mnem = None
                wrapmnem509 = RefOutArgWrapper(None)
                inoutres510 = Utils.tryGetValue(WordDocument.M_NUM_TYPES_MAP, lvl.nfc, wrapmnem509)
                mnem = wrapmnem509.value
                if (inoutres510): 
                    nl.type0_ = DocNumStyles._get_num_typ(mnem)
                else: 
                    nl.type0_ = UniTextGenNumType.DECIMAL
                j += 1
            i += 1
    
    M_NUM_TYPES_MAP = None
    
    # static constructor for class WordDocument
    @staticmethod
    def _static_ctor():
        WordDocument.M_NUM_TYPES_MAP = dict()
        WordDocument.M_NUM_TYPES_MAP[0x00] = "decimal msonfcUCRoman"
        WordDocument.M_NUM_TYPES_MAP[0x01] = "upperRoman"
        WordDocument.M_NUM_TYPES_MAP[0x02] = "lowerRoman"
        WordDocument.M_NUM_TYPES_MAP[0x03] = "upperLetter"
        WordDocument.M_NUM_TYPES_MAP[0x04] = "lowerLetter"
        WordDocument.M_NUM_TYPES_MAP[0x05] = "ordinal"
        WordDocument.M_NUM_TYPES_MAP[0x06] = "cardinalText"
        WordDocument.M_NUM_TYPES_MAP[0x07] = "ordinalText"
        WordDocument.M_NUM_TYPES_MAP[0x08] = "hex"
        WordDocument.M_NUM_TYPES_MAP[0x09] = "chicago"
        WordDocument.M_NUM_TYPES_MAP[0x0A] = "ideographDigital"
        WordDocument.M_NUM_TYPES_MAP[0x0B] = "japaneseCounting"
        WordDocument.M_NUM_TYPES_MAP[0x0C] = "Aiueo"
        WordDocument.M_NUM_TYPES_MAP[0x0D] = "Iroha"
        WordDocument.M_NUM_TYPES_MAP[0x0E] = "decimalFullWidth"
        WordDocument.M_NUM_TYPES_MAP[0x0F] = "decimalHalfWidth"
        WordDocument.M_NUM_TYPES_MAP[0x10] = "japaneseLegal"
        WordDocument.M_NUM_TYPES_MAP[0x11] = "japaneseDigitalTenThousand"
        WordDocument.M_NUM_TYPES_MAP[0x12] = "decimalEnclosedCircle"
        WordDocument.M_NUM_TYPES_MAP[0x13] = "decimalFullWidth2"
        WordDocument.M_NUM_TYPES_MAP[0x14] = "aiueoFullWidth"
        WordDocument.M_NUM_TYPES_MAP[0x15] = "irohaFullWidth"
        WordDocument.M_NUM_TYPES_MAP[0x16] = "decimalZero"
        WordDocument.M_NUM_TYPES_MAP[0x17] = "bullet"
        WordDocument.M_NUM_TYPES_MAP[0x18] = "ganada"
        WordDocument.M_NUM_TYPES_MAP[0x19] = "chosung"
        WordDocument.M_NUM_TYPES_MAP[0x1A] = "decimalEnclosedFullstop"
        WordDocument.M_NUM_TYPES_MAP[0x1D] = "ideographEnclosedCircle"
        WordDocument.M_NUM_TYPES_MAP[0x1E] = "ideographTraditional"
        WordDocument.M_NUM_TYPES_MAP[0x1F] = "ideographZodiac"
        WordDocument.M_NUM_TYPES_MAP[0x20] = "ideographZodiacTraditional"
        WordDocument.M_NUM_TYPES_MAP[0x21] = "taiwaneseCounting"
        WordDocument.M_NUM_TYPES_MAP[0x22] = "ideographLegalTraditional"
        WordDocument.M_NUM_TYPES_MAP[0x23] = "taiwaneseCountingThousand"
        WordDocument.M_NUM_TYPES_MAP[0x24] = "taiwaneseDigital"
        WordDocument.M_NUM_TYPES_MAP[0x25] = "chineseCounting"
        WordDocument.M_NUM_TYPES_MAP[0x26] = "chineseLegalSimplified"
        WordDocument.M_NUM_TYPES_MAP[0x27] = "chineseCountingThousand"
        WordDocument.M_NUM_TYPES_MAP[0x28] = "decimal"
        WordDocument.M_NUM_TYPES_MAP[0x29] = "koreanDigital"
        WordDocument.M_NUM_TYPES_MAP[0x2A] = "koreanCounting"
        WordDocument.M_NUM_TYPES_MAP[0x2B] = "koreanLegal"
        WordDocument.M_NUM_TYPES_MAP[0x2C] = "koreanDigital2"
        WordDocument.M_NUM_TYPES_MAP[0x2D] = "hebrew1"
        WordDocument.M_NUM_TYPES_MAP[0x2E] = "arabicAlpha"
        WordDocument.M_NUM_TYPES_MAP[0x2F] = "hebrew2"
        WordDocument.M_NUM_TYPES_MAP[0x30] = "arabicAbjad"
        WordDocument.M_NUM_TYPES_MAP[0x31] = "hindiVowels"
        WordDocument.M_NUM_TYPES_MAP[0x32] = "hindiConsonants"
        WordDocument.M_NUM_TYPES_MAP[0x33] = "hindiNumbers"
        WordDocument.M_NUM_TYPES_MAP[0x34] = "hindiCounting"
        WordDocument.M_NUM_TYPES_MAP[0x35] = "thaiLetters"
        WordDocument.M_NUM_TYPES_MAP[0x36] = "thaiNumbers"
        WordDocument.M_NUM_TYPES_MAP[0x37] = "thaiCounting"
        WordDocument.M_NUM_TYPES_MAP[0x38] = "vietnameseCounting"
        WordDocument.M_NUM_TYPES_MAP[0x39] = "numberInDash"
        WordDocument.M_NUM_TYPES_MAP[0x3A] = "russianLower"
        WordDocument.M_NUM_TYPES_MAP[0x3B] = "russianUpper"

WordDocument._static_ctor()