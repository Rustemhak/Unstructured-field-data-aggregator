# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class INameTransform:
    # INameTransform defines how file system names are transformed for use with archives, or vice versa.
    
    def transform_file(self, name : str) -> str:
        return None
    
    def transform_directory(self, name : str) -> str:
        return None