# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.word.GrLPUpxSw import GrLPUpxSw
from pullenti.unitext.internal.word.StkCharGRLPUPX import StkCharGRLPUPX
from pullenti.unitext.internal.word.StkTableGRLPUPX import StkTableGRLPUPX
from pullenti.unitext.internal.word.StkListGRLPUPX import StkListGRLPUPX
from pullenti.unitext.internal.word.StyleCollection import StyleCollection
from pullenti.unitext.internal.word.StdfBase import StdfBase
from pullenti.unitext.internal.word.StkParaGRLPUPX import StkParaGRLPUPX

class StyleDefinition:
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("'{0}'".format(self.name), end="", file=tmp, flush=True)
        print(str(self.get_styles()).format(), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @property
    def name(self) -> str:
        return str(self.__std._xstz_name)
    
    @property
    def is_text_style(self) -> bool:
        return self.__std._stdf._stdf_base._stk == (GrLPUpxSw._stk_chargrlpupxstk_value)
    
    def __init__(self, owner : 'WordDocument', std : 'STD') -> None:
        self.__owner = None;
        self.__std = None;
        self.__owner = owner
        self.__std = std
    
    def get_styles(self) -> 'StyleCollection':
        styles = list()
        self._expand_styles(styles)
        return StyleCollection(styles)
    
    def _expand_styles(self, styles : typing.List[typing.List['Prl']]) -> None:
        if (self.__std._stdf._stdf_base._istd_base != StdfBase._istd_null): 
            self.__owner.style_definitions_map[self.__std._stdf._stdf_base._istd_base]._expand_styles(styles)
        swichVal = self.__std._stdf._stdf_base._stk
        if (swichVal == GrLPUpxSw._stk_paragrlpupxstk_value): 
            styles.append(self.__std._grlpupx_sw._upx_papx._grpprl_papx)
            styles.append(self.__std._grlpupx_sw._upx_chpx._grpprl_chpx)
        elif (swichVal == GrLPUpxSw._stk_chargrlpupxstk_value): 
            styles.append(self.__std._grlpupx_sw._upx_chpx._grpprl_chpx)
        elif (swichVal == GrLPUpxSw._stk_tablegrlpupxstk_value): 
            styles.append(self.__std._grlpupx_sw._upx_tapx._grpprl_tapx)
            styles.append(self.__std._grlpupx_sw._upx_papx._grpprl_papx)
            styles.append(self.__std._grlpupx_sw._upx_chpx._grpprl_chpx)
        elif (swichVal == GrLPUpxSw._stk_listgrlpupxstk_value): 
            styles.append(self.__std._grlpupx_sw._upx_papx._grpprl_papx)