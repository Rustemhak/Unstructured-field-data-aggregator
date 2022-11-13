# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
from pullenti.unitext.internal.word.StyleCollection import StyleCollection
from pullenti.unitext.internal.word.FormattingLevel import FormattingLevel

class CharacterFormatting:
    
    @property
    def offset(self) -> int:
        return self.__offset
    @offset.setter
    def offset(self, value) -> int:
        self.__offset = value
        return self.__offset
    
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
    def pos(self) -> int:
        return self._file_character_position._character_index + self.offset
    
    @property
    def _chpx(self) -> 'Chpx':
        return self.__chpx
    @_chpx.setter
    def _chpx(self, value) -> 'Chpx':
        self.__chpx = value
        return self.__chpx
    
    def __str__(self) -> str:
        return "Pos:{0} Len:{1} Styles:{2}".format(self.pos, self.length, str(self.get_styles(FormattingLevel.CHARACTER)))
    
    @property
    def style(self) -> 'StyleDefinition':
        istd_data = self.get_property(SinglePropertyModifiers._sprm_cistd)
        if (istd_data is not None): 
            istd = int.from_bytes(istd_data[0:0+2], byteorder="little")
            if (istd in self.__owner.style_definitions_map): 
                return self.__owner.style_definitions_map[istd]
        return None
    
    def __init__(self, owner : 'WordDocument', offset_ : int, length_ : int, fcp : 'FileCharacterPosition', chpx : 'Chpx') -> None:
        self.__owner = None;
        self.__offset = 0
        self.__length = 0
        self.__filecharacterposition = None;
        self.__chpx = None;
        self.__owner = owner
        self.offset = offset_
        self.length = length_
        self._file_character_position = fcp
        self._chpx = chpx
    
    def get_property(self, sprm : int) -> bytearray:
        for p in self._chpx._grpprl: 
            if (p._sprm._sprm == sprm): 
                return p._operand
        for p in self._file_character_position._prls: 
            if (p._sprm._sprm == sprm): 
                return p._operand
        return None
    
    def get_styles(self, level : 'FormattingLevel'=FormattingLevel.CHARACTER) -> 'StyleCollection':
        prls = list()
        prls.append(self._chpx._grpprl)
        if (level == FormattingLevel.CHARACTERSTYLE): 
            def0_ = self.style
            if (def0_ is not None): 
                def0_._expand_styles(prls)
        return StyleCollection(prls)