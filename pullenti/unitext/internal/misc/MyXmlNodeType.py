# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class MyXmlNodeType(IntEnum):
    NONE = 0
    ELEMENT = 1
    ATTRIBUTE = 2
    TEXT = 3
    CDATA = 4
    ENTITYREFERENCE = 5
    ENTITY = 6
    PROCESSINGINSTRUCTION = 7
    COMMENT = 8
    DOCUMENT = 9
    DOCUMENTTYPE = 10
    DOCUMENTFRAGMENT = 11
    NOTATION = 12
    WHITESPACE = 13
    SIGNIFICANTWHITESPACE = 14
    ENDELEMENT = 15
    ENDENTITY = 16
    XMLDECLARATION = 17
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)