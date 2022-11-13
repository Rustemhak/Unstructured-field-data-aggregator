# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math

from pullenti.unitext.internal.word.Pcd import Pcd

class PlcPcd:
    
    def __init__(self) -> None:
        self._cps = None;
        self._pcds = None;
    
    @staticmethod
    def _calc_length(size : int) -> int:
        return (math.floor((((size) - 4)) / ((4 + Pcd._size))))