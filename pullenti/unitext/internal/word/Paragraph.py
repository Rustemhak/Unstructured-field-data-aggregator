# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
from pullenti.unitext.internal.word.StyleCollection import StyleCollection
from pullenti.unitext.internal.word.FormattingLevel import FormattingLevel

class Paragraph(object):
    
    @property
    def offset(self) -> int:
        return self.__offset
    @offset.setter
    def offset(self, value) -> int:
        self.__offset = value
        return self.__offset
    
    @property
    def pos(self) -> int:
        return self._file_character_position._character_index + self.offset
    
    @property
    def length(self) -> int:
        return self.__length
    @length.setter
    def length(self, value) -> int:
        self.__length = value
        return self.__length
    
    @property
    def _file_character_position(self) -> 'FileCharacterPosition':
        return self.__filecharacterposition
    @_file_character_position.setter
    def _file_character_position(self, value) -> 'FileCharacterPosition':
        self.__filecharacterposition = value
        return self.__filecharacterposition
    
    @property
    def _papx_in_fkps(self) -> 'PapxInFkps':
        return self.__papxinfkps
    @_papx_in_fkps.setter
    def _papx_in_fkps(self, value) -> 'PapxInFkps':
        self.__papxinfkps = value
        return self.__papxinfkps
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("Pos:{0}, Len:{1}".format(self._file_character_position._character_index + self.offset, self.length), end="", file=res, flush=True)
        if (self.is_in_table): 
            print(" InTable ({0})".format(self.table_depth), end="", file=res, flush=True)
        if (self.is_list): 
            print(" IsList ({0})".format(self.list_level), end="", file=res, flush=True)
        if (self.is_table_cell_end): 
            print(" TableCellEnd", end="", file=res)
        if (self.is_table_row_end): 
            print(" TableRowEnd", end="", file=res)
        print(" {0}".format(self.get_styles(FormattingLevel.ALL)), end="", file=res, flush=True)
        if (self._papx_in_fkps is not None and self._papx_in_fkps._grpprl_in_papx is not None and self._papx_in_fkps._grpprl_in_papx._grpprl is not None): 
            for p in self._papx_in_fkps._grpprl_in_papx._grpprl: 
                print(" {0}".format(Utils.ifNotNull(SinglePropertyModifiers.get_sprm_name(p._sprm._sprm), "")), end="", file=res, flush=True)
        for p in self._file_character_position._prls: 
            print(" {0}".format(Utils.ifNotNull(SinglePropertyModifiers.get_sprm_name(p._sprm._sprm), "")), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def is_in_table(self) -> bool:
        data = self.get_property(SinglePropertyModifiers._sprmpfin_table)
        return data is not None and data[0] != (0)
    
    @property
    def table_depth(self) -> int:
        data = self.get_property(SinglePropertyModifiers._sprm_pitap)
        if (data is None): 
            return 0
        else: 
            return int.from_bytes(data[0:0+4], byteorder="little")
    
    @property
    def is_table_row_end(self) -> bool:
        pos_ = (self._file_character_position._character_index + self.offset + self.length) - 1
        if ((pos_ < self.__owner.text.tell()) and Utils.getCharAtStringIO(self.__owner.text, pos_) == '\u0007'): 
            data = self.get_property(SinglePropertyModifiers._sprmpfttp)
            if (data is not None and data[0] != (0)): 
                return True
        else: 
            data = self.get_property(SinglePropertyModifiers._sprmpfinner_ttp)
            if (data is not None and data[0] != (0)): 
                return True
        return False
    
    @property
    def is_table_cell_end(self) -> bool:
        pos_ = (self._file_character_position._character_index + self.offset + self.length) - 1
        if ((pos_ < self.__owner.text.tell()) and Utils.getCharAtStringIO(self.__owner.text, pos_) == '\u0007'): 
            return True
        else: 
            data = self.get_property(SinglePropertyModifiers._sprmpfinner_table_cell)
            return data is not None and data[0] != (0)
    
    @property
    def is_list(self) -> bool:
        data = self.get_property(SinglePropertyModifiers._sprm_pilfo)
        return data is not None and int.from_bytes(data[0:0+2], byteorder="little") != (0)
    
    @property
    def list_level(self) -> int:
        data = self.get_property(SinglePropertyModifiers._sprm_pilvl)
        return (data[0] if data is not None else 0)
    
    @property
    def style(self) -> 'StyleDefinition':
        return self.__owner.style_definitions_map[self._papx_in_fkps._grpprl_in_papx._istd]
    
    def __init__(self, owner : 'WordDocument', offset_ : int, length_ : int, fcp : 'FileCharacterPosition', papx_in_fkps : 'PapxInFkps') -> None:
        self.__owner = None;
        self.__offset = 0
        self.__length = 0
        self.__filecharacterposition = None;
        self.__papxinfkps = None;
        self.__owner = owner
        self.offset = offset_
        self.length = length_
        self._file_character_position = fcp
        self._papx_in_fkps = papx_in_fkps
    
    def get_property(self, sprm : int) -> bytearray:
        if (self._papx_in_fkps is not None and self._papx_in_fkps._grpprl_in_papx is not None and self._papx_in_fkps._grpprl_in_papx._grpprl is not None): 
            for p in self._papx_in_fkps._grpprl_in_papx._grpprl: 
                if (p._sprm._sprm == sprm): 
                    return p._operand
        for p in self._file_character_position._prls: 
            if (p._sprm._sprm == sprm): 
                return p._operand
        return None
    
    def get_styles(self, level : 'FormattingLevel') -> 'StyleCollection':
        if (level != FormattingLevel.PARAGRAPH and level != FormattingLevel.PARAGRAPHSTYLE): 
            return None
        prls = list()
        prls.append(self._papx_in_fkps._grpprl_in_papx._grpprl)
        if (level == FormattingLevel.PARAGRAPHSTYLE): 
            self.style._expand_styles(prls)
        return StyleCollection(prls)
    
    def compareTo(self, other : 'Paragraph') -> int:
        if (self.pos < other.pos): 
            return -1
        if (self.pos > other.pos): 
            return 1
        if (self.length < other.length): 
            return -1
        if (self.length > other.length): 
            return 1
        return 0