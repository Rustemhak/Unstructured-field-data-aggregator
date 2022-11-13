# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

class WindowsPathUtils:
    # WindowsPathUtils provides simple utilities for handling windows paths.
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def drop_path_root(path : str) -> str:
        result = path
        if (((path is not None)) and ((len(path) > 0))): 
            if (((path[0] == '\\')) or ((path[0] == '/'))): 
                if (((len(path) > 1)) and ((((path[1] == '\\')) or ((path[1] == '/'))))): 
                    index = 2
                    elements = 2
                    while True:
                        elements -= 1
                        if (((index <= len(path))) and ((((((path[index] != '\\')) and ((path[index] != '/')))) or ((elements > 0))))): pass
                        else: 
                            break
                        index += 1
                    index += 1
                    if (index < len(path)): 
                        result = path[index:]
                    else: 
                        result = ""
            elif (((len(path) > 1)) and ((path[1] == ':'))): 
                drop_count = 2
                if (((len(path) > 2)) and ((((path[2] == '\\')) or ((path[2] == '/'))))): 
                    drop_count = 3
                result = result[drop_count:]
        return result