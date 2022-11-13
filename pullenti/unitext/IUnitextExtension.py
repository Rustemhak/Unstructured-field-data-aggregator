# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing

class IUnitextExtension:
    # Интерфейс для расширения функционала сервиса
    
    def create_document(self, frm : 'FileFormat', file_name : str, file_content : bytearray, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        return None
    
    def get_file_names_from_archive(self, file_name : str, content : bytearray) -> typing.List[tuple]:
        return None
    
    def get_files_from_archive(self, file_name : str, content : bytearray) -> typing.List['FileInArchive']:
        return None
    
    def get_file_from_archive(self, file_name : str, content : bytearray, internal_name : str) -> bytearray:
        return None