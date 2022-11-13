# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class FileInArchive:
    """ Файл в архиве, см. ArchiveHelper.GetFilesFromArchive
    Файл в архиве
    """
    
    def __init__(self) -> None:
        self.key = None;
        self.content = None;
        self.tag = None;
    
    def __str__(self) -> str:
        return self.key
    
    @staticmethod
    def _new589(_arg1 : str, _arg2 : bytearray) -> 'FileInArchive':
        res = FileInArchive()
        res.key = _arg1
        res.content = _arg2
        return res