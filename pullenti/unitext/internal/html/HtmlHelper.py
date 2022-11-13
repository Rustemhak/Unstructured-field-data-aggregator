# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.util.EncodingStandard import EncodingStandard
from pullenti.util.EncodingWrapper import EncodingWrapper
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.internal.html.UnitextHtmlGen import UnitextHtmlGen
from pullenti.unitext.internal.html.HtmlParser import HtmlParser
from pullenti.util.TextHelper import TextHelper

class HtmlHelper:
    
    @staticmethod
    def create_node(file_name : str, file_content : bytearray=None, content_type : str=None) -> 'HtmlNode':
        if (file_content is None): 
            file_content = UnitextHelper.load_data_from_file(file_name, 0)
        if (file_content is None): 
            return None
        str0_ = TextHelper.read_string_from_bytes(file_content, False)
        if (str0_ is None): 
            return None
        for k in range(2):
            str0 = (content_type if k == 0 else str0_)
            if (str0 is None): 
                continue
            i = str0.find("charset=")
            if (i > 0): 
                i += 8
                if (str0[i] == '\'' or str0[i] == '"'): 
                    i += 1
                j = 0
                j = i
                while j < len(str0): 
                    if (not str.isalnum(str0[j]) and str0[j] != '-'): 
                        break
                    j += 1
                if (j > i): 
                    encod = str0[i:i+j - i]
                    wr = EncodingWrapper(EncodingStandard.UNDEFINED, encod)
                    str0_ = wr.get_string(file_content, 0, -1)
                    break
        tmp = Utils.newStringIO(str0_)
        nod = HtmlParser.parse(tmp, False)
        return nod
    
    @staticmethod
    def create(nod : 'HtmlNode', dir_name : str, images : typing.List[tuple], pars : 'CreateDocumentParam') -> 'UnitextDocument':
        gen = UnitextHtmlGen()
        return gen.create(nod, dir_name, images, pars)