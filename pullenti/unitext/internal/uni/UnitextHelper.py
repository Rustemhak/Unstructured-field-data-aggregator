# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import base64
import xml.etree
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.UnilayPage import UnilayPage
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.internal.misc.TiffHelper import TiffHelper
from pullenti.unitext.internal.misc.MyXmlReader import MyXmlReader
from pullenti.unitext.internal.word.MSOfficeHelper import MSOfficeHelper
from pullenti.unitext.UnitextDocblock import UnitextDocblock
from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextListitem import UnitextListitem
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.UnitextMiscType import UnitextMiscType
from pullenti.util.FileFormatsHelper import FileFormatsHelper
from pullenti.unitext.UnitextService import UnitextService
from pullenti.unitext.UnitextMisc import UnitextMisc
from pullenti.unitext.FileFormatClass import FileFormatClass
from pullenti.unitext.internal.uni.StyleHelper import StyleHelper
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak

class UnitextHelper:
    
    @staticmethod
    def create(file_name : str, file_content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        from pullenti.unitext.UnitextNewline import UnitextNewline
        from pullenti.util.ArchiveHelper import ArchiveHelper
        from pullenti.unitext.UnitextList import UnitextList
        from pullenti.unitext.UnitextDocument import UnitextDocument
        from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
        from pullenti.unitext.UnitextTable import UnitextTable
        if (file_content is None): 
            if (file_name is None): 
                return UnitextDocument._new357(FileFormat.UNKNOWN, "Not filename, not content...".format(file_name))
            file_name = pathlib.PurePath(file_name).absolute()
            if (not pathlib.Path(file_name).is_file()): 
                return UnitextDocument._new357(FileFormat.UNKNOWN, "File '{0}' not exists".format(file_name))
        frm = FileFormatsHelper.analize_file_format(file_name, file_content)
        doc = None
        try: 
            if (UnitextService.EXTENSION is not None): 
                doc = UnitextService.EXTENSION.create_document(frm, file_name, file_content, pars)
            if (doc is None): 
                doc = UnitextHelper.__create(frm, file_name, file_content, pars)
            if (doc is None): 
                doc = UnitextDocument._new357(frm, ("Format unknown" if frm == FileFormat.UNKNOWN else "Can't create document"))
        except Exception as ex: 
            doc = UnitextDocument._new357(frm, str(ex))
        if (doc.source_file_name is None): 
            doc.source_file_name = file_name
        all0_ = list()
        doc.get_all_items(all0_, 0)
        in_hyps = list()
        ancs = dict()
        for it in all0_: 
            mi = Utils.asObjectOrNull(it, UnitextMisc)
            if (mi is not None and mi.typ == UnitextMiscType.ANCHOR): 
                if (not mi.id0_ in ancs): 
                    ancs[mi.id0_] = mi
                mi.tag = None
            hyp = Utils.asObjectOrNull(it, UnitextHyperlink)
            if (hyp is not None and hyp.href is not None and hyp.is_internal): 
                in_hyps.append(hyp)
                if (hyp.content is None): 
                    cnt = Utils.asObjectOrNull(hyp.parent, UnitextContainer)
                    if (cnt is not None): 
                        i = cnt.get_child_index_of(hyp)
                        if (i >= 0 and ((i + 1) < len(cnt.children))): 
                            i0 = i
                            i += 1
                            vv = cnt.children[i]
                            while (isinstance(vv, UnitextNewline)) and ((i + 1) < len(cnt.children)):
                                i += 1
                                vv = cnt.children[i]
                            if (not (isinstance(vv, UnitextNewline))): 
                                hyp.content = vv
                                vv.parent = (hyp)
                                cnt.children[i] = (hyp)
                                del cnt.children[i0]
            img = Utils.asObjectOrNull(it, UnitextImage)
            if (img is not None): 
                if (img.content is None and img.id0_ is not None): 
                    if (img.id0_.startswith("data:image")): 
                        ii = img.id0_.find("base64,")
                        if (ii > 0): 
                            try: 
                                img.content = base64.decodestring((img.id0_[ii + 7:]).encode('utf-8', 'ignore'))
                                img.id0_ = (None)
                            except Exception as ex: 
                                pass
                    elif (img.id0_.startswith("http") or img.id0_.startswith("www")): 
                        img.html_src_uri = img.id0_
                        continue
                if (img.content is not None and len(img.content) > 10): 
                    if (img.content[0] == (0x1F) and img.content[1] == (0x8B)): 
                        try: 
                            img.content = ArchiveHelper.decompress_gzip(img.content)
                        except Exception as ex361: 
                            pass
                if (img.content is None and img.id0_ is not None and (len(img.id0_) < 30)): 
                    continue
        refid = 1
        for h in in_hyps: 
            anc = None
            wrapanc362 = RefOutArgWrapper(None)
            inoutres363 = Utils.tryGetValue(ancs, h.href, wrapanc362)
            anc = wrapanc362.value
            if (not inoutres363): 
                continue
            cnt = Utils.asObjectOrNull(anc.parent, UnitextContainer)
            anc0 = anc
            if (cnt is not None): 
                i = cnt.get_child_index_of(anc)
                ait = None
                if (i >= 0): 
                    for j in range(i - 1, -1, -1):
                        it = cnt.children[j]
                        if (((isinstance(it, UnitextNewline)) or (isinstance(it, UnitextPagebreak)) or (isinstance(it, UnitextTable))) or (isinstance(it, UnitextList))): 
                            break
                        um = Utils.asObjectOrNull(it, UnitextMisc)
                        if (um is not None): 
                            if (um.typ == UnitextMiscType.HORIZONTALLINE): 
                                break
                            continue
                        ait = it
                    if (ait is None): 
                        j = i + 1
                        first_pass684 = True
                        while True:
                            if first_pass684: first_pass684 = False
                            else: j += 1
                            if (not (j < len(cnt.children))): break
                            it = cnt.children[j]
                            if ((isinstance(it, UnitextNewline)) or (isinstance(it, UnitextMisc)) or (isinstance(it, UnitextPagebreak))): 
                                continue
                            ait = it
                            break
                    if (ait is not None): 
                        if (ait.id0_ is None): 
                            if (refid == 101): 
                                pass
                            ait.id0_ = "{0}_ref{1}".format(ait._inner_tag, refid)
                            refid += 1
                        h.href = ait.id0_
                        anc0 = (None)
                if (i > 0 and ait is None): 
                    for j in range(i - 1, -1, -1):
                        if ((isinstance(cnt.children[j], UnitextMisc)) and cnt.children[j].typ == UnitextMiscType.ANCHOR): 
                            anc0 = (Utils.asObjectOrNull(cnt.children[j], UnitextMisc))
                        else: 
                            break
            if (anc0 is not None): 
                if (anc0 != anc): 
                    h.href = anc0.id0_
                anc0.tag = (h)
        for a in ancs.values(): 
            if (a.tag is None): 
                cnt = Utils.asObjectOrNull(a.parent, UnitextContainer)
                if (cnt is None): 
                    continue
                i = cnt.get_child_index_of(a)
                if (i >= 0): 
                    del cnt.children[i]
        return doc
    
    @staticmethod
    def load_data_from_file(file_name : str, attampts : int=0) -> bytearray:
        fstr = None
        buf = None
        try: 
            ex = None
            i = 0
            while i <= attampts: 
                try: 
                    fstr = FileStream(file_name, "rb")
                    break
                except Exception as e0_: 
                    ex = e0_
                if (i == 0 and not pathlib.Path(file_name).is_file()): 
                    break
                i += 1
            if (fstr is None): 
                raise ex
            if (fstr.length == (0)): 
                return None
            buf = Utils.newArrayOfBytes(fstr.length, 0)
            fstr.read(buf, 0, fstr.length)
        finally: 
            if (fstr is not None): 
                fstr.close()
        return buf
    
    @staticmethod
    def __create(frm : 'FileFormat', file_name : str, file_content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        from pullenti.unitext.internal.misc.EpubHelper import EpubHelper
        from pullenti.unitext.internal.misc.Fb2Helper import Fb2Helper
        from pullenti.unitext.internal.html.MhtHelper import MhtHelper
        from pullenti.unitext.UnitextDocument import UnitextDocument
        from pullenti.unitext.internal.misc.CsvHelper import CsvHelper
        from pullenti.util.TextHelper import TextHelper
        from pullenti.unitext.internal.html.HtmlHelper import HtmlHelper
        from pullenti.unitext.internal.rtf.RtfHelper import RtfHelper
        from pullenti.unitext.internal.misc.ExcelHelper import ExcelHelper
        from pullenti.util.ArchiveHelper import ArchiveHelper
        from pullenti.unitext.internal.pdf.PdfHelper import PdfHelper
        from pullenti.unitext.internal.word.DocxToText import DocxToText
        frmcl = FileFormatsHelper.get_format_class(frm)
        if (frmcl == FileFormatClass.ARCHIVE): 
            res = UnitextDocument._new63(file_name, frm)
            if (pars.ignore_inner_documents): 
                return res
            files = None
            try: 
                files = ArchiveHelper.get_file_names_from_archive(file_name, file_content)
            except Exception as ex: 
                res.error_message = ex.__str__()
                return res
            if (files is None): 
                res.error_message = "Archive format {0} not supported".format(Utils.enumToString(frm))
                return res
            if (len(files) == 0): 
                return res
            for f in files.items(): 
                ext = pathlib.PurePath(f[0]).suffix
                if (ext == ".exe" or ext == ".dll"): 
                    continue
                try: 
                    cnt = ArchiveHelper.get_file_from_archive(file_name, file_content, f[0])
                    if (cnt is None or len(cnt) == 0): 
                        continue
                    d = UnitextService.create_document(f[0], cnt, pars)
                    res.inner_documents.append(d)
                except Exception as ex: 
                    d = UnitextDocument._new63(f[0], FileFormatsHelper.analize_format(ext, None))
                    d.error_message = ex.__str__()
                    res.inner_documents.append(d)
            return res
        if (file_content is None): 
            fi = pathlib.Path(file_name)
            if (fi.stat().st_size < (10000000)): 
                file_content = UnitextHelper.load_data_from_file(file_name, 0)
        if (frm == FileFormat.RTF): 
            if (file_content is not None): 
                with MemoryStream(file_content) as mem: 
                    return RtfHelper._create_uni_doc(mem, pars)
            else: 
                with FileStream(file_name, "rb") as f: 
                    return RtfHelper._create_uni_doc(f, pars)
        if ((frm == FileFormat.DOCX or frm == FileFormat.XLSX or frm == FileFormat.PPTX) or frm == FileFormat.ODT or frm == FileFormat.DOCXML): 
            with DocxToText(file_name, file_content, frm == FileFormat.DOCXML) as d2t: 
                doc = d2t.create_uni_doc(pars.only_for_pure_text, frm, pars)
                if (doc is not None): 
                    StyleHelper.process_doc(doc)
                    doc.optimize(False, pars)
                return doc
        if (frm == FileFormat.XLSXML): 
            xm = None
            if (file_content is not None): 
                xm = MyXmlReader.create(file_content)
                return ExcelHelper._create_doc_for_xml(xm)
            else: 
                xm = MyXmlReader.create(UnitextHelper.load_data_from_file(file_name, 0))
                return ExcelHelper._create_doc_for_xml(xm)
        if (frm == FileFormat.DOC): 
            doc = None
            if (file_content is not None): 
                doc = MSOfficeHelper._uni_from_word97arr(file_content)
            else: 
                doc = MSOfficeHelper._uni_from_word97file(file_name)
            if (doc is None): 
                return None
            if ("word" in doc.attrs and doc.attrs["word"] == "6"): 
                if (pars.ignore_word6): 
                    doc = UnitextDocument._new41(FileFormat.DOC)
                    doc.error_message = "Word6 not supported"
                    return doc
            doc.optimize(False, pars)
            return doc
        if (frm == FileFormat.PDF): 
            return PdfHelper._create_uni(file_name, file_content, pars)
        if (frm == FileFormat.HTML): 
            nod = HtmlHelper.create_node(file_name, file_content, None)
            if (nod is None): 
                return None
            dir_name = None
            if (not pars.only_for_pure_text and file_name is not None and pathlib.Path(file_name).is_file()): 
                dir0_ = pathlib.PurePath(pathlib.PurePath(file_name).absolute()).parent.absolute()
                if (pathlib.Path(dir0_).is_dir()): 
                    dir_name = dir0_
            doc = HtmlHelper.create(nod, dir_name, None, pars)
            return doc
        if (frm == FileFormat.MHT or frm == FileFormat.EML): 
            fs = None
            if (file_content is None): 
                file_content = UnitextHelper.load_data_from_file(file_name, 0)
            try: 
                doc = MhtHelper._create_doc(file_content, pars, frm == FileFormat.MHT)
                if (doc is not None): 
                    doc.optimize(False, pars)
                    doc.source_file_name = file_name
                    doc.source_format = frm
                else: 
                    doc = UnitextDocument._new357(frm, "Не удалось сформировать письмо")
                return doc
            finally: 
                if (fs is not None): 
                    fs.close()
        if (frm == FileFormat.FB2): 
            return Fb2Helper.create_doc(file_name, file_content, pars)
        if (frm == FileFormat.FB3): 
            return Fb2Helper.create_doc_zip(file_name, file_content, pars)
        if (frm == FileFormat.EPUB): 
            return EpubHelper.create_doc(file_name, file_content, pars)
        if (frm == FileFormat.TXT or frm == FileFormat.CSV): 
            txt = None
            if (file_content is not None): 
                txt = TextHelper.read_string_from_bytes(file_content, False)
            else: 
                txt = TextHelper.read_string_from_file(file_name, False)
            if (Utils.isNullOrEmpty(txt)): 
                return None
            len0_ = len(txt)
            if (frm == FileFormat.CSV): 
                csv = CsvHelper._create(txt)
                if (csv is not None): 
                    return csv
            gen = UnitextGen()
            gen.append_text(txt, True)
            doc = UnitextDocument._new41(FileFormat.TXT)
            doc.content = gen.finish(True, None)
            if (doc.content is None): 
                return None
            return doc
        if (frm == FileFormat.TIF): 
            if (file_content is None): 
                file_content = UnitextHelper.load_data_from_file(file_name, 0)
            doc = TiffHelper.create_doc(file_content)
            doc.refresh_content_by_pages()
            return doc
        if (frmcl == FileFormatClass.IMAGE): 
            doc = UnitextDocument._new369(frm, file_name)
            page = UnilayPage()
            page.image_content = (Utils.ifNotNull(file_content, UnitextHelper.load_data_from_file(file_name, 0)))
            doc.pages.append(page)
            doc.refresh_content_by_pages()
            return doc
        err = UnitextDocument._new357(frm, "Unsupported format")
        if (frm != FileFormat.UNKNOWN): 
            err.error_message = "{0} {1}".format(err.error_message, Utils.enumToString(frm))
        return err
    
    @staticmethod
    def create_item(xml0_ : xml.etree.ElementTree.Element) -> 'UnitextItem':
        from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
        from pullenti.unitext.UnitextNewline import UnitextNewline
        from pullenti.unitext.UnitextList import UnitextList
        from pullenti.unitext.UnitextTablecell import UnitextTablecell
        from pullenti.unitext.UnitextTable import UnitextTable
        res = None
        swichVal = Utils.getXmlLocalName(xml0_)
        if (swichVal == "container"): 
            res = (UnitextContainer())
        elif (swichVal == "text"): 
            res = (UnitextPlaintext())
        elif (swichVal == "newline"): 
            res = (UnitextNewline())
        elif (swichVal == "pagebreak"): 
            res = (UnitextPagebreak())
        elif (swichVal == "table"): 
            res = (UnitextTable())
        elif (swichVal == "cell"): 
            res = (UnitextTablecell())
        elif (swichVal == "hyperlink"): 
            res = (UnitextHyperlink())
        elif (swichVal == "footnote"): 
            res = (UnitextFootnote())
        elif (swichVal == "list"): 
            res = (UnitextList())
        elif (swichVal == "listitem"): 
            res = (UnitextListitem())
        elif (swichVal == "image"): 
            res = (UnitextImage())
        elif (swichVal == "comment"): 
            res = (UnitextComment())
        elif (swichVal == "docblock"): 
            res = (UnitextDocblock())
        elif (swichVal == "misc"): 
            res = (UnitextMisc())
        if (res is not None): 
            res.from_xml(xml0_)
        return res
    
    @staticmethod
    def create_doc_from_text(text : str) -> 'UnitextDocument':
        from pullenti.unitext.UnitextNewline import UnitextNewline
        from pullenti.unitext.UnitextDocument import UnitextDocument
        doc = UnitextDocument._new371(Utils.ifNotNull(text, ""))
        if (Utils.isNullOrEmpty(text)): 
            return doc
        cur = None
        cnt = UnitextContainer._new372(len(text) - 1)
        doc.content = (cnt)
        cnt.parent = (doc)
        doc.end_char = (len(text) - 1)
        i = 0
        while i < len(text): 
            ch = text[i]
            if (ch == '\r' or ch == '\n'): 
                if (not (isinstance(cur, UnitextNewline))): 
                    cur = (UnitextNewline._new373(cnt))
                    cnt.children.append(cur)
                    cur.begin_char = i
                cur.end_char = i
                if (ch == '\r'): 
                    cur.count += 1
                elif (ch == '\n'): 
                    if (i == 0 or text[i - 1] != '\r'): 
                        cur.count += 1
            elif ((ord(ch)) == 0xC): 
                cur = (UnitextPagebreak._new374(cnt))
                cnt.children.append(cur)
                cur.begin_char = i
                cur.end_char = i
            else: 
                if (not (isinstance(cur, UnitextPlaintext))): 
                    cur = (UnitextPlaintext._new375(cnt))
                    cnt.children.append(cur)
                    cur.begin_char = i
                cur.end_char = i
            i += 1
        for ch in cnt.children: 
            if ((isinstance(ch, UnitextPlaintext)) and ch.begin_char <= ch.end_char): 
                ch.text = text[ch.begin_char:ch.begin_char+(ch.end_char - ch.begin_char) + 1]
        doc.generate_ids()
        return doc
    
    __m_std_params = None
    
    @staticmethod
    def get_plaintext(it : 'UnitextItem', pars : 'GetPlaintextParam'=None) -> str:
        if (it is None): 
            return None
        if (pars is None): 
            pars = UnitextHelper.__m_std_params
        res = io.StringIO()
        it.get_plaintext(res, pars)
        if (res.tell() == 0): 
            return None
        return Utils.toStringStringIO(res)
    
    _m_romans = None
    
    # static constructor for class UnitextHelper
    @staticmethod
    def _static_ctor():
        UnitextHelper.__m_std_params = GetPlaintextParam._new339(False)
        UnitextHelper._m_romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"]

UnitextHelper._static_ctor()