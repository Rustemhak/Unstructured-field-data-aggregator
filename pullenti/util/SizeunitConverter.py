# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.MiscHelper import MiscHelper

class SizeunitConverter:
    """ Преобразователь единиц измерения размеров (Html, Css).
    Поддерживаются: pt, cm, mm, in, px """
    
    def __init__(self, num_with_unit : str=None) -> None:
        """ Конструктор
        
        Args:
            num_with_unit(str): строковое представление значения и единицы измерения
        """
        self.val = 0
        self.unit = None;
        if (not Utils.isNullOrEmpty(num_with_unit) and len(num_with_unit) > 2 and str.isalpha(num_with_unit[len(num_with_unit) - 1])): 
            self.unit = num_with_unit[len(num_with_unit) - 2:]
            d = 0
            wrapd605 = RefOutArgWrapper(0)
            inoutres606 = MiscHelper.try_parse_double(num_with_unit[0:0+len(num_with_unit) - 2].strip(), wrapd605)
            d = wrapd605.value
            if (inoutres606): 
                self.val = d
        else: 
            d = 0
            wrapd607 = RefOutArgWrapper(0)
            inoutres608 = MiscHelper.try_parse_double(num_with_unit, wrapd607)
            d = wrapd607.value
            if (inoutres608): 
                self.val = d
    
    def __str__(self) -> str:
        return "{0}{1}".format(MiscHelper.out_double(self.val), Utils.ifNotNull(self.unit, "?"))
    
    def convert_to(self, unit_ : str) -> 'SizeunitConverter':
        """ Преобразовать в новую единицу измерения
        
        Args:
            unit_(str): новая единица (pt, cm, mm, in, px)
        
        Returns:
            SizeunitConverter: результат или null
        """
        pt = 0
        if (self.unit == "pt" or Utils.isNullOrEmpty(self.unit)): 
            pt = self.val
        elif (self.unit == "cm"): 
            pt = ((self.val * (72)) / 2.54)
        elif (self.unit == "mm"): 
            pt = ((self.val * (72)) / 0.254)
        elif (self.unit == "in"): 
            pt = (self.val * (72))
        elif (self.unit == "px"): 
            pt = ((self.val * (72)) / (96))
        else: 
            return None
        val_ = 0
        if (unit_ == "pt"): 
            val_ = pt
        elif (unit_ == "cm"): 
            val_ = ((pt * 2.54) / (72))
        elif (unit_ == "mm"): 
            val_ = ((pt * 0.254) / (72))
        elif (unit_ == "in"): 
            val_ = (pt / (72))
        elif (unit_ == "px"): 
            val_ = ((pt * (96)) / (72))
        elif (Utils.isNullOrEmpty(unit_) and Utils.isNullOrEmpty(self.unit)): 
            val_ = pt
        elif (pt == 0): 
            val_ = (0)
        else: 
            return None
        res = SizeunitConverter()
        res.unit = unit_
        res.val = round(val_, 2)
        return res
    
    @staticmethod
    def convert(num_with_unit : str, new_unit : str) -> float:
        """ Преобразовать строку с числом и единицей измерения в другую единицу измерения
        
        Args:
            num_with_unit(str): число с единицей измерения
            new_unit(str): новая единица изменения (pt, cm, mm, in, px)
        
        Returns:
            float: результат или null
        """
        cnv = SizeunitConverter(num_with_unit)
        res = cnv.convert_to(new_unit)
        if (res is None): 
            return None
        return res.val