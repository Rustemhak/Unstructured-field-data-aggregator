# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import base64
import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.internal.misc.WingdingsHelper import WingdingsHelper
from pullenti.unitext.UnitextMiscType import UnitextMiscType
from pullenti.unitext.internal.word.DocTable import DocTable
from pullenti.unitext.internal.misc.MyXmlReader import MyXmlReader
from pullenti.unitext.UnitextPagesectionItemPages import UnitextPagesectionItemPages
from pullenti.unitext.internal.misc.SymbolHelper import SymbolHelper
from pullenti.unitext.internal.misc.ExcelHelper import ExcelHelper
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.internal.uni.IUnitextGenNumStyle import IUnitextGenNumStyle
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.UnitextStyle import UnitextStyle
from pullenti.unitext.UnitextMisc import UnitextMisc
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.misc.BorderInfo import BorderInfo
from pullenti.unitext.internal.word.DocTextStyles import DocTextStyles
from pullenti.unitext.internal.misc.MyZipFile import MyZipFile
from pullenti.unitext.internal.word.DocxPart import DocxPart
from pullenti.unitext.internal.word.DocNumStyles import DocNumStyles
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.UnitextService import UnitextService
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.internal.word.DocSection import DocSection
from pullenti.unitext.UnitextStyledFragment import UnitextStyledFragment
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.internal.misc.OdtHelper import OdtHelper

