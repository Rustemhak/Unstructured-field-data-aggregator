# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class Fib:
    
    def __init__(self) -> None:
        self.__base = None;
        self.__csw = 0
        self.__fibrgw = None;
        self.__cslw = 0
        self.__fibrglw = None;
        self.__cbrgfclcb = 0
        self.__fibrgfclcbblob = None;
        self.__cswnew = 0
        self.__fibrgcswnew = None;
    
    @property
    def _base(self) -> 'FibBase':
        return self.__base
    @_base.setter
    def _base(self, value) -> 'FibBase':
        self.__base = value
        return self.__base
    
    @property
    def _csw(self) -> int:
        return self.__csw
    @_csw.setter
    def _csw(self, value) -> int:
        self.__csw = value
        return self.__csw
    
    @property
    def _fib_rgw(self) -> 'FibRgW97':
        return self.__fibrgw
    @_fib_rgw.setter
    def _fib_rgw(self, value) -> 'FibRgW97':
        self.__fibrgw = value
        return self.__fibrgw
    
    @property
    def _cslw(self) -> int:
        return self.__cslw
    @_cslw.setter
    def _cslw(self, value) -> int:
        self.__cslw = value
        return self.__cslw
    
    @property
    def _fib_rg_lw(self) -> 'FibRgLw97':
        return self.__fibrglw
    @_fib_rg_lw.setter
    def _fib_rg_lw(self, value) -> 'FibRgLw97':
        self.__fibrglw = value
        return self.__fibrglw
    
    @property
    def _cb_rg_fc_lcb(self) -> int:
        return self.__cbrgfclcb
    @_cb_rg_fc_lcb.setter
    def _cb_rg_fc_lcb(self, value) -> int:
        self.__cbrgfclcb = value
        return self.__cbrgfclcb
    
    @property
    def _fib_rg_fc_lcb_blob(self) -> 'FibRgFcLcb':
        return self.__fibrgfclcbblob
    @_fib_rg_fc_lcb_blob.setter
    def _fib_rg_fc_lcb_blob(self, value) -> 'FibRgFcLcb':
        self.__fibrgfclcbblob = value
        return self.__fibrgfclcbblob
    
    @property
    def _csw_new(self) -> int:
        return self.__cswnew
    @_csw_new.setter
    def _csw_new(self, value) -> int:
        self.__cswnew = value
        return self.__cswnew
    
    @property
    def _fib_rg_csw_new(self) -> 'FibRgCswNew':
        return self.__fibrgcswnew
    @_fib_rg_csw_new.setter
    def _fib_rg_csw_new(self, value) -> 'FibRgCswNew':
        self.__fibrgcswnew = value
        return self.__fibrgcswnew