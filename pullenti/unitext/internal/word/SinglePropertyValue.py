# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.ReadUtils import ReadUtils
from pullenti.unitext.internal.word.ToggleOperand import ToggleOperand
from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
from pullenti.unitext.internal.word.ColorRef import ColorRef
from pullenti.unitext.internal.word.BasicTypesReader import BasicTypesReader

class SinglePropertyValue:
    
    @staticmethod
    def _parse_value(sprm : int, value : bytearray) -> object:
        swichVal = sprm
        if (swichVal == SinglePropertyModifiers._sprmcfrmark_del): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfrmark_ins): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcffld_vanish): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cpic_location): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cibst_rmark): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cdttm_rmark): 
            return SinglePropertyValue.__parsedttm(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfdata): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cidsl_rmark): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_csymbol): 
            return SinglePropertyValue.__parse_csymbol_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfole2): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_chighlight): 
            return SinglePropertyValue.__parse_ico(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfweb_hidden): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crsid_prop): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crsid_text): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crsidrmdel): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfspec_vanish): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfmath_pr): 
            return SinglePropertyValue.__parse_math_pr_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cistd): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cistd_permute): 
            return SinglePropertyValue.__parsesppoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cplain): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ckcd): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfbold): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfitalic): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfstrike): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfoutline): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfshadow): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfsmall_caps): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfcaps): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfvanish): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ckul): 
            return SinglePropertyValue.__parse_kul(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cdxa_space): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cico): 
            return SinglePropertyValue.__parse_ico(value)
        elif (swichVal == SinglePropertyModifiers._sprm_chps): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_chps_pos): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cmajority): 
            return SinglePropertyValue.__parse_cmajority_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ciss): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_chps_kern): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_chresi): 
            return SinglePropertyValue.__parse_hresi_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_ftc0): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_ftc1): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_ftc2): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cchar_scale): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfdstrike): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfimprint): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfspec): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfobj): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cprop_rmark90): 
            return SinglePropertyValue.__parse_prop_rmark_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfemboss): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_csfx_text): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfbi_di): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfbold_bi): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfitalic_bi): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cftc_bi): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_clid_bi): 
            return SinglePropertyValue.__parselid(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cico_bi): 
            return SinglePropertyValue.__parse_ico(value)
        elif (swichVal == SinglePropertyModifiers._sprm_chps_bi): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cdisp_fld_rmark): 
            return SinglePropertyValue.__parse_disp_fld_rm_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cibst_rmark_del): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cdttm_rmark_del): 
            return SinglePropertyValue.__parsedttm(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cbrc80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cshd80): 
            return SinglePropertyValue.__parse_shd80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cidsl_rmark_del): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfuse_pgsu_settings): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_lid0_80): 
            return SinglePropertyValue.__parselid(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_lid1_80): 
            return SinglePropertyValue.__parselid(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cidct_hint): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ccv): 
            return SinglePropertyValue.__parsecolorref(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cshd): 
            return SinglePropertyValue.__parseshdoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cbrc): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_lid0): 
            return SinglePropertyValue.__parselid(value)
        elif (swichVal == SinglePropertyModifiers._sprm_crg_lid1): 
            return SinglePropertyValue.__parselid(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfno_proof): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cfit_text): 
            return SinglePropertyValue.__parse_cfit_text_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ccv_ul): 
            return SinglePropertyValue.__parsecolorref(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfelayout): 
            return SinglePropertyValue.__parse_far_east_layout_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_clbccrj): 
            return SinglePropertyValue.__parselbcoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfcomplex_scripts): 
            return SinglePropertyValue.__parse_toggle_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cwall): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ccnf): 
            return SinglePropertyValue.__parsecnfoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cneed_font_fixup): 
            return SinglePropertyValue.__parseffm(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cpbi_ibullet): 
            return SinglePropertyValue.__parsecp(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cpbi_grf): 
            return SinglePropertyValue.__parse_pbi_grf_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_cprop_rmark): 
            return SinglePropertyValue.__parse_prop_rmark_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmcfsdt_vanish): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pistd): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pistd_permute): 
            return SinglePropertyValue.__parsesppoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pinc_lvl): 
            return SinglePropertyValue.__parse_sbyte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pjc80): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfkeep): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfkeep_follow): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfpage_break_before): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pilvl): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pilfo): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfno_line_numb): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pchg_tabs_papx): 
            return SinglePropertyValue.__parse_pchg_tabs_papx_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_right80): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_left80): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pnest80): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_left180): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdya_line): 
            return SinglePropertyValue.__parselspd(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdya_before): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdya_after): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pchg_tabs): 
            return SinglePropertyValue.__parse_pchg_tabs_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfin_table): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfttp): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_abs): 
            return SinglePropertyValue.__parsexas_plus_one(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdya_abs): 
            return SinglePropertyValue.__parseyas_plus_one(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_width): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ppc): 
            return SinglePropertyValue.__parse_position_code_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pwr): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_top80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_left80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_bottom80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_right80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_between80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_bar80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfno_auto_hyph): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpwheight_abs): 
            return SinglePropertyValue.__parse_wheight_abs(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdcs): 
            return SinglePropertyValue.__parsedcs(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pshd80): 
            return SinglePropertyValue.__parse_shd80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdya_from_text): 
            return SinglePropertyValue.__parseyas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_from_text): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprmpflocked): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfwidow_control): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfkinsoku): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfword_wrap): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfoverflow_punct): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpftop_line_punct): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfauto_spacede): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfauto_spacedn): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpwalign_font): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pframe_text_flow): 
            return SinglePropertyValue.__parse_frame_text_flow_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pout_lvl): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfbi_di): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfnumrmins): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pnumrm): 
            return SinglePropertyValue.__parse_numrmoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_phuge_papx): 
            return SinglePropertyValue.__parse_uint32(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfuse_pgsu_settings): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfadjust_right): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pitap): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdtap): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfinner_table_cell): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfinner_ttp): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pshd): 
            return SinglePropertyValue.__parseshdoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_top): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_left): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_bottom): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_right): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_between): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pbrc_bar): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxc_right): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxc_left): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxc_left1): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdyl_before): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdyl_after): 
            return SinglePropertyValue.__parse_int16(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfopen_tch): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfdya_before_auto): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfdya_after_auto): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_right): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_left): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pnest): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pdxa_left1): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pjc): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfno_allow_overlap): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pwall): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pipgp): 
            return SinglePropertyValue.__parse_uint32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pcnf): 
            return SinglePropertyValue.__parsecnfoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_prsid): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pistd_list_permute): 
            return SinglePropertyValue.__parsesppoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ptable_props): 
            return SinglePropertyValue.__parse_uint32(value)
        elif (swichVal == SinglePropertyModifiers._sprmptistd_info): 
            return SinglePropertyValue.__parseptistd_info_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfcontextual_spacing): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pprop_rmark): 
            return SinglePropertyValue.__parse_prop_rmark_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmpfmirror_indents): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pttwo): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tjc90): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdxa_left): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdxa_gap_half): 
            return SinglePropertyValue.__parsexas(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfcant_split90): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ttable_header): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ttable_borders80): 
            return SinglePropertyValue.__parse_table_borders_operand80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdya_row_height): 
            return SinglePropertyValue.__parseyas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table): 
            return SinglePropertyValue.__parse_tdef_table_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd80): 
            return SinglePropertyValue.__parse_def_table_shd80operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ttlp): 
            return SinglePropertyValue.__parsetlp(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfbi_di): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd3rd): 
            return SinglePropertyValue.__parse_def_table_shd_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tpc): 
            return SinglePropertyValue.__parse_position_code_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdxa_abs): 
            return SinglePropertyValue.__parsexas_plus_one(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdya_abs): 
            return SinglePropertyValue.__parseyas_plus_one(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdxa_from_text): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdya_from_text): 
            return SinglePropertyValue.__parseyas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd): 
            return SinglePropertyValue.__parse_def_table_shd_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ttable_borders): 
            return SinglePropertyValue.__parse_table_borders_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ttable_width): 
            return SinglePropertyValue.__parse_fts_wwidth_table(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfautofit): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd2nd): 
            return SinglePropertyValue.__parse_def_table_shd_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_twidth_before): 
            return SinglePropertyValue.__parse_fts_wwidth_table_part(value)
        elif (swichVal == SinglePropertyModifiers._sprm_twidth_after): 
            return SinglePropertyValue.__parse_fts_wwidth_table_part(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfkeep_follow): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tbrc_top_cv): 
            return SinglePropertyValue.__parse_brc_cv_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tbrc_left_cv): 
            return SinglePropertyValue.__parse_brc_cv_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tbrc_bottom_cv): 
            return SinglePropertyValue.__parse_brc_cv_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tbrc_right_cv): 
            return SinglePropertyValue.__parse_brc_cv_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdxa_from_text_right): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdya_from_text_bottom): 
            return SinglePropertyValue.__parseyas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tset_brc80): 
            return SinglePropertyValue.__parse_table_brc80operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tinsert): 
            return SinglePropertyValue.__parse_tinsert_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdelete): 
            return SinglePropertyValue.__parse_itc_first_lim(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdxa_col): 
            return SinglePropertyValue.__parse_tdxa_col_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tmerge): 
            return SinglePropertyValue.__parse_itc_first_lim(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tsplit): 
            return SinglePropertyValue.__parse_itc_first_lim(value)
        elif (swichVal == SinglePropertyModifiers._sprm_ttext_flow): 
            return SinglePropertyValue.__parse_cell_range_text_flow(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tvert_merge): 
            return SinglePropertyValue.__parse_vert_merge_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tvert_align): 
            return SinglePropertyValue.__parse_cell_range_vert_align(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tset_shd): 
            return SinglePropertyValue.__parse_table_shade_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tset_shd_odd): 
            return SinglePropertyValue.__parse_table_shade_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tset_brc): 
            return SinglePropertyValue.__parse_table_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_padding): 
            return SinglePropertyValue.__parsecssaoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_spacing_default): 
            return SinglePropertyValue.__parsecssaoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_padding_default): 
            return SinglePropertyValue.__parsecssaoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_width): 
            return SinglePropertyValue.__parse_table_cell_width_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tfit_text): 
            return SinglePropertyValue.__parse_cell_range_fit_text(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfcell_no_wrap): 
            return SinglePropertyValue.__parse_cell_range_no_wrap(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tistd): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_padding_style): 
            return SinglePropertyValue.__parsecssaoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_fhide_mark): 
            return SinglePropertyValue.__parse_cell_hide_mark_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tset_shd_table): 
            return SinglePropertyValue.__parseshdoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_twidth_indent): 
            return SinglePropertyValue.__parse_fts_wwidth_indent(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_type): 
            return SinglePropertyValue.__parse_tcell_brc_type_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfbi_di90): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfno_allow_overlap): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmtfcant_split): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tprop_rmark): 
            return SinglePropertyValue.__parse_prop_rmark_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_twall): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tipgp): 
            return SinglePropertyValue.__parse_uint32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcnf): 
            return SinglePropertyValue.__parsecnfoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd_raw): 
            return SinglePropertyValue.__parse_def_table_shd_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd_raw2nd): 
            return SinglePropertyValue.__parse_def_table_shd_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tdef_table_shd_raw3rd): 
            return SinglePropertyValue.__parse_def_table_shd_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_trsid): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_vert_align_style): 
            return SinglePropertyValue.__parse_vertical_align(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_no_wrap_style): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_top_style): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_bottom_style): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_left_style): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_right_style): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_inside_hstyle): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brc_inside_vstyle): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brctl2brstyle): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_brctr2blstyle): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tcell_shd_style): 
            return SinglePropertyValue.__parseshdoperand(value)
        elif (swichVal == SinglePropertyModifiers._sprmtchorz_bands): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprmtcvert_bands): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_tjc): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_scns_pgn): 
            return SinglePropertyValue.__parsecns(value)
        elif (swichVal == SinglePropertyModifiers._sprm_si_heading_pgn): 
            return SinglePropertyValue.__parse_byte(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxa_col_width): 
            return SinglePropertyValue.__parse_sdxa_col_width_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxa_col_spacing): 
            return SinglePropertyValue.__parse_sdxa_col_spacing_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmsfevenly_spaced): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmsfprotected): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdm_bin_first): 
            return SinglePropertyValue.__parse_sdm_bin_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdm_bin_other): 
            return SinglePropertyValue.__parse_sdm_bin_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbkc): 
            return SinglePropertyValue.__parse_sbkc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmsftitle_page): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sccolumns): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxa_columns): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_snfc_pgn): 
            return SinglePropertyValue.__parsemsonfc(value)
        elif (swichVal == SinglePropertyModifiers._sprmsfpgn_restart): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmsfendnote): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_slnc): 
            return SinglePropertyValue.__parse_slnc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprmsnlnn_mod): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxa_lnn): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdya_hdr_top): 
            return SinglePropertyValue.__parseyas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdya_hdr_bottom): 
            return SinglePropertyValue.__parseyas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprmslbetween): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_svjc): 
            return SinglePropertyValue.__parse_vic(value)
        elif (swichVal == SinglePropertyModifiers._sprm_slnn_min): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_spgn_start97): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprmsborientation): 
            return SinglePropertyValue.__parsesborientation_operan(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sxa_page): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sya_page): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxa_left): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxa_right): 
            return SinglePropertyValue.__parsexas_non_neg(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdya_top): 
            return SinglePropertyValue.__parseyas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdya_bottom): 
            return SinglePropertyValue.__parseyas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdza_gutter): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdm_paper_req): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprmsfbi_di): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprmsfrtlgutter): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_top80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_left80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_bottom80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_right80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_spgb_prop): 
            return SinglePropertyValue.__parse_spgb_prop_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdxt_char_space): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sdya_line_pitch): 
            return SinglePropertyValue.__parseyas(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sclm): 
            return SinglePropertyValue.__parse_sclm_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_stext_flow): 
            return SinglePropertyValue.__parsemsotxfl(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_top): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_left): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_bottom): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sbrc_right): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_swall): 
            return SinglePropertyValue.__parse_bool(value)
        elif (swichVal == SinglePropertyModifiers._sprm_srsid): 
            return SinglePropertyValue.__parse_int32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sfpc): 
            return SinglePropertyValue.__parse_sfpc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_srnc_ftn): 
            return SinglePropertyValue.__parse_rnc(value)
        elif (swichVal == SinglePropertyModifiers._sprm_srnc_edn): 
            return SinglePropertyValue.__parse_rnc(value)
        elif (swichVal == SinglePropertyModifiers._sprmsnftn): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_snfc_ftn_ref): 
            return SinglePropertyValue.__parsemsonfc(value)
        elif (swichVal == SinglePropertyModifiers._sprmsnedn): 
            return SinglePropertyValue.__parse_uint16(value)
        elif (swichVal == SinglePropertyModifiers._sprm_snfc_edn_ref): 
            return SinglePropertyValue.__parsemsonfc(value)
        elif (swichVal == SinglePropertyModifiers._sprm_sprop_rmark): 
            return SinglePropertyValue.__parse_prop_rmark_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_spgn_start): 
            return SinglePropertyValue.__parse_uint32(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_top80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_left80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_bottom80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_right80): 
            return SinglePropertyValue.__parse_brc80(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_top): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_left): 
            return SinglePropertyValue.__parse_brc_operand(value)
        elif (swichVal == SinglePropertyModifiers._sprm_pic_brc_bottom): 
            return SinglePropertyValue.__parse_brc_operand(value)
        else: 
            raise Utils.newException("Unknow sprm value", None)
    
    __dpt_constant = 0.125
    
    __dxa_constant = 0.125
    
    @staticmethod
    def __parse_bool(value : bytearray) -> object:
        return value[0] != (0)
    
    @staticmethod
    def __parse_brc80(value : bytearray) -> object:
        result = dict()
        result["LineWidth"] = (value[0]) * SinglePropertyValue.__dpt_constant
        result["BorderType"] = value[1]
        result["Color"] = value[2]
        result["Space"] = (((value[3]) & 0x1F)) * SinglePropertyValue.__dpt_constant
        result["Shadow"] = (((value[3]) & 0x20)) != 0
        result["Frame"] = (((value[3]) & 0x40)) != 0
        return result
    
    @staticmethod
    def __parse_brc_cv_operand(value : bytearray) -> object:
        return [ColorRef._from_bytes(value, 0), ColorRef._from_bytes(value, 4), ColorRef._from_bytes(value, 8), ColorRef._from_bytes(value, 12)]
    
    @staticmethod
    def __parse_brc_operand(value : bytearray) -> object:
        result = dict()
        result["Color"] = ColorRef._from_bytes(value, 0)
        result["LineWidth"] = (value[4]) * SinglePropertyValue.__dpt_constant
        result["BorderType"] = value[5]
        result["Space"] = (((value[6]) & 0x1F)) * SinglePropertyValue.__dpt_constant
        result["Shadow"] = (((value[6]) & 0x20)) != 0
        result["Frame"] = (((value[6]) & 0x40)) != 0
        return result
    
    @staticmethod
    def __parse_byte(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parse_cell_hide_mark_operand(value : bytearray) -> object:
        result = dict()
        result["Range"] = [value[0], value[1]]
        result["NoHeight"] = value[2] != (0)
        return result
    
    @staticmethod
    def __parse_cell_range_fit_text(value : bytearray) -> object:
        result = dict()
        result["Range"] = [value[0], value[1]]
        result["FitText"] = value[2] != (0)
        return result
    
    @staticmethod
    def __parse_cell_range_no_wrap(value : bytearray) -> object:
        result = dict()
        result["Range"] = [value[0], value[1]]
        result["NoWrap"] = value[2] != (0)
        return result
    
    @staticmethod
    def __parse_cell_range_text_flow(value : bytearray) -> object:
        result = dict()
        result["Range"] = [value[0], value[1]]
        result["TextFlow"] = int.from_bytes(value[2:2+2], byteorder="little")
        return result
    
    @staticmethod
    def __parse_cell_range_vert_align(value : bytearray) -> object:
        result = dict()
        result["Range"] = [value[0], value[1]]
        result["VertAlign"] = value[2]
        return result
    
    @staticmethod
    def __parse_cfit_text_operand(value : bytearray) -> object:
        result = dict()
        result["FitText"] = (int.from_bytes(value[0:0+4], byteorder="little")) * SinglePropertyValue.__dxa_constant
        result["FitTextID"] = int.from_bytes(value[2:2+4], byteorder="little")
        return result
    
    @staticmethod
    def __parse_cmajority_operand(value : bytearray) -> object:
        with MemoryStream(value) as ms: 
            read = 0
            wrapread488 = RefOutArgWrapper(read)
            prls = BasicTypesReader._read_prls(ms, len(value), wrapread488)
            read = wrapread488.value
            result = dict()
            for prl in prls: 
                name = SinglePropertyModifiers._map0_[prl._sprm._sprm]
                result[name[4:]] = SinglePropertyValue._parse_value(prl._sprm._sprm, prl._operand)
            return result
    
    @staticmethod
    def __parsecnfoperand(value : bytearray) -> object:
        with MemoryStream(value) as ms: 
            read = 0
            result = dict()
            wrapread490 = RefOutArgWrapper(read)
            result["$FormattingCondition"] = int.from_bytes(ReadUtils._read_exact_ref(ms, ReadUtils._word_size, wrapread490)[0:0+2], byteorder="little")
            read = wrapread490.value
            wrapread489 = RefOutArgWrapper(read)
            prls = BasicTypesReader._read_prls(ms, len(value) - read, wrapread489)
            read = wrapread489.value
            for prl in prls: 
                name = SinglePropertyModifiers._map0_[prl._sprm._sprm]
                result[name[4:]] = SinglePropertyValue._parse_value(prl._sprm._sprm, prl._operand)
            return result
    
    @staticmethod
    def __parsecns(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parsecolorref(value : bytearray) -> object:
        return ColorRef._from_bytes(value, 0)
    
    @staticmethod
    def __parsecp(value : bytearray) -> object:
        return int.from_bytes(value[0:0+4], byteorder="little")
    
    @staticmethod
    def __parsecssaoperand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_csymbol_operand(value : bytearray) -> object:
        result = dict()
        result["FontIndex"] = int.from_bytes(value[0:0+2], byteorder="little")
        result["Symbol"] = chr(int.from_bytes(value[2:2+2], byteorder="little"))
        return result
    
    @staticmethod
    def __parsedcs(value : bytearray) -> object:
        result = dict()
        result["DropCap"] = ((value[0]) & 0x1F)
        result["DropLines"] = ((value[0]) >> 5)
        return result
    
    @staticmethod
    def __parse_def_table_shd80operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_def_table_shd_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_disp_fld_rm_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsedttm(value : bytearray) -> object:
        return BasicTypesReader._parsedttm(int.from_bytes(value[0:0+4], byteorder="little"))
    
    @staticmethod
    def __parse_far_east_layout_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parseffm(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parse_frame_text_flow_operand(value : bytearray) -> object:
        result = dict()
        result["Vertical"] = (((value[0]) & 0x01)) != 0
        result["Backwards"] = (((value[0]) & 0x02)) != 0
        result["RotateFont"] = (((value[0]) & 0x04)) != 0
        return result
    
    @staticmethod
    def __parse_fts_wwidth_indent(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_fts_wwidth_table(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_fts_wwidth_table_part(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_hresi_operand(value : bytearray) -> object:
        result = dict()
        result["WordBreakingMethod"] = value[0]
        result["Character"] = chr(value[1])
        return result
    
    @staticmethod
    def __parse_ico(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parse_int16(value : bytearray) -> object:
        return int.from_bytes(value[0:0+2], byteorder="little")
    
    @staticmethod
    def __parse_int32(value : bytearray) -> object:
        return int.from_bytes(value[0:0+4], byteorder="little")
    
    @staticmethod
    def __parse_itc_first_lim(value : bytearray) -> object:
        return [value[0], value[1]]
    
    @staticmethod
    def __parse_kul(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parselbcoperand(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parselid(value : bytearray) -> object:
        return int.from_bytes(value[0:0+2], byteorder="little")
    
    @staticmethod
    def __parselspd(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_math_pr_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsemsonfc(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsemsotxfl(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_numrmoperand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_pbi_grf_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_pchg_tabs_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_pchg_tabs_papx_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_position_code_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_prop_rmark_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parseptistd_info_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_rnc(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_sbkc_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsesborientation_operan(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_sbyte(value : bytearray) -> object:
        return value[0]
    
    @staticmethod
    def __parse_sclm_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_sdm_bin_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_sdxa_col_spacing_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_sdxa_col_width_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_sfpc_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_shd80(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parseshdoperand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_slnc_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_spgb_prop_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsesppoperand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_table_borders_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_table_borders_operand80(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_table_brc80operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_table_brc_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_table_cell_width_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_table_shade_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_tcell_brc_type_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_tdef_table_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_tdxa_col_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_tinsert_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsetlp(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_toggle_operand(value : bytearray) -> object:
        return Utils.valToEnum(value[0], ToggleOperand)
    
    @staticmethod
    def __parse_uint16(value : bytearray) -> object:
        return int.from_bytes(value[0:0+2], byteorder="little")
    
    @staticmethod
    def __parse_uint32(value : bytearray) -> object:
        return int.from_bytes(value[0:0+4], byteorder="little")
    
    @staticmethod
    def __parse_vertical_align(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_vert_merge_operand(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_vic(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parse_wheight_abs(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsexas(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsexas_non_neg(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parsexas_plus_one(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parseyas(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parseyas_non_neg(value : bytearray) -> object:
        raise Exception()
    
    @staticmethod
    def __parseyas_plus_one(value : bytearray) -> object:
        raise Exception()