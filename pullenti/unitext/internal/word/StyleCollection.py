# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
from pullenti.unitext.internal.word.SinglePropertyValue import SinglePropertyValue

class StyleCollection:
    
    PROPERTY_NAME_PREFIX = "sprm"
    
    def get_indexer_item(self, name : str) -> object:
        return self.get(name)
    
    def __init__(self, prls : typing.List[typing.List['Prl']]) -> None:
        self.__prls = None;
        self.__prls = prls
    
    def __str__(self) -> str:
        res = io.StringIO()
        for prl_set in self.__prls: 
            for prl in prl_set: 
                s = SinglePropertyModifiers.get_sprm_name(prl._sprm._sprm)
                if (s is not None): 
                    print("{0}; ".format(s), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def get_by_ushort(self, sprm : int) -> object:
        for prl_set in self.__prls: 
            for prl in prl_set: 
                if (prl._sprm._sprm == sprm): 
                    return SinglePropertyValue._parse_value(sprm, prl._operand)
        return None
    
    def get(self, name : str) -> object:
        if (name is None): 
            raise Exception("name")
        sprm = SinglePropertyModifiers._get_sprm_by_name(name)
        for prl_set in self.__prls: 
            for prl in prl_set: 
                if (prl._sprm._sprm == sprm): 
                    return SinglePropertyValue._parse_value(sprm, prl._operand)
        return None
    
    def get_all(self, name : str) -> typing.List[object]:
        if (name is None): 
            raise Exception("name")
        sprm = SinglePropertyModifiers._get_sprm_by_name(name)
        res = list()
        for prl_set in self.__prls: 
            for prl in prl_set: 
                if (prl._sprm._sprm == sprm): 
                    res.append(SinglePropertyValue._parse_value(sprm, prl._operand))
        return res
    
    def get_names(self) -> typing.List[str]:
        return None