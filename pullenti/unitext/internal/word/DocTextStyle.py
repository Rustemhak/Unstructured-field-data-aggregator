# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

class DocTextStyle:
    
    def __init__(self) -> None:
        self.name = None;
        self.aliases = None;
        self.ustyle = None;
        self.num_id = None;
        self.num_lvl = 0
        self.is_default = False
    
    @property
    def is_heading(self) -> bool:
        if (self.name is not None): 
            if (Utils.startsWithString(self.name, "head", True)): 
                return True
        if (self.aliases is not None): 
            if (Utils.startsWithString(self.aliases, "head", True)): 
                return True
            if ("аголовок" in self.aliases): 
                return True
        return False
    
    def calc_heading_level(self) -> int:
        if (not self.is_heading): 
            return 0
        if (self.aliases is not None): 
            for i in range(len(self.aliases) - 1, -1, -1):
                if (not str.isdigit(self.aliases[i])): 
                    if ((i + 1) < len(self.aliases)): 
                        return int(self.aliases[i + 1:])
                    break
        if (self.name is not None): 
            for i in range(len(self.name) - 1, -1, -1):
                if (not str.isdigit(self.name[i])): 
                    if ((i + 1) < len(self.name)): 
                        return int(self.name[i + 1:])
                    break
        return 0
    
    def __str__(self) -> str:
        return self.name