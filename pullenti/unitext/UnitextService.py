# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.FileFormatClass import FileFormatClass
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.CreateDocumentParam import CreateDocumentParam
from pullenti.util.FileFormatsHelper import FileFormatsHelper

class UnitextService:
    """ Сервис поддержки технологии Unitext
    
    """
    
    VERSION = "4.14"
    """ Текущая версия """
    
    VERSION_DATE = "2022.09.01"
    """ Дата выхода версии """
    
    @staticmethod
    def create_document(file_name : str, file_content : bytearray=None, pars : 'CreateDocumentParam'=None) -> 'UnitextDocument':
        """ Создать документ из файла или байтового потока.
        ВНИМАНИЕ! Функция всегда возвращает экземпляр UnitextDocument и не выбрасывает Exceptions,
        а ошибки оформляются в свойстве ErrorMessage;
        
        Args:
            file_name(str): имя файла (может быть null)
            file_content(bytearray): содержимое файла (если null, то fileName есть имя файла в локальной файловой системе)
            pars(CreateDocumentParam): дополнительные параметры выделения (может быть null)
        
        Returns:
            UnitextDocument: экземпляр документа
        
        """
        from pullenti.unitext.internal.uni.UnitextCorrHelper import UnitextCorrHelper
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        if (pars is None): 
            pars = CreateDocumentParam()
        doc = UnitextHelper.create(file_name, file_content, pars)
        opt = False
        if (pars.correct_params is not None): 
            if (doc.correct(pars.correct_params)): 
                opt = True
        elif (doc.source_format == FileFormat.TXT or FileFormatsHelper.get_format_class(doc.source_format) == FileFormatClass.PAGELAYOUT): 
            UnitextCorrHelper.remove_page_break_numeration(doc)
            UnitextCorrHelper.remove_false_new_lines(doc, True)
        if (opt): 
            doc.optimize(False, None)
        if (pars.dont_generate_items_id): 
            doc.refresh_parents()
        else: 
            doc.generate_ids()
        if (doc.source_format == FileFormat.UNKNOWN): 
            doc.source_format = FileFormat.TXT
        return doc
    
    @staticmethod
    def create_document_from_text(text : str) -> 'UnitextDocument':
        """ Создать документ из чистого текста, при этом позиции всех элементов
        будут относительно именно его! GetPlaintext будет не генерировать, а возвращает именно его!
        
        Args:
            text(str): текст
        
        Returns:
            UnitextDocument: экземпляр документа
        
        """
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        if (Utils.isNullOrEmpty(text)): 
            return None
        doc = UnitextHelper.create_doc_from_text(text)
        doc.refresh_parents()
        return doc
    
    EXTENSION = None
    # Реализация извне дополнительного функцонала