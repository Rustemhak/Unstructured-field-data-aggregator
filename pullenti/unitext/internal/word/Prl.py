# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class Prl:
    
    def __str__(self) -> str:
        return "Prl: " + str(self._sprm)
    
    def __init__(self, sprm : 'Sprm', operand : bytearray) -> None:
        self._sprm = None;
        self._operand = None;
        self._sprm = sprm
        self._operand = operand