# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.pdf.PdfObject import PdfObject
from pullenti.unitext.internal.pdf.PdfIntValue import PdfIntValue
from pullenti.unitext.internal.pdf.PdfDictionary import PdfDictionary
from pullenti.unitext.internal.pdf.PdfStream import PdfStream

class PdfFile(PdfObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.root_object = None
        self.info = None
        self.encrypt = None
        self.pages = list()
        self.all_resources = list()
        self.objs = None
        self.__m_stream = None
        self.__m_head = None;
        self.__m_indirect_objs = list()
        self.__m_indirect_obj_disp = list()
    
    def open0_(self, file_name : str, file_content : bytearray=None) -> None:
        self.root_object = (None)
        self.info = (None)
        if (self.__m_stream is not None): 
            self.__m_stream.close()
        self.__m_stream = PdfStream(file_name, file_content)
        self.__m_head = self.__m_stream.read_head()
        hpos = self.__m_stream.position
        if (self.__read_xrefs()): 
            pass
        else: 
            i = 0
            root_obj = None
            info_obj = None
            self.__m_stream.position = hpos
            while True:
                i = self.__m_stream.peek_solid_byte()
                if (i < 0): 
                    break
                ch = i
                p0 = self.__m_stream.position
                id0__ = 0
                v = 0
                is_obj = False
                str0_ = None
                obj = None
                if ((chr(ch)) >= '0' and (chr(ch)) <= '9'): 
                    wrapid176 = RefOutArgWrapper(0)
                    wrapv177 = RefOutArgWrapper(0)
                    is_obj = self.__m_stream.try_read_id_and_version(False, wrapid176, wrapv177)
                    id0__ = wrapid176.value
                    v = wrapv177.value
                if (is_obj): 
                    obj = (None)
                    try: 
                        obj = self.__m_stream.parse_object(self, False)
                    except Exception as ex: 
                        pass
                    if (obj is None): 
                        self.__m_stream.position = self.__m_stream.position + 1
                        continue
                    obj.id0_ = id0__
                    obj.version = v
                    obj.source_file = self
                    self.__add_obj(id0__, obj)
                    str0_ = self.__m_stream.read_word(False)
                    continue
                str0_ = self.__m_stream.read_word(False)
                if (str0_ == "xref"): 
                    i1 = 0
                    str0_ = self.__m_stream.read_word(False)
                    wrapi1180 = RefOutArgWrapper(0)
                    inoutres181 = Utils.tryParseInt(str0_, wrapi1180)
                    i1 = wrapi1180.value
                    if (inoutres181): 
                        i2 = 0
                        str0_ = self.__m_stream.read_word(False)
                        wrapi2178 = RefOutArgWrapper(0)
                        inoutres179 = Utils.tryParseInt(str0_, wrapi2178)
                        i2 = wrapi2178.value
                        if (inoutres179): 
                            if (i2 > i1): 
                                self.__m_stream.position = self.__m_stream.position + (((i2 - i1)) * 20)
                    while True:
                        str0_ = self.__m_stream.read_word(False)
                        if (Utils.isNullOrEmpty(str0_) or str0_ == "trailer"): 
                            break
                if (str0_ == "trailer"): 
                    i = self.__m_stream.peek_solid_byte()
                    if (((i)) < 0): 
                        break
                    ch = (i)
                    if ((chr(ch)) != '<'): 
                        continue
                    self.__m_stream.position = self.__m_stream.position + 1
                    i = self.__m_stream.read_byte()
                    if (((i)) < 0): 
                        break
                    ch = (i)
                    if ((chr(ch)) != '<'): 
                        break
                    trailer = PdfDictionary()
                    trailer.source_file = self
                    trailer._post_parse(self.__m_stream)
                    if (root_obj is None): 
                        root_obj = trailer.get_object("Root", True)
                    if (info_obj is None): 
                        info_obj = trailer.get_object("Info", True)
                    if (trailer.get_object("Encrypt", True) is not None): 
                        self.encrypt = trailer.get_dictionary("Encrypt", None)
                    continue
                pos = self.__m_stream.position
                obj = self.__m_stream.parse_object(self, False)
                if (pos == (self.__m_stream.position)): 
                    self.__m_stream.position = self.__m_stream.position + 1
            if (root_obj is not None): 
                self.root_object = (Utils.asObjectOrNull(self.get_object(root_obj.id0_), PdfDictionary))
            if (info_obj is not None): 
                self.info = (Utils.asObjectOrNull(self.get_object(info_obj.id0_), PdfDictionary))
        i = 1
        while i < len(self.__m_indirect_objs): 
            if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                if (self.__m_indirect_objs[i].is_type_item("ObjStm")): 
                    if (not self.__read_obj_stm(Utils.asObjectOrNull(self.__m_indirect_objs[i], PdfDictionary))): 
                        if (self.__check_encrypt()): 
                            return
            i += 1
        is_linearized = False
        if (self.root_object is None): 
            i = 1
            while i < len(self.__m_indirect_objs): 
                if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                    if (self.__m_indirect_objs[i].get_object("Linearized", False) is not None): 
                        is_linearized = True
                        break
                i += 1
        self.__read_all_resources()
        if (is_linearized): 
            first_page = None
            pos0 = self.__m_stream.length
            i = 1
            while i < len(self.__m_indirect_objs): 
                if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                    dic = Utils.asObjectOrNull(self.__m_indirect_objs[i], PdfDictionary)
                    if (dic.is_type_item("Page")): 
                        self.pages.append(dic)
                        if (dic._m_file_pos > 0 and (dic._m_file_pos < pos0)): 
                            first_page = dic
                            pos0 = dic._m_file_pos
                    elif (dic.is_type_item("Catalog")): 
                        self.root_object = dic
                    elif (dic.is_type_item("Info")): 
                        self.info = dic
                i += 1
            if (first_page is not None and self.pages[0] != first_page): 
                self.pages.remove(first_page)
                self.pages.insert(0, first_page)
            return
        if (self.root_object is None): 
            i = 1
            while i < len(self.__m_indirect_objs): 
                if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                    if (self.__m_indirect_objs[i].is_type_item("Catalog")): 
                        self.root_object = (Utils.asObjectOrNull(self.__m_indirect_objs[i], PdfDictionary))
                        break
                i += 1
        if (self.info is None): 
            i = 1
            while i < len(self.__m_indirect_objs): 
                if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                    if (self.__m_indirect_objs[i].is_type_item("Info")): 
                        self.info = (Utils.asObjectOrNull(self.__m_indirect_objs[i], PdfDictionary))
                        break
                i += 1
        if (self.root_object is None): 
            i = 1
            while i < len(self.__m_indirect_objs): 
                if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                    if (self.__m_indirect_objs[i].is_type_item("XRef")): 
                        self.objs = list()
                        for v in self.__m_indirect_objs: 
                            if (v is not None): 
                                self.objs.append(v)
                        break
                i += 1
        if (self.root_object is not None): 
            self.root_object.get_all_pages(self.pages)
    
    def __read_all_resources(self) -> None:
        i = 1
        while i < len(self.__m_indirect_objs): 
            if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                dic = Utils.asObjectOrNull(self.__m_indirect_objs[i], PdfDictionary)
                sub = dic.get_string_item("Subtype")
                if (sub == "Image" or sub == "Font"): 
                    self.all_resources.append(dic)
            i += 1
    
    def __check_encrypt(self) -> bool:
        i = 1
        while i < len(self.__m_indirect_objs): 
            if (isinstance(self.__m_indirect_objs[i], PdfDictionary)): 
                dic = Utils.asObjectOrNull(self.__m_indirect_objs[i], PdfDictionary)
                if (dic.is_type_item("Encrypt")): 
                    self.encrypt = dic
                    return True
                self.encrypt = dic.get_dictionary("Encrypt", None)
                if (self.encrypt is not None): 
                    return True
            i += 1
        return False
    
    def close(self) -> None:
        if (self.__m_stream is not None): 
            self.__m_stream.close()
        self.__m_stream = (None)
    
    @property
    def max_objs_count(self) -> int:
        return len(self.__m_indirect_objs)
    
    def get_object(self, id0__ : int) -> 'PdfObject':
        if ((id0__ < 1) or id0__ >= len(self.__m_indirect_objs)): 
            return None
        if (self.__m_indirect_objs[id0__] is not None): 
            return self.__m_indirect_objs[id0__]
        if (self.__m_indirect_obj_disp[id0__] == 0): 
            return None
        self.__m_stream.position = self.__m_indirect_obj_disp[id0__]
        uid = 0
        v = 0
        wrapuid182 = RefOutArgWrapper(0)
        wrapv183 = RefOutArgWrapper(0)
        inoutres184 = self.__m_stream.try_read_id_and_version(False, wrapuid182, wrapv183)
        uid = wrapuid182.value
        v = wrapv183.value
        if (not inoutres184): 
            return None
        if (uid != id0__): 
            return None
        obj = None
        try: 
            obj = self.__m_stream.parse_object(self, False)
        except Exception as ex: 
            pass
        if (obj is None): 
            return None
        obj.id0_ = id0__
        obj.version = v
        self.__m_indirect_objs[id0__] = obj
        return obj
    
    def __add_obj(self, id0__ : int, obj : 'PdfObject') -> None:
        while id0__ >= len(self.__m_indirect_objs):
            self.__m_indirect_objs.append(None)
            self.__m_indirect_obj_disp.append(0)
        self.__m_indirect_objs[id0__] = obj
    
    def __add_indir(self, id0__ : int, disp : int) -> None:
        while id0__ >= len(self.__m_indirect_objs):
            self.__m_indirect_objs.append(None)
            self.__m_indirect_obj_disp.append(0)
        self.__m_indirect_obj_disp[id0__] = disp
    
    def __read_xrefs(self) -> bool:
        if (self.__m_stream.length < 100): 
            return False
        self.__m_stream.position = self.__m_stream.length - 100
        str0_ = None
        while True:
            str0_ = self.__m_stream.read_word(True)
            if ((str0_) is not None): pass
            else: 
                break
            if (str0_ == "startxref"): 
                break
        if (str0_ is None): 
            return False
        str0_ = self.__m_stream.read_word(True)
        disp = 0
        wrapdisp191 = RefOutArgWrapper(0)
        inoutres192 = Utils.tryParseInt(str0_, wrapdisp191)
        disp = wrapdisp191.value
        if (not inoutres192): 
            return False
        inf_obj = None
        while True:
            if ((disp < 0) or disp >= self.__m_stream.length): 
                return False
            self.__m_stream.position = disp
            str0_ = self.__m_stream.read_word(False)
            if (str0_ != "xref"): 
                return False
            while True:
                id0 = 0
                count = 0
                i = 0
                wrapid0189 = RefOutArgWrapper(0)
                str0_ = self.__m_stream.read_word(True)
                inoutres190 = Utils.tryParseInt(str0_, wrapid0189)
                id0 = wrapid0189.value
                if (not inoutres190): 
                    break
                wrapcount187 = RefOutArgWrapper(0)
                inoutres188 = Utils.tryParseInt(self.__m_stream.read_word(True), wrapcount187)
                count = wrapcount187.value
                if (not inoutres188): 
                    break
                i = 0
                while i < count: 
                    w = self.__m_stream.read_word(True)
                    wrapdisp185 = RefOutArgWrapper(0)
                    inoutres186 = Utils.tryParseInt(w, wrapdisp185)
                    disp = wrapdisp185.value
                    if (not inoutres186): 
                        break
                    self.__m_stream.read_word(True)
                    str0_ = self.__m_stream.read_word(True)
                    if (str0_ is None or len(str0_) != 1): 
                        break
                    if (str0_ == "n"): 
                        self.__add_indir(id0, disp)
                    i += 1; id0 += 1
                if (i < count): 
                    break
            if (str0_ != "trailer"): 
                return False
            if (self.__m_stream.read_word(True) != "<"): 
                return False
            if (self.__m_stream.read_word(True) != "<"): 
                return False
            trailer = PdfDictionary()
            trailer.source_file = self
            trailer._post_parse(self.__m_stream)
            if (trailer.get_object("Encrypt", False) is not None): 
                self.encrypt = trailer.get_dictionary("Encrypt", None)
            if (self.root_object is None): 
                oo = trailer.get_object("Root", False)
                if (oo is not None): 
                    self.root_object = (Utils.asObjectOrNull(self.get_object(oo.id0_), PdfDictionary))
            if (inf_obj is None): 
                inf_obj = trailer.get_object("Info", True)
            d = 0
            prev = Utils.asObjectOrNull(trailer.get_object("Prev", False), PdfIntValue)
            if (prev is None): 
                break
            disp = prev.val
        if (inf_obj is not None): 
            self.info = (Utils.asObjectOrNull(self.get_object(inf_obj.id0_), PdfDictionary))
        return self.root_object is not None
    
    def __read_obj_stm(self, dic : 'PdfDictionary') -> bool:
        dat = dic.extract_data()
        if (dat is None or (len(dat) < 1)): 
            return False
        count = dic.get_int_item("N")
        if (count < 1): 
            return False
        with PdfStream(None, dat) as pstr: 
            ids = Utils.newArray(count, 0)
            disps = Utils.newArray(count, 0)
            i = 0
            while i < count: 
                id0__ = Utils.asObjectOrNull(pstr.parse_object(self, False), PdfIntValue)
                if (id0__ is None): 
                    break
                disp = Utils.asObjectOrNull(pstr.parse_object(self, False), PdfIntValue)
                if (disp is None): 
                    break
                ids[i] = (id0__.val)
                disps[i] = (disp.val)
                i += 1
            n0 = pstr.position
            i = 0
            while i < count: 
                pstr.position = n0 + disps[i]
                obj = pstr.parse_object(self, False)
                if (obj is not None): 
                    obj.id0_ = ids[i]
                    obj.source_file = self
                    self.__add_obj(obj.id0_, obj)
                    if (isinstance(obj, PdfDictionary)): 
                        if (obj.is_type_item("ObjStm")): 
                            pass
                i += 1
        return True
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()