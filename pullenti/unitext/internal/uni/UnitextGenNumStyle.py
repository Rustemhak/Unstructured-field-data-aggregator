# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.uni.IUnitextGenNumStyle import IUnitextGenNumStyle

class UnitextGenNumStyle(IUnitextGenNumStyle):
    # Стиль нумерации
    
    def __init__(self) -> None:
        self.__id = None;
        self.levels = list()
        self.__lvl = 0
        self.__isbullet = False
        self.__txt = None;
        self.__nums = list()
    
    @property
    def id0_(self) -> str:
        return self.__id
    @id0_.setter
    def id0_(self, value) -> str:
        self.__id = value
        return self.__id
    
    @property
    def lvl(self) -> int:
        return self.__lvl
    @lvl.setter
    def lvl(self, value) -> int:
        self.__lvl = value
        return self.__lvl
    
    @property
    def is_bullet(self) -> bool:
        return self.__isbullet
    @is_bullet.setter
    def is_bullet(self, value) -> bool:
        self.__isbullet = value
        return self.__isbullet
    
    @property
    def txt(self) -> str:
        return self.__txt
    @txt.setter
    def txt(self, value) -> str:
        self.__txt = value
        return self.__txt
    
    def __str__(self) -> str:
        if (self.txt is not None): 
            return "Level: {0} Val: {1}".format(self.lvl, self.txt)
        return "Id: {0} Levels: {1} FirstLevel: {2}".format(self.id0_, len(self.levels), ("" if len(self.levels) == 0 else str(self.levels[0])))
    
    def get_level(self, lev : int) -> 'UniTextGenNumLevel':
        if ((lev < 0) or lev >= len(self.levels)): 
            return None
        return self.levels[lev]
    
    def process(self, lev : int) -> str:
        if (self.txt is not None): 
            return self.txt
        if (lev >= len(self.levels)): 
            return None
        if (lev >= len(self.__nums)): 
            if (len(self.__nums) == 0): 
                ii = 0
                while ii <= lev: 
                    if (ii < len(self.levels)): 
                        self.__nums.append(self.levels[ii].start)
                    else: 
                        self.__nums.append(1)
                    ii += 1
            else: 
                while lev >= len(self.__nums):
                    if (lev < len(self.levels)): 
                        self.__nums.append(self.levels[lev].start)
                    else: 
                        self.__nums.append(1)
        elif (lev == (len(self.__nums) - 1)): 
            self.__nums[lev] += 1
            if (self.__nums[lev] < self.levels[lev].start): 
                self.__nums[lev] = self.levels[lev].start
        else: 
            if ((lev + 1) < len(self.__nums)): 
                del self.__nums[lev + 1:lev + 1+len(self.__nums) - lev - 1]
                k = lev + 1
                while k < len(self.levels): 
                    self.levels[k].start = 1
                    k += 1
            self.__nums[lev] += 1
        val = Utils.ifNotNull(self.levels[lev].format0_, "")
        ii = 0
        while ii <= lev: 
            if ("%" + str((ii + 1)) in val): 
                nn = self.levels[ii].get_value(self.__nums[ii])
                if (nn is not None): 
                    val = val.replace("%" + str((ii + 1)), nn)
            ii += 1
        return val
    
    @staticmethod
    def _new108(_arg1 : str) -> 'UnitextGenNumStyle':
        res = UnitextGenNumStyle()
        res.id0_ = _arg1
        return res