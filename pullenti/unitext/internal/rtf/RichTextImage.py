# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.rtf.RichTextItem import RichTextItem

class RichTextImage(RichTextItem):
    
    def __init__(self) -> None:
        super().__init__()
        self.image = None;
        self.unique_id = 0
    
    def __str__(self) -> str:
        return "Image: {0} bytes ".format((0 if self.image is None else len(self.image)))