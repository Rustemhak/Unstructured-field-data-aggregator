# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import math
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.pdf.PdfImage import PdfImage
from pullenti.unitext.internal.pdf.PdfText import PdfText
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.internal.uni.UnilayoutHelper import UnilayoutHelper
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.internal.pdf.PdfFile import PdfFile
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.pdf.PdfFig import PdfFig
from pullenti.unitext.UnilayRectangle import UnilayRectangle
from pullenti.unitext.UnilayPage import UnilayPage
from pullenti.unitext.internal.pdf.PdfPage import PdfPage

class PdfHelper:
    """ Работа с PDF """
    
    @staticmethod
    def _create_uni(pdf_file_name : str, file_content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        pages = list()
        doc = UnitextDocument._new41(FileFormat.PDF)
        try: 
            with PdfFile() as file: 
                file.open0_(pdf_file_name, file_content)
                if (file.encrypt is not None): 
                    doc.error_message = "Can't extract pages from encrypted pdf"
                if (file.root_object is not None): 
                    mt = file.root_object.get_dictionary("Metadata", None)
                    if (mt is not None): 
                        dat = mt.extract_data()
                        if (dat is not None): 
                            try: 
                                str0_ = dat.decode("UTF-8", 'ignore')
                                i = str0_.find("?>")
                                if (i > 0): 
                                    str0_ = str0_[i + 2:].strip()
                                xml0_ = None # new XmlDocument
                                xml0_ = Utils.parseXmlFromString(str0_)
                                PdfHelper.__read_metadata0(doc, xml0_.getroot(), None)
                            except Exception as ex218: 
                                pass
                if (file.info is not None): 
                    str0_ = file.info.get_string_item("Title")
                    if (not Utils.isNullOrEmpty(str0_) and not "title" in doc.attrs): 
                        doc.attrs["title"] = str0_
                    str0_ = file.info.get_string_item("Author")
                    if (not Utils.isNullOrEmpty(str0_) and not "author" in doc.attrs): 
                        doc.attrs["author"] = str0_
                for pdic in file.pages: 
                    ppage = PdfPage(pdic)
                    up = UnilayPage()
                    up.width = (math.floor(ppage.width))
                    up.height = (math.floor(ppage.height))
                    pages.append(up)
                    up.number = len(pages)
                    for it in ppage.items: 
                        if (isinstance(it, PdfFig)): 
                            continue
                        r = UnilayRectangle()
                        r.left = it.left
                        r.top = it.top
                        r.right = it.right
                        r.bottom = it.bottom
                        r.page = up
                        if (isinstance(it, PdfText)): 
                            r.text = it.text
                        elif (isinstance(it, PdfImage)): 
                            r.image_content = it.content
                            r.tag = (it)
                        up.rects.append(r)
                    if (up.image_content is None and len(up.rects) > 0 and up.rects[0].image_content is not None): 
                        up.image_content = up.rects[0].image_content
                        del up.rects[0]
        except Exception as ex: 
            doc.error_message = ex.__str__()
            return doc
        if (pages is None or len(pages) == 0 or doc.error_message is not None): 
            if (doc.error_message is None): 
                doc.error_message = "Can't extract pages from pdf-file"
            return doc
        doc.pages = pages
        UnilayoutHelper.create_content_from_pages(doc, False)
        cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is None): 
            return doc
        i = 0
        first_pass647 = True
        while True:
            if first_pass647: first_pass647 = False
            else: i += 1
            if (not (i < len(cnt.children))): break
            pt = Utils.asObjectOrNull(cnt.children[i], UnitextPlaintext)
            if (pt is None): 
                continue
            if (not pt.is_whitespaces): 
                continue
            if (i == 0 or (isinstance(cnt.children[i - 1], UnitextNewline)) or (isinstance(cnt.children[i - 1], UnitextPagebreak))): 
                pass
            else: 
                continue
            if ((i + 1) == len(cnt.children) or (isinstance(cnt.children[i + 1], UnitextNewline)) or (isinstance(cnt.children[i + 1], UnitextPagebreak))): 
                pass
            else: 
                continue
            del cnt.children[i]
            i -= 1
        doc.content = doc.content.optimize(True, None)
        return doc
    
    @staticmethod
    def __read_metadata0(doc : 'UnitextDocument', xml0_ : xml.etree.ElementTree.Element, typ : str) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "title"): 
                PdfHelper.__read_metadata0(doc, x, "title")
            elif (Utils.getXmlLocalName(x) == "creator"): 
                PdfHelper.__read_metadata0(doc, x, "author")
            elif (Utils.getXmlLocalName(x) == "subject"): 
                PdfHelper.__read_metadata0(doc, x, "subject")
            elif (Utils.getXmlLocalName(x) == "Keywords"): 
                val = Utils.getXmlInnerText(x)
                if (not Utils.isNullOrEmpty(val) and not "keywords" in doc.attrs): 
                    doc.attrs["keywords"] = val
            elif (typ is not None and Utils.getXmlLocalName(x) == "li" and not Utils.isNullOrEmpty(Utils.getXmlInnerText(x))): 
                txt = Utils.getXmlInnerText(x)
                if (not typ in doc.attrs): 
                    doc.attrs[typ] = txt
                else: 
                    doc.attrs[typ] = "{0}; {1}".format(doc.attrs[typ], txt)
            else: 
                PdfHelper.__read_metadata0(doc, x, typ)