# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Xml import XmlWriter

class IXmlReadWriteSupport:
    """ Объекты, реализующие данный интерфейс, сериализуются одинаково на всех
    языках программирования. См. MiscHelper.SerializeToBin и MiscHelper.DeserializeFromBin.
    Универсальная сериализация
    """
    
    def write_to_xml(self, xml0_ : XmlWriter, tag_name : str) -> None:
        """ Сериализация в Xml
        
        Args:
            xml0_(XmlWriter): 
            tag_name(str): имя тега
        """
        pass
    
    def read_from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        """ Десериализация из узла Xml
        
        Args:
            xml0_(xml.etree.ElementTree.Element): узел
        """
        pass