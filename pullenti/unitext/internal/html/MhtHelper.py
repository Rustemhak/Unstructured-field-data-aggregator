# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import base64
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextService import UnitextService
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.util.EncodingWrapper import EncodingWrapper
from pullenti.unitext.internal.html.EmlPart import EmlPart
from pullenti.util.EncodingStandard import EncodingStandard
from pullenti.unitext.internal.html.HtmlParser import HtmlParser
from pullenti.unitext.internal.html.HtmlHelper import HtmlHelper

class MhtHelper:
    """ Поддержка формата MHT и EML """
    
    @staticmethod
    def _create_doc(content : bytearray, pars : 'CreateDocumentParam', is_mht : bool) -> 'UnitextDocument':
        txt = MiscHelper.decode_string_utf8(content, 0, -1)
        return MhtHelper._create_doc_txt(txt, pars, is_mht, content)
    
    @staticmethod
    def _create_doc_txt(txt : str, pars : 'CreateDocumentParam', is_mht : bool, content : bytearray) -> 'UnitextDocument':
        pos = 0
        wrappos40 = RefOutArgWrapper(pos)
        p = EmlPart.try_parse(txt, wrappos40)
        pos = wrappos40.value
        if (p is None): 
            return None
        p0 = p
        nod = None
        parts = list()
        parts.append(p)
        images = dict()
        image_types = dict()
        while pos < len(txt):
            if (txt[pos] != '-'): 
                pos += 1
                continue
            wrappos39 = RefOutArgWrapper(pos)
            p = EmlPart.try_parse(txt, wrappos39)
            pos = wrappos39.value
            if (p is None): 
                break
            if (p.content_charset is not None and content is not None): 
                try: 
                    ee = EncodingWrapper(EncodingStandard.UNDEFINED, p.content_charset)
                    if (ee is not None): 
                        txt = ee.get_string(content, 0, -1)
                        return MhtHelper._create_doc_txt(txt, pars, is_mht, None)
                except Exception as ex: 
                    pass
            if (p.data is not None and p.content_type is not None and p.content_type.startswith("image")): 
                if (pars.only_for_pure_text): 
                    continue
                if (p.filename is None): 
                    ii = len(images)
                    if (p.content_location is not None and not p.content_location in images): 
                        images[p.content_location] = p.data
                        if (p.content_type is not None): 
                            image_types[p.content_location] = p.content_type
                    if (p.content_id is not None and not "cid:" + p.content_id in images): 
                        images["cid:" + p.content_id] = p.data
                        if (p.content_type is not None): 
                            image_types["cid:" + p.content_id] = p.content_type
                    if (len(images) > ii): 
                        continue
            parts.append(p)
            if (p.content_type == "text/html"): 
                if (pars.ignore_inner_documents): 
                    break
        doc = None
        i = 0
        first_pass623 = True
        while True:
            if first_pass623: first_pass623 = False
            else: i += 1
            if (not (i < len(parts))): break
            if (parts[i].content_type == "text/html"): 
                p = parts[i]
                if (p.string_data is not None): 
                    tmp = Utils.newStringIO(p.string_data)
                    nod = HtmlParser.parse(tmp, False)
                elif (p.data is not None): 
                    nod = HtmlHelper.create_node(None, p.data, p.content_charset)
                if (nod is None): 
                    continue
                doc = HtmlHelper.create(nod, None, images, pars)
                if (doc is None): 
                    continue
                del parts[i]
                if (i > 0 and parts[i - 1].content_type == "text/plain"): 
                    del parts[i - 1]
                break
        if (doc is None): 
            i = 0
            while i < len(parts): 
                if (parts[i].content_type == "text/plain"): 
                    if (parts[i].string_data is not None): 
                        doc = UnitextService.create_document_from_text(parts[i].string_data)
                        del parts[i]
                        break
                i += 1
        if (doc is None): 
            doc = UnitextDocument()
        doc.source_format = (FileFormat.MHT if is_mht else FileFormat.EML)
        for a in p0.attrs.items(): 
            if (not a[0] in doc.attrs): 
                doc.attrs[a[0]] = a[1]
        if (not is_mht): 
            kk = 0
            gen = UnitextGen()
            for s in ["From", "To", "CC", "Date", "Subject"]: 
                if (s in doc.attrs): 
                    gen.append_text("{0}: {1}".format(s, doc.attrs[s]), False)
                    gen.append_newline(False)
                    kk += 1
            if (kk > 0): 
                gen.append_newline(False)
                if (doc.content is not None): 
                    gen.append(doc.content, None, -1, False)
                doc.content = gen.finish(True, None)
                doc.optimize(False, None)
                doc.refresh_parents()
        if (pars.ignore_inner_documents): 
            return doc
        for pp in parts: 
            if (pp.data is not None): 
                if (pp.filename is not None): 
                    try: 
                        aa = UnitextService.create_document(pp.filename, pp.data, pars)
                        if (aa is not None): 
                            doc.inner_documents.append(aa)
                    except Exception as ex: 
                        pass
        return doc
    
    @staticmethod
    def _encode_string(val : str) -> str:
        res = io.StringIO()
        col = 0
        i = 0
        while i < len(val): 
            ch = val[i]
            if (ch == '\r' or ch == '\n'): 
                col = 0
            else: 
                col += 1
            if (col > 80): 
                print("=\r\n", end="", file=res)
                col = 0
            if (ch == '='): 
                print("=3D", end="", file=res)
            else: 
                print(ch, end="", file=res)
            i += 1
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _decode_string(val : str) -> str:
        if (Utils.isNullOrEmpty(val) or (len(val) < 3)): 
            return val
        if (len(val) < 10): 
            return val
        if (not "=?" in val): 
            return val
        res = io.StringIO()
        i = 0
        while i < len(val): 
            if (val[i] == '=' and ((i + 1) < len(val)) and val[i + 1] == '?'): 
                j = 0
                i += 2
                j = i
                while j < len(val): 
                    if (val[j] == '?'): 
                        break
                    j += 1
                if (j >= len(val)): 
                    return val
                charset = val[i:i+j - i].strip()
                enc = None
                try: 
                    enc = EncodingWrapper(EncodingStandard.UNDEFINED, charset)
                except Exception as ex: 
                    return val
                i = (j + 1)
                typ = '?'
                j += 1
                while j < len(val): 
                    if (val[j] == '?'): 
                        break
                    elif (val[j] == 'Q' or val[j] == 'q'): 
                        typ = 'Q'
                    elif (val[j] == 'B' or val[j] == 'b'): 
                        typ = 'B'
                    j += 1
                if (typ != 'Q' and typ != 'B'): 
                    return val
                i = (j + 1)
                j += 1
                while j < len(val): 
                    if (val[j] == '?' and ((j + 1) < len(val)) and val[j + 1] == '='): 
                        break
                    j += 1
                data = val[i:i+j - i].strip()
                bdata = None
                if (typ == 'B'): 
                    bdata = base64.decodestring((data).encode('utf-8', 'ignore'))
                else: 
                    bbb = bytearray()
                    k = 0
                    while k < len(data): 
                        if (data[k] != '=' or (k + 1) >= len(data)): 
                            bbb.append(ord(data[k]))
                        elif ((k + 2) < len(data)): 
                            v1 = EmlPart._to_int(data[k + 1])
                            v2 = EmlPart._to_int(data[k + 2])
                            if (v1 >= 0 and v2 >= 0): 
                                bbb.append((((v1 << 4)) | v2))
                                k += 2
                            else: 
                                bbb.append(ord(data[k]))
                        k += 1
                    bdata = (bytearray(bbb))
                if (bdata is None): 
                    return val
                ooo = enc.get_string(bdata, 0, -1)
                print(ooo, end="", file=res)
                i = (j + 1)
            else: 
                print(val[i], end="", file=res)
            i += 1
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _corr_string(val : str) -> str:
        if (Utils.isNullOrEmpty(val) or (len(val) < 3)): 
            return val
        i = val.find(';')
        if (i > 0): 
            val = val[0:0+i].strip()
        if (val[0] == '"' and val[len(val) - 1] == '"'): 
            val = val[1:1+len(val) - 2]
        return val