class DocxToText(object):
    
    def __init__(self, file_name : str, content : bytearray, is_xml : bool) -> None:
        self.__zip_file = None
        self.__xml_file = None
        self.__parts = list()
        self.__m_hyperlinks = dict()
        self.__m_data_controls = dict()
        self.m_styles = DocTextStyles()
        self.m_num_styles = DocNumStyles()
        self.__m_sections = list()
        self.__m_cur_section = None;
        self.__m_collontituls = dict()
        self.__m_comments = dict()
        self.__m_embeds = dict()
        self.__m_footnotes = dict()
        self.__m_lastrsid = ""
        self.__m_last_char = ' '
        if (is_xml): 
            self.__xml_file = None # new XmlDocument
            if (content is not None): 
                with MemoryStream(content) as mem: 
                    self.__xml_file = Utils.parseXmlFromStream(mem)
            else: 
                with FileStream(file_name, "rb") as fs: 
                    self.__xml_file = Utils.parseXmlFromStream(fs)
            self.__prepare_xml()
        else: 
            self.__zip_file = MyZipFile(file_name, content)
            self.__prepare_zip()
    
    def __prepare_zip(self) -> None:
        for o in self.__zip_file.entries: 
            if (o.is_directory or o.encrypted or o.uncompress_data_size == 0): 
                continue
            self.__parts.append(DocxPart._new445(o.name, o))
    
    def __prepare_xml(self) -> None:
        if (Utils.getXmlLocalName(self.__xml_file.getroot()) == "wordDocument"): 
            self.__parts.append(DocxPart._new446("word/document.xml", self.__xml_file.getroot()))
            return
        for xml0_ in self.__xml_file.getroot(): 
            if (Utils.getXmlLocalName(xml0_) == "part"): 
                p = DocxPart()
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "name"): 
                            p.name = a[1]
                            if (p.name.startswith("/")): 
                                p.name = p.name[1:]
                            break
                for x in xml0_: 
                    if (Utils.getXmlLocalName(x) == "xmlData"): 
                        for xx in x: 
                            p.xml0_ = xx
                            break
                        break
                    elif (Utils.getXmlLocalName(x) == "binaryData"): 
                        try: 
                            p.data = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
                        except Exception as ex: 
                            pass
                        break
                if (p.name is not None and ((p.xml0_ is not None or p.data is not None))): 
                    self.__parts.append(p)
    
    def close(self) -> None:
        try: 
            if (self.__zip_file is not None): 
                self.__zip_file.close()
                self.__zip_file = (None)
        except Exception as ex: 
            pass
    
    def create_uni_doc(self, only_for_pure_text : bool, frm : 'FileFormat', pars : 'CreateDocumentParam') -> 'UnitextDocument':
        sheets = dict()
        id_images = dict()
        id_embeds = dict()
        shared_strings = list()
        cell_borders = dict()
        ppt_slides = dict()
        ppt_images = dict()
        xml_doc = None
        xml_book = None
        xml_comments = None
        xml_settings = None
        xml_footnotes = None
        xml_endnotes = None
        xml_odt_content = None
        xml_odt_style = None
        for p in self.__parts: 
            if (p.name is not None and p.name.startswith("word/theme/")): 
                self.m_styles.read_theme(p.get_xml_node(False))
        for p in self.__parts: 
            if (p.is_name("word/styles.xml")): 
                self.m_styles.read_all_styles(p.get_xml_node(False))
        for p in self.__parts: 
            if (p.is_name("word/document.xml")): 
                xml_doc = p.get_xml_node(False)
            elif (p.is_name("word/footnotes.xml")): 
                xml_footnotes = p.get_xml_node(False)
            elif (p.is_name("word/endnotes.xml")): 
                xml_endnotes = p.get_xml_node(False)
            elif (p.is_name("word/styles.xml")): 
                pass
            elif (p.is_name("word/settings.xml")): 
                xml_settings = p.get_xml_node(False)
            elif (p.is_name("word/comments.xml")): 
                xml_comments = p.get_xml_node(False)
                if (xml_comments is not None): 
                    for x in xml_comments: 
                        if (Utils.getXmlLocalName(x) == "comment"): 
                            cmt = UnitextComment()
                            id0_ = None
                            if (x.attrib is not None): 
                                for a in x.attrib.items(): 
                                    if (Utils.getXmlAttrLocalName(a) == "id"): 
                                        id0_ = a[1]
                                    elif (Utils.getXmlAttrLocalName(a) == "author"): 
                                        cmt.author = a[1]
                            if (id0_ is None or id0_ in self.__m_comments): 
                                continue
                            gen = UnitextGen()
                            xxx = list()
                            xxx.append(x)
                            self.m_styles.ignore = True
                            self._read_node(xxx, gen, None, -1)
                            self.m_styles.ignore = False
                            it = gen.finish(True, None)
                            if (it is not None): 
                                tmp = io.StringIO()
                                it.get_plaintext(tmp, None)
                                if (tmp.tell() > 0): 
                                    cmt.text = Utils.toStringStringIO(tmp)
                                    self.__m_comments[id0_] = cmt
            elif (p.is_name("content.xml")): 
                xml_odt_content = p.get_xml_node(True)
            elif (p.is_name("styles.xml")): 
                xml_odt_style = p.get_xml_node(True)
            elif (p.is_name("xl/workbook.xml")): 
                xml_book = p.get_xml_node(False)
            elif (p.is_name("xl/sharedStrings.xml")): 
                xml0_ = p.get_xml_node(False)
                if (xml0_ is not None): 
                    for xx in xml0_: 
                        if (Utils.getXmlLocalName(xx) == "si"): 
                            gg = UnitextGen()
                            xxx = list()
                            xxx.append(xx)
                            self.m_styles.ignore = True
                            self._read_node(xxx, gg, None, -1)
                            self.m_styles.ignore = False
                            shared_strings.append(gg.finish(True, None))
            elif (p.is_name("xl/styles.xml")): 
                xml0_ = p.get_xml_node(False)
                if (xml0_ is not None): 
                    brdr = list()
                    for xx in xml0_: 
                        if (Utils.getXmlLocalName(xx) == "borders"): 
                            for xxx in xx: 
                                if (Utils.getXmlLocalName(xxx) == "border"): 
                                    brd = BorderInfo()
                                    brdr.append(brd)
                                    for y in xxx: 
                                        if (len(y.attrib) > 0 or len(y) > 0): 
                                            if (Utils.getXmlLocalName(y) == "left"): 
                                                brd.left = True
                                            elif (Utils.getXmlLocalName(y) == "right"): 
                                                brd.right = True
                                            elif (Utils.getXmlLocalName(y) == "top"): 
                                                brd.top = True
                                            elif (Utils.getXmlLocalName(y) == "bottom"): 
                                                brd.bottom = True
                        elif (Utils.getXmlLocalName(xx) == "cellXfs"): 
                            nu = 0
                            for xxx in xx: 
                                if (Utils.getXmlLocalName(xxx) == "xf"): 
                                    ind = 0
                                    if (xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "borderId"): 
                                                wrapind447 = RefOutArgWrapper(0)
                                                Utils.tryParseInt(a[1], wrapind447)
                                                ind = wrapind447.value
                                                break
                                    if (ind >= 0 and (ind < len(brdr))): 
                                        cell_borders[str(nu)] = brdr[ind]
                                    nu += 1
            elif (((p.is_name_starts("word/_rels/") or p.is_name_starts("xl/_rels/") or p.is_name_starts("ppt/slides/_rels/"))) and ((p.zip_entry is not None and not p.zip_entry.is_directory))): 
                xml_rels = p.get_xml_node(False)
                if (xml_rels is not None): 
                    ppt_imgs = None
                    if (p.name.startswith("ppt")): 
                        ii = p.name.find("rels/slide")
                        if (ii < 0): 
                            continue
                        nam = p.name[ii + 10:]
                        ii = nam.find('.')
                        if (ii < 0): 
                            continue
                        wrapii448 = RefOutArgWrapper(0)
                        inoutres449 = Utils.tryParseInt(nam[0:0+ii], wrapii448)
                        ii = wrapii448.value
                        if (not inoutres449): 
                            continue
                        if (ii in ppt_images): 
                            continue
                        ppt_imgs = dict()
                        ppt_images[ii] = ppt_imgs
                    for xx in xml_rels: 
                        if (xx.attrib is not None): 
                            if (Utils.getXmlAttrByName(xx.attrib, "Id") is not None and Utils.getXmlAttrByName(xx.attrib, "Target") is not None and Utils.getXmlAttrByName(xx.attrib, "Type") is not None): 
                                id0_ = Utils.getXmlAttrByName(xx.attrib, "Id")[1]
                                val = Utils.getXmlAttrByName(xx.attrib, "Target")[1]
                                typ = Utils.getXmlAttrByName(xx.attrib, "Type")[1]
                                if (typ.endswith("/header")): 
                                    self.__m_collontituls[id0_] = val
                                elif (typ.endswith("/footer")): 
                                    self.__m_collontituls[id0_] = val
                                elif (typ.endswith("/worksheet")): 
                                    sheets[id0_] = val
                                elif (typ.endswith("/image")): 
                                    if (ppt_imgs is not None): 
                                        if (not id0_ in ppt_imgs): 
                                            ppt_imgs[id0_] = val
                                    elif (not id0_ in id_images): 
                                        id_images[id0_] = val
                                elif (typ.endswith("/package")): 
                                    if (not id0_ in id_embeds): 
                                        id_embeds[id0_] = val
                                elif (typ.endswith("/hyperlink")): 
                                    if (not Utils.isNullOrEmpty(val) and not id0_ in self.__m_hyperlinks): 
                                        self.__m_hyperlinks[id0_] = val
            elif (p.is_name("word/numbering.xml")): 
                xml_num = p.get_xml_node(False)
                if (xml_num is not None): 
                    self.m_num_styles.read_all_styles(xml_num)
            elif (p.is_name_starts("ppt/slides/slide") and p.name.endswith(".xml")): 
                xml_doc = p.get_xml_node(False)
                if (xml_doc is None): 
                    continue
                gen = UnitextGen()
                xxx = list()
                xxx.append(xml_doc)
                self._read_node(xxx, gen, None, -1)
                slide = gen.finish(True, None)
                if (slide is None): 
                    continue
                nam = p.name[len("ppt/slides/slide"):]
                ii = nam.find('.')
                if (ii < 0): 
                    continue
                wrapii450 = RefOutArgWrapper(0)
                inoutres451 = Utils.tryParseInt(nam[0:0+ii], wrapii450)
                ii = wrapii450.value
                if (inoutres451): 
                    pass
                else: 
                    ii = (len(ppt_slides) + 1)
                while True: 
                    if (not ii in ppt_slides): 
                        ppt_slides[ii] = slide
                        break
                    ii += 1
        if (xml_odt_content is not None): 
            dh = OdtHelper()
            res = dh.create_uni(xml_odt_content, (None if xml_odt_style is None else xml_odt_style))
            if (res is None): 
                return None
            its = list()
            keys = list()
            res.get_all_items(its, 0)
            for it in its: 
                if ((isinstance(it, UnitextImage)) and it.id0_ is not None and not it.id0_.lower() in keys): 
                    keys.append(it.id0_.lower())
            if (len(its) > 0 and not only_for_pure_text): 
                for o in self.__zip_file.entries: 
                    kkk = o.name.lower()
                    if (not kkk in keys): 
                        continue
                    dat = o.get_data()
                    if (dat is not None and len(dat) > 0): 
                        for it in its: 
                            if ((isinstance(it, UnitextImage)) and it.id0_ is not None and it.id0_.lower() == kkk): 
                                it.content = dat
            return res
        if (len(ppt_slides) > 0): 
            res = UnitextDocument._new452(FileFormat.PPTX, self.__m_data_controls)
            cnt = UnitextContainer()
            res.content = (cnt)
            for kp in ppt_slides.items(): 
                if (len(cnt.children) > 0): 
                    cnt.children.append(UnitextPagebreak())
                cnt.children.append(kp[1])
                if (kp[0] in ppt_images): 
                    imgs = list()
                    kp[1].get_all_items(imgs, 0)
                    for it in imgs: 
                        im = Utils.asObjectOrNull(it, UnitextImage)
                        if (im is not None and Utils.ifNotNull(im.id0_, "") in ppt_images[kp[0]]): 
                            im.id0_ = ppt_images[kp[0]][im.id0_]
                            if (im.id0_.startswith("../")): 
                                im.id0_ = im.id0_[3:]
            if (not only_for_pure_text): 
                ims = list()
                res.get_all_items(ims, 0)
                for p in self.__parts: 
                    kkk = p.name.lower()
                    dat = None
                    for im in ims: 
                        if ((isinstance(im, UnitextImage)) and im.id0_ is not None): 
                            if (kkk.endswith(im.id0_)): 
                                if (dat is None): 
                                    dat = p.get_bytes()
                                im.content = dat
            return res
        if (len(id_embeds) > 0): 
            for p in self.__parts: 
                for kp in id_embeds.items(): 
                    if (not kp[0] in self.__m_embeds): 
                        if (p.name.lower().endswith(kp[1].lower())): 
                            dat = p.get_bytes()
                            if (dat is not None and len(dat) > 0): 
                                doc1 = UnitextService.create_document(p.name, dat, None)
                                if (doc1 is not None and doc1.content is not None): 
                                    self.__m_embeds[kp[0]] = doc1.content
                            break
        if (xml_doc is not None): 
            res = UnitextDocument._new452(FileFormat.DOCX, self.__m_data_controls)
            root_style = UnitextStyledFragment()
            root_style.doc = res
            if (self.m_styles.def_style is not None): 
                self.m_styles.def_style = self.m_styles.register_style(self.m_styles.def_style)
                root_style.style = self.m_styles.def_style
            self.__m_sections.append(DocSection())
            self.__m_cur_section = self.__m_sections[0].usect
            self.__m_cur_section.id0_ = "ps1"
            even_and_odd_headers = False
            if (xml_settings is not None): 
                for x in xml_settings: 
                    if (Utils.getXmlLocalName(x) == "evenAndOddHeaders"): 
                        even_and_odd_headers = True
            if (xml_footnotes is not None): 
                li = list()
                li.append(xml_footnotes)
                self.__read_footnotes(li, False, root_style)
            if (xml_endnotes is not None): 
                li = list()
                li.append(xml_endnotes)
                self.__read_footnotes(li, True, root_style)
            gen = UnitextGen()
            gen.set_style(root_style)
            xxx = list()
            xxx.append(xml_doc)
            self._read_node(xxx, gen, root_style, -1)
            body = gen.finish(True, None)
            if (body is None): 
                return None
            res.content = body
            res.content._m_styled_frag = root_style
            if (len(self.__m_sections) > 0 and not self.__m_sections[len(self.__m_sections) - 1].loaded): 
                del self.__m_sections[len(self.__m_sections) - 1]
            self.__m_cur_section = (None)
            for s in self.__m_sections: 
                res.sections.append(s.usect)
                for k in range(2):
                    ids = (s.head_ids if k == 0 else s.foot_ids)
                    pits = list()
                    for kp in ids.items(): 
                        if (not kp[1] in self.__m_collontituls): 
                            continue
                        if (not even_and_odd_headers): 
                            if (kp[0] == UnitextPagesectionItemPages.EVEN or kp[0] == UnitextPagesectionItemPages.ODD): 
                                continue
                        if (not s.title_pg): 
                            if (kp[0] == UnitextPagesectionItemPages.FIRST): 
                                continue
                        fnam = self.__m_collontituls[kp[1]]
                        sect_root_style = UnitextStyledFragment()
                        sect_root_style.doc = res
                        g = UnitextGen()
                        g.set_style(sect_root_style)
                        for p in self.__parts: 
                            kkk = p.name
                            ii = kkk.find('/')
                            if (ii < 0): 
                                continue
                            kkk = kkk[ii + 1:]
                            if (kkk != fnam): 
                                continue
                            xml0_ = p.get_xml_node(False)
                            if (xml0_ is not None): 
                                xxx.clear()
                                xxx.append(xml0_)
                                self._read_node(xxx, g, sect_root_style, -1)
                                break
                        fi = g.finish(True, None)
                        it = UnitextPagesectionItem()
                        if (k > 0): 
                            it.is_footer = True
                        it.pages = kp[0]
                        it.content = fi
                        if (it.pages == UnitextPagesectionItemPages.FIRST): 
                            pits.insert(0, it)
                        else: 
                            pits.append(it)
                    s.usect.items.extend(pits)
                    if (s.title_pg): 
                        has_title = False
                        for pi0_ in pits: 
                            if (pi0_.pages == UnitextPagesectionItemPages.FIRST): 
                                has_title = True
                        if (not has_title and len(res.sections) > 1): 
                            sprev = res.sections[len(res.sections) - 2]
                            for it in sprev.items: 
                                if (it.pages == UnitextPagesectionItemPages.FIRST and it.is_footer == ((k > 0))): 
                                    it2 = Utils.asObjectOrNull(it.clone(), UnitextPagesectionItem)
                                    s.usect.items.append(it2)
                                    break
                    if (not even_and_odd_headers): 
                        has = False
                        for pi0_ in pits: 
                            if (pi0_.pages == UnitextPagesectionItemPages.DEFAULT): 
                                has = True
                        if (not has and len(res.sections) > 1): 
                            sprev = res.sections[len(res.sections) - 2]
                            for it in sprev.items: 
                                if (it.pages == UnitextPagesectionItemPages.DEFAULT and it.is_footer == ((k > 0))): 
                                    it2 = Utils.asObjectOrNull(it.clone(), UnitextPagesectionItem)
                                    s.usect.items.append(it2)
                                    break
                    else: 
                        has = False
                        for pi0_ in pits: 
                            if (pi0_.pages == UnitextPagesectionItemPages.EVEN): 
                                has = True
                        if (not has and len(res.sections) > 1): 
                            sprev = res.sections[len(res.sections) - 2]
                            for it in sprev.items: 
                                if (it.pages == UnitextPagesectionItemPages.EVEN and it.is_footer == ((k > 0))): 
                                    it2 = Utils.asObjectOrNull(it.clone(), UnitextPagesectionItem)
                                    s.usect.items.append(it2)
                                    break
                        has = False
                        for pi0_ in pits: 
                            if (pi0_.pages == UnitextPagesectionItemPages.DEFAULT or pi0_.pages == UnitextPagesectionItemPages.ODD): 
                                has = True
                        if (not has and len(res.sections) > 1): 
                            sprev = res.sections[len(res.sections) - 2]
                            for it in sprev.items: 
                                if (((it.pages == UnitextPagesectionItemPages.DEFAULT or it.pages == UnitextPagesectionItemPages.ODD)) and it.is_footer == ((k > 0))): 
                                    it2 = Utils.asObjectOrNull(it.clone(), UnitextPagesectionItem)
                                    s.usect.items.append(it2)
                                    break
            res.styles = self.m_styles.ustyles
            if (not only_for_pure_text): 
                its = list()
                res.get_all_items(its, 0)
                iii = list()
                iiids = list()
                for i in its: 
                    if ((isinstance(i, UnitextImage)) and i.id0_ is not None and i.id0_ in id_images): 
                        iii.append(Utils.asObjectOrNull(i, UnitextImage))
                        i.tag = (id_images[i.id0_])
                        iiids.append(Utils.asObjectOrNull(i.tag, str))
                        i.id0_ = (None)
                if (len(iii) > 0): 
                    for p in self.__parts: 
                        kkk = p.name
                        if (not kkk in iiids): 
                            ii = kkk.find('/')
                            if (ii < 0): 
                                continue
                            kkk = kkk[ii + 1:]
                            if (not kkk in iiids): 
                                continue
                        dat = p.get_bytes()
                        if (dat is not None): 
                            for kp in iii: 
                                if ((Utils.asObjectOrNull(kp.tag, str)) == kkk): 
                                    kp.content = dat
            return res
        if (xml_book is not None and self.__zip_file is not None): 
            res = UnitextDocument._new452(FileFormat.XLSX, self.__m_data_controls)
            books = dict()
            for xml0_ in xml_book: 
                if (Utils.getXmlLocalName(xml0_) == "sheets"): 
                    for xx in xml0_: 
                        id0_ = None
                        nams = None
                        if (xx.attrib is not None): 
                            for a in xx.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "name"): 
                                    nams = a[1]
                                elif (Utils.getXmlAttrLocalName(a) == "id"): 
                                    id0_ = a[1]
                        if (id0_ is not None and nams is not None and not nams in books): 
                            books[id0_] = nams
            sss = dict()
            for o in self.__zip_file.entries: 
                kkk = o.name
                ii = kkk.find('/')
                if (ii < 0): 
                    continue
                kkk = kkk[ii + 1:]
                id0_ = None
                for kp in sheets.items(): 
                    if (kp[1] == kkk): 
                        id0_ = kp[0]
                        break
                if (id0_ is None): 
                    continue
                sheet_name = None
                wrapsheet_name455 = RefOutArgWrapper(None)
                Utils.tryGetValue(books, id0_, wrapsheet_name455)
                sheet_name = wrapsheet_name455.value
                dat = o.get_data()
                if (dat is None): 
                    continue
                xr = MyXmlReader.create(dat)
                cnt = ExcelHelper._read_sheet(xr, shared_strings, cell_borders, sheet_name)
                if (cnt is None): 
                    continue
                sss[id0_] = cnt
            ss = list()
            for kp in books.items(): 
                if (kp[0] in sss): 
                    if (sss[kp[0]] is not None): 
                        ss.append(sss[kp[0]])
            if (len(ss) == 0): 
                return None
            if (len(ss) == 1): 
                res.content = ss[0]
            else: 
                cnt = UnitextContainer()
                ii = 0
                while ii < len(ss): 
                    if (ii > 0): 
                        cnt.children.append(UnitextPagebreak())
                    cnt.children.append(ss[ii])
                    ii += 1
                res.content = (cnt)
            res.optimize(False, pars)
            return res
        return None
    
    def __read_footnotes(self, stack_list : typing.List[xml.etree.ElementTree.Element], end : bool, root_style : 'UnitextStyledFragment') -> None:
        node = stack_list[len(stack_list) - 1]
        for xml0_ in node: 
            if (Utils.getXmlLocalName(xml0_) == "footnote" or Utils.getXmlLocalName(xml0_) == "endnote"): 
                id0_ = None
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            id0_ = a[1]
                            if (end): 
                                id0_ = ("end" + id0_)
                            break
                if (id0_ is None or id0_ in self.__m_footnotes): 
                    continue
                gen = UnitextGen()
                gen.set_style(root_style)
                stack_list.append(xml0_)
                self._read_node(stack_list, gen, root_style, -1)
                del stack_list[len(stack_list) - 1]
                fi = gen.finish(True, None)
                if (fi is not None): 
                    self.__m_footnotes[id0_] = fi
    
    def _read_node(self, stack_nodes : typing.List[xml.etree.ElementTree.Element], gen : 'UnitextGen', sfrag : 'UnitextStyledFragment', pict_top : int) -> None:
        if (len(stack_nodes) == 0): 
            return
        node = stack_nodes[len(stack_nodes) - 1]
        for child in node: 
            if (Utils.getXmlLocalName(child) == "Fallback"): 
                stack_nodes.append(child)
                self._read_node(stack_nodes, gen, sfrag, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                return
        del_text = None
        proof_err = False
        i = 0
        first_pass691 = True
        while True:
            if first_pass691: first_pass691 = False
            else: i += 1
            if (not (i < len(node))): break
            child = node[i]
            locname = Utils.getXmlLocalName(child)
            if (Utils.isNullOrEmpty(locname)): 
                continue
            if (locname == "#text"): 
                continue
            if (proof_err): 
                continue
            swichVal = locname
            if (swichVal == "del"): 
                pass
            elif (swichVal == "delText"): 
                pass
            elif (swichVal == "moveFrom"): 
                pass
            elif (swichVal == "AlternateContent"): 
                for x in child: 
                    if (Utils.getXmlLocalName(x) == "Choice"): 
                        stack_nodes.append(x)
                        self._read_node(stack_nodes, gen, sfrag, pict_top)
                        del stack_nodes[len(stack_nodes) - 1]
                        break
            elif (swichVal == "t"): 
                text = Utils.getXmlInnerText(child)
                if (text == "Introduction"): 
                    pass
                if (Utils.isNullOrEmpty(text) or text == del_text): 
                    self.__m_last_char = ' '
                else: 
                    if (del_text is not None): 
                        if (text.startswith(del_text)): 
                            text = text[len(del_text):]
                    if (sfrag is not None and sfrag.style is not None and sfrag.style.get_attr("upper-case") == "true"): 
                        text = text.upper()
                    self.__m_last_char = text[len(text) - 1]
                    gen.append_text(text, False)
                    if (text.startswith("Дого")): 
                        pass
                del_text = (None)
            elif (swichVal == "sym"): 
                ch = None
                if (child.attrib is not None): 
                    font = None
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "font"): 
                            font = a[1]
                            break
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "char"): 
                            nn = 0
                            jj = 0
                            while jj < len(a[1]): 
                                dig = ord(a[1][jj])
                                if (dig >= 0x30 and dig <= 0x39): 
                                    nn = (((nn * 16) + dig) - 0x30)
                                elif (dig >= 0x41 and dig <= 0x46): 
                                    nn = ((((nn * 16) + dig) - 0x41) + 10)
                                elif (dig >= 0x61 and dig <= 0x66): 
                                    nn = ((((nn * 16) + dig) - 0x61) + 10)
                                jj += 1
                            if (a[1][0] == 'F'): 
                                nn -= 0xF000
                            uch = chr(0)
                            if (Utils.compareStrings(Utils.ifNotNull(font, ""), "Symbol", True) == 0): 
                                uch = SymbolHelper.get_unicode(nn)
                            else: 
                                uch = WingdingsHelper.get_unicode(nn)
                            if (uch == (chr(0))): 
                                ch = " "
                            else: 
                                ch = "{0}".format(uch)
                if (ch is not None): 
                    gen.append_text(ch, False)
                    self.__m_last_char = ch[0]
            elif (swichVal == "cr"): 
                gen.append_newline(False)
            elif (swichVal == "commentRangeStart"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            cmt = None
                            wrapcmt456 = RefOutArgWrapper(None)
                            inoutres457 = Utils.tryGetValue(self.__m_comments, Utils.ifNotNull(a[1], ""), wrapcmt456)
                            cmt = wrapcmt456.value
                            if (inoutres457): 
                                if (cmt.id0_ is None): 
                                    cmt.id0_ = ("comment" + a[1])
                                gen.append(cmt, None, -1, False)
            elif (swichVal == "commentRangeEnd"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            cmt = None
                            wrapcmt459 = RefOutArgWrapper(None)
                            inoutres460 = Utils.tryGetValue(self.__m_comments, Utils.ifNotNull(a[1], ""), wrapcmt459)
                            cmt = wrapcmt459.value
                            if (inoutres460): 
                                ecmt = UnitextComment._new458(cmt.id0_ + "_end", cmt.id0_, True)
                                cmt.twin_id = ecmt.id0_
                                ecmt.text = cmt.text
                                ecmt.author = cmt.author
                                gen.append(ecmt, None, -1, False)
                                del self.__m_comments[a[1]]
            elif (swichVal == "br"): 
                val = None
                if (child.attrib is not None and len(child.attrib) > 0 and "type" in Utils.getXmlAttrName(Utils.getXmlAttrByIndex(child.attrib, 0))): 
                    val = Utils.getXmlAttrByIndex(child.attrib, 0)[1]
                if (val == "page"): 
                    gen.append_pagebreak()
                else: 
                    is_new_line = False
                    if (gen.last_not_space_char == ':' or gen.last_not_space_char == '.'): 
                        is_new_line = True
                    if (is_new_line): 
                        gen.append_newline(False)
                    else: 
                        gen.append_newline(False)
            elif (swichVal == "pict"): 
                while True:
                    img1 = None
                    for x in child: 
                        if (Utils.getXmlLocalName(x) == "binData"): 
                            if (img1 is None): 
                                img1 = UnitextImage()
                            try: 
                                img1.content = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
                            except Exception as ex: 
                                pass
                            gen.append(img1, None, -1, False)
                        elif (Utils.getXmlLocalName(x) == "shape" and x.attrib is not None): 
                            for a in x.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "style" and a[1] is not None): 
                                    if (img1 is None): 
                                        img1 = UnitextImage()
                                    DocxToText.__set_image_size(img1, a[1])
                    if (img1 is not None and img1.content is not None): 
                        return
                    gg = UnitextGen()
                    gg.append_pagesection(self.__m_cur_section)
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gg, sfrag, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
                    it = gg.finish(True, None)
                    if (it is None): 
                        break
                    if (isinstance(it, UnitextContainer)): 
                        it.typ = UnitextContainerType.SHAPE
                    else: 
                        cnt = UnitextContainer._new92(UnitextContainerType.SHAPE)
                        cnt.children.append(it)
                        it = cnt.optimize(False, None)
                    if (it is not None): 
                        gen.append(it, None, -1, False)
                        gen.append_newline(False)
                    break
            elif (swichVal == "tab"): 
                if (Utils.getXmlLocalName(node) == "tabs"): 
                    pass
                else: 
                    gen.append_text("\t", False)
            elif (swichVal == "sectPr"): 
                self.__m_sections[len(self.__m_sections) - 1].load(child)
                se = DocSection()
                self.__m_sections.append(se)
                se.usect.id0_ = "ps{0}".format(len(self.__m_sections))
                self.__m_cur_section = se.usect
                gen.append_pagesection(self.__m_cur_section)
            elif (swichVal == "tbl"): 
                tbl = DocTable()
                stack_nodes.append(child)
                tbl.read(self, sfrag, stack_nodes)
                del stack_nodes[len(stack_nodes) - 1]
                tab = tbl.create_uni()
                if (tab is not None): 
                    gen.append(tab, None, -1, False)
            elif (swichVal == "bookmarkStart"): 
                for a in child.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "name"): 
                        if (a[1] == "_GoBack"): 
                            continue
                        mi = UnitextMisc()
                        mi.typ = UnitextMiscType.ANCHOR
                        mi.id0_ = a[1]
                        if (mi.id0_ == "_GoBack"): 
                            pass
                        gen.append(mi, None, -1, False)
                        break
            elif (swichVal == "fldSimple"): 
                ggg1 = UnitextGen()
                ggg1.append_pagesection(self.__m_cur_section)
                for a in child.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "instr"): 
                        vvv = a[1].strip()
                        if (vvv.startswith("SEQ")): 
                            ggg1.text_gen_regime = True
                stack_nodes.append(child)
                self._read_node(stack_nodes, ggg1, sfrag, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                ggt = ggg1.finish(True, None)
                if (ggg1.text_gen_regime and ggt is not None): 
                    gen.append(ggt, None, -1, False)
                else: 
                    txt = (None if ggt is None else UnitextHelper.get_plaintext(ggt, None))
                    if (not Utils.isNullOrEmpty(txt) and not gen.last_text.endswith(txt)): 
                        gen.append_text(txt, False)
            elif (swichVal == "hyperlink" or swichVal == "hlink"): 
                ok = False
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            if (a[1] in self.__m_hyperlinks): 
                                ggg = UnitextGen()
                                ggg.append_pagesection(self.__m_cur_section)
                                stack_nodes.append(child)
                                self._read_node(stack_nodes, ggg, sfrag, pict_top)
                                del stack_nodes[len(stack_nodes) - 1]
                                cnt = ggg.finish(True, None)
                                if (cnt is not None): 
                                    if (Utils.ifNotNull(a[1], "") in self.__m_hyperlinks): 
                                        try: 
                                            hr = UnitextHyperlink._new53(str(self.__m_hyperlinks[a[1]]))
                                            hr.content = cnt
                                            gen.append(hr, None, -1, False)
                                        except Exception as xx: 
                                            gen.append(cnt, None, -1, False)
                                    else: 
                                        gen.append(cnt, None, -1, False)
                                    ok = True
                                    break
                        elif (Utils.getXmlAttrLocalName(a) == "dest" or Utils.getXmlAttrLocalName(a) == "anchor"): 
                            ggg = UnitextGen()
                            ggg.append_pagesection(self.__m_cur_section)
                            stack_nodes.append(child)
                            self._read_node(stack_nodes, ggg, sfrag, pict_top)
                            del stack_nodes[len(stack_nodes) - 1]
                            cnt = ggg.finish(True, None)
                            if (cnt is not None): 
                                hr = UnitextHyperlink._new53(a[1])
                                if (Utils.getXmlAttrLocalName(a) == "anchor"): 
                                    hr.is_internal = True
                                hr.content = cnt
                                gen.append(hr, None, -1, False)
                                ok = True
                                break
                if (not ok): 
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gen, sfrag, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
            elif (swichVal == "p"): 
                while True:
                    num_style = None
                    lev = 0
                    num_txt_style = None
                    para = None
                    if (sfrag is not None): 
                        para = UnitextStyledFragment._new464(sfrag, UnitextStyledFragmentType.PARAGRAPH)
                        sfrag.children.append(para)
                    pgen = UnitextGen()
                    pgen.set_style(para)
                    pgen.append_pagesection(self.__m_cur_section)
                    hidden = False
                    for xx in child: 
                        if (Utils.getXmlLocalName(xx) == "pPr"): 
                            if (para is not None): 
                                ust0 = UnitextStyle()
                                self.m_styles.read_unitext_style(xx, ust0)
                                ust0.remove_inherit_attrs(para.parent)
                                if (ust0.get_attr("font-size") == "1pt"): 
                                    hidden = True
                                    if (sfrag is not None): 
                                        sfrag.children.remove(sfrag)
                                    break
                                para.style = self.m_styles.register_style(ust0)
                            id0_ = None
                            for xxx in xx: 
                                if (Utils.getXmlLocalName(xxx) == "numPr"): 
                                    for chh in xxx: 
                                        if (Utils.getXmlLocalName(chh) == "numId" and chh.attrib is not None and len(chh.attrib) == 1): 
                                            id0_ = Utils.getXmlAttrByIndex(chh.attrib, 0)[1]
                                        elif (Utils.getXmlLocalName(chh) == "ilvl" and chh.attrib is not None and len(chh.attrib) == 1): 
                                            wraplev465 = RefOutArgWrapper(0)
                                            Utils.tryParseInt(Utils.ifNotNull(Utils.getXmlAttrByIndex(chh.attrib, 0)[1], ""), wraplev465)
                                            lev = wraplev465.value
                                elif (Utils.getXmlLocalName(xxx) == "listPr"): 
                                    num_style = (DocNumStyles._read_number_style(xxx))
                                    lev = num_style.lvl
                                elif (Utils.getXmlLocalName(xxx) == "pStyle"): 
                                    num_txt_style = self.m_styles.get_style(xxx, "val")
                                    if (num_txt_style is not None and num_txt_style.num_id is not None): 
                                        if (id0_ is not None or lev > 0): 
                                            pass
                                        else: 
                                            id0_ = num_txt_style.num_id
                                            lev = num_txt_style.num_lvl
                            num_style = (self.m_num_styles.get_style(id0_))
                    if (hidden): 
                        break
                    gen.append_pagesection(self.__m_cur_section)
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, pgen, para, pict_top)
                    pgen.text_gen_regime = False
                    if (pict_top < 0): 
                        pgen.append_newline(False)
                        if (para is not None and para.style is not None and para.style.get_attr("heading-level") is not None): 
                            pgen.append_newline(False)
                    fi = pgen.finish(False, None)
                    if (fi is not None): 
                        gen.append(fi, num_style, lev, False)
                    del stack_nodes[len(stack_nodes) - 1]
                    break
            elif (swichVal == "r"): 
                while True:
                    if (child.attrib is not None): 
                        for a in child.attrib.items(): 
                            if (Utils.getXmlAttrLocalName(a) == "rsidRPr"): 
                                if (not Utils.isNullOrEmpty(self.__m_lastrsid) and Utils.compareStrings(a[1], self.__m_lastrsid, True) != 0): 
                                    self.__m_lastrsid = Utils.getXmlAttrLocalName(a)
                                    if ((ord(gen.last_char)) != 0 and not Utils.isWhitespace(gen.last_char)): 
                                        gen.append_text(" ", False)
                    ust = None
                    is_sup = -1
                    fld_char_begin = False
                    hidden2 = False
                    gtr = gen.text_gen_regime
                    for rpr in child: 
                        if (Utils.getXmlLocalName(rpr) == "rPr"): 
                            ust = UnitextStyle()
                            self.m_styles.read_unitext_style(rpr, ust)
                            if (sfrag is not None): 
                                ust.remove_inherit_attrs(sfrag)
                            if (ust.get_attr("font-size") == "1pt"): 
                                hidden2 = True
                                break
                            ust = self.m_styles.register_style(ust)
                            for xxx in rpr: 
                                if (Utils.getXmlLocalName(xxx) == "vertAlign" and xxx.attrib is not None and len(xxx.attrib) > 0): 
                                    if (Utils.getXmlAttrByIndex(xxx.attrib, 0)[1] == "superscript"): 
                                        is_sup = 1
                                    elif (Utils.getXmlAttrByIndex(xxx.attrib, 0)[1] == "subscript"): 
                                        is_sup = 0
                        elif (Utils.getXmlLocalName(rpr) == "fldChar"): 
                            for aa in rpr.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(aa) == "fldCharType" and aa[1] == "begin"): 
                                    fld_char_begin = True
                    if (hidden2): 
                        break
                    if (fld_char_begin): 
                        gg1 = UnitextGen()
                        anchor = None
                        gg1.append_pagesection(self.__m_cur_section)
                        ii = -1
                        instr_text = None
                        j = i
                        while j < len(node): 
                            chh = node[j]
                            if (Utils.getXmlLocalName(chh) != "r"): 
                                break
                            for rpr in chh: 
                                if (Utils.getXmlLocalName(rpr) == "instrText" or Utils.getXmlLocalName(rpr) == "instr"): 
                                    if (instr_text is None): 
                                        instr_text = io.StringIO()
                                    print(Utils.ifNotNull(Utils.getXmlInnerText(rpr), ""), end="", file=instr_text)
                                elif (Utils.getXmlLocalName(rpr) == "fldChar"): 
                                    for aa in rpr.attrib.items(): 
                                        if (Utils.getXmlAttrLocalName(aa) == "fldCharType" and aa[1] == "end"): 
                                            fld_char_begin = False
                            stack_nodes.append(chh)
                            self._read_node(stack_nodes, gg1, sfrag, pict_top)
                            del stack_nodes[len(stack_nodes) - 1]
                            ii = j
                            if (not fld_char_begin): 
                                break
                            j += 1
                        if (instr_text is not None): 
                            vvv = Utils.toStringStringIO(instr_text).strip()
                            if (vvv.startswith("SEQ ")): 
                                gg1.text_gen_regime = True
                            iii = vvv.find("REF ")
                            if (iii >= 0 and not "STYLEREF" in vvv): 
                                vvv = vvv[iii + 4:]
                                k = 1
                                while k < len(vvv): 
                                    if (Utils.isWhitespace(vvv[k])): 
                                        vvv = vvv[0:0+k]
                                        break
                                    k += 1
                                anchor = vvv
                        if (anchor is not None): 
                            hy = UnitextHyperlink._new466(True, anchor)
                            hy.content = gg1.finish(False, None)
                            gen.append(hy, None, -1, False)
                            i = ii
                            break
                        if (gg1.text_gen_regime): 
                            tmp = gg1.finish(True, None)
                            if (tmp is not None): 
                                gen.append(tmp, None, -1, False)
                                i = ii
                                break
                            else: 
                                gen.text_gen_regime = True
                    if (is_sup >= 0): 
                        gg1 = UnitextGen()
                        gg1.append_pagesection(self.__m_cur_section)
                        stack_nodes.append(child)
                        self._read_node(stack_nodes, gg1, sfrag, pict_top)
                        del stack_nodes[len(stack_nodes) - 1]
                        tmp = gg1.finish(True, None)
                        if (tmp is None): 
                            break
                        tt = UnitextHelper.get_plaintext(tmp, None)
                        if (tt is None): 
                            tt = ""
                        tt = tt.strip()
                        if (tt.startswith("<") and tt.endswith(">")): 
                            tt = tt[1:1+len(tt) - 2]
                        if (len(tt) > 0 and (len(tt) < 10)): 
                            tp = UnitextPlaintext._new52(tt, (UnitextPlaintextType.SUB if is_sup == 0 else UnitextPlaintextType.SUP))
                            gen.append(tp, None, -1, False)
                            break
                    stack_nodes.append(child)
                    if (ust is None or sfrag is None): 
                        self._read_node(stack_nodes, gen, sfrag, pict_top)
                    else: 
                        ifr = UnitextStyledFragment._new464(sfrag, UnitextStyledFragmentType.INLINE)
                        ifr.style = ust
                        gg1 = UnitextGen()
                        gg1.set_style(ifr)
                        gg1.append_pagesection(self.__m_cur_section)
                        gg1.text_gen_regime = gen.text_gen_regime
                        self._read_node(stack_nodes, gg1, ifr, pict_top)
                        v = gg1.finish(False, None)
                        if (v is not None): 
                            gen.append(v, None, -1, False)
                            sfrag.children.append(ifr)
                            gen.text_gen_regime = False
                    del stack_nodes[len(stack_nodes) - 1]
                    break
            elif (swichVal == "footnoteReference"): 
                while True:
                    del_text = (None)
                    if (child.attrib is None): 
                        break
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "customMarkFollows" and a[1] == "1" and ((i + 1) < len(node))): 
                            ch1 = node[i + 1]
                            if (Utils.getXmlLocalName(ch1) == "t"): 
                                del_text = Utils.getXmlInnerText(ch1)
                                i += 1
                                break
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id" and a[1] in self.__m_footnotes): 
                            cnt = self.__m_footnotes[a[1]]
                            if (not Utils.isNullOrEmpty(del_text)): 
                                pl = Utils.asObjectOrNull(cnt, UnitextPlaintext)
                                if (pl is not None and pl.text.startswith(del_text)): 
                                    pl.text = pl.text[len(del_text):].strip()
                            if ((cnt._m_styled_frag is not None and cnt._m_styled_frag.parent is None and (isinstance(cnt, UnitextContainer))) and sfrag is not None): 
                                cc = Utils.asObjectOrNull(cnt, UnitextContainer)
                                if (len(cc.children) == 1 and (isinstance(cc.children[0], UnitextContainer))): 
                                    cnt = cc.children[0]
                                    if (cnt._m_styled_frag is not None and cnt._m_styled_frag.parent is not None): 
                                        cnt._m_styled_frag.typ = UnitextStyledFragmentType.FOOTNOTE
                                        cnt._m_styled_frag.parent.children.remove(cnt._m_styled_frag)
                                        sfrag.children.append(cnt._m_styled_frag)
                                        cnt._m_styled_frag.parent = sfrag
                            gen.append(UnitextFootnote._new469(cnt, del_text), None, -1, False)
                            break
                    break
            elif (swichVal == "endnoteReference"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id" and "end" + a[1] in self.__m_footnotes): 
                            cnt = self.__m_footnotes["end" + a[1]]
                            if ((cnt._m_styled_frag is not None and cnt._m_styled_frag.parent is None and (isinstance(cnt, UnitextContainer))) and sfrag is not None): 
                                cc = Utils.asObjectOrNull(cnt, UnitextContainer)
                                if (len(cc.children) == 1 and (isinstance(cc.children[0], UnitextContainer))): 
                                    cnt = cc.children[0]
                                    if (cnt._m_styled_frag is not None and cnt._m_styled_frag.parent is not None): 
                                        cnt._m_styled_frag.typ = UnitextStyledFragmentType.FOOTNOTE
                                        cnt._m_styled_frag.parent.children.remove(cnt._m_styled_frag)
                                        sfrag.children.append(cnt._m_styled_frag)
                                        cnt._m_styled_frag.parent = sfrag
                            gen.append(UnitextFootnote._new267(cnt, True), None, -1, False)
                            break
            elif (swichVal == "footnote" or swichVal == "endnote"): 
                while True:
                    gg2 = UnitextGen()
                    gg2.append_pagesection(self.__m_cur_section)
                    stack_nodes.append(child)
                    self._read_node(stack_nodes, gg2, sfrag, pict_top)
                    del stack_nodes[len(stack_nodes) - 1]
                    tmp2 = gg2.finish(True, None)
                    if (tmp2 is None): 
                        break
                    fn = UnitextFootnote._new471(locname == "endnote", tmp2)
                    gen.append(fn, None, -1, False)
                    break
            elif (swichVal == "blip"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "embed"): 
                            img = UnitextImage._new94(a[1])
                            gen.append(img, None, -1, False)
                            for ii in range(len(stack_nodes) - 1, -1, -1):
                                for xxx in stack_nodes[ii]: 
                                    if (Utils.getXmlLocalName(xxx) == "extent" and xxx.attrib is not None): 
                                        xw = 0
                                        yh = 0
                                        for aa in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(aa) == "cx"): 
                                                wrapxw473 = RefOutArgWrapper(0)
                                                Utils.tryParseInt(aa[1], wrapxw473)
                                                xw = wrapxw473.value
                                            elif (Utils.getXmlAttrLocalName(aa) == "cy"): 
                                                wrapyh474 = RefOutArgWrapper(0)
                                                Utils.tryParseInt(aa[1], wrapyh474)
                                                yh = wrapyh474.value
                                        if (xw > 0 and yh > 0): 
                                            img.width = "{0}pt".format(math.floor((xw * 72) / 914400))
                                            img.height = "{0}pt".format(math.floor((yh * 72) / 914400))
                            break
            elif (swichVal == "imagedata"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            img = UnitextImage._new94(a[1])
                            gen.append(img, None, -1, False)
                            if (Utils.getXmlLocalName(node) == "shape" and node.attrib is not None): 
                                for aa in node.attrib.items(): 
                                    if (Utils.getXmlAttrLocalName(aa) == "style"): 
                                        DocxToText.__set_image_size(img, aa[1])
                                        break
                            break
            elif (swichVal == "OLEObject"): 
                if (child.attrib is not None): 
                    for a in child.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            if (a[1] in self.__m_embeds): 
                                gen.append(self.__m_embeds[a[1]], None, -1, False)
                                break
            elif (swichVal == "sdt"): 
                tag = None
                valu = None
                ust1 = None
                for x in child: 
                    if (Utils.getXmlLocalName(x) == "sdtPr"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "tag"): 
                                tag = DocxToText.__get_attr_value(xx, "val")
                            elif (Utils.getXmlLocalName(xx) == "date"): 
                                valu = DocxToText.__get_attr_value(xx, "fullDate")
                        ust1 = UnitextStyle()
                        self.m_styles.read_unitext_style(x, ust1)
                        if (sfrag is not None): 
                            ust1.remove_inherit_attrs(sfrag)
                        ust1 = self.m_styles.register_style(ust1)
                for x in child: 
                    if (Utils.getXmlLocalName(x) == "sdtContent"): 
                        sfrag1 = sfrag
                        if (ust1 is not None): 
                            sfrag1 = UnitextStyledFragment._new476(UnitextStyledFragmentType.INLINE, ust1, sfrag1)
                            sfrag.children.append(sfrag1)
                        gg3 = UnitextGen()
                        gg3.set_style(sfrag1)
                        gg3.append_pagesection(self.__m_cur_section)
                        stack_nodes.append(x)
                        self._read_node(stack_nodes, gg3, sfrag1, pict_top)
                        del stack_nodes[len(stack_nodes) - 1]
                        tmp3 = gg3.finish(True, None)
                        if (tmp3 is None): 
                            break
                        if (valu is None): 
                            valu = UnitextHelper.get_plaintext(tmp3, None)
                        if (isinstance(tmp3, UnitextContainer)): 
                            tmp3.typ = UnitextContainerType.CONTENTCONTROL
                        else: 
                            ccc = UnitextContainer._new427(UnitextContainerType.CONTENTCONTROL, sfrag1)
                            ccc.children.append(tmp3)
                            tmp3.parent = (ccc)
                            tmp3 = (ccc)
                        tmp3.html_title = "Content control: {0}".format(Utils.ifNotNull(tag, "?"))
                        tmp3.data = valu
                        tmp3.id0_ = tag
                        gen.append(tmp3, None, -1, False)
                if (tag is not None and valu is not None): 
                    if (not tag in self.__m_data_controls): 
                        self.__m_data_controls[tag] = valu
            elif (swichVal == "ffData"): 
                nam1 = None
                for x in child: 
                    if (Utils.getXmlLocalName(x) == "name"): 
                        nam1 = DocxToText.__get_attr_value(x, "val")
                    elif (Utils.getXmlLocalName(x) == "textInput"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "default"): 
                                val1 = DocxToText.__get_attr_value(xx, "val")
                                if (val1 is not None and nam1 is not None): 
                                    if (not nam1 in self.__m_data_controls): 
                                        self.__m_data_controls[nam1] = val1
            elif (swichVal == "rect"): 
                for a in child.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "style"): 
                        if (pict_top < 0): 
                            pict_top = 0
                        for s in Utils.splitString(a[1], ';', False): 
                            ii = s.find(':')
                            if (ii <= 0): 
                                continue
                            key = s[0:0+ii].strip().lower()
                            va = s[ii + 1:].strip()
                            if (key == "position"): 
                                if (va != "absolute"): 
                                    break
                            if (key != "top"): 
                                continue
                            for j in range(len(va) - 1, 0, -1):
                                if (str.isdigit(va[j])): 
                                    wrapii478 = RefOutArgWrapper(0)
                                    inoutres479 = Utils.tryParseInt(va[0:0+j + 1], wrapii478)
                                    ii = wrapii478.value
                                    if (not inoutres479): 
                                        break
                                    if (ii > pict_top): 
                                        gen.append_newline(True)
                                        pict_top = ii
                                    break
                            break
                stack_nodes.append(child)
                self._read_node(stack_nodes, gen, sfrag, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
            elif (swichVal == "drawing"): 
                gg4 = UnitextGen()
                gg4.set_style(sfrag)
                gg4.append_pagesection(self.__m_cur_section)
                stack_nodes.append(child)
                self._read_node(stack_nodes, gg4, sfrag, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                drsh = UnitextContainer._new427(UnitextContainerType.SHAPE, sfrag)
                tgg4 = gg4.finish(False, None)
                if (tgg4 is not None): 
                    drsh.children.append(tgg4)
                gen.append(drsh, None, -1, False)
            else: 
                if ((pict_top < 0) and Utils.getXmlLocalName(child) == "txbxContent"): 
                    gen.append_text(" ", False)
                stack_nodes.append(child)
                self._read_node(stack_nodes, gen, sfrag, pict_top)
                del stack_nodes[len(stack_nodes) - 1]
                if ((pict_top < 0) and Utils.getXmlLocalName(child) == "txbxContent"): 
                    gen.append_text(" ", False)
    
    @staticmethod
    def __set_image_size(img : 'UnitextImage', style : str) -> None:
        ii = style.find("width:")
        if (ii >= 0): 
            img.width = style[ii + 6:].strip()
            ii = img.width.find(';')
            if (((ii)) > 0): 
                img.width = img.width[0:0+ii].strip()
        ii = style.find("height:")
        if (ii >= 0): 
            img.height = style[ii + 7:].strip()
            ii = img.height.find(';')
            if (((ii)) > 0): 
                img.height = img.height[0:0+ii].strip()
    
    @staticmethod
    def __get_attr_value(n : xml.etree.ElementTree.Element, attr_name : str) -> str:
        if (n.attrib is not None): 
            for a in n.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == attr_name): 
                    return a[1]
        return None
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()