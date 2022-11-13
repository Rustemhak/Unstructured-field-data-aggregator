# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.pdf.PdfName import PdfName
from pullenti.unitext.internal.pdf.PdfRect import PdfRect
from pullenti.unitext.internal.pdf.PdfBoolValue import PdfBoolValue
from pullenti.unitext.internal.pdf.PdfText import PdfText
from pullenti.unitext.internal.pdf.PdfTextState import PdfTextState
from pullenti.unitext.internal.pdf.PdfArray import PdfArray
from pullenti.unitext.internal.pdf.PdfStream import PdfStream
from pullenti.unitext.internal.pdf.PdfImage import PdfImage
from pullenti.unitext.internal.pdf.Matrix import Matrix
from pullenti.unitext.internal.pdf.PdfFont import PdfFont
from pullenti.unitext.internal.pdf.PdfPathState import PdfPathState

class PdfPage(PdfRect):
    
    def __init__(self, dic_ : 'PdfDictionary', state0 : object=None) -> None:
        super().__init__()
        self.dic = None;
        self.items = list()
        self.dic = dic_
        crop = Utils.asObjectOrNull(dic_.get_object("CropBox", False), PdfArray)
        if (crop is None): 
            crop = (Utils.asObjectOrNull(dic_.get_object("TrimBox", False), PdfArray))
        if (crop is None): 
            crop = (Utils.asObjectOrNull(dic_.get_object("MediaBox", False), PdfArray))
        if (crop is None): 
            crop = (Utils.asObjectOrNull(dic_.get_object("BBox", False), PdfArray))
        if (crop is None): 
            if (dic_.source_file.root_object is not None): 
                pages = dic_.source_file.root_object.get_dictionary("Pages", None)
                if (pages is not None): 
                    crop = (Utils.asObjectOrNull(pages.get_object("MediaBox", False), PdfArray))
                    if (crop is None): 
                        crop = (Utils.asObjectOrNull(pages.get_object("TrimBox", False), PdfArray))
                    if (crop is None): 
                        crop = (Utils.asObjectOrNull(pages.get_object("CropBox", False), PdfArray))
        if (crop is not None and crop.items_count == 4): 
            self.x2 = crop.get_item(2).get_double()
            self.y2 = crop.get_item(3).get_double()
            rot = dic_.get_object("Rotate", False)
            if (rot is not None and ((rot.get_double() == 90 or rot.get_double() == 270))): 
                xx = self.x2
                self.x2 = self.y2
                self.y2 = xx
        res = self.dic.get_dictionary("Resources", None)
        fnts = (None if res is None else res.get_dictionary("Font", None))
        imgs = (None if res is None else res.get_dictionary("XObject", None))
        val = self.dic.get_total_data_stream("Contents")
        if (val is None and state0 is not None): 
            val = self.dic.extract_data()
        if (val is None or (len(val) < 1)): 
            return
        lex = None
        with PdfStream(None, val) as pstr: 
            lex = pstr.parse_content()
        all_fonts = dict()
        state = Utils.asObjectOrNull(state0, PdfTextState)
        if (state is None): 
            state = PdfTextState()
            state.box_height = self.y2
        else: 
            mat = Utils.asObjectOrNull(dic_.get_object("Matrix", False), PdfArray)
            if (mat is not None and mat.items_count == 6): 
                m = Matrix()
                m.set0_(mat.get_item(0).get_double(), mat.get_item(1).get_double(), mat.get_item(2).get_double(), mat.get_item(3).get_double(), mat.get_item(4).get_double(), mat.get_item(5).get_double())
                if (len(state.ctm_stack) > 0): 
                    m.multiply(state.ctm_stack[0])
                    state.ctm_stack[0] = m
        text_regime = False
        buf = io.StringIO()
        path = PdfPathState(self)
        i = 0
        first_pass648 = True
        while True:
            if first_pass648: first_pass648 = False
            else: i += 1
            if (not (i < len(lex))): break
            if (not (isinstance(lex[i], PdfName))): 
                continue
            if (lex[i]._has_slash): 
                continue
            nam = lex[i].name
            if (nam == "ET"): 
                text_regime = False
                continue
            if (nam == "BT"): 
                text_regime = True
                state.tm.init()
                state.tlm.init()
                continue
            if (nam == "Do" and (isinstance(lex[i - 1], PdfName))): 
                nam = lex[i - 1].name
                xobjs = (None if res is None else res.get_dictionary("XObject", None))
                xobj = (None if xobjs is None else xobjs.get_dictionary(nam, None))
                if (xobj is None): 
                    for rr in dic_.source_file.all_resources: 
                        if (rr.get_string_item("Name") == nam): 
                            xobj = rr
                            break
                if (xobj is not None): 
                    sub = Utils.asObjectOrNull(xobj.get_object("Subtype", False), PdfName)
                    if (sub is not None and sub.name == "Image"): 
                        im = Utils.asObjectOrNull(xobj.get_object("ImageMask", False), PdfBoolValue)
                        if (im is not None and im.val): 
                            pass
                        else: 
                            img = PdfImage(xobj)
                            if (len(state.ctm_stack) > 0): 
                                img.x2 = state.ctm_stack[0].e0_
                                img.x1 = img.x2
                                img.x2 += state.ctm_stack[0].a
                                img.y2 = state.box_height - state.ctm_stack[0].f
                                img.y1 = img.y2
                                img.y1 -= state.ctm_stack[0].d
                                if (((img.y1 < -0.1) or img.y2 > self.y2 or (img.x1 < -0.1)) or img.x2 > self.x2): 
                                    pass
                            self.items.append(img)
                    else: 
                        ppp = PdfPage(xobj, state)
                        self.items.extend(ppp.items)
                continue
            if (state.parse_one(lex, i)): 
                continue
            if (path.parse_one(lex, i)): 
                continue
            if (nam == "Tf" and (isinstance(lex[i - 2], PdfName))): 
                state.font_size = lex[i - 1].get_double()
                fnam = lex[i - 2].name
                if (not fnam in all_fonts): 
                    fff = None
                    if (fnts is not None): 
                        fff = fnts.get_dictionary(fnam, None)
                    if (fff is not None): 
                        if (isinstance(fff.tag, PdfFont)): 
                            state.font = (Utils.asObjectOrNull(fff.tag, PdfFont))
                        else: 
                            state.font = PdfFont(fff)
                            state.font.alias = fnam
                        fff.tag = (state.font)
                        all_fonts[fnam] = state.font
                else: 
                    state.font = all_fonts[fnam]
                continue
            if (text_regime and (((nam == "Tj" or nam == "TJ" or nam == "\"") or nam == "'"))): 
                if (state.font is None): 
                    continue
                if (nam == "\""): 
                    state.char_space = lex[i - 2].get_double()
                    state.word_space = lex[i - 3].get_double()
                if (nam == "\"" or nam == "'"): 
                    state.newline()
                txt = state.font._extract_text(lex[i - 1], state)
                if (txt is not None): 
                    self.items.append(txt)
                continue
        if (self.y2 > 0): 
            for it in self.items: 
                while it.y1 > self.y2:
                    it.y1 -= self.y2
                    it.y2 -= self.y2
        i = 0
        while i < (len(self.items) - 1): 
            if ((isinstance(self.items[i], PdfText)) and (isinstance(self.items[i + 1], PdfText))): 
                if (self.items[i].can_be_merged_with(Utils.asObjectOrNull(self.items[i + 1], PdfText))): 
                    self.items[i].merge_with(Utils.asObjectOrNull(self.items[i + 1], PdfText))
                    del self.items[i + 1]
                    i -= 1
            i += 1
        maxx = 0
        for it in self.items: 
            if (it.right > maxx): 
                maxx = it.right
        if (maxx > self.x2): 
            ratio = ((self.x2 - (3))) / maxx
            for it in self.items: 
                it.x1 *= ratio
                it.x2 *= ratio