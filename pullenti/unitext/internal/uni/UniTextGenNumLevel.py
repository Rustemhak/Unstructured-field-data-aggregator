# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.uni.UniTextGenNumType import UniTextGenNumType
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper

class UniTextGenNumLevel:
    # Уровень стиля нумерации
    
    def __init__(self) -> None:
        self.type0_ = UniTextGenNumType.BULLET
        self.format0_ = None;
        self.start = 1
        self.current = 0
    
    def clone(self) -> 'UniTextGenNumLevel':
        res = UniTextGenNumLevel()
        res.type0_ = self.type0_
        res.format0_ = self.format0_
        res.start = self.start
        res.current = self.current
        return res
    
    def __str__(self) -> str:
        return "{0} '{1}' from {2}".format(Utils.enumToString(self.type0_), self.format0_, self.start)
    
    def get_value(self, cur : int) -> str:
        if (self.type0_ == UniTextGenNumType.BULLET): 
            return self.format0_
        if (self.type0_ == UniTextGenNumType.DECIMAL): 
            return str(cur)
        if (self.type0_ == UniTextGenNumType.LOWERLETTER): 
            return "{0}".format(chr((((ord('a')) + cur) - 1)))
        if (self.type0_ == UniTextGenNumType.LOWERCYRLETTER): 
            if (cur >= 10): 
                cur += 1
            return "{0}".format(chr((((ord('а')) + cur) - 1)))
        if (self.type0_ == UniTextGenNumType.UPPERCYRLETTER): 
            if (cur >= 10): 
                cur += 1
            return "{0}".format(chr((((ord('А')) + cur) - 1)))
        if (self.type0_ == UniTextGenNumType.UPPERLETTER): 
            return "{0}".format(chr((((ord('A')) + cur) - 1)))
        if (self.type0_ == UniTextGenNumType.LOWERROMAN): 
            if (cur > 0 and ((cur - 1) < len(UnitextHelper._m_romans))): 
                return UnitextHelper._m_romans[cur - 1].lower()
        if (self.type0_ == UniTextGenNumType.UPPERROMAN): 
            if (cur > 0 and ((cur - 1) < len(UnitextHelper._m_romans))): 
                return UnitextHelper._m_romans[cur - 1]
        return str(cur)
    
    @staticmethod
    def _new112(_arg1 : 'UniTextGenNumType') -> 'UniTextGenNumLevel':
        res = UniTextGenNumLevel()
        res.type0_ = _arg1
        return res
    
    @staticmethod
    def _new130(_arg1 : 'UniTextGenNumType', _arg2 : str) -> 'UniTextGenNumLevel':
        res = UniTextGenNumLevel()
        res.type0_ = _arg1
        res.format0_ = _arg2
        return res