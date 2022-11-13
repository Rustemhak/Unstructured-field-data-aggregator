# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import pathlib
import base64
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocblock import UnitextDocblock
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.internal.misc.MyZipFile import MyZipFile
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.UnitextPagesection import UnitextPagesection

class Fb2Helper:
    
    @staticmethod
    def create_doc_zip(file_name : str, content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        zip0_ = MyZipFile(file_name, content)
        doc = UnitextDocument._new63(file_name, FileFormat.EPUB)
        doc.content = (UnitextContainer())
        foot_notes = dict()
        cover_image = None
        try: 
            for entry in zip0_.entries: 
                if (Utils.endsWithString(entry.name, "body.xml", True)): 
                    dat = entry.get_data()
                    if (dat is None): 
                        continue
                    xml0_ = None # new XmlDocument
                    with MemoryStream(dat) as document_xml: 
                        xml0_ = Utils.parseXmlFromStream(document_xml)
                        document_xml.close()
                    img = Fb2Helper.__load_body(xml0_.getroot(), doc, foot_notes, pars)
                    if (img is not None): 
                        cover_image = img
        finally: 
            if (zip0_ is not None): 
                zip0_.close()
        doc.optimize(False, None)
        return doc
    
    @staticmethod
    def create_doc(file_name : str, content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        xml0_ = None # new XmlDocument
        if (content is None and pathlib.Path(file_name).is_file()): 
            with FileStream(file_name, "rb") as fs: 
                xml0_ = Utils.parseXmlFromStream(fs)
        elif (content is not None): 
            with MemoryStream(content) as mem: 
                try: 
                    xml0_ = Utils.parseXmlFromStream(mem)
                except Exception as ex: 
                    if (xml0_.getroot() is None): 
                        raise ex
        else: 
            return None
        foot_notes = dict()
        for x in xml0_.getroot(): 
            if (Utils.getXmlLocalName(x) == "body"): 
                name = None
                if (x.attrib is not None): 
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "name"): 
                            name = a[1]
                if (name != "notes"): 
                    continue
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "section"): 
                        id0_ = None
                        if (xx.attrib is not None): 
                            for a in xx.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "id"): 
                                    id0_ = a[1]
                        if (id0_ is None or id0_ in foot_notes): 
                            continue
                        gen = UnitextGen()
                        Fb2Helper.__get_uni_text(xx, gen, None, None, pars)
                        foot_notes[id0_] = gen.finish(True, None)
        doc = UnitextDocument._new63(file_name, FileFormat.FB2)
        cover_image = None
        for x in xml0_.getroot(): 
            if (Utils.getXmlLocalName(x) == "body"): 
                img = Fb2Helper.__load_body(x, doc, foot_notes, pars)
                if (img is not None): 
                    cover_image = img
                break
            elif (Utils.getXmlLocalName(x) == "description"): 
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "title-info"): 
                        for xxx in xx: 
                            if (Utils.getXmlLocalName(xxx) == "book-title"): 
                                gen = UnitextGen()
                                Fb2Helper.__get_uni_text(xxx, gen, None, None, pars)
                                if (not pars.load_document_structure): 
                                    fi = gen.finish(True, None)
                                    if (fi is not None): 
                                        doc.sections.append(UnitextPagesection())
                                        doc.sections[0].items.append(UnitextPagesectionItem._new42(fi))
                                if (not "title" in doc.attrs): 
                                    doc.attrs["title"] = Utils.getXmlInnerText(xxx)
                            elif (Utils.getXmlLocalName(xxx) == "author"): 
                                for xxxx in xxx: 
                                    if (Utils.getXmlLocalName(xxxx) == "first-name"): 
                                        if (not "author-firstname" in doc.attrs): 
                                            doc.attrs["author-firstname"] = Utils.getXmlInnerText(xxxx)
                                    elif (Utils.getXmlLocalName(xxxx) == "last-name"): 
                                        if (not "author-lastname" in doc.attrs): 
                                            doc.attrs["author-lastname"] = Utils.getXmlInnerText(xxxx)
                cover_image = Fb2Helper.load_title_info(doc.attrs, x, None)
        if (not pars.only_for_pure_text): 
            for x in xml0_.getroot(): 
                if (Utils.getXmlLocalName(x) == "binary"): 
                    id0_ = None
                    if (x.attrib is not None): 
                        for a in x.attrib.items(): 
                            if (Utils.getXmlAttrLocalName(a) == "id"): 
                                id0_ = a[1]
                    if (id0_ is None): 
                        continue
                    img = Utils.asObjectOrNull(doc.find_by_id(id0_), UnitextImage)
                    if (img is not None): 
                        try: 
                            img.content = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
                        except Exception as ex91: 
                            pass
        return doc
    
    @staticmethod
    def __load_body(x : xml.etree.ElementTree.Element, doc : 'UnitextDocument', foot_notes : typing.List[tuple], pars : 'CreateDocumentParam') -> str:
        cover_image = None
        if (pars.load_document_structure): 
            dbl = UnitextDocblock()
            dbl.typname = "Document"
            dbl.body = (UnitextContainer())
            gg = UnitextGen()
            Fb2Helper.__get_uni_text(x, gg, dbl, foot_notes, pars)
            doc.content = (dbl)
            for xx in x: 
                if (Utils.getXmlLocalName(xx) == "title"): 
                    g = UnitextGen()
                    Fb2Helper.__get_uni_text(xx, g, None, foot_notes, pars)
                    dbl.head = UnitextContainer._new92(UnitextContainerType.HEAD)
                    nn = g.finish(True, None)
                    ccc = Utils.asObjectOrNull(nn, UnitextContainer)
                    if (ccc is None): 
                        ccc = UnitextContainer()
                        ccc.children.append(nn)
                    ccc.typ = UnitextContainerType.NAME
                    dbl.head.children.append(ccc)
                    dbl.head.children.append(UnitextNewline())
                    break
            if (cover_image is not None): 
                if (cover_image.startswith("#")): 
                    cover_image = cover_image[1:]
                if (dbl.head is None): 
                    dbl.head = UnitextContainer._new92(UnitextContainerType.HEAD)
                dbl.head.children.insert(0, UnitextImage._new94(cover_image))
                dbl.head.children.insert(1, UnitextNewline())
        else: 
            gen = UnitextGen()
            Fb2Helper.__get_uni_text(x, gen, None, foot_notes, pars)
            doc.content = gen.finish(True, None)
        return cover_image
    
    @staticmethod
    def __get_uni_text(xml0_ : xml.etree.ElementTree.Element, gen : 'UnitextGen', dbl : 'UnitextDocblock', foot_notes : typing.List[tuple], pars : 'CreateDocumentParam') -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "#text"): 
                if (gen is not None): 
                    gen.append_text(Utils.getXmlInnerText(x), False)
            elif (Utils.getXmlLocalName(x) == "p" or Utils.getXmlLocalName(x) == "v"): 
                gen.append_newline(True)
                Fb2Helper.__get_uni_text(x, gen, dbl, foot_notes, pars)
                gen.append_newline(False)
            elif (Utils.getXmlLocalName(x) == "title"): 
                if (foot_notes is None or pars.load_document_structure): 
                    continue
                gen.append_newline(False)
                Fb2Helper.__get_uni_text(x, gen, dbl, foot_notes, pars)
                gen.append_newline(False)
                gen.append_newline(False)
            elif (Utils.getXmlLocalName(x) == "section"): 
                if (not pars.load_document_structure): 
                    gen.append_newline(False)
                    Fb2Helper.__get_uni_text(x, gen, None, foot_notes, pars)
                    gen.append_pagebreak()
                else: 
                    db = UnitextDocblock._new32("Section")
                    if (dbl.typname == "Section"): 
                        db.typname = "Subsection"
                    elif (dbl.typname == "Subsection"): 
                        db.typname = "Chapter"
                    db.body = (UnitextContainer())
                    dbl.body.children.append(db)
                    for xx in x: 
                        if (Utils.getXmlLocalName(xx) == "title"): 
                            g = UnitextGen()
                            Fb2Helper.__get_uni_text(xx, g, None, foot_notes, pars)
                            db.head = UnitextContainer._new92(UnitextContainerType.HEAD)
                            nn = g.finish(True, None)
                            ccc = Utils.asObjectOrNull(nn, UnitextContainer)
                            if (ccc is None): 
                                ccc = UnitextContainer()
                                ccc.children.append(nn)
                            ccc.typ = UnitextContainerType.NAME
                            db.head.children.append(ccc)
                            db.head.children.append(UnitextNewline())
                            break
                    gg = UnitextGen()
                    Fb2Helper.__get_uni_text(x, gg, db, foot_notes, pars)
                    bb = gg.finish(False, None)
                    if (bb is None): 
                        continue
                    if (len(db.body.children) == 0): 
                        db.body = bb
                    else: 
                        db.body.children.insert(0, bb)
                    cnt = Utils.asObjectOrNull(db.body, UnitextContainer)
                    if (cnt is not None and len(cnt.children) > 0 and (isinstance(cnt.children[0], UnitextNewline))): 
                        del cnt.children[0]
            elif (Utils.getXmlLocalName(x) == "empty-line"): 
                gen.append_newline(False)
            elif (Utils.getXmlLocalName(x) == "image"): 
                id0_ = None
                if (x.attrib is not None): 
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "href" and not Utils.isNullOrEmpty(a[1]) and a[1][0] == '#'): 
                            id0_ = a[1][1:]
                            break
                if (id0_ is not None): 
                    gen.append(UnitextImage._new94(id0_), None, -1, False)
            elif (Utils.getXmlLocalName(x) == "a"): 
                id0_ = None
                typ = None
                if (x.attrib is not None): 
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "href" and not Utils.isNullOrEmpty(a[1]) and a[1][0] == '#'): 
                            id0_ = a[1][1:]
                        elif (Utils.getXmlAttrLocalName(a) == "type"): 
                            typ = a[1]
                if ((id0_ is not None and typ == "note" and foot_notes is not None) and id0_ in foot_notes): 
                    fn = UnitextFootnote._new98(Utils.getXmlInnerText(x))
                    fn.content = foot_notes[id0_]
                    gen.append(fn, None, -1, False)
                    continue
                gen.append_text(Utils.getXmlInnerText(x), False)
            elif (Utils.getXmlLocalName(x) == "subtitle"): 
                gen.append_newline(False)
            elif (Utils.getXmlLocalName(x) == "epigraph"): 
                g = UnitextGen()
                Fb2Helper.__get_uni_text(x, g, None, None, pars)
                fn = UnitextFootnote()
                fn.content = g.finish(True, None)
                if (fn.content is not None): 
                    gen.append(fn, None, -1, False)
            else: 
                Fb2Helper.__get_uni_text(x, gen, dbl, foot_notes, pars)
    
    @staticmethod
    def load_title_info(attrs : typing.List[tuple], xml0_ : xml.etree.ElementTree.Element, nam : str) -> str:
        ret = None
        for ch in xml0_: 
            if (Utils.getXmlLocalName(ch) == "image" and Utils.getXmlLocalName(xml0_) == "coverpage"): 
                for a in ch.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "href"): 
                        ret = a[1]
                continue
            key = (Utils.getXmlLocalName(ch) if nam is None else (nam if Utils.getXmlLocalName(ch) == "#text" else "{0}/{1}".format(nam, Utils.getXmlLocalName(ch))))
            if (len(ch) > 0): 
                img = Fb2Helper.load_title_info(attrs, ch, key)
                if (img is not None): 
                    ret = img
                continue
            val = Utils.getXmlInnerText(ch)
            if (Utils.isNullOrEmpty(val)): 
                continue
            if (not key in attrs): 
                attrs[key] = val
            else: 
                attrs[key] = "{0}; {1}".format(attrs[key], val)
        return ret