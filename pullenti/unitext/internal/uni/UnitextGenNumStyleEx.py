# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.uni.IUnitextGenNumStyle import IUnitextGenNumStyle

class UnitextGenNumStyleEx(IUnitextGenNumStyle):
    
    def __init__(self) -> None:
        self.src = None;
        self.override_starts = dict()
        self.__m_overs = False
        self.__id = None;
    
    @property
    def id0_(self) -> str:
        return self.__id
    @id0_.setter
    def id0_(self, value) -> str:
        self.__id = value
        return self.__id
    
    @property
    def txt(self) -> str:
        return self.src.txt
    
    @property
    def lvl(self) -> int:
        return self.src.lvl
    
    @property
    def is_bullet(self) -> bool:
        return self.src.is_bullet
    
    def __str__(self) -> str:
        res = "Id={0} => {1}".format(self.id0_, str(self.src))
        for kp in self.override_starts.items(): 
            res = "{0} Strrt[{1}]={2}".format(res, kp[0], kp[1])
        return res
    
    def __prep(self) -> None:
        if (not self.__m_overs): 
            for kp in self.override_starts.items(): 
                if (kp[0] >= 0 and (kp[0] < len(self.src.levels))): 
                    self.src.levels[kp[0]].start = kp[1]
            self.__m_overs = True
    
    def get_level(self, lev : int) -> 'UniTextGenNumLevel':
        self.__prep()
        return self.src.get_level(lev)
    
    def process(self, lev : int) -> str:
        self.__prep()
        return self.src.process(lev)
    
    @staticmethod
    def _new413(_arg1 : 'UnitextGenNumStyle') -> 'UnitextGenNumStyleEx':
        res = UnitextGenNumStyleEx()
        res.src = _arg1
        return res