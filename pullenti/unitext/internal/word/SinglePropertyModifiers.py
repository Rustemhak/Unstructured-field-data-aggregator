# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class SinglePropertyModifiers:
    
    _sprmcfrmark_del = 0x0800
    
    _sprmcfrmark_ins = 0x0801
    
    _sprmcffld_vanish = 0x0802
    
    _sprm_cpic_location = 0x6A03
    
    _sprm_cibst_rmark = 0x4804
    
    _sprm_cdttm_rmark = 0x6805
    
    _sprmcfdata = 0x0806
    
    _sprm_cidsl_rmark = 0x4807
    
    _sprm_csymbol = 0x6A09
    
    _sprmcfole2 = 0x080A
    
    _sprm_chighlight = 0x2A0C
    
    _sprmcfweb_hidden = 0x0811
    
    _sprm_crsid_prop = 0x6815
    
    _sprm_crsid_text = 0x6816
    
    _sprm_crsidrmdel = 0x6817
    
    _sprmcfspec_vanish = 0x0818
    
    _sprmcfmath_pr = 0xC81A
    
    _sprm_cistd = 0x4A30
    
    _sprm_cistd_permute = 0xCA31
    
    _sprm_cplain = 0x2A33
    
    _sprm_ckcd = 0x2A34
    
    _sprmcfbold = 0x0835
    
    _sprmcfitalic = 0x0836
    
    _sprmcfstrike = 0x0837
    
    _sprmcfoutline = 0x0838
    
    _sprmcfshadow = 0x0839
    
    _sprmcfsmall_caps = 0x083A
    
    _sprmcfcaps = 0x083B
    
    _sprmcfvanish = 0x083C
    
    _sprm_ckul = 0x2A3E
    
    _sprm_cdxa_space = 0x8840
    
    _sprm_cico = 0x2A42
    
    _sprm_chps = 0x4A43
    
    _sprm_chps_pos = 0x4845
    
    _sprm_cmajority = 0xCA47
    
    _sprm_ciss = 0x2A48
    
    _sprm_chps_kern = 0x484B
    
    _sprm_chresi = 0x484E
    
    _sprm_crg_ftc0 = 0x4A4F
    
    _sprm_crg_ftc1 = 0x4A50
    
    _sprm_crg_ftc2 = 0x4A51
    
    _sprm_cchar_scale = 0x4852
    
    _sprmcfdstrike = 0x2A53
    
    _sprmcfimprint = 0x0854
    
    _sprmcfspec = 0x0855
    
    _sprmcfobj = 0x0856
    
    _sprm_cprop_rmark90 = 0xCA57
    
    _sprmcfemboss = 0x0858
    
    _sprm_csfx_text = 0x2859
    
    _sprmcfbi_di = 0x085A
    
    _sprmcfbold_bi = 0x085C
    
    _sprmcfitalic_bi = 0x085D
    
    _sprm_cftc_bi = 0x4A5E
    
    _sprm_clid_bi = 0x485F
    
    _sprm_cico_bi = 0x4A60
    
    _sprm_chps_bi = 0x4A61
    
    _sprm_cdisp_fld_rmark = 0xCA62
    
    _sprm_cibst_rmark_del = 0x4863
    
    _sprm_cdttm_rmark_del = 0x6864
    
    _sprm_cbrc80 = 0x6865
    
    _sprm_cshd80 = 0x4866
    
    _sprm_cidsl_rmark_del = 0x4867
    
    _sprmcfuse_pgsu_settings = 0x0868
    
    _sprm_crg_lid0_80 = 0x486D
    
    _sprm_crg_lid1_80 = 0x486E
    
    _sprm_cidct_hint = 0x286F
    
    _sprm_ccv = 0x6870
    
    _sprm_cshd = 0xCA71
    
    _sprm_cbrc = 0xCA72
    
    _sprm_crg_lid0 = 0x4873
    
    _sprm_crg_lid1 = 0x4874
    
    _sprmcfno_proof = 0x0875
    
    _sprm_cfit_text = 0xCA76
    
    _sprm_ccv_ul = 0x6877
    
    _sprmcfelayout = 0xCA78
    
    _sprm_clbccrj = 0x2879
    
    _sprmcfcomplex_scripts = 0x0882
    
    _sprm_cwall = 0x2A83
    
    _sprm_ccnf = 0xCA85
    
    _sprm_cneed_font_fixup = 0x2A86
    
    _sprm_cpbi_ibullet = 0x6887
    
    _sprm_cpbi_grf = 0x4888
    
    _sprm_cprop_rmark = 0xCA89
    
    _sprmcfsdt_vanish = 0x2A90
    
    _sprm_pistd = 0x4600
    
    _sprm_pistd_permute = 0xC601
    
    _sprm_pinc_lvl = 0x2602
    
    _sprm_pjc80 = 0x2403
    
    _sprmpfkeep = 0x2405
    
    _sprmpfkeep_follow = 0x2406
    
    _sprmpfpage_break_before = 0x2407
    
    _sprm_pilvl = 0x260A
    
    _sprm_pilfo = 0x460B
    
    _sprmpfno_line_numb = 0x240C
    
    _sprm_pchg_tabs_papx = 0xC60D
    
    _sprm_pdxa_right80 = 0x840E
    
    _sprm_pdxa_left80 = 0x840F
    
    _sprm_pnest80 = 0x4610
    
    _sprm_pdxa_left180 = 0x8411
    
    _sprm_pdya_line = 0x6412
    
    _sprm_pdya_before = 0xA413
    
    _sprm_pdya_after = 0xA414
    
    _sprm_pchg_tabs = 0xC615
    
    _sprmpfin_table = 0x2416
    
    _sprmpfttp = 0x2417
    
    _sprm_pdxa_abs = 0x8418
    
    _sprm_pdya_abs = 0x8419
    
    _sprm_pdxa_width = 0x841A
    
    _sprm_ppc = 0x261B
    
    _sprm_pwr = 0x2423
    
    _sprm_pbrc_top80 = 0x6424
    
    _sprm_pbrc_left80 = 0x6425
    
    _sprm_pbrc_bottom80 = 0x6426
    
    _sprm_pbrc_right80 = 0x6427
    
    _sprm_pbrc_between80 = 0x6428
    
    _sprm_pbrc_bar80 = 0x6629
    
    _sprmpfno_auto_hyph = 0x242A
    
    _sprmpwheight_abs = 0x442B
    
    _sprm_pdcs = 0x442C
    
    _sprm_pshd80 = 0x442D
    
    _sprm_pdya_from_text = 0x842E
    
    _sprm_pdxa_from_text = 0x842F
    
    _sprmpflocked = 0x2430
    
    _sprmpfwidow_control = 0x2431
    
    _sprmpfkinsoku = 0x2433
    
    _sprmpfword_wrap = 0x2434
    
    _sprmpfoverflow_punct = 0x2435
    
    _sprmpftop_line_punct = 0x2436
    
    _sprmpfauto_spacede = 0x2437
    
    _sprmpfauto_spacedn = 0x2438
    
    _sprmpwalign_font = 0x4439
    
    _sprm_pframe_text_flow = 0x443A
    
    _sprm_pout_lvl = 0x2640
    
    _sprmpfbi_di = 0x2441
    
    _sprmpfnumrmins = 0x2443
    
    _sprm_pnumrm = 0xC645
    
    _sprm_phuge_papx = 0x6646
    
    _sprmpfuse_pgsu_settings = 0x2447
    
    _sprmpfadjust_right = 0x2448
    
    _sprm_pitap = 0x6649
    
    _sprm_pdtap = 0x664A
    
    _sprmpfinner_table_cell = 0x244B
    
    _sprmpfinner_ttp = 0x244C
    
    _sprm_pshd = 0xC64D
    
    _sprm_pbrc_top = 0xC64E
    
    _sprm_pbrc_left = 0xC64F
    
    _sprm_pbrc_bottom = 0xC650
    
    _sprm_pbrc_right = 0xC651
    
    _sprm_pbrc_between = 0xC652
    
    _sprm_pbrc_bar = 0xC653
    
    _sprm_pdxc_right = 0x4455
    
    _sprm_pdxc_left = 0x4456
    
    _sprm_pdxc_left1 = 0x4457
    
    _sprm_pdyl_before = 0x4458
    
    _sprm_pdyl_after = 0x4459
    
    _sprmpfopen_tch = 0x245A
    
    _sprmpfdya_before_auto = 0x245B
    
    _sprmpfdya_after_auto = 0x245C
    
    _sprm_pdxa_right = 0x845D
    
    _sprm_pdxa_left = 0x845E
    
    _sprm_pnest = 0x465F
    
    _sprm_pdxa_left1 = 0x8460
    
    _sprm_pjc = 0x2461
    
    _sprmpfno_allow_overlap = 0x2462
    
    _sprm_pwall = 0x2664
    
    _sprm_pipgp = 0x6465
    
    _sprm_pcnf = 0xC666
    
    _sprm_prsid = 0x6467
    
    _sprm_pistd_list_permute = 0xC669
    
    _sprm_ptable_props = 0x646B
    
    _sprmptistd_info = 0xC66C
    
    _sprmpfcontextual_spacing = 0x246D
    
    _sprm_pprop_rmark = 0xC66F
    
    _sprmpfmirror_indents = 0x2470
    
    _sprm_pttwo = 0x2471
    
    _sprm_tjc90 = 0x5400
    
    _sprm_tdxa_left = 0x9601
    
    _sprm_tdxa_gap_half = 0x9602
    
    _sprmtfcant_split90 = 0x3403
    
    _sprm_ttable_header = 0x3404
    
    _sprm_ttable_borders80 = 0xD605
    
    _sprm_tdya_row_height = 0x9407
    
    _sprm_tdef_table = 0xD608
    
    _sprm_tdef_table_shd80 = 0xD609
    
    _sprm_ttlp = 0x740A
    
    _sprmtfbi_di = 0x560B
    
    _sprm_tdef_table_shd3rd = 0xD60C
    
    _sprm_tpc = 0x360D
    
    _sprm_tdxa_abs = 0x940E
    
    _sprm_tdya_abs = 0x940F
    
    _sprm_tdxa_from_text = 0x9410
    
    _sprm_tdya_from_text = 0x9411
    
    _sprm_tdef_table_shd = 0xD612
    
    _sprm_ttable_borders = 0xD613
    
    _sprm_ttable_width = 0xF614
    
    _sprmtfautofit = 0x3615
    
    _sprm_tdef_table_shd2nd = 0xD616
    
    _sprm_twidth_before = 0xF617
    
    _sprm_twidth_after = 0xF618
    
    _sprmtfkeep_follow = 0x3619
    
    _sprm_tbrc_top_cv = 0xD61A
    
    _sprm_tbrc_left_cv = 0xD61B
    
    _sprm_tbrc_bottom_cv = 0xD61C
    
    _sprm_tbrc_right_cv = 0xD61D
    
    _sprm_tdxa_from_text_right = 0x941E
    
    _sprm_tdya_from_text_bottom = 0x941F
    
    _sprm_tset_brc80 = 0xD620
    
    _sprm_tinsert = 0x7621
    
    _sprm_tdelete = 0x5622
    
    _sprm_tdxa_col = 0x7623
    
    _sprm_tmerge = 0x5624
    
    _sprm_tsplit = 0x5625
    
    _sprm_ttext_flow = 0x7629
    
    _sprm_tvert_merge = 0xD62B
    
    _sprm_tvert_align = 0xD62C
    
    _sprm_tset_shd = 0xD62D
    
    _sprm_tset_shd_odd = 0xD62E
    
    _sprm_tset_brc = 0xD62F
    
    _sprm_tcell_padding = 0xD632
    
    _sprm_tcell_spacing_default = 0xD633
    
    _sprm_tcell_padding_default = 0xD634
    
    _sprm_tcell_width = 0xD635
    
    _sprm_tfit_text = 0xF636
    
    _sprmtfcell_no_wrap = 0xD639
    
    _sprm_tistd = 0x563A
    
    _sprm_tcell_padding_style = 0xD63E
    
    _sprm_tcell_fhide_mark = 0xD642
    
    _sprm_tset_shd_table = 0xD660
    
    _sprm_twidth_indent = 0xF661
    
    _sprm_tcell_brc_type = 0xD662
    
    _sprmtfbi_di90 = 0x5664
    
    _sprmtfno_allow_overlap = 0x3465
    
    _sprmtfcant_split = 0x3466
    
    _sprm_tprop_rmark = 0xD667
    
    _sprm_twall = 0x3668
    
    _sprm_tipgp = 0x7469
    
    _sprm_tcnf = 0xD66A
    
    _sprm_tdef_table_shd_raw = 0xD670
    
    _sprm_tdef_table_shd_raw2nd = 0xD671
    
    _sprm_tdef_table_shd_raw3rd = 0xD672
    
    _sprm_trsid = 0x7479
    
    _sprm_tcell_vert_align_style = 0x347C
    
    _sprm_tcell_no_wrap_style = 0x347D
    
    _sprm_tcell_brc_top_style = 0xD47F
    
    _sprm_tcell_brc_bottom_style = 0xD680
    
    _sprm_tcell_brc_left_style = 0xD681
    
    _sprm_tcell_brc_right_style = 0xD682
    
    _sprm_tcell_brc_inside_hstyle = 0xD683
    
    _sprm_tcell_brc_inside_vstyle = 0xD684
    
    _sprm_tcell_brctl2brstyle = 0xD685
    
    _sprm_tcell_brctr2blstyle = 0xD686
    
    _sprm_tcell_shd_style = 0xD687
    
    _sprmtchorz_bands = 0x3488
    
    _sprmtcvert_bands = 0x3489
    
    _sprm_tjc = 0x548A
    
    _sprm_scns_pgn = 0x3000
    
    _sprm_si_heading_pgn = 0x3001
    
    _sprm_sdxa_col_width = 0xF203
    
    _sprm_sdxa_col_spacing = 0xF204
    
    _sprmsfevenly_spaced = 0x3005
    
    _sprmsfprotected = 0x3006
    
    _sprm_sdm_bin_first = 0x5007
    
    _sprm_sdm_bin_other = 0x5008
    
    _sprm_sbkc = 0x3009
    
    _sprmsftitle_page = 0x300A
    
    _sprm_sccolumns = 0x500B
    
    _sprm_sdxa_columns = 0x900C
    
    _sprm_snfc_pgn = 0x300E
    
    _sprmsfpgn_restart = 0x3011
    
    _sprmsfendnote = 0x3012
    
    _sprm_slnc = 0x3013
    
    _sprmsnlnn_mod = 0x5015
    
    _sprm_sdxa_lnn = 0x9016
    
    _sprm_sdya_hdr_top = 0xB017
    
    _sprm_sdya_hdr_bottom = 0xB018
    
    _sprmslbetween = 0x3019
    
    _sprm_svjc = 0x301A
    
    _sprm_slnn_min = 0x501B
    
    _sprm_spgn_start97 = 0x501C
    
    _sprmsborientation = 0x301D
    
    _sprm_sxa_page = 0xB01F
    
    _sprm_sya_page = 0xB020
    
    _sprm_sdxa_left = 0xB021
    
    _sprm_sdxa_right = 0xB022
    
    _sprm_sdya_top = 0x9023
    
    _sprm_sdya_bottom = 0x9024
    
    _sprm_sdza_gutter = 0xB025
    
    _sprm_sdm_paper_req = 0x5026
    
    _sprmsfbi_di = 0x3228
    
    _sprmsfrtlgutter = 0x322A
    
    _sprm_sbrc_top80 = 0x702B
    
    _sprm_sbrc_left80 = 0x702C
    
    _sprm_sbrc_bottom80 = 0x702D
    
    _sprm_sbrc_right80 = 0x702E
    
    _sprm_spgb_prop = 0x522F
    
    _sprm_sdxt_char_space = 0x7030
    
    _sprm_sdya_line_pitch = 0x9031
    
    _sprm_sclm = 0x5032
    
    _sprm_stext_flow = 0x5033
    
    _sprm_sbrc_top = 0xD234
    
    _sprm_sbrc_left = 0xD235
    
    _sprm_sbrc_bottom = 0xD236
    
    _sprm_sbrc_right = 0xD237
    
    _sprm_swall = 0x3239
    
    _sprm_srsid = 0x703A
    
    _sprm_sfpc = 0x303B
    
    _sprm_srnc_ftn = 0x303C
    
    _sprm_srnc_edn = 0x303E
    
    _sprmsnftn = 0x503F
    
    _sprm_snfc_ftn_ref = 0x5040
    
    _sprmsnedn = 0x5041
    
    _sprm_snfc_edn_ref = 0x5042
    
    _sprm_sprop_rmark = 0xD243
    
    _sprm_spgn_start = 0x7044
    
    _sprm_pic_brc_top80 = 0x6C02
    
    _sprm_pic_brc_left80 = 0x6C03
    
    _sprm_pic_brc_bottom80 = 0x6C04
    
    _sprm_pic_brc_right80 = 0x6C05
    
    _sprm_pic_brc_top = 0xCE08
    
    _sprm_pic_brc_left = 0xCE09
    
    _sprm_pic_brc_bottom = 0xCE0A
    
    _map0_ = None
    
    _map2 = None
    
    _prm0map = None
    
    @staticmethod
    def _get_sprm_by_name(name : str) -> int:
        res = 0
        wrapres484 = RefOutArgWrapper(0)
        inoutres485 = Utils.tryGetValue(SinglePropertyModifiers._map2, name, wrapres484)
        res = wrapres484.value
        if (inoutres485): 
            return res
        raise Utils.newException("Invalid SPRM name: " + name, None)
    
    @staticmethod
    def get_sprm_name(sprm : int) -> str:
        res = None
        wrapres486 = RefOutArgWrapper(None)
        inoutres487 = Utils.tryGetValue(SinglePropertyModifiers._map0_, sprm, wrapres486)
        res = wrapres486.value
        if (not inoutres487): 
            return None
        else: 
            return res
    
    # static constructor for class SinglePropertyModifiers
    @staticmethod
    def _static_ctor():
        SinglePropertyModifiers._map0_ = dict()
        SinglePropertyModifiers._map0_[0x0800] = "sprmCFRMarkDel"
        SinglePropertyModifiers._map0_[0x0801] = "sprmCFRMarkIns"
        SinglePropertyModifiers._map0_[0x0802] = "sprmCFFldVanish"
        SinglePropertyModifiers._map0_[0x6A03] = "sprmCPicLocation"
        SinglePropertyModifiers._map0_[0x4804] = "sprmCIbstRMark"
        SinglePropertyModifiers._map0_[0x6805] = "sprmCDttmRMark"
        SinglePropertyModifiers._map0_[0x0806] = "sprmCFData"
        SinglePropertyModifiers._map0_[0x4807] = "sprmCIdslRMark"
        SinglePropertyModifiers._map0_[0x6A09] = "sprmCSymbol"
        SinglePropertyModifiers._map0_[0x080A] = "sprmCFOle2"
        SinglePropertyModifiers._map0_[0x2A0C] = "sprmCHighlight"
        SinglePropertyModifiers._map0_[0x0811] = "sprmCFWebHidden"
        SinglePropertyModifiers._map0_[0x6815] = "sprmCRsidProp"
        SinglePropertyModifiers._map0_[0x6816] = "sprmCRsidText"
        SinglePropertyModifiers._map0_[0x6817] = "sprmCRsidRMDel"
        SinglePropertyModifiers._map0_[0x0818] = "sprmCFSpecVanish"
        SinglePropertyModifiers._map0_[0xC81A] = "sprmCFMathPr"
        SinglePropertyModifiers._map0_[0x4A30] = "sprmCIstd"
        SinglePropertyModifiers._map0_[0xCA31] = "sprmCIstdPermute"
        SinglePropertyModifiers._map0_[0x2A33] = "sprmCPlain"
        SinglePropertyModifiers._map0_[0x2A34] = "sprmCKcd"
        SinglePropertyModifiers._map0_[0x0835] = "sprmCFBold"
        SinglePropertyModifiers._map0_[0x0836] = "sprmCFItalic"
        SinglePropertyModifiers._map0_[0x0837] = "sprmCFStrike"
        SinglePropertyModifiers._map0_[0x0838] = "sprmCFOutline"
        SinglePropertyModifiers._map0_[0x0839] = "sprmCFShadow"
        SinglePropertyModifiers._map0_[0x083A] = "sprmCFSmallCaps"
        SinglePropertyModifiers._map0_[0x083B] = "sprmCFCaps"
        SinglePropertyModifiers._map0_[0x083C] = "sprmCFVanish"
        SinglePropertyModifiers._map0_[0x2A3E] = "sprmCKul"
        SinglePropertyModifiers._map0_[0x8840] = "sprmCDxaSpace"
        SinglePropertyModifiers._map0_[0x2A42] = "sprmCIco"
        SinglePropertyModifiers._map0_[0x4A43] = "sprmCHps"
        SinglePropertyModifiers._map0_[0x4845] = "sprmCHpsPos"
        SinglePropertyModifiers._map0_[0xCA47] = "sprmCMajority"
        SinglePropertyModifiers._map0_[0x2A48] = "sprmCIss"
        SinglePropertyModifiers._map0_[0x484B] = "sprmCHpsKern"
        SinglePropertyModifiers._map0_[0x484E] = "sprmCHresi"
        SinglePropertyModifiers._map0_[0x4A4F] = "sprmCRgFtc0"
        SinglePropertyModifiers._map0_[0x4A50] = "sprmCRgFtc1"
        SinglePropertyModifiers._map0_[0x4A51] = "sprmCRgFtc2"
        SinglePropertyModifiers._map0_[0x4852] = "sprmCCharScale"
        SinglePropertyModifiers._map0_[0x2A53] = "sprmCFDStrike"
        SinglePropertyModifiers._map0_[0x0854] = "sprmCFImprint"
        SinglePropertyModifiers._map0_[0x0855] = "sprmCFSpec"
        SinglePropertyModifiers._map0_[0x0856] = "sprmCFObj"
        SinglePropertyModifiers._map0_[0xCA57] = "sprmCPropRMark90"
        SinglePropertyModifiers._map0_[0x0858] = "sprmCFEmboss"
        SinglePropertyModifiers._map0_[0x2859] = "sprmCSfxText"
        SinglePropertyModifiers._map0_[0x085A] = "sprmCFBiDi"
        SinglePropertyModifiers._map0_[0x085C] = "sprmCFBoldBi"
        SinglePropertyModifiers._map0_[0x085D] = "sprmCFItalicBi"
        SinglePropertyModifiers._map0_[0x4A5E] = "sprmCFtcBi"
        SinglePropertyModifiers._map0_[0x485F] = "sprmCLidBi"
        SinglePropertyModifiers._map0_[0x4A60] = "sprmCIcoBi"
        SinglePropertyModifiers._map0_[0x4A61] = "sprmCHpsBi"
        SinglePropertyModifiers._map0_[0xCA62] = "sprmCDispFldRMark"
        SinglePropertyModifiers._map0_[0x4863] = "sprmCIbstRMarkDel"
        SinglePropertyModifiers._map0_[0x6864] = "sprmCDttmRMarkDel"
        SinglePropertyModifiers._map0_[0x6865] = "sprmCBrc80"
        SinglePropertyModifiers._map0_[0x4866] = "sprmCShd80"
        SinglePropertyModifiers._map0_[0x4867] = "sprmCIdslRMarkDel"
        SinglePropertyModifiers._map0_[0x0868] = "sprmCFUsePgsuSettings"
        SinglePropertyModifiers._map0_[0x486D] = "sprmCRgLid0_80"
        SinglePropertyModifiers._map0_[0x486E] = "sprmCRgLid1_80"
        SinglePropertyModifiers._map0_[0x286F] = "sprmCIdctHint"
        SinglePropertyModifiers._map0_[0x6870] = "sprmCCv"
        SinglePropertyModifiers._map0_[0xCA71] = "sprmCShd"
        SinglePropertyModifiers._map0_[0xCA72] = "sprmCBrc"
        SinglePropertyModifiers._map0_[0x4873] = "sprmCRgLid0"
        SinglePropertyModifiers._map0_[0x4874] = "sprmCRgLid1"
        SinglePropertyModifiers._map0_[0x0875] = "sprmCFNoProof"
        SinglePropertyModifiers._map0_[0xCA76] = "sprmCFitText"
        SinglePropertyModifiers._map0_[0x6877] = "sprmCCvUl"
        SinglePropertyModifiers._map0_[0xCA78] = "sprmCFELayout"
        SinglePropertyModifiers._map0_[0x2879] = "sprmCLbcCRJ"
        SinglePropertyModifiers._map0_[0x0882] = "sprmCFComplexScripts"
        SinglePropertyModifiers._map0_[0x2A83] = "sprmCWall"
        SinglePropertyModifiers._map0_[0xCA85] = "sprmCCnf"
        SinglePropertyModifiers._map0_[0x2A86] = "sprmCNeedFontFixup"
        SinglePropertyModifiers._map0_[0x6887] = "sprmCPbiIBullet"
        SinglePropertyModifiers._map0_[0x4888] = "sprmCPbiGrf"
        SinglePropertyModifiers._map0_[0xCA89] = "sprmCPropRMark"
        SinglePropertyModifiers._map0_[0x2A90] = "sprmCFSdtVanish"
        SinglePropertyModifiers._map0_[0x4600] = "sprmPIstd"
        SinglePropertyModifiers._map0_[0xC601] = "sprmPIstdPermute"
        SinglePropertyModifiers._map0_[0x2602] = "sprmPIncLvl"
        SinglePropertyModifiers._map0_[0x2403] = "sprmPJc80"
        SinglePropertyModifiers._map0_[0x2405] = "sprmPFKeep"
        SinglePropertyModifiers._map0_[0x2406] = "sprmPFKeepFollow"
        SinglePropertyModifiers._map0_[0x2407] = "sprmPFPageBreakBefore"
        SinglePropertyModifiers._map0_[0x260A] = "sprmPIlvl"
        SinglePropertyModifiers._map0_[0x460B] = "sprmPIlfo"
        SinglePropertyModifiers._map0_[0x240C] = "sprmPFNoLineNumb"
        SinglePropertyModifiers._map0_[0xC60D] = "sprmPChgTabsPapx"
        SinglePropertyModifiers._map0_[0x840E] = "sprmPDxaRight80"
        SinglePropertyModifiers._map0_[0x840F] = "sprmPDxaLeft80"
        SinglePropertyModifiers._map0_[0x4610] = "sprmPNest80"
        SinglePropertyModifiers._map0_[0x8411] = "sprmPDxaLeft180"
        SinglePropertyModifiers._map0_[0x6412] = "sprmPDyaLine"
        SinglePropertyModifiers._map0_[0xA413] = "sprmPDyaBefore"
        SinglePropertyModifiers._map0_[0xA414] = "sprmPDyaAfter"
        SinglePropertyModifiers._map0_[0xC615] = "sprmPChgTabs"
        SinglePropertyModifiers._map0_[0x2416] = "sprmPFInTable"
        SinglePropertyModifiers._map0_[0x2417] = "sprmPFTtp"
        SinglePropertyModifiers._map0_[0x8418] = "sprmPDxaAbs"
        SinglePropertyModifiers._map0_[0x8419] = "sprmPDyaAbs"
        SinglePropertyModifiers._map0_[0x841A] = "sprmPDxaWidth"
        SinglePropertyModifiers._map0_[0x261B] = "sprmPPc"
        SinglePropertyModifiers._map0_[0x2423] = "sprmPWr"
        SinglePropertyModifiers._map0_[0x6424] = "sprmPBrcTop80"
        SinglePropertyModifiers._map0_[0x6425] = "sprmPBrcLeft80"
        SinglePropertyModifiers._map0_[0x6426] = "sprmPBrcBottom80"
        SinglePropertyModifiers._map0_[0x6427] = "sprmPBrcRight80"
        SinglePropertyModifiers._map0_[0x6428] = "sprmPBrcBetween80"
        SinglePropertyModifiers._map0_[0x6629] = "sprmPBrcBar80"
        SinglePropertyModifiers._map0_[0x242A] = "sprmPFNoAutoHyph"
        SinglePropertyModifiers._map0_[0x442B] = "sprmPWHeightAbs"
        SinglePropertyModifiers._map0_[0x442C] = "sprmPDcs"
        SinglePropertyModifiers._map0_[0x442D] = "sprmPShd80"
        SinglePropertyModifiers._map0_[0x842E] = "sprmPDyaFromText"
        SinglePropertyModifiers._map0_[0x842F] = "sprmPDxaFromText"
        SinglePropertyModifiers._map0_[0x2430] = "sprmPFLocked"
        SinglePropertyModifiers._map0_[0x2431] = "sprmPFWidowControl"
        SinglePropertyModifiers._map0_[0x2433] = "sprmPFKinsoku"
        SinglePropertyModifiers._map0_[0x2434] = "sprmPFWordWrap"
        SinglePropertyModifiers._map0_[0x2435] = "sprmPFOverflowPunct"
        SinglePropertyModifiers._map0_[0x2436] = "sprmPFTopLinePunct"
        SinglePropertyModifiers._map0_[0x2437] = "sprmPFAutoSpaceDE"
        SinglePropertyModifiers._map0_[0x2438] = "sprmPFAutoSpaceDN"
        SinglePropertyModifiers._map0_[0x4439] = "sprmPWAlignFont"
        SinglePropertyModifiers._map0_[0x443A] = "sprmPFrameTextFlow"
        SinglePropertyModifiers._map0_[0x2640] = "sprmPOutLvl"
        SinglePropertyModifiers._map0_[0x2441] = "sprmPFBiDi"
        SinglePropertyModifiers._map0_[0x2443] = "sprmPFNumRMIns"
        SinglePropertyModifiers._map0_[0xC645] = "sprmPNumRM"
        SinglePropertyModifiers._map0_[0x6646] = "sprmPHugePapx"
        SinglePropertyModifiers._map0_[0x2447] = "sprmPFUsePgsuSettings"
        SinglePropertyModifiers._map0_[0x2448] = "sprmPFAdjustRight"
        SinglePropertyModifiers._map0_[0x6649] = "sprmPItap"
        SinglePropertyModifiers._map0_[0x664A] = "sprmPDtap"
        SinglePropertyModifiers._map0_[0x244B] = "sprmPFInnerTableCell"
        SinglePropertyModifiers._map0_[0x244C] = "sprmPFInnerTtp"
        SinglePropertyModifiers._map0_[0xC64D] = "sprmPShd"
        SinglePropertyModifiers._map0_[0xC64E] = "sprmPBrcTop"
        SinglePropertyModifiers._map0_[0xC64F] = "sprmPBrcLeft"
        SinglePropertyModifiers._map0_[0xC650] = "sprmPBrcBottom"
        SinglePropertyModifiers._map0_[0xC651] = "sprmPBrcRight"
        SinglePropertyModifiers._map0_[0xC652] = "sprmPBrcBetween"
        SinglePropertyModifiers._map0_[0xC653] = "sprmPBrcBar"
        SinglePropertyModifiers._map0_[0x4455] = "sprmPDxcRight"
        SinglePropertyModifiers._map0_[0x4456] = "sprmPDxcLeft"
        SinglePropertyModifiers._map0_[0x4457] = "sprmPDxcLeft1"
        SinglePropertyModifiers._map0_[0x4458] = "sprmPDylBefore"
        SinglePropertyModifiers._map0_[0x4459] = "sprmPDylAfter"
        SinglePropertyModifiers._map0_[0x245A] = "sprmPFOpenTch"
        SinglePropertyModifiers._map0_[0x245B] = "sprmPFDyaBeforeAuto"
        SinglePropertyModifiers._map0_[0x245C] = "sprmPFDyaAfterAuto"
        SinglePropertyModifiers._map0_[0x845D] = "sprmPDxaRight"
        SinglePropertyModifiers._map0_[0x845E] = "sprmPDxaLeft"
        SinglePropertyModifiers._map0_[0x465F] = "sprmPNest"
        SinglePropertyModifiers._map0_[0x8460] = "sprmPDxaLeft1"
        SinglePropertyModifiers._map0_[0x2461] = "sprmPJc"
        SinglePropertyModifiers._map0_[0x2462] = "sprmPFNoAllowOverlap"
        SinglePropertyModifiers._map0_[0x2664] = "sprmPWall"
        SinglePropertyModifiers._map0_[0x6465] = "sprmPIpgp"
        SinglePropertyModifiers._map0_[0xC666] = "sprmPCnf"
        SinglePropertyModifiers._map0_[0x6467] = "sprmPRsid"
        SinglePropertyModifiers._map0_[0xC669] = "sprmPIstdListPermute"
        SinglePropertyModifiers._map0_[0x646B] = "sprmPTableProps"
        SinglePropertyModifiers._map0_[0xC66C] = "sprmPTIstdInfo"
        SinglePropertyModifiers._map0_[0x246D] = "sprmPFContextualSpacing"
        SinglePropertyModifiers._map0_[0xC66F] = "sprmPPropRMark"
        SinglePropertyModifiers._map0_[0x2470] = "sprmPFMirrorIndents"
        SinglePropertyModifiers._map0_[0x2471] = "sprmPTtwo"
        SinglePropertyModifiers._map0_[0x5400] = "sprmTJc90"
        SinglePropertyModifiers._map0_[0x9601] = "sprmTDxaLeft"
        SinglePropertyModifiers._map0_[0x9602] = "sprmTDxaGapHalf"
        SinglePropertyModifiers._map0_[0x3403] = "sprmTFCantSplit90"
        SinglePropertyModifiers._map0_[0x3404] = "sprmTTableHeader"
        SinglePropertyModifiers._map0_[0xD605] = "sprmTTableBorders80"
        SinglePropertyModifiers._map0_[0x9407] = "sprmTDyaRowHeight"
        SinglePropertyModifiers._map0_[0xD608] = "sprmTDefTable"
        SinglePropertyModifiers._map0_[0xD609] = "sprmTDefTableShd80"
        SinglePropertyModifiers._map0_[0x740A] = "sprmTTlp"
        SinglePropertyModifiers._map0_[0x560B] = "sprmTFBiDi"
        SinglePropertyModifiers._map0_[0xD60C] = "sprmTDefTableShd3rd"
        SinglePropertyModifiers._map0_[0x360D] = "sprmTPc"
        SinglePropertyModifiers._map0_[0x940E] = "sprmTDxaAbs"
        SinglePropertyModifiers._map0_[0x940F] = "sprmTDyaAbs"
        SinglePropertyModifiers._map0_[0x9410] = "sprmTDxaFromText"
        SinglePropertyModifiers._map0_[0x9411] = "sprmTDyaFromText"
        SinglePropertyModifiers._map0_[0xD612] = "sprmTDefTableShd"
        SinglePropertyModifiers._map0_[0xD613] = "sprmTTableBorders"
        SinglePropertyModifiers._map0_[0xF614] = "sprmTTableWidth"
        SinglePropertyModifiers._map0_[0x3615] = "sprmTFAutofit"
        SinglePropertyModifiers._map0_[0xD616] = "sprmTDefTableShd2nd"
        SinglePropertyModifiers._map0_[0xF617] = "sprmTWidthBefore"
        SinglePropertyModifiers._map0_[0xF618] = "sprmTWidthAfter"
        SinglePropertyModifiers._map0_[0x3619] = "sprmTFKeepFollow"
        SinglePropertyModifiers._map0_[0xD61A] = "sprmTBrcTopCv"
        SinglePropertyModifiers._map0_[0xD61B] = "sprmTBrcLeftCv"
        SinglePropertyModifiers._map0_[0xD61C] = "sprmTBrcBottomCv"
        SinglePropertyModifiers._map0_[0xD61D] = "sprmTBrcRightCv"
        SinglePropertyModifiers._map0_[0x941E] = "sprmTDxaFromTextRight"
        SinglePropertyModifiers._map0_[0x941F] = "sprmTDyaFromTextBottom"
        SinglePropertyModifiers._map0_[0xD620] = "sprmTSetBrc80"
        SinglePropertyModifiers._map0_[0x7621] = "sprmTInsert"
        SinglePropertyModifiers._map0_[0x5622] = "sprmTDelete"
        SinglePropertyModifiers._map0_[0x7623] = "sprmTDxaCol"
        SinglePropertyModifiers._map0_[0x5624] = "sprmTMerge"
        SinglePropertyModifiers._map0_[0x5625] = "sprmTSplit"
        SinglePropertyModifiers._map0_[0x7629] = "sprmTTextFlow"
        SinglePropertyModifiers._map0_[0xD62B] = "sprmTVertMerge"
        SinglePropertyModifiers._map0_[0xD62C] = "sprmTVertAlign"
        SinglePropertyModifiers._map0_[0xD62D] = "sprmTSetShd"
        SinglePropertyModifiers._map0_[0xD62E] = "sprmTSetShdOdd"
        SinglePropertyModifiers._map0_[0xD62F] = "sprmTSetBrc"
        SinglePropertyModifiers._map0_[0xD632] = "sprmTCellPadding"
        SinglePropertyModifiers._map0_[0xD633] = "sprmTCellSpacingDefault"
        SinglePropertyModifiers._map0_[0xD634] = "sprmTCellPaddingDefault"
        SinglePropertyModifiers._map0_[0xD635] = "sprmTCellWidth"
        SinglePropertyModifiers._map0_[0xF636] = "sprmTFitText"
        SinglePropertyModifiers._map0_[0xD639] = "sprmTFCellNoWrap"
        SinglePropertyModifiers._map0_[0x563A] = "sprmTIstd"
        SinglePropertyModifiers._map0_[0xD63E] = "sprmTCellPaddingStyle"
        SinglePropertyModifiers._map0_[0xD642] = "sprmTCellFHideMark"
        SinglePropertyModifiers._map0_[0xD660] = "sprmTSetShdTable"
        SinglePropertyModifiers._map0_[0xF661] = "sprmTWidthIndent"
        SinglePropertyModifiers._map0_[0xD662] = "sprmTCellBrcType"
        SinglePropertyModifiers._map0_[0x5664] = "sprmTFBiDi90"
        SinglePropertyModifiers._map0_[0x3465] = "sprmTFNoAllowOverlap"
        SinglePropertyModifiers._map0_[0x3466] = "sprmTFCantSplit"
        SinglePropertyModifiers._map0_[0xD667] = "sprmTPropRMark"
        SinglePropertyModifiers._map0_[0x3668] = "sprmTWall"
        SinglePropertyModifiers._map0_[0x7469] = "sprmTIpgp"
        SinglePropertyModifiers._map0_[0xD66A] = "sprmTCnf"
        SinglePropertyModifiers._map0_[0xD670] = "sprmTDefTableShdRaw"
        SinglePropertyModifiers._map0_[0xD671] = "sprmTDefTableShdRaw2nd"
        SinglePropertyModifiers._map0_[0xD672] = "sprmTDefTableShdRaw3rd"
        SinglePropertyModifiers._map0_[0x7479] = "sprmTRsid"
        SinglePropertyModifiers._map0_[0x347C] = "sprmTCellVertAlignStyle"
        SinglePropertyModifiers._map0_[0x347D] = "sprmTCellNoWrapStyle"
        SinglePropertyModifiers._map0_[0xD47F] = "sprmTCellBrcTopStyle"
        SinglePropertyModifiers._map0_[0xD680] = "sprmTCellBrcBottomStyle"
        SinglePropertyModifiers._map0_[0xD681] = "sprmTCellBrcLeftStyle"
        SinglePropertyModifiers._map0_[0xD682] = "sprmTCellBrcRightStyle"
        SinglePropertyModifiers._map0_[0xD683] = "sprmTCellBrcInsideHStyle"
        SinglePropertyModifiers._map0_[0xD684] = "sprmTCellBrcInsideVStyle"
        SinglePropertyModifiers._map0_[0xD685] = "sprmTCellBrcTL2BRStyle"
        SinglePropertyModifiers._map0_[0xD686] = "sprmTCellBrcTR2BLStyle"
        SinglePropertyModifiers._map0_[0xD687] = "sprmTCellShdStyle"
        SinglePropertyModifiers._map0_[0x3488] = "sprmTCHorzBands"
        SinglePropertyModifiers._map0_[0x3489] = "sprmTCVertBands"
        SinglePropertyModifiers._map0_[0x548A] = "sprmTJc"
        SinglePropertyModifiers._map0_[0x3000] = "sprmScnsPgn"
        SinglePropertyModifiers._map0_[0x3001] = "sprmSiHeadingPgn"
        SinglePropertyModifiers._map0_[0xF203] = "sprmSDxaColWidth"
        SinglePropertyModifiers._map0_[0xF204] = "sprmSDxaColSpacing"
        SinglePropertyModifiers._map0_[0x3005] = "sprmSFEvenlySpaced"
        SinglePropertyModifiers._map0_[0x3006] = "sprmSFProtected"
        SinglePropertyModifiers._map0_[0x5007] = "sprmSDmBinFirst"
        SinglePropertyModifiers._map0_[0x5008] = "sprmSDmBinOther"
        SinglePropertyModifiers._map0_[0x3009] = "sprmSBkc"
        SinglePropertyModifiers._map0_[0x300A] = "sprmSFTitlePage"
        SinglePropertyModifiers._map0_[0x500B] = "sprmSCcolumns"
        SinglePropertyModifiers._map0_[0x900C] = "sprmSDxaColumns"
        SinglePropertyModifiers._map0_[0x300E] = "sprmSNfcPgn"
        SinglePropertyModifiers._map0_[0x3011] = "sprmSFPgnRestart"
        SinglePropertyModifiers._map0_[0x3012] = "sprmSFEndnote"
        SinglePropertyModifiers._map0_[0x3013] = "sprmSLnc"
        SinglePropertyModifiers._map0_[0x5015] = "sprmSNLnnMod"
        SinglePropertyModifiers._map0_[0x9016] = "sprmSDxaLnn"
        SinglePropertyModifiers._map0_[0xB017] = "sprmSDyaHdrTop"
        SinglePropertyModifiers._map0_[0xB018] = "sprmSDyaHdrBottom"
        SinglePropertyModifiers._map0_[0x3019] = "sprmSLBetween"
        SinglePropertyModifiers._map0_[0x301A] = "sprmSVjc"
        SinglePropertyModifiers._map0_[0x501B] = "sprmSLnnMin"
        SinglePropertyModifiers._map0_[0x501C] = "sprmSPgnStart97"
        SinglePropertyModifiers._map0_[0x301D] = "sprmSBOrientation"
        SinglePropertyModifiers._map0_[0xB01F] = "sprmSXaPage"
        SinglePropertyModifiers._map0_[0xB020] = "sprmSYaPage"
        SinglePropertyModifiers._map0_[0xB021] = "sprmSDxaLeft"
        SinglePropertyModifiers._map0_[0xB022] = "sprmSDxaRight"
        SinglePropertyModifiers._map0_[0x9023] = "sprmSDyaTop"
        SinglePropertyModifiers._map0_[0x9024] = "sprmSDyaBottom"
        SinglePropertyModifiers._map0_[0xB025] = "sprmSDzaGutter"
        SinglePropertyModifiers._map0_[0x5026] = "sprmSDmPaperReq"
        SinglePropertyModifiers._map0_[0x3228] = "sprmSFBiDi"
        SinglePropertyModifiers._map0_[0x322A] = "sprmSFRTLGutter"
        SinglePropertyModifiers._map0_[0x702B] = "sprmSBrcTop80"
        SinglePropertyModifiers._map0_[0x702C] = "sprmSBrcLeft80"
        SinglePropertyModifiers._map0_[0x702D] = "sprmSBrcBottom80"
        SinglePropertyModifiers._map0_[0x702E] = "sprmSBrcRight80"
        SinglePropertyModifiers._map0_[0x522F] = "sprmSPgbProp"
        SinglePropertyModifiers._map0_[0x7030] = "sprmSDxtCharSpace"
        SinglePropertyModifiers._map0_[0x9031] = "sprmSDyaLinePitch"
        SinglePropertyModifiers._map0_[0x5032] = "sprmSClm"
        SinglePropertyModifiers._map0_[0x5033] = "sprmSTextFlow"
        SinglePropertyModifiers._map0_[0xD234] = "sprmSBrcTop"
        SinglePropertyModifiers._map0_[0xD235] = "sprmSBrcLeft"
        SinglePropertyModifiers._map0_[0xD236] = "sprmSBrcBottom"
        SinglePropertyModifiers._map0_[0xD237] = "sprmSBrcRight"
        SinglePropertyModifiers._map0_[0x3239] = "sprmSWall"
        SinglePropertyModifiers._map0_[0x703A] = "sprmSRsid"
        SinglePropertyModifiers._map0_[0x303B] = "sprmSFpc"
        SinglePropertyModifiers._map0_[0x303C] = "sprmSRncFtn"
        SinglePropertyModifiers._map0_[0x303E] = "sprmSRncEdn"
        SinglePropertyModifiers._map0_[0x503F] = "sprmSNFtn"
        SinglePropertyModifiers._map0_[0x5040] = "sprmSNfcFtnRef"
        SinglePropertyModifiers._map0_[0x5041] = "sprmSNEdn"
        SinglePropertyModifiers._map0_[0x5042] = "sprmSNfcEdnRef"
        SinglePropertyModifiers._map0_[0xD243] = "sprmSPropRMark"
        SinglePropertyModifiers._map0_[0x7044] = "sprmSPgnStart"
        SinglePropertyModifiers._map0_[0x6C02] = "sprmPicBrcTop80"
        SinglePropertyModifiers._map0_[0x6C03] = "sprmPicBrcLeft80"
        SinglePropertyModifiers._map0_[0x6C04] = "sprmPicBrcBottom80"
        SinglePropertyModifiers._map0_[0x6C05] = "sprmPicBrcRight80"
        SinglePropertyModifiers._map0_[0xCE08] = "sprmPicBrcTop"
        SinglePropertyModifiers._map0_[0xCE09] = "sprmPicBrcLeft"
        SinglePropertyModifiers._map0_[0xCE0A] = "sprmPicBrcBottom"
        SinglePropertyModifiers._map2 = dict()
        for kp in SinglePropertyModifiers._map0_.items(): 
            SinglePropertyModifiers._map2[kp[1]] = kp[0]
        SinglePropertyModifiers._prm0map = dict()
        SinglePropertyModifiers._prm0map[0x00] = SinglePropertyModifiers._sprm_clbccrj
        SinglePropertyModifiers._prm0map[0x04] = SinglePropertyModifiers._sprm_pinc_lvl
        SinglePropertyModifiers._prm0map[0x05] = SinglePropertyModifiers._sprm_pjc
        SinglePropertyModifiers._prm0map[0x07] = SinglePropertyModifiers._sprmpfkeep
        SinglePropertyModifiers._prm0map[0x08] = SinglePropertyModifiers._sprmpfkeep_follow
        SinglePropertyModifiers._prm0map[0x09] = SinglePropertyModifiers._sprmpfpage_break_before
        SinglePropertyModifiers._prm0map[0x0C] = SinglePropertyModifiers._sprm_pilvl
        SinglePropertyModifiers._prm0map[0x0D] = SinglePropertyModifiers._sprmpfmirror_indents
        SinglePropertyModifiers._prm0map[0x0E] = SinglePropertyModifiers._sprmpfno_line_numb
        SinglePropertyModifiers._prm0map[0x0F] = SinglePropertyModifiers._sprm_pttwo
        SinglePropertyModifiers._prm0map[0x18] = SinglePropertyModifiers._sprmpfin_table
        SinglePropertyModifiers._prm0map[0x19] = SinglePropertyModifiers._sprmpfttp
        SinglePropertyModifiers._prm0map[0x1D] = SinglePropertyModifiers._sprm_ppc
        SinglePropertyModifiers._prm0map[0x25] = SinglePropertyModifiers._sprm_pwr
        SinglePropertyModifiers._prm0map[0x2C] = SinglePropertyModifiers._sprmpfno_auto_hyph
        SinglePropertyModifiers._prm0map[0x32] = SinglePropertyModifiers._sprmpflocked
        SinglePropertyModifiers._prm0map[0x33] = SinglePropertyModifiers._sprmpfwidow_control
        SinglePropertyModifiers._prm0map[0x35] = SinglePropertyModifiers._sprmpfkinsoku
        SinglePropertyModifiers._prm0map[0x36] = SinglePropertyModifiers._sprmpfword_wrap
        SinglePropertyModifiers._prm0map[0x37] = SinglePropertyModifiers._sprmpfoverflow_punct
        SinglePropertyModifiers._prm0map[0x38] = SinglePropertyModifiers._sprmpftop_line_punct
        SinglePropertyModifiers._prm0map[0x39] = SinglePropertyModifiers._sprmpfauto_spacede
        SinglePropertyModifiers._prm0map[0x3A] = SinglePropertyModifiers._sprmpfauto_spacedn
        SinglePropertyModifiers._prm0map[0x41] = SinglePropertyModifiers._sprmcfrmark_del
        SinglePropertyModifiers._prm0map[0x42] = SinglePropertyModifiers._sprmcfrmark_ins
        SinglePropertyModifiers._prm0map[0x43] = SinglePropertyModifiers._sprmcffld_vanish
        SinglePropertyModifiers._prm0map[0x47] = SinglePropertyModifiers._sprmcfdata
        SinglePropertyModifiers._prm0map[0x4B] = SinglePropertyModifiers._sprmcfole2
        SinglePropertyModifiers._prm0map[0x4D] = SinglePropertyModifiers._sprm_chighlight
        SinglePropertyModifiers._prm0map[0x4E] = SinglePropertyModifiers._sprmcfemboss
        SinglePropertyModifiers._prm0map[0x4F] = SinglePropertyModifiers._sprm_csfx_text
        SinglePropertyModifiers._prm0map[0x50] = SinglePropertyModifiers._sprmcfweb_hidden
        SinglePropertyModifiers._prm0map[0x51] = SinglePropertyModifiers._sprmcfspec_vanish
        SinglePropertyModifiers._prm0map[0x53] = SinglePropertyModifiers._sprm_cplain
        SinglePropertyModifiers._prm0map[0x55] = SinglePropertyModifiers._sprmcfbold
        SinglePropertyModifiers._prm0map[0x56] = SinglePropertyModifiers._sprmcfitalic
        SinglePropertyModifiers._prm0map[0x57] = SinglePropertyModifiers._sprmcfstrike
        SinglePropertyModifiers._prm0map[0x58] = SinglePropertyModifiers._sprmcfoutline
        SinglePropertyModifiers._prm0map[0x59] = SinglePropertyModifiers._sprmcfshadow
        SinglePropertyModifiers._prm0map[0x5A] = SinglePropertyModifiers._sprmcfsmall_caps
        SinglePropertyModifiers._prm0map[0x5B] = SinglePropertyModifiers._sprmcfcaps
        SinglePropertyModifiers._prm0map[0x5C] = SinglePropertyModifiers._sprmcfvanish
        SinglePropertyModifiers._prm0map[0x5E] = SinglePropertyModifiers._sprm_ckul
        SinglePropertyModifiers._prm0map[0x62] = SinglePropertyModifiers._sprm_cico
        SinglePropertyModifiers._prm0map[0x68] = SinglePropertyModifiers._sprm_ciss
        SinglePropertyModifiers._prm0map[0x73] = SinglePropertyModifiers._sprmcfdstrike
        SinglePropertyModifiers._prm0map[0x74] = SinglePropertyModifiers._sprmcfimprint
        SinglePropertyModifiers._prm0map[0x75] = SinglePropertyModifiers._sprmcfspec
        SinglePropertyModifiers._prm0map[0x76] = SinglePropertyModifiers._sprmcfobj
        SinglePropertyModifiers._prm0map[0x78] = SinglePropertyModifiers._sprm_pout_lvl
        SinglePropertyModifiers._prm0map[0x7B] = SinglePropertyModifiers._sprmcfsdt_vanish
        SinglePropertyModifiers._prm0map[0x7C] = SinglePropertyModifiers._sprm_cneed_font_fixup
        SinglePropertyModifiers._prm0map[0x7E] = SinglePropertyModifiers._sprmpfnumrmins

SinglePropertyModifiers._static_ctor()