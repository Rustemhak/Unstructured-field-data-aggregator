# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.word.FibRbFcLcb2003 import FibRbFcLcb2003

class FibRbFcLcb2007(FibRbFcLcb2003):
    
    def __init__(self) -> None:
        super().__init__()
        self.__fcplcfmthd = 0
        self.__lcbplcfmthd = 0
        self.__fcsttbfbkmkmovefrom = 0
        self.__lcbsttbfbkmkmovefrom = 0
        self.__fcplcfbkfmovefrom = 0
        self.__lcbplcfbkfmovefrom = 0
        self.__fcplcfbklmovefrom = 0
        self.__lcbplcfbklmovefrom = 0
        self.__fcsttbfbkmkmoveto = 0
        self.__lcbsttbfbkmkmoveto = 0
        self.__fcplcfbkfmoveto = 0
        self.__lcbplcfbkfmoveto = 0
        self.__fcplcfbklmoveto = 0
        self.__lcbplcfbklmoveto = 0
        self.__fcunused11 = 0
        self.__lcbunused11 = 0
        self.__fcunused22 = 0
        self.__lcbunused22 = 0
        self.__fcunused33 = 0
        self.__lcbunused33 = 0
        self.__fcsttbfbkmkarto = 0
        self.__lcbsttbfbkmkarto = 0
        self.__fcplcfbkfarto = 0
        self.__lcbplcfbkfarto = 0
        self.__fcplcfbklarto = 0
        self.__lcbplcfbklarto = 0
        self.__fcartodata = 0
        self.__lcbartodata = 0
        self.__fcunused44 = 0
        self.__lcbunused44 = 0
        self.__fcunused5 = 0
        self.__lcbunused5 = 0
        self.__fcunused6 = 0
        self.__lcbunused6 = 0
        self.__fcosstheme = 0
        self.__lcbosstheme = 0
        self.__fccolorschememapping = 0
        self.__lcbcolorschememapping = 0
    
    @property
    def _fc_plcfmthd(self) -> int:
        return self.__fcplcfmthd
    @_fc_plcfmthd.setter
    def _fc_plcfmthd(self, value) -> int:
        self.__fcplcfmthd = value
        return self.__fcplcfmthd
    
    @property
    def _lcb_plcfmthd(self) -> int:
        return self.__lcbplcfmthd
    @_lcb_plcfmthd.setter
    def _lcb_plcfmthd(self, value) -> int:
        self.__lcbplcfmthd = value
        return self.__lcbplcfmthd
    
    @property
    def _fc_sttbf_bkmk_move_from(self) -> int:
        return self.__fcsttbfbkmkmovefrom
    @_fc_sttbf_bkmk_move_from.setter
    def _fc_sttbf_bkmk_move_from(self, value) -> int:
        self.__fcsttbfbkmkmovefrom = value
        return self.__fcsttbfbkmkmovefrom
    
    @property
    def _lcb_sttbf_bkmk_move_from(self) -> int:
        return self.__lcbsttbfbkmkmovefrom
    @_lcb_sttbf_bkmk_move_from.setter
    def _lcb_sttbf_bkmk_move_from(self, value) -> int:
        self.__lcbsttbfbkmkmovefrom = value
        return self.__lcbsttbfbkmkmovefrom
    
    @property
    def _fc_plcf_bkf_move_from(self) -> int:
        return self.__fcplcfbkfmovefrom
    @_fc_plcf_bkf_move_from.setter
    def _fc_plcf_bkf_move_from(self, value) -> int:
        self.__fcplcfbkfmovefrom = value
        return self.__fcplcfbkfmovefrom
    
    @property
    def _lcb_plcf_bkf_move_from(self) -> int:
        return self.__lcbplcfbkfmovefrom
    @_lcb_plcf_bkf_move_from.setter
    def _lcb_plcf_bkf_move_from(self, value) -> int:
        self.__lcbplcfbkfmovefrom = value
        return self.__lcbplcfbkfmovefrom
    
    @property
    def _fc_plcf_bkl_move_from(self) -> int:
        return self.__fcplcfbklmovefrom
    @_fc_plcf_bkl_move_from.setter
    def _fc_plcf_bkl_move_from(self, value) -> int:
        self.__fcplcfbklmovefrom = value
        return self.__fcplcfbklmovefrom
    
    @property
    def _lcb_plcf_bkl_move_from(self) -> int:
        return self.__lcbplcfbklmovefrom
    @_lcb_plcf_bkl_move_from.setter
    def _lcb_plcf_bkl_move_from(self, value) -> int:
        self.__lcbplcfbklmovefrom = value
        return self.__lcbplcfbklmovefrom
    
    @property
    def _fc_sttbf_bkmk_move_to(self) -> int:
        return self.__fcsttbfbkmkmoveto
    @_fc_sttbf_bkmk_move_to.setter
    def _fc_sttbf_bkmk_move_to(self, value) -> int:
        self.__fcsttbfbkmkmoveto = value
        return self.__fcsttbfbkmkmoveto
    
    @property
    def _lcb_sttbf_bkmk_move_to(self) -> int:
        return self.__lcbsttbfbkmkmoveto
    @_lcb_sttbf_bkmk_move_to.setter
    def _lcb_sttbf_bkmk_move_to(self, value) -> int:
        self.__lcbsttbfbkmkmoveto = value
        return self.__lcbsttbfbkmkmoveto
    
    @property
    def _fc_plcf_bkf_move_to(self) -> int:
        return self.__fcplcfbkfmoveto
    @_fc_plcf_bkf_move_to.setter
    def _fc_plcf_bkf_move_to(self, value) -> int:
        self.__fcplcfbkfmoveto = value
        return self.__fcplcfbkfmoveto
    
    @property
    def _lcb_plcf_bkf_move_to(self) -> int:
        return self.__lcbplcfbkfmoveto
    @_lcb_plcf_bkf_move_to.setter
    def _lcb_plcf_bkf_move_to(self, value) -> int:
        self.__lcbplcfbkfmoveto = value
        return self.__lcbplcfbkfmoveto
    
    @property
    def _fc_plcf_bkl_move_to(self) -> int:
        return self.__fcplcfbklmoveto
    @_fc_plcf_bkl_move_to.setter
    def _fc_plcf_bkl_move_to(self, value) -> int:
        self.__fcplcfbklmoveto = value
        return self.__fcplcfbklmoveto
    
    @property
    def _lcb_plcf_bkl_move_to(self) -> int:
        return self.__lcbplcfbklmoveto
    @_lcb_plcf_bkl_move_to.setter
    def _lcb_plcf_bkl_move_to(self, value) -> int:
        self.__lcbplcfbklmoveto = value
        return self.__lcbplcfbklmoveto
    
    @property
    def _fc_unused11(self) -> int:
        return self.__fcunused11
    @_fc_unused11.setter
    def _fc_unused11(self, value) -> int:
        self.__fcunused11 = value
        return self.__fcunused11
    
    @property
    def _lcb_unused11(self) -> int:
        return self.__lcbunused11
    @_lcb_unused11.setter
    def _lcb_unused11(self, value) -> int:
        self.__lcbunused11 = value
        return self.__lcbunused11
    
    @property
    def _fc_unused22(self) -> int:
        return self.__fcunused22
    @_fc_unused22.setter
    def _fc_unused22(self, value) -> int:
        self.__fcunused22 = value
        return self.__fcunused22
    
    @property
    def _lcb_unused22(self) -> int:
        return self.__lcbunused22
    @_lcb_unused22.setter
    def _lcb_unused22(self, value) -> int:
        self.__lcbunused22 = value
        return self.__lcbunused22
    
    @property
    def _fc_unused33(self) -> int:
        return self.__fcunused33
    @_fc_unused33.setter
    def _fc_unused33(self, value) -> int:
        self.__fcunused33 = value
        return self.__fcunused33
    
    @property
    def _lcb_unused33(self) -> int:
        return self.__lcbunused33
    @_lcb_unused33.setter
    def _lcb_unused33(self, value) -> int:
        self.__lcbunused33 = value
        return self.__lcbunused33
    
    @property
    def _fc_sttbf_bkmk_arto(self) -> int:
        return self.__fcsttbfbkmkarto
    @_fc_sttbf_bkmk_arto.setter
    def _fc_sttbf_bkmk_arto(self, value) -> int:
        self.__fcsttbfbkmkarto = value
        return self.__fcsttbfbkmkarto
    
    @property
    def _lcb_sttbf_bkmk_arto(self) -> int:
        return self.__lcbsttbfbkmkarto
    @_lcb_sttbf_bkmk_arto.setter
    def _lcb_sttbf_bkmk_arto(self, value) -> int:
        self.__lcbsttbfbkmkarto = value
        return self.__lcbsttbfbkmkarto
    
    @property
    def _fc_plcf_bkf_arto(self) -> int:
        return self.__fcplcfbkfarto
    @_fc_plcf_bkf_arto.setter
    def _fc_plcf_bkf_arto(self, value) -> int:
        self.__fcplcfbkfarto = value
        return self.__fcplcfbkfarto
    
    @property
    def _lcb_plcf_bkf_arto(self) -> int:
        return self.__lcbplcfbkfarto
    @_lcb_plcf_bkf_arto.setter
    def _lcb_plcf_bkf_arto(self, value) -> int:
        self.__lcbplcfbkfarto = value
        return self.__lcbplcfbkfarto
    
    @property
    def _fc_plcf_bkl_arto(self) -> int:
        return self.__fcplcfbklarto
    @_fc_plcf_bkl_arto.setter
    def _fc_plcf_bkl_arto(self, value) -> int:
        self.__fcplcfbklarto = value
        return self.__fcplcfbklarto
    
    @property
    def _lcb_plcf_bkl_arto(self) -> int:
        return self.__lcbplcfbklarto
    @_lcb_plcf_bkl_arto.setter
    def _lcb_plcf_bkl_arto(self, value) -> int:
        self.__lcbplcfbklarto = value
        return self.__lcbplcfbklarto
    
    @property
    def _fc_arto_data(self) -> int:
        return self.__fcartodata
    @_fc_arto_data.setter
    def _fc_arto_data(self, value) -> int:
        self.__fcartodata = value
        return self.__fcartodata
    
    @property
    def _lcb_arto_data(self) -> int:
        return self.__lcbartodata
    @_lcb_arto_data.setter
    def _lcb_arto_data(self, value) -> int:
        self.__lcbartodata = value
        return self.__lcbartodata
    
    @property
    def _fc_unused44(self) -> int:
        return self.__fcunused44
    @_fc_unused44.setter
    def _fc_unused44(self, value) -> int:
        self.__fcunused44 = value
        return self.__fcunused44
    
    @property
    def _lcb_unused44(self) -> int:
        return self.__lcbunused44
    @_lcb_unused44.setter
    def _lcb_unused44(self, value) -> int:
        self.__lcbunused44 = value
        return self.__lcbunused44
    
    @property
    def _fc_unused5(self) -> int:
        return self.__fcunused5
    @_fc_unused5.setter
    def _fc_unused5(self, value) -> int:
        self.__fcunused5 = value
        return self.__fcunused5
    
    @property
    def _lcb_unused5(self) -> int:
        return self.__lcbunused5
    @_lcb_unused5.setter
    def _lcb_unused5(self, value) -> int:
        self.__lcbunused5 = value
        return self.__lcbunused5
    
    @property
    def _fc_unused6(self) -> int:
        return self.__fcunused6
    @_fc_unused6.setter
    def _fc_unused6(self, value) -> int:
        self.__fcunused6 = value
        return self.__fcunused6
    
    @property
    def _lcb_unused6(self) -> int:
        return self.__lcbunused6
    @_lcb_unused6.setter
    def _lcb_unused6(self, value) -> int:
        self.__lcbunused6 = value
        return self.__lcbunused6
    
    @property
    def _fc_oss_theme(self) -> int:
        return self.__fcosstheme
    @_fc_oss_theme.setter
    def _fc_oss_theme(self, value) -> int:
        self.__fcosstheme = value
        return self.__fcosstheme
    
    @property
    def _lcb_oss_theme(self) -> int:
        return self.__lcbosstheme
    @_lcb_oss_theme.setter
    def _lcb_oss_theme(self, value) -> int:
        self.__lcbosstheme = value
        return self.__lcbosstheme
    
    @property
    def _fc_color_scheme_mapping(self) -> int:
        return self.__fccolorschememapping
    @_fc_color_scheme_mapping.setter
    def _fc_color_scheme_mapping(self, value) -> int:
        self.__fccolorschememapping = value
        return self.__fccolorschememapping
    
    @property
    def _lcb_color_scheme_mapping(self) -> int:
        return self.__lcbcolorschememapping
    @_lcb_color_scheme_mapping.setter
    def _lcb_color_scheme_mapping(self, value) -> int:
        self.__lcbcolorschememapping = value
        return self.__lcbcolorschememapping