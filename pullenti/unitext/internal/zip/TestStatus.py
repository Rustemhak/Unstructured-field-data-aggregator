# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.zip.TestOperation import TestOperation

class TestStatus:
    """ Status returned returned by <see cref="ZipTestResultHandler"/> during testing. """
    
    def __init__(self, file_ : 'ZipFile') -> None:
        """ Initialise a new instance of <see cref="TestStatus"/>
        
        Args:
            file_(ZipFile): The <see cref="ZipFile"/> this status applies to.
        """
        self.__m_file = None;
        self.__m_entry = None;
        self.__m_entry_valid = False
        self.__m_error_count = 0
        self.__m_bytes_tested = 0
        self.__m_operation = TestOperation.INITIALISING
        self.__m_file = file_
    
    @property
    def operation(self) -> 'TestOperation':
        """ Get the current <see cref="TestOperation"/> in progress. """
        return self.__m_operation
    
    @property
    def file(self) -> 'ZipFile':
        """ Get the <see cref="ZipFile"/> this status is applicable to. """
        return self.__m_file
    
    @property
    def entry(self) -> 'ZipEntry':
        """ Get the current/last entry tested. """
        return self.__m_entry
    
    @property
    def error_count(self) -> int:
        """ Get the number of errors detected so far. """
        return self.__m_error_count
    
    @property
    def bytes_tested(self) -> int:
        """ Get the number of bytes tested so far for the current entry. """
        return self.__m_bytes_tested
    
    @property
    def entry_valid(self) -> bool:
        """ Get a value indicating wether the last entry test was valid. """
        return self.__m_entry_valid
    
    def _add_error(self) -> None:
        self.__m_error_count += 1
        self.__m_entry_valid = False
    
    def _set_operation(self, operation_ : 'TestOperation') -> None:
        self.__m_operation = operation_
    
    def _set_entry(self, entry_ : 'ZipEntry') -> None:
        self.__m_entry = entry_
        self.__m_entry_valid = True
        self.__m_bytes_tested = 0
    
    def _set_bytes_tested(self, value : int) -> None:
        self.__m_bytes_tested = value