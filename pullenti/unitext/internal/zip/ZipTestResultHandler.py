# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class ZipTestResultHandler:
    """ Delegate invoked during <see cref="ZipFile.TestArchiveEx(bool, TestStrategy, ZipTestResultHandler)">testing</see> if supplied indicating current progress and status. """
    
    def call(self, status : 'TestStatus', message : str) -> None:
        pass