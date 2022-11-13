# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.pdf.PdfStringValue import PdfStringValue
from pullenti.unitext.internal.misc.PngWrapper import PngWrapper
from pullenti.unitext.internal.pdf.PdfRect import PdfRect
from pullenti.unitext.internal.pdf.PdfIntValue import PdfIntValue
from pullenti.unitext.internal.pdf.PdfArray import PdfArray
from pullenti.unitext.internal.pdf.PdfName import PdfName
from pullenti.unitext.internal.pdf.PdfDictionary import PdfDictionary
from pullenti.unitext.internal.misc.TiffHelper import TiffHelper

class PdfImage(PdfRect):
    
    def __init__(self, xobj : 'PdfDictionary') -> None:
        super().__init__()
        self.content = None;
        self.image_width = 0
        self.image_height = 0
        wi = xobj.get_object("Width", False)
        if (wi is not None): 
            self.image_width = (math.floor(wi.get_double()))
        hi = xobj.get_object("Height", False)
        if (hi is not None): 
            self.image_height = (math.floor(hi.get_double()))
        sub = Utils.asObjectOrNull(xobj.get_object("Filter", False), PdfName)
        data = xobj.data
        if (sub is None): 
            aaa = Utils.asObjectOrNull(xobj.get_object("Filter", False), PdfArray)
            if (aaa is not None and aaa.items_count == 1): 
                sub = (Utils.asObjectOrNull(aaa.get_item(0), PdfName))
            elif ((aaa is not None and aaa.items_count == 2 and (isinstance(aaa.get_item(0), PdfName))) and aaa.get_item(0).name == "FlateDecode"): 
                data = xobj.extract_data()
                sub = (Utils.asObjectOrNull(aaa.get_item(1), PdfName))
        if (sub is not None and sub.name == "DCTDecode"): 
            self.content = data
            return
        if (sub is not None and sub.name == "JPXDecode"): 
            self.content = data
            return
        if (sub is not None and sub.name == "CCITTFaxDecode"): 
            parms = xobj.get_dictionary("DecodeParms", None)
            if (parms is not None): 
                k = parms.get_int_item("K")
                width_ = parms.get_int_item("Columns")
                if (width_ < 10): 
                    width_ = (xobj.get_int_item("Width"))
                height_ = parms.get_int_item("Rows")
                if (height_ < 10): 
                    height_ = (xobj.get_int_item("Height"))
                invert = False
                str0_ = parms.get_string_item("BlackIs1")
                if (str0_ is None): 
                    str0_ = xobj.get_string_item("ImageMask")
                if (str0_ is not None): 
                    if (str0_ == "true"): 
                        invert = True
                if (width_ > 0 and height_ > 0): 
                    with MemoryStream() as mem: 
                        tif = TiffHelper.Tiff(None)
                        tif.write_tiff(mem, width_, height_, (TiffHelper.CCITT_Types.G4 if k < 0 else ((TiffHelper.CCITT_Types.G3_2D if k == 0 else TiffHelper.CCITT_Types.G3_1D))), 300, 300, invert, data)
                        self.content = mem.toarray()
            return
        if (((sub is None or sub.name == "FlateDecode")) and self.image_width > 0 and self.image_height > 0): 
            data = xobj.extract_data()
            bpi = xobj.get_object("BitsPerComponent", False)
            dparms = xobj.get_dictionary("DecodeParms", None)
            predict = 0
            if (dparms is not None): 
                pred = Utils.asObjectOrNull(dparms.get_object("Predictor", False), PdfIntValue)
                if (pred is not None and pred.val > 1): 
                    predict = pred.val
                    if (predict >= 10 and (predict < 15)): 
                        pass
            colorsp = xobj.get_object("ColorSpace", False)
            color_map = None
            if (bpi is not None and ((bpi.get_double() == 8 or bpi.get_double() == 4 or bpi.get_double() == 1)) and colorsp is not None): 
                color_typ = None
                bpi_val = math.floor(bpi.get_double())
                is_icc_based = False
                if (isinstance(colorsp, PdfName)): 
                    color_typ = colorsp.name
                elif (isinstance(colorsp, PdfArray)): 
                    arr = Utils.asObjectOrNull(colorsp, PdfArray)
                    it0 = Utils.asObjectOrNull(arr.get_item(0), PdfName)
                    if (it0 is not None and it0.name == "ICCBased"): 
                        is_icc_based = True
                    if (it0 is not None and it0.name == "Indexed"): 
                        sss = Utils.asObjectOrNull(arr.get_item(3), PdfStringValue)
                        if (sss is not None): 
                            color_map = sss.val
                        else: 
                            ddd = Utils.asObjectOrNull(arr.get_item(3), PdfDictionary)
                            if (ddd is not None): 
                                color_map = ddd.extract_data()
                    dii = Utils.asObjectOrNull(arr.get_item(3), PdfDictionary)
                    if (dii is None and arr.items_count == 2): 
                        dii = (Utils.asObjectOrNull(arr.get_item(1), PdfDictionary))
                        ddd = Utils.asObjectOrNull(arr.get_item(1), PdfDictionary)
                        if (ddd is not None and (isinstance(ddd.get_object("Alternate", False), PdfName))): 
                            color_typ = ddd.get_object("Alternate", False).name
                    if (arr.items_count > 2 and (isinstance(arr.get_item(1), PdfArray))): 
                        arr = (Utils.asObjectOrNull(arr.get_item(1), PdfArray))
                        if (arr.items_count == 2): 
                            ddd = Utils.asObjectOrNull(arr.get_item(1), PdfDictionary)
                            if (ddd is not None and (isinstance(ddd.get_object("Alternate", False), PdfName))): 
                                color_typ = ddd.get_object("Alternate", False).name
                    elif (arr.items_count == 4 and (isinstance(arr.get_item(1), PdfName))): 
                        color_typ = arr.get_item(1).name
                if (color_typ == "DeviceRGB" or color_typ == "DeviceGray" or color_typ == "DeviceCMYK"): 
                    if (data is not None): 
                        row_width = math.floor(len(data) / self.image_height)
                        mmm = len(data) % self.image_height
                        if (mmm != 0): 
                            pass
                        nn = math.floor(row_width / self.image_width)
                        if (nn == 0 and (bpi_val < 8)): 
                            nn = 1
                        is_gray = color_typ == "DeviceGray"
                        is_cmyk = color_typ == "DeviceCMYK"
                        if ((nn == 3 or ((nn == 4 and is_cmyk)) or ((is_cmyk and color_map is not None))) or bpi_val == 4 or (((nn == 1 and ((color_map is not None or color_typ == "DeviceGray"))) or ((bpi_val == 1 and color_map is not None))))): 
                            if (color_typ == "DeviceGray"): 
                                pass
                            if (color_typ == "DeviceRGB" and color_map is not None and ((len(color_map) % 3)) == 0): 
                                pass
                            if (is_cmyk and color_map is not None): 
                                rgb = Utils.newArrayOfBytes(((math.floor(len(color_map) / 4))) * 3, 0)
                                j = 0
                                i = 0
                                while (i + 3) < len(color_map): 
                                    rgb[j] = PdfImage.__corrcmyk(color_map[i], color_map[i + 3])
                                    rgb[j + 1] = PdfImage.__corrcmyk(color_map[i + 1], color_map[i + 3])
                                    rgb[j + 2] = PdfImage.__corrcmyk(color_map[i + 2], color_map[i + 3])
                                    j += 3
                                    i += 4
                                color_map = rgb
                            img = PngWrapper(self.image_width, self.image_height, is_gray, color_map)
                            row = 0
                            while row < self.image_height: 
                                pp = row * row_width
                                img.begin_row()
                                if (bpi_val == 1): 
                                    ii = 0
                                    while ii < row_width: 
                                        if ((pp + ii) >= len(data)): 
                                            break
                                        b = data[pp + ii]
                                        for jj in range(7, -1, -1):
                                            img.add_pixel_index(((((b) >> jj)) & 1))
                                        ii += 1
                                else: 
                                    w = 0
                                    while w < self.image_width: 
                                        if (nn == 3): 
                                            if ((pp + 2) >= len(data)): 
                                                break
                                            img.add_pixel_rgb(data[pp + 2], data[pp], data[pp + 1])
                                            pp += 3
                                        elif (nn == 4): 
                                            if ((pp + 3) >= len(data)): 
                                                break
                                            r = PdfImage.__corrcmyk(data[pp], data[pp + 3])
                                            g = PdfImage.__corrcmyk(data[pp + 1], data[pp + 3])
                                            b = PdfImage.__corrcmyk(data[pp + 2], data[pp + 3])
                                            img.add_pixel_rgb(b, r, g)
                                            pp += 4
                                        elif (color_typ == "DeviceGray" and color_map is None): 
                                            if (pp < len(data)): 
                                                bb = data[pp]
                                                img.add_pixel_gray(bb)
                                                pp += 1
                                        elif (pp < len(data)): 
                                            b1 = data[pp]
                                            if (bpi_val == 4): 
                                                if (color_map is not None): 
                                                    img.add_pixel_index((((b1 >> 4)) & 0xF))
                                                    img.add_pixel_index((b1 & 0xF))
                                                    pp += 1
                                                elif ((pp + 2) < len(data)): 
                                                    b2 = data[pp + 1]
                                                    b3 = data[pp + 2]
                                                    img.add_pixel_rgb(b3, b1, b2)
                                                    img.add_pixel_rgb(b3, b1, b2)
                                                    pp += 3
                                            else: 
                                                img.add_pixel_index(b1)
                                                pp += 1
                                        w += 1
                                img.end_row()
                                row += 1
                            img.commit()
                            self.content = img.get_bytes()
                            return
    
    @staticmethod
    def __corrcmyk(b1 : int, b2 : int) -> int:
        i = b1
        i += (b2)
        if (i >= 256): 
            i = 256
        return (256 - i)
    
    def __str__(self) -> str:
        return "{0}: Image {1} bytes".format(super().__str__(), ("?" if self.content is None else str(len(self.content))))