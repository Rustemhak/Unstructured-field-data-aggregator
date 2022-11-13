# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.FibRbFcLcb2003 import FibRbFcLcb2003
from pullenti.unitext.internal.word.FibRbFcLcb2007 import FibRbFcLcb2007
from pullenti.unitext.internal.word.FibRbFcLcb97 import FibRbFcLcb97
from pullenti.unitext.internal.word.FibBase import FibBase
from pullenti.unitext.internal.word.FibRgW97 import FibRgW97
from pullenti.unitext.internal.word.FibRgLw97 import FibRgLw97
from pullenti.unitext.internal.word.FibRbFcLcb2000 import FibRbFcLcb2000
from pullenti.unitext.internal.word.FibRgCswNew import FibRgCswNew
from pullenti.unitext.internal.word.ReadUtils import ReadUtils
from pullenti.unitext.internal.word.Fib import Fib
from pullenti.unitext.internal.word.FibRbFcLcb2002 import FibRbFcLcb2002
from pullenti.unitext.internal.word.FibRgCswNew2000 import FibRgCswNew2000
from pullenti.unitext.internal.word.FibRgCswNew2007 import FibRgCswNew2007

class FibStructuresReader:
    
    @staticmethod
    def _read_fib(s : Stream) -> 'Fib':
        fib = Fib()
        fib._base = FibStructuresReader.__read_fib_base(s)
        if (fib._base is None): 
            return None
        fib._csw = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._word_size)[0:0+2], byteorder="little")
        fib._fib_rgw = FibStructuresReader.__read_fib_rgw97(s, fib._csw)
        fib._cslw = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._word_size)[0:0+2], byteorder="little")
        fib._fib_rg_lw = FibStructuresReader.__read_fib_rg_lw97(s, fib._cslw)
        fib._cb_rg_fc_lcb = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._word_size)[0:0+2], byteorder="little")
        fib._fib_rg_fc_lcb_blob = FibStructuresReader.__read_fib_rg_fc_lcb_blob(s, fib._base._nfib, fib._cb_rg_fc_lcb)
        fib._csw_new = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._word_size)[0:0+2], byteorder="little")
        fib._fib_rg_csw_new = FibStructuresReader.__read_fib_rg_csw_new(s, fib._base._nfib, fib._csw_new)
        return fib
    
    @staticmethod
    def __read_fib_rg_csw_new(s : Stream, nfib : int, size : int) -> 'FibRgCswNew':
        fib_rg_csw_new2000 = None
        fib_rg_csw_new2007 = None
        swichVal = size
        if (swichVal == 0): 
            return FibRgCswNew()
        elif (swichVal == 2): 
            fib_rg_csw_new2000 = FibRgCswNew2000()
        elif (swichVal == 5): 
            fib_rg_csw_new2007 = FibRgCswNew2007()
            fib_rg_csw_new2000 = (fib_rg_csw_new2007)
        else: 
            fib_rg_csw_new2007 = FibRgCswNew2007()
            fib_rg_csw_new2000 = (fib_rg_csw_new2007)
        data = ReadUtils._read_exact(s, (size) * 2)
        fib_rg_csw_new2000._cquick_saves_new = int.from_bytes(data[0:0+2], byteorder="little")
        return fib_rg_csw_new2000
    
    @staticmethod
    def __read_fib_rg_fc_lcb_blob(s : Stream, nfib : int, size : int) -> 'FibRgFcLcb':
        fib_rb_fc_lcb97 = None
        fib_rb_fc_lcb2000 = None
        fib_rb_fc_lcb2002 = None
        fib_rb_fc_lcb2003 = None
        fib_rb_fc_lcb2007 = None
        swichVal = size
        if (swichVal == 0x005D): 
            fib_rb_fc_lcb97 = FibRbFcLcb97()
        elif (swichVal == 0x006C): 
            fib_rb_fc_lcb2000 = FibRbFcLcb2000()
            fib_rb_fc_lcb97 = (fib_rb_fc_lcb2000)
        elif (swichVal == 0x0088): 
            fib_rb_fc_lcb2002 = FibRbFcLcb2002()
            fib_rb_fc_lcb2000 = fib_rb_fc_lcb2002
            fib_rb_fc_lcb97 = (fib_rb_fc_lcb2000)
        elif (swichVal == 0x00A4): 
            fib_rb_fc_lcb2003 = FibRbFcLcb2003()
            fib_rb_fc_lcb2002 = fib_rb_fc_lcb2003
            fib_rb_fc_lcb2000 = fib_rb_fc_lcb2002
            fib_rb_fc_lcb97 = (fib_rb_fc_lcb2000)
        elif (swichVal == 0x00B7): 
            fib_rb_fc_lcb2007 = FibRbFcLcb2007()
            fib_rb_fc_lcb2003 = fib_rb_fc_lcb2007
            fib_rb_fc_lcb2002 = fib_rb_fc_lcb2003
            fib_rb_fc_lcb2000 = fib_rb_fc_lcb2002
            fib_rb_fc_lcb97 = (fib_rb_fc_lcb2000)
        else: 
            if (size >= (0x00B7)): 
                fib_rb_fc_lcb2007 = FibRbFcLcb2007()
                fib_rb_fc_lcb2003 = fib_rb_fc_lcb2007
                fib_rb_fc_lcb2002 = fib_rb_fc_lcb2003
                fib_rb_fc_lcb2000 = fib_rb_fc_lcb2002
                fib_rb_fc_lcb97 = (fib_rb_fc_lcb2000)
            else: 
                fib_rb_fc_lcb97 = FibRbFcLcb97()
        data = ReadUtils._read_exact(s, (size) * 8)
        fib_rb_fc_lcb97._fc_stshf_orig = int.from_bytes(data[0:0+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_stshf_orig = int.from_bytes(data[4:4+4], byteorder="little")
        fib_rb_fc_lcb97._fc_stshf = int.from_bytes(data[8:8+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_stshf = int.from_bytes(data[12:12+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcffnd_ref = int.from_bytes(data[16:16+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcffnd_ref = int.from_bytes(data[20:20+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcffnd_txt = int.from_bytes(data[24:24+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcffnd_txt = int.from_bytes(data[28:28+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcfand_ref = int.from_bytes(data[32:32+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcfand_ref = int.from_bytes(data[36:36+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcfand_txt = int.from_bytes(data[40:40+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcfand_txt = int.from_bytes(data[44:44+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_sed = int.from_bytes(data[48:48+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_sed = int.from_bytes(data[52:52+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plc_pad = int.from_bytes(data[56:56+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plc_pad = int.from_bytes(data[60:60+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_phe = int.from_bytes(data[64:64+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_phe = int.from_bytes(data[68:68+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_glsy = int.from_bytes(data[72:72+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_glsy = int.from_bytes(data[76:76+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_glsy = int.from_bytes(data[80:80+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_glsy = int.from_bytes(data[84:84+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_hdd = int.from_bytes(data[88:88+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_hdd = int.from_bytes(data[92:92+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_bte_chpx = int.from_bytes(data[96:96+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_bte_chpx = int.from_bytes(data[100:100+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_bte_papx = int.from_bytes(data[104:104+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_bte_papx = int.from_bytes(data[108:108+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_sea = int.from_bytes(data[112:112+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_sea = int.from_bytes(data[116:116+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_ffn = int.from_bytes(data[120:120+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_ffn = int.from_bytes(data[124:124+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_mom = int.from_bytes(data[128:128+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_mom = int.from_bytes(data[132:132+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_hdr = int.from_bytes(data[136:136+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_hdr = int.from_bytes(data[140:140+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_ftn = int.from_bytes(data[144:144+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_ftn = int.from_bytes(data[148:148+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_atn = int.from_bytes(data[152:152+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_atn = int.from_bytes(data[156:156+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_mcr = int.from_bytes(data[160:160+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_mcr = int.from_bytes(data[164:164+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_bkmk = int.from_bytes(data[168:168+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_bkmk = int.from_bytes(data[172:172+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_bkf = int.from_bytes(data[176:176+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_bkf = int.from_bytes(data[180:180+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_bkl = int.from_bytes(data[184:184+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_bkl = int.from_bytes(data[188:188+4], byteorder="little")
        fib_rb_fc_lcb97._fc_cmds = int.from_bytes(data[192:192+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_cmds = int.from_bytes(data[196:196+4], byteorder="little")
        fib_rb_fc_lcb97._fc_unused1 = int.from_bytes(data[200:200+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_unused1 = int.from_bytes(data[204:204+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_mcr = int.from_bytes(data[208:208+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_mcr = int.from_bytes(data[212:212+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pr_drvr = int.from_bytes(data[216:216+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pr_drvr = int.from_bytes(data[220:220+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pr_env_port = int.from_bytes(data[224:224+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pr_env_port = int.from_bytes(data[228:228+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pr_env_land = int.from_bytes(data[232:232+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pr_env_land = int.from_bytes(data[236:236+4], byteorder="little")
        fib_rb_fc_lcb97._fc_wss = int.from_bytes(data[240:240+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_wss = int.from_bytes(data[244:244+4], byteorder="little")
        fib_rb_fc_lcb97._fc_dop = int.from_bytes(data[248:248+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_dop = int.from_bytes(data[252:252+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_assoc = int.from_bytes(data[256:256+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_assoc = int.from_bytes(data[260:260+4], byteorder="little")
        fib_rb_fc_lcb97._fc_clx = int.from_bytes(data[264:264+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_clx = int.from_bytes(data[268:268+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_pgd_ftn = int.from_bytes(data[272:272+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_pgd_ftn = int.from_bytes(data[276:276+4], byteorder="little")
        fib_rb_fc_lcb97._fc_autosave_source = int.from_bytes(data[280:280+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_autosave_source = int.from_bytes(data[284:284+4], byteorder="little")
        fib_rb_fc_lcb97._fc_grp_xst_atn_owners = int.from_bytes(data[288:288+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_grp_xst_atn_owners = int.from_bytes(data[292:292+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_atn_bkmk = int.from_bytes(data[296:296+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_atn_bkmk = int.from_bytes(data[300:300+4], byteorder="little")
        fib_rb_fc_lcb97._fc_unused2 = int.from_bytes(data[304:304+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_unused2 = int.from_bytes(data[308:308+4], byteorder="little")
        fib_rb_fc_lcb97._fc_unused3 = int.from_bytes(data[312:312+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_unused3 = int.from_bytes(data[316:316+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plc_spa_mom = int.from_bytes(data[320:320+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plc_spa_mom = int.from_bytes(data[324:324+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plc_spa_hdr = int.from_bytes(data[328:328+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plc_spa_hdr = int.from_bytes(data[332:332+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_atn_bkf = int.from_bytes(data[336:336+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_atn_bkf = int.from_bytes(data[340:340+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_atn_bkl = int.from_bytes(data[344:344+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_atn_bkl = int.from_bytes(data[348:348+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pms = int.from_bytes(data[352:352+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pms = int.from_bytes(data[356:356+4], byteorder="little")
        fib_rb_fc_lcb97._fc_form_fld_sttbs = int.from_bytes(data[360:360+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_form_fld_sttbs = int.from_bytes(data[364:364+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcfend_ref = int.from_bytes(data[368:368+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcfend_ref = int.from_bytes(data[372:372+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcfend_txt = int.from_bytes(data[376:376+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcfend_txt = int.from_bytes(data[380:380+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_edn = int.from_bytes(data[384:384+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_edn = int.from_bytes(data[388:388+4], byteorder="little")
        fib_rb_fc_lcb97._fc_unused4 = int.from_bytes(data[392:392+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_unused4 = int.from_bytes(data[396:396+4], byteorder="little")
        fib_rb_fc_lcb97._fc_dgg_info = int.from_bytes(data[400:400+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_dgg_info = int.from_bytes(data[404:404+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_rmark = int.from_bytes(data[408:408+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_rmark = int.from_bytes(data[412:412+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_caption = int.from_bytes(data[416:416+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_caption = int.from_bytes(data[420:420+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_auto_caption = int.from_bytes(data[424:424+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_auto_caption = int.from_bytes(data[428:428+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_wkb = int.from_bytes(data[432:432+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_wkb = int.from_bytes(data[436:436+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_spl = int.from_bytes(data[440:440+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_spl = int.from_bytes(data[444:444+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcftxbx_txt = int.from_bytes(data[448:448+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcftxbx_txt = int.from_bytes(data[452:452+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_fld_txbx = int.from_bytes(data[456:456+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_fld_txbx = int.from_bytes(data[460:460+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_hdrtxbx_txt = int.from_bytes(data[464:464+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_hdrtxbx_txt = int.from_bytes(data[468:468+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcffld_hdr_txbx = int.from_bytes(data[472:472+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcffld_hdr_txbx = int.from_bytes(data[476:476+4], byteorder="little")
        fib_rb_fc_lcb97._fc_stw_user = int.from_bytes(data[480:480+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_stw_user = int.from_bytes(data[484:484+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttb_ttmbd = int.from_bytes(data[488:488+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttb_ttmbd = int.from_bytes(data[492:492+4], byteorder="little")
        fib_rb_fc_lcb97._fc_cookie_data = int.from_bytes(data[496:496+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_cookie_data = int.from_bytes(data[500:500+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pgd_mother_old_old = int.from_bytes(data[504:504+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pgd_mother_old_old = int.from_bytes(data[508:508+4], byteorder="little")
        fib_rb_fc_lcb97._fc_bkd_mother_old_old = int.from_bytes(data[512:512+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_bkd_mother_old_old = int.from_bytes(data[516:516+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pgd_ftn_old_old = int.from_bytes(data[520:520+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pgd_ftn_old_old = int.from_bytes(data[524:524+4], byteorder="little")
        fib_rb_fc_lcb97._fc_bkd_ftn_old_old = int.from_bytes(data[528:528+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_bkd_ftn_old_old = int.from_bytes(data[532:532+4], byteorder="little")
        fib_rb_fc_lcb97._fc_pgd_edn_old_old = int.from_bytes(data[536:536+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_pgd_edn_old_old = int.from_bytes(data[540:540+4], byteorder="little")
        fib_rb_fc_lcb97._fc_bkd_edn_old_old = int.from_bytes(data[544:544+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_bkd_edn_old_old = int.from_bytes(data[548:548+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_intl_fld = int.from_bytes(data[552:552+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_intl_fld = int.from_bytes(data[556:556+4], byteorder="little")
        fib_rb_fc_lcb97._fc_route_slip = int.from_bytes(data[560:560+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_route_slip = int.from_bytes(data[564:564+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttb_saved_by = int.from_bytes(data[568:568+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttb_saved_by = int.from_bytes(data[572:572+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttb_fnm = int.from_bytes(data[576:576+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttb_fnm = int.from_bytes(data[580:580+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plf_lst = int.from_bytes(data[584:584+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plf_lst = int.from_bytes(data[588:588+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plf_lfo = int.from_bytes(data[592:592+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plf_lfo = int.from_bytes(data[596:596+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_txbx_bkd = int.from_bytes(data[600:600+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_txbx_bkd = int.from_bytes(data[604:604+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_txbx_hdr_bkd = int.from_bytes(data[608:608+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_txbx_hdr_bkd = int.from_bytes(data[612:612+4], byteorder="little")
        fib_rb_fc_lcb97._fc_doc_undo_word9 = int.from_bytes(data[616:616+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_doc_undo_word9 = int.from_bytes(data[620:620+4], byteorder="little")
        fib_rb_fc_lcb97._fc_rgb_use = int.from_bytes(data[624:624+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_rgb_use = int.from_bytes(data[628:628+4], byteorder="little")
        fib_rb_fc_lcb97._fc_usp = int.from_bytes(data[632:632+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_usp = int.from_bytes(data[636:636+4], byteorder="little")
        fib_rb_fc_lcb97._fc_uskf = int.from_bytes(data[640:640+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_uskf = int.from_bytes(data[644:644+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcupc_rgb_use = int.from_bytes(data[648:648+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcupc_rgb_use = int.from_bytes(data[652:652+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcupc_usp = int.from_bytes(data[656:656+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcupc_usp = int.from_bytes(data[660:660+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttb_glsy_style = int.from_bytes(data[664:664+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttb_glsy_style = int.from_bytes(data[668:668+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plgosl = int.from_bytes(data[672:672+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plgosl = int.from_bytes(data[676:676+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcocx = int.from_bytes(data[680:680+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcocx = int.from_bytes(data[684:684+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_bte_lvc = int.from_bytes(data[688:688+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_bte_lvc = int.from_bytes(data[692:692+4], byteorder="little")
        fib_rb_fc_lcb97._dw_low_date_time = int.from_bytes(data[696:696+4], byteorder="little")
        fib_rb_fc_lcb97._dw_high_date_time = int.from_bytes(data[700:700+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_lvc_pre10 = int.from_bytes(data[704:704+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_lvc_pre10 = int.from_bytes(data[708:708+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_asumy = int.from_bytes(data[712:712+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_asumy = int.from_bytes(data[716:716+4], byteorder="little")
        fib_rb_fc_lcb97._fc_plcf_gram = int.from_bytes(data[720:720+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_plcf_gram = int.from_bytes(data[724:724+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttb_list_names = int.from_bytes(data[728:728+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttb_list_names = int.from_bytes(data[732:732+4], byteorder="little")
        fib_rb_fc_lcb97._fc_sttbf_ussr = int.from_bytes(data[736:736+4], byteorder="little")
        fib_rb_fc_lcb97._lcb_sttbf_ussr = int.from_bytes(data[740:740+4], byteorder="little")
        if (fib_rb_fc_lcb2000 is not None): 
            fib_rb_fc_lcb2000._fc_plcf_tch = int.from_bytes(data[744:744+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_plcf_tch = int.from_bytes(data[748:748+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_rmd_threading = int.from_bytes(data[752:752+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_rmd_threading = int.from_bytes(data[756:756+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_mid = int.from_bytes(data[760:760+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_mid = int.from_bytes(data[764:764+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_sttb_rgtplc = int.from_bytes(data[768:768+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_sttb_rgtplc = int.from_bytes(data[772:772+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_mso_envelope = int.from_bytes(data[776:776+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_mso_envelope = int.from_bytes(data[780:780+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_plcf_lad = int.from_bytes(data[784:784+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_plcf_lad = int.from_bytes(data[788:788+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_rg_dofr = int.from_bytes(data[792:792+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_rg_dofr = int.from_bytes(data[796:796+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_plcosl = int.from_bytes(data[800:800+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_plcosl = int.from_bytes(data[804:804+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_plcf_cookie_old = int.from_bytes(data[808:808+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_plcf_cookie_old = int.from_bytes(data[812:812+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_pgd_mother_old = int.from_bytes(data[816:816+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_pgd_mother_old = int.from_bytes(data[820:820+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_bkd_mother_old = int.from_bytes(data[824:824+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_bkd_mother_old = int.from_bytes(data[828:828+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_pgd_ftn_old = int.from_bytes(data[832:832+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_pgd_ftn_old = int.from_bytes(data[836:836+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_bkd_ftn_old = int.from_bytes(data[840:840+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_bkd_ftn_old = int.from_bytes(data[844:844+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_pgd_edn_old = int.from_bytes(data[848:848+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_pgd_edn_old = int.from_bytes(data[852:852+4], byteorder="little")
            fib_rb_fc_lcb2000._fc_bkd_edn_old = int.from_bytes(data[856:856+4], byteorder="little")
            fib_rb_fc_lcb2000._lcb_bkd_edn_old = int.from_bytes(data[860:860+4], byteorder="little")
        if (fib_rb_fc_lcb2002 is not None): 
            fib_rb_fc_lcb2002._fc_unused10 = int.from_bytes(data[864:864+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_unused10 = int.from_bytes(data[868:868+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcf_pgp = int.from_bytes(data[872:872+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcf_pgp = int.from_bytes(data[876:876+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfuim = int.from_bytes(data[880:880+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfuim = int.from_bytes(data[884:884+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plfguid_uim = int.from_bytes(data[888:888+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plfguid_uim = int.from_bytes(data[892:892+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_atrd_extra = int.from_bytes(data[896:896+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_atrd_extra = int.from_bytes(data[900:900+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plrsid = int.from_bytes(data[904:904+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plrsid = int.from_bytes(data[908:908+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_sttbf_bkmk_factoid = int.from_bytes(data[912:912+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_sttbf_bkmk_factoid = int.from_bytes(data[916:916+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcf_bkf_factoid = int.from_bytes(data[920:920+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcf_bkf_factoid = int.from_bytes(data[924:924+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfcookie = int.from_bytes(data[928:928+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfcookie = int.from_bytes(data[932:932+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcf_bkl_factoid = int.from_bytes(data[936:936+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcf_bkl_factoid = int.from_bytes(data[940:940+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_factoid_data = int.from_bytes(data[944:944+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_factoid_data = int.from_bytes(data[948:948+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_doc_undo = int.from_bytes(data[952:952+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_doc_undo = int.from_bytes(data[956:956+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_sttbf_bkmk_fcc = int.from_bytes(data[960:960+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_sttbf_bkmk_fcc = int.from_bytes(data[964:964+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcf_bkf_fcc = int.from_bytes(data[968:968+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcf_bkf_fcc = int.from_bytes(data[972:972+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcf_bkl_fcc = int.from_bytes(data[976:976+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcf_bkl_fcc = int.from_bytes(data[980:980+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_sttbfbkmkbprepairs = int.from_bytes(data[984:984+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_sttbfbkmkbprepairs = int.from_bytes(data[988:988+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfbkfbprepairs = int.from_bytes(data[992:992+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfbkfbprepairs = int.from_bytes(data[996:996+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfbklbprepairs = int.from_bytes(data[1000:1000+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfbklbprepairs = int.from_bytes(data[1004:1004+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_pms_new = int.from_bytes(data[1008:1008+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_pms_new = int.from_bytes(data[1012:1012+4], byteorder="little")
            fib_rb_fc_lcb2002._fcodso = int.from_bytes(data[1016:1016+4], byteorder="little")
            fib_rb_fc_lcb2002._lcbodso = int.from_bytes(data[1020:1020+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfpmi_oldxp = int.from_bytes(data[1024:1024+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfpmi_oldxp = int.from_bytes(data[1028:1028+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfpmi_newxp = int.from_bytes(data[1032:1032+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfpmi_newxp = int.from_bytes(data[1036:1036+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcfpmi_mixedxp = int.from_bytes(data[1040:1040+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcfpmi_mixedxp = int.from_bytes(data[1044:1044+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_unused20 = int.from_bytes(data[1048:1048+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_unused20 = int.from_bytes(data[1052:1052+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcffactoid = int.from_bytes(data[1056:1056+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcffactoid = int.from_bytes(data[1060:1060+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcflvc_oldxp = int.from_bytes(data[1064:1064+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcflvc_oldxp = int.from_bytes(data[1068:1068+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcflvc_newxp = int.from_bytes(data[1072:1072+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcflvc_newxp = int.from_bytes(data[1076:1076+4], byteorder="little")
            fib_rb_fc_lcb2002._fc_plcflvc_mixedxp = int.from_bytes(data[1080:1080+4], byteorder="little")
            fib_rb_fc_lcb2002._lcb_plcflvc_mixedxp = int.from_bytes(data[1084:1084+4], byteorder="little")
        if (fib_rb_fc_lcb2003 is not None): 
            fib_rb_fc_lcb2003._fc_hplxsdr = int.from_bytes(data[1088:1088+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_hplxsdr = int.from_bytes(data[1092:1092+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_sttbf_bkmk_sdt = int.from_bytes(data[1096:1096+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_sttbf_bkmk_sdt = int.from_bytes(data[1100:1100+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcf_bkf_sdt = int.from_bytes(data[1104:1104+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcf_bkf_sdt = int.from_bytes(data[1108:1108+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcf_bkl_sdt = int.from_bytes(data[1112:1112+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcf_bkl_sdt = int.from_bytes(data[1116:1116+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_custom_xform = int.from_bytes(data[1120:1120+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_custom_xform = int.from_bytes(data[1124:1124+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_sttbf_bkmk_prot = int.from_bytes(data[1128:1128+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_sttbf_bkmk_prot = int.from_bytes(data[1132:1132+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcf_bkf_prot = int.from_bytes(data[1136:1136+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcf_bkf_prot = int.from_bytes(data[1140:1140+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcf_bkl_prot = int.from_bytes(data[1144:1144+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcf_bkl_prot = int.from_bytes(data[1148:1148+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_sttb_prot_user = int.from_bytes(data[1152:1152+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_sttb_prot_user = int.from_bytes(data[1156:1156+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_unused = int.from_bytes(data[1160:1160+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_unused = int.from_bytes(data[1164:1164+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcfpmi_old = int.from_bytes(data[1168:1168+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcfpmi_old = int.from_bytes(data[1172:1172+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcfpmi_old_inline = int.from_bytes(data[1176:1176+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcfpmi_old_inline = int.from_bytes(data[1180:1180+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcfpmi_new = int.from_bytes(data[1184:1184+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcfpmi_new = int.from_bytes(data[1188:1188+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcfpmi_new_inline = int.from_bytes(data[1192:1192+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcfpmi_new_inline = int.from_bytes(data[1196:1196+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcflvc_old = int.from_bytes(data[1200:1200+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcflvc_old = int.from_bytes(data[1204:1204+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcflvc_old_inline = int.from_bytes(data[1208:1208+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcflvc_old_inline = int.from_bytes(data[1212:1212+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcflvc_new = int.from_bytes(data[1216:1216+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcflvc_new = int.from_bytes(data[1220:1220+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_plcflvc_new_inline = int.from_bytes(data[1224:1224+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_plcflvc_new_inline = int.from_bytes(data[1228:1228+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_pgd_mother = int.from_bytes(data[1232:1232+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_pgd_mother = int.from_bytes(data[1236:1236+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_bkd_mother = int.from_bytes(data[1240:1240+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_bkd_mother = int.from_bytes(data[1244:1244+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_afd_mother = int.from_bytes(data[1248:1248+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_afd_mother = int.from_bytes(data[1252:1252+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_pgd_ftn = int.from_bytes(data[1256:1256+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_pgd_ftn = int.from_bytes(data[1260:1260+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_bkd_ftn = int.from_bytes(data[1264:1264+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_bkd_ftn = int.from_bytes(data[1268:1268+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_afd_ftn = int.from_bytes(data[1272:1272+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_afd_ftn = int.from_bytes(data[1276:1276+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_pgd_edn = int.from_bytes(data[1280:1280+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_pgd_edn = int.from_bytes(data[1284:1284+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_bkd_edn = int.from_bytes(data[1288:1288+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_bkd_edn = int.from_bytes(data[1292:1292+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_afd_edn = int.from_bytes(data[1296:1296+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_afd_edn = int.from_bytes(data[1300:1300+4], byteorder="little")
            fib_rb_fc_lcb2003._fc_afd = int.from_bytes(data[1304:1304+4], byteorder="little")
            fib_rb_fc_lcb2003._lcb_afd = int.from_bytes(data[1308:1308+4], byteorder="little")
        if (fib_rb_fc_lcb2007 is not None): 
            fib_rb_fc_lcb2007._fc_plcfmthd = int.from_bytes(data[1312:1312+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcfmthd = int.from_bytes(data[1316:1316+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_sttbf_bkmk_move_from = int.from_bytes(data[1320:1320+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_sttbf_bkmk_move_from = int.from_bytes(data[1324:1324+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_plcf_bkf_move_from = int.from_bytes(data[1328:1328+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcf_bkf_move_from = int.from_bytes(data[1332:1332+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_plcf_bkl_move_from = int.from_bytes(data[1336:1336+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcf_bkl_move_from = int.from_bytes(data[1340:1340+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_sttbf_bkmk_move_to = int.from_bytes(data[1344:1344+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_sttbf_bkmk_move_to = int.from_bytes(data[1348:1348+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_plcf_bkf_move_to = int.from_bytes(data[1352:1352+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcf_bkf_move_to = int.from_bytes(data[1356:1356+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_plcf_bkl_move_to = int.from_bytes(data[1360:1360+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcf_bkl_move_to = int.from_bytes(data[1364:1364+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_unused11 = int.from_bytes(data[1368:1368+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_unused11 = int.from_bytes(data[1372:1372+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_unused22 = int.from_bytes(data[1376:1376+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_unused22 = int.from_bytes(data[1380:1380+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_unused33 = int.from_bytes(data[1384:1384+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_unused33 = int.from_bytes(data[1388:1388+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_sttbf_bkmk_arto = int.from_bytes(data[1392:1392+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_sttbf_bkmk_arto = int.from_bytes(data[1396:1396+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_plcf_bkf_arto = int.from_bytes(data[1400:1400+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcf_bkf_arto = int.from_bytes(data[1404:1404+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_plcf_bkl_arto = int.from_bytes(data[1408:1408+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_plcf_bkl_arto = int.from_bytes(data[1412:1412+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_arto_data = int.from_bytes(data[1416:1416+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_arto_data = int.from_bytes(data[1420:1420+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_unused44 = int.from_bytes(data[1424:1424+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_unused44 = int.from_bytes(data[1428:1428+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_unused5 = int.from_bytes(data[1432:1432+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_unused5 = int.from_bytes(data[1436:1436+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_unused6 = int.from_bytes(data[1440:1440+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_unused6 = int.from_bytes(data[1444:1444+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_oss_theme = int.from_bytes(data[1448:1448+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_oss_theme = int.from_bytes(data[1452:1452+4], byteorder="little")
            fib_rb_fc_lcb2007._fc_color_scheme_mapping = int.from_bytes(data[1456:1456+4], byteorder="little")
            fib_rb_fc_lcb2007._lcb_color_scheme_mapping = int.from_bytes(data[1460:1460+4], byteorder="little")
        return fib_rb_fc_lcb97
    
    @staticmethod
    def __read_fib_rg_lw97(s : Stream, size : int) -> 'FibRgLw97':
        fib_rg_lw97size = 88
        if (((size) * 4) != fib_rg_lw97size): 
            raise Utils.newException("Invalid FibRgLw97 size", None)
        data = ReadUtils._read_exact(s, fib_rg_lw97size)
        fib_rg_lw97 = FibRgLw97()
        fib_rg_lw97._cb_mac = int.from_bytes(data[0:0+4], byteorder="little")
        fib_rg_lw97._ccp_text = int.from_bytes(data[12:12+4], byteorder="little")
        fib_rg_lw97._ccp_ftn = int.from_bytes(data[16:16+4], byteorder="little")
        fib_rg_lw97._ccp_hdd = int.from_bytes(data[20:20+4], byteorder="little")
        fib_rg_lw97._ccp_atn = int.from_bytes(data[28:28+4], byteorder="little")
        fib_rg_lw97._ccp_edn = int.from_bytes(data[32:32+4], byteorder="little")
        fib_rg_lw97._ccp_txbx = int.from_bytes(data[36:36+4], byteorder="little")
        fib_rg_lw97._ccp_hdr_txbx = int.from_bytes(data[40:40+4], byteorder="little")
        return fib_rg_lw97
    
    @staticmethod
    def __read_fib_rgw97(s : Stream, size : int) -> 'FibRgW97':
        fib_rgw97size = 28
        if (((size) * 2) < fib_rgw97size): 
            raise Utils.newException("Invalid FibRgW97 size", None)
        data = ReadUtils._read_exact(s, fib_rgw97size)
        fib_rgw97 = FibRgW97()
        fib_rgw97._lidfe = int.from_bytes(data[26:26+2], byteorder="little")
        return fib_rgw97
    
    @staticmethod
    def __read_fib_base(s : Stream) -> 'FibBase':
        word_file_signature = 0xA5EC
        word_file_signature6 = 0xA5DC
        data = ReadUtils._read_exact(s, 32)
        fib_base = FibBase()
        fib_base._wident = int.from_bytes(data[0:0+2], byteorder="little")
        fib_base._nfib = int.from_bytes(data[2:2+2], byteorder="little")
        if ((fib_base._wident) == word_file_signature6): 
            return None
        if ((fib_base._wident) != word_file_signature): 
            raise Utils.newException("Invalid word file signature", None)
        fib_base._lid = int.from_bytes(data[6:6+2], byteorder="little")
        fib_base._pn_next = int.from_bytes(data[8:8+2], byteorder="little")
        flags = 0
        flags = int.from_bytes(data[10:10+2], byteorder="little")
        fib_base._fdot = (((flags) & 0x0001)) != 0
        fib_base._fglsy = (((flags) & 0x0002)) != 0
        fib_base._fcomplex = (((flags) & 0x0004)) != 0
        fib_base._fhas_pic = (((flags) & 0x0008)) != 0
        fib_base._cquick_saves = ((((flags) >> 4)) & 0x0F)
        fib_base._fencrypted = (((flags) & 0x0100)) != 0
        fib_base._fwhich_tbl_stm = (((flags) & 0x0200)) != 0
        fib_base._fread_only_recommended = (((flags) & 0x0400)) != 0
        fib_base._fwrite_reservation = (((flags) & 0x0800)) != 0
        fib_base._fext_char = (((flags) & 0x1000)) != 0
        fib_base._fload_override = (((flags) & 0x2000)) != 0
        fib_base._ffar_east = (((flags) & 0x4000)) != 0
        fib_base._fobfuscated = (((flags) & 0x8000)) != 0
        fib_base._lkey = int.from_bytes(data[14:14+4], byteorder="little")
        fib_base._envr = data[18]
        flags = (data[19])
        fib_base._fmac = (((flags) & 0x0001)) != 0
        fib_base._fempty_special = (((flags) & 0x0002)) != 0
        fib_base._fload_override_page = (((flags) & 0x0004)) != 0
        return fib_base