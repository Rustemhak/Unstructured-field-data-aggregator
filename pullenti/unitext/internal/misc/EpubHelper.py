# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.CreateDocumentParam import CreateDocumentParam
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.misc.MyZipFile import MyZipFile
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.UnitextPagesection import UnitextPagesection
from pullenti.unitext.internal.html.HtmlHelper import HtmlHelper

class EpubHelper:
    
    @staticmethod
    def create_doc(file_name : str, content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        zip0_ = MyZipFile(file_name, content)
        doc = UnitextDocument._new63(file_name, FileFormat.EPUB)
        doc.content = (UnitextContainer())
        try: 
            text_entries = dict()
            items_order = list()
            images_entries = dict()
            for entry in zip0_.entries: 
                if (Utils.endsWithString(entry.name, "content.opf", True)): 
                    xml0_ = None # new XmlDocument
                    dat = entry.get_data()
                    if (dat is None): 
                        continue
                    with MemoryStream(dat) as document_xml: 
                        xml0_ = Utils.parseXmlFromStream(document_xml)
                        document_xml.close()
                    for x in xml0_.getroot(): 
                        if (Utils.getXmlLocalName(x) == "manifest"): 
                            for xx in x: 
                                if (Utils.getXmlLocalName(xx) == "item"): 
                                    typ = None
                                    id0_ = None
                                    href = None
                                    if (xx.attrib is not None): 
                                        for a in xx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "id"): 
                                                id0_ = a[1]
                                            elif (Utils.getXmlAttrLocalName(a) == "href"): 
                                                href = a[1]
                                            elif (Utils.getXmlAttrLocalName(a) == "media-type"): 
                                                typ = a[1]
                                    if (typ is None or href is None): 
                                        continue
                                    if (typ.startswith("application") and "xhtml" in typ): 
                                        if (not href in text_entries): 
                                            text_entries[href] = None
                                        items_order.append(href)
                                    elif (typ.startswith("image/")): 
                                        if (not href in images_entries): 
                                            images_entries[href] = None
                        elif (Utils.getXmlLocalName(x) == "metadata"): 
                            for xxx in x: 
                                if (Utils.getXmlLocalName(xxx) == "title"): 
                                    if (not "title" in doc.attrs): 
                                        doc.attrs["title"] = Utils.getXmlInnerText(xxx)
                                elif (Utils.getXmlLocalName(xxx) == "creator"): 
                                    is_auth = False
                                    if (xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "role"): 
                                                if (a[1] == "aut"): 
                                                    is_auth = True
                                    if (is_auth): 
                                        if (not "author" in doc.attrs): 
                                            doc.attrs["author"] = Utils.getXmlInnerText(xxx)
            buf = Utils.newArrayOfBytes(100000, 0)
            for entry in zip0_.entries: 
                txt = None
                for kp in text_entries.items(): 
                    if (entry.name.endswith(kp[0])): 
                        txt = kp[0]
                        break
                if (txt is None): 
                    continue
                if ("annotation" in txt or "about" in txt or "info" in txt): 
                    continue
                try: 
                    dat = entry.get_data()
                    nod = HtmlHelper.create_node(None, dat, None)
                    if (nod is None): 
                        continue
                    doc0 = HtmlHelper.create(nod, None, None, CreateDocumentParam())
                    if (doc0 is not None and doc0.content is not None): 
                        if ("title" in txt): 
                            doc.sections.append(UnitextPagesection())
                            doc.sections[0].items.append(UnitextPagesectionItem._new42(doc0.content))
                        else: 
                            text_entries[txt] = doc0.content
                except Exception as ex: 
                    pass
            cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
            for key in items_order: 
                if (key in text_entries): 
                    ccc = text_entries[key]
                    if (ccc is None): 
                        continue
                    if (Utils.endsWithString(key, "TOC.NCX", True)): 
                        continue
                    if ("CONTENT." in key.upper()): 
                        continue
                    if (len(cnt.children) > 0): 
                        cnt.children.append(UnitextPagebreak())
                    if (isinstance(ccc, UnitextContainer)): 
                        cnt.children.extend(ccc.children)
                    else: 
                        cnt.children.append(ccc)
            its = list()
            doc.get_all_items(its, 0)
            for entry in zip0_.entries: 
                if (pars.only_for_pure_text): 
                    break
                img = None
                for it in its: 
                    if (isinstance(it, UnitextImage)): 
                        if (entry.name.endswith(it.id0_)): 
                            img = (Utils.asObjectOrNull(it, UnitextImage))
                            break
                if (img is None): 
                    continue
                img.content = entry.get_data()
        finally: 
            if (zip0_ is not None): 
                zip0_.close()
        doc.optimize(False, None)
        return doc