# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.zip.PendingBuffer import PendingBuffer
from pullenti.unitext.internal.zip.DeflaterConstants import DeflaterConstants

class DeflaterPending(PendingBuffer):
    # This class stores the pending output of the Deflater.
    
    def __init__(self) -> None:
        super().__init__(DeflaterConstants.PENDING_BUF_SIZE)