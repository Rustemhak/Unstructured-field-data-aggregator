# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.Stshi import Stshi
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.internal.word.Stshif import Stshif
from pullenti.unitext.internal.word.LSD import LSD
from pullenti.unitext.internal.word.StshiLsd import StshiLsd
from pullenti.unitext.internal.word.StdfPost2000OrNone import StdfPost2000OrNone
from pullenti.unitext.internal.word.GRFSTD import GRFSTD
from pullenti.unitext.internal.word.GrLPUpxSw import GrLPUpxSw
from pullenti.unitext.internal.word.Xst import Xst
from pullenti.unitext.internal.word.Xstz import Xstz
from pullenti.unitext.internal.word.StkParaGRLPUPX import StkParaGRLPUPX
from pullenti.unitext.internal.word.StkTableGRLPUPX import StkTableGRLPUPX
from pullenti.unitext.internal.word.StkCharUpxGrLPUpxRM import StkCharUpxGrLPUpxRM
from pullenti.unitext.internal.word.UpxTapx import UpxTapx
from pullenti.unitext.internal.word.DTTM import DTTM
from pullenti.unitext.internal.word.StkListGRLPUPX import StkListGRLPUPX
from pullenti.unitext.internal.word.UpxRm import UpxRm
from pullenti.unitext.internal.word.StkParaUpxGrLPUpxRM import StkParaUpxGrLPUpxRM
from pullenti.unitext.internal.word.UpxPapx import UpxPapx
from pullenti.unitext.internal.word.StkCharGRLPUPX import StkCharGRLPUPX
from pullenti.unitext.internal.word.UpxChpx import UpxChpx
from pullenti.unitext.internal.word.StdfBase import StdfBase
from pullenti.unitext.internal.word.FcCompressed import FcCompressed
from pullenti.unitext.internal.word.Pcd import Pcd
from pullenti.unitext.internal.word.Prm import Prm
from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers
from pullenti.unitext.internal.word.Prl import Prl
from pullenti.unitext.internal.word.Prc import Prc
from pullenti.unitext.internal.word.ReadUtils import ReadUtils
from pullenti.unitext.internal.word.Pcdt import Pcdt
from pullenti.unitext.internal.word.PlcPcd import PlcPcd
from pullenti.unitext.internal.word.Clx import Clx
from pullenti.unitext.internal.word.Sprm import Sprm
from pullenti.unitext.internal.word.Chpx import Chpx
from pullenti.unitext.internal.word.ChpxFkp import ChpxFkp
from pullenti.unitext.internal.word.STSH import STSH
from pullenti.unitext.internal.word.Stdf import Stdf
from pullenti.unitext.internal.word.STD import STD
from pullenti.unitext.internal.word.PapxFkp import PapxFkp
from pullenti.unitext.internal.word.PlcBtePapx import PlcBtePapx
from pullenti.unitext.internal.word.PapxInFkps import PapxInFkps
from pullenti.unitext.internal.word.PlcBteChpx import PlcBteChpx
from pullenti.unitext.internal.word.GrpPrlAndIstd import GrpPrlAndIstd

class BasicTypesReader:
    
    @staticmethod
    def _read_clx(s : Stream, length : int) -> 'Clx':
        position = 0
        prcs = list()
        if (length < 1): 
            return None
        clxt = ReadUtils._read_byte(s)
        position += 1
        while clxt == Prc._default_clxt:
            read = 0
            wrapread387 = RefOutArgWrapper(0)
            prcs.append(BasicTypesReader.__read_prc_without_cltx(s, length - position, wrapread387))
            read = wrapread387.value
            position += read
            if (position >= length): 
                return None
            clxt = ReadUtils._read_byte(s)
            position += 1
        if (clxt != Pcdt._default_clxt): 
            return None
        pcdt = BasicTypesReader.__read_pcdt_without_clxt(s, length - position)
        clx = Clx()
        clx._rg_prc = list(prcs)
        clx._pcdt = pcdt
        return clx
    
    @staticmethod
    def _read_cps(s : Stream, length : int) -> typing.List[int]:
        res = list()
        while (s.position + (4)) <= s.length and length > 0:
            ui = ReadUtils._read_int(s)
            if (ui < 0): 
                break
            res.append(ui)
            length -= 4
        return res
    
    @staticmethod
    def __read_pcdt_without_clxt(s : Stream, length : int) -> 'Pcdt':
        if (length < ReadUtils._dword_size): 
            raise Utils.newException("Invalid Prc: length", None)
        read = 0
        pcdt = Pcdt()
        pcdt._clxt = Pcdt._default_clxt
        wrapread388 = RefOutArgWrapper(read)
        pcdt._lcb = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._dword_size, wrapread388)[0:0+4], byteorder="little")
        read = wrapread388.value
        if (((read) + (pcdt._lcb)) > length): 
            raise Utils.newException("Invalid Prc: length", None)
        pcdt._plc_pcd = BasicTypesReader.__read_plc_pcd(s, pcdt._lcb)
        return pcdt
    
    @staticmethod
    def __read_plc_pcd(s : Stream, length : int) -> 'PlcPcd':
        if (length < (4)): 
            raise Utils.newException("Invalid Prc: length (0)", None)
        n = PlcPcd._calc_length(length)
        read = 0
        plc_pcd = PlcPcd()
        plc_pcd._cps = Utils.newArray(n + 1, 0)
        i = 0
        while i <= n: 
            wrapread389 = RefOutArgWrapper(read)
            plc_pcd._cps[i] = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._dword_size, wrapread389)[0:0+4], byteorder="little")
            read = wrapread389.value
            i += 1
        plc_pcd._pcds = Utils.newArray(n, None)
        i = 0
        while i < n: 
            plc_pcd._pcds[i] = BasicTypesReader.__read_pcd(s)
            read += Pcd._size
            i += 1
        if (read != (length)): 
            raise Utils.newException("Invalid PlcPcd: length", None)
        return plc_pcd
    
    @staticmethod
    def __read_pcd(s : Stream) -> 'Pcd':
        data = ReadUtils._read_exact(s, Pcd._size)
        pcd = Pcd()
        pcd._fno_para_last = (((data[0]) & 0x01)) != 0
        pcd._fr1 = (((data[0]) & 0x02)) != 0
        pcd._fdirty = (((data[0]) & 0x04)) != 0
        ucompressed = int.from_bytes(data[2:2+4], byteorder="little")
        comressed = FcCompressed()
        comressed._fc = (((ucompressed) & 0x3FFFFFFF))
        comressed._fcompressed = (((ucompressed) & 0x40000000)) != 0
        pcd._fc = comressed
        uprm = int.from_bytes(data[6:6+2], byteorder="little")
        prm = Prm()
        prm._prm = uprm
        pcd._prm = prm
        return pcd
    
    @staticmethod
    def __read_prc_without_cltx(s : Stream, length : int, read : int) -> 'Prc':
        if (length < ReadUtils._word_size): 
            raise Utils.newException("Invalid Prc: length", None)
        read.value = 0
        prc = Prc()
        prc._clxt = Prc._default_clxt
        prc._cb_grpprl = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        cb_grpprl = prc._cb_grpprl
        if ((length < cb_grpprl) or (cb_grpprl < 0)): 
            raise Utils.newException("Invalid Prc: array length", None)
        prc._grp_prl = BasicTypesReader._read_prls(s, cb_grpprl, read)
        return prc
    
    @staticmethod
    def _read_prls(s : Stream, length : int, read : int) -> typing.List['Prl']:
        prls = list()
        position = 0
        while position < length:
            read_portion = 0
            if ((length - position) == 1): 
                read_portion = 1
            else: 
                try: 
                    wrapread_portion390 = RefOutArgWrapper(0)
                    prl = BasicTypesReader.__read_prl(s, length - position, wrapread_portion390)
                    read_portion = wrapread_portion390.value
                    if (prl is None): 
                        break
                    prls.append(prl)
                except Exception as ex391: 
                    break
            position += read_portion
        read.value += position
        return list(prls)
    
    @staticmethod
    def __read_prl(s : Stream, length : int, read : int) -> 'Prl':
        if (length < 2): 
            raise Utils.newException("Invalid Prl: length", None)
        read.value = 0
        prl = Prl(BasicTypesReader.__read_sprm(s, read), None)
        operand_length = BasicTypesReader.__get_length_from_sprm(prl._sprm)
        if (operand_length < 0): 
            if (prl._sprm._sprm == SinglePropertyModifiers._sprm_pchg_tabs): 
                if ((read.value + ReadUtils._byte_size) > length): 
                    raise Utils.newException("Invalid Prl: operand length (1)", None)
                operand_length = (ReadUtils._read_byte_ref(s, read))
                if (operand_length == 255): 
                    if ((read.value + ReadUtils._byte_size) > length): 
                        raise Utils.newException("Invalid Prl: operand length (2)", None)
                    operand_length = (ReadUtils._read_byte_ref(s, read))
                    with MemoryStream() as ms: 
                        ctabs = ReadUtils._read_byte(s)
                        ms.writebyte(ctabs)
                        del_portion_size = 1 + ((ctabs) * 4)
                        if ((read.value + del_portion_size) > length): 
                            raise Utils.newException("Invalid Prl: operand length (3)", None)
                        data = ReadUtils._read_exact(s, (ctabs) * 4)
                        ms.write(data, 0, len(data))
                        if ((read.value + 1 + del_portion_size) > length): 
                            raise Utils.newException("Invalid Prl: operand length (4)", None)
                        ctabs = ReadUtils._read_byte(s)
                        ms.writebyte(ctabs)
                        add_portion_size = 1 + ((ctabs) * 3)
                        if ((read.value + del_portion_size + add_portion_size) > length): 
                            raise Utils.newException("Invalid Prl: operand length (5)", None)
                        data = ReadUtils._read_exact(s, (ctabs) * 3)
                        ms.write(data, 0, len(data))
                        data = ms.toarray()
                        operand_length = len(data)
                        prl._operand = data
                    read.value += operand_length
                    return prl
            elif (prl._sprm._sprm == SinglePropertyModifiers._sprm_tdef_table): 
                if ((read.value + ReadUtils._word_size) > length): 
                    return None
                operand_length = ((int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")) + 1)
            else: 
                if ((read.value + ReadUtils._byte_size) > length): 
                    return None
                operand_length = (ReadUtils._read_byte_ref(s, read))
        if ((read.value + operand_length) > length): 
            return None
        prl._operand = ReadUtils._read_exact_ref(s, operand_length, read)
        return prl
    
    @staticmethod
    def __read_sprm(s : Stream, read : int) -> 'Sprm':
        data = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (data == SinglePropertyModifiers._sprm_tvert_merge or data == SinglePropertyModifiers._sprm_tmerge): 
            pass
        return Sprm(data)
    
    @staticmethod
    def __get_length_from_sprm(sprm : 'Sprm') -> int:
        swichVal = sprm._spra
        if (swichVal == 0 or swichVal == 1): 
            return 1
        elif (swichVal == 2 or swichVal == 4 or swichVal == 5): 
            return 2
        elif (swichVal == 3): 
            return 4
        elif (swichVal == 6): 
            return -1
        elif (swichVal == 7): 
            return 3
        else: 
            raise Utils.newException("Invalid Sprm.spra value", None)
    
    @staticmethod
    def _read_plcf_bte_papx(s : Stream, length : int) -> 'PlcBtePapx':
        n = PlcBtePapx._get_length(length)
        plcf_bte_papx = PlcBtePapx()
        plcf_bte_papx._afc = Utils.newArray(n + 1, 0)
        i = 0
        while i <= n: 
            plcf_bte_papx._afc[i] = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._dword_size)[0:0+4], byteorder="little")
            i += 1
        plcf_bte_papx._apn_bte_papx = Utils.newArray(n, 0)
        i = 0
        while i < n: 
            pn = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._dword_size)[0:0+4], byteorder="little")
            plcf_bte_papx._apn_bte_papx[i] = pn
            i += 1
        return plcf_bte_papx
    
    @staticmethod
    def _read_papx_fkp(s : Stream, err : bool) -> 'PapxFkp':
        err.value = False
        data = ReadUtils._read_exact(s, PapxFkp._size)
        with MemoryStream(data) as data_stream: 
            papx_fkp = PapxFkp()
            papx_fkp._cpara = data[PapxFkp._size - 1]
            cpara = papx_fkp._cpara
            if ((cpara < 1) or cpara > 0x1D): 
                raise Utils.newException("Invalid PapxFkp: cpara", None)
            papx_fkp._rgfc = Utils.newArray(cpara + 1, 0)
            i = 0
            while i <= cpara: 
                papx_fkp._rgfc[i] = int.from_bytes(data[i * 4:i * 4+4], byteorder="little")
                i += 1
            papx_fkp._rgbx = Utils.newArray(cpara, None)
            rgbx_offset = ((cpara + 1)) * 4
            i = 0
            while i < cpara: 
                boffset = data[rgbx_offset + (i * 13)]
                papx_in_fkps_offset = 2 * (boffset)
                papx_in_fkps = PapxInFkps()
                papx_in_fkps._cb = data[papx_in_fkps_offset]
                papx_in_fkps_offset += 1
                grpprl_in_papx_length = 0
                if (papx_in_fkps._cb == (0)): 
                    cb_ = data[papx_in_fkps_offset]
                    papx_in_fkps_offset += 1
                    grpprl_in_papx_length = (2 * cb_)
                else: 
                    grpprl_in_papx_length = ((2 * (papx_in_fkps._cb)) - 1)
                grp_prl_and_istd = GrpPrlAndIstd()
                grp_prl_and_istd._istd = int.from_bytes(data[papx_in_fkps_offset:papx_in_fkps_offset+2], byteorder="little")
                data_stream.position = papx_in_fkps_offset + 2
                position = 2
                papx_in_fkps._grpprl_in_papx = grp_prl_and_istd
                papx_fkp._rgbx[i] = (boffset, papx_in_fkps)
                try: 
                    wrapposition392 = RefOutArgWrapper(position)
                    grp_prl_and_istd._grpprl = BasicTypesReader._read_prls(data_stream, grpprl_in_papx_length - position, wrapposition392)
                    position = wrapposition392.value
                except Exception as ex: 
                    err.value = True
                    break
                i += 1
            return papx_fkp
    
    @staticmethod
    def _read_plc_bte_chpx(s : Stream, length : int) -> 'PlcBteChpx':
        n = PlcBteChpx._get_length(length)
        plcf_bte_chpx = PlcBteChpx()
        plcf_bte_chpx._afc = Utils.newArray(n + 1, 0)
        i = 0
        while i <= n: 
            plcf_bte_chpx._afc[i] = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._dword_size)[0:0+4], byteorder="little")
            i += 1
        plcf_bte_chpx._apn_bte_chpx = Utils.newArray(n, 0)
        i = 0
        while i < n: 
            pn = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._dword_size)[0:0+4], byteorder="little")
            plcf_bte_chpx._apn_bte_chpx[i] = pn
            i += 1
        return plcf_bte_chpx
    
    @staticmethod
    def _read_chpx_fkp(s : Stream) -> 'ChpxFkp':
        data = ReadUtils._read_exact(s, ChpxFkp._size)
        with MemoryStream(data) as data_stream: 
            chpx_fkp = ChpxFkp()
            chpx_fkp._crun = data[PapxFkp._size - 1]
            crun = chpx_fkp._crun
            if ((crun < 1) or crun > 0x65): 
                raise Utils.newException("Invalid ChpxFkp: cpara", None)
            chpx_fkp._rgfc = Utils.newArray(crun + 1, 0)
            i = 0
            while i <= crun: 
                chpx_fkp._rgfc[i] = int.from_bytes(data[i * ReadUtils._dword_size:i * ReadUtils._dword_size+4], byteorder="little")
                i += 1
            chpx_fkp._rgb = Utils.newArray(crun, None)
            rgb_offset = ((crun + 1)) * ReadUtils._dword_size
            i = 0
            while i < crun: 
                offset = data[rgb_offset + i]
                chpx_fkp_offset = 2 * (offset)
                chpx = Chpx()
                chpx._cb = data[chpx_fkp_offset]
                chpx_fkp_offset += 1
                grpprl_length = chpx._cb
                data_stream.position = chpx_fkp_offset
                position = 0
                wrapposition393 = RefOutArgWrapper(position)
                chpx._grpprl = BasicTypesReader._read_prls(data_stream, grpprl_length - position, wrapposition393)
                position = wrapposition393.value
                chpx_fkp._rgb[i] = (offset, chpx)
                i += 1
            return chpx_fkp
    
    @staticmethod
    def _read_stsh(s : Stream, stsh_length : int) -> 'STSH':
        read = 0
        stsh = STSH()
        read = 0
        wrapread397 = RefOutArgWrapper(read)
        cb_stshi = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, wrapread397)[0:0+2], byteorder="little")
        read = wrapread397.value
        read_portion = 0
        wrapread_portion396 = RefOutArgWrapper(0)
        stshi = BasicTypesReader.__read_stshi(s, cb_stshi, wrapread_portion396)
        read_portion = wrapread_portion396.value
        read += read_portion
        stsh._stshi = stshi
        stsh._rglpstd = Utils.newArray(stsh._stshi._stshif._cstd, None)
        i = 0
        while i < len(stsh._rglpstd): 
            wrapread395 = RefOutArgWrapper(read)
            cb_std = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, wrapread395)[0:0+2], byteorder="little")
            read = wrapread395.value
            if (cb_std > (0)): 
                wrapread_portion394 = RefOutArgWrapper(0)
                std = BasicTypesReader.__read_std(s, cb_std, stshi._stshif._cbstdbase_in_file, wrapread_portion394)
                read_portion = wrapread_portion394.value
                stsh._rglpstd[i] = std
                read += read_portion
            i += 1
        return stsh
    
    @staticmethod
    def __read_std(s : Stream, length : int, stdf_length : int, read : int) -> 'STD':
        std = STD()
        read.value = 0
        stdf = Stdf()
        stdf_base = StdfBase()
        data = ReadUtils._read_exact_ref(s, StdfBase._size, read)
        stdf_base._sti = (((int.from_bytes(data[0:0+2], byteorder="little")) & 0xFFF))
        stdf_base._stk = (((data[2]) & 0x0F))
        stdf_base._istd_base = (((int.from_bytes(data[2:2+2], byteorder="little")) >> 4))
        stdf_base._cupx = (((data[4]) & 0x0F))
        stdf_base._istd_next = (((int.from_bytes(data[4:4+2], byteorder="little")) >> 4))
        stdf_base._bch_upe = int.from_bytes(data[6:6+2], byteorder="little")
        grfstd_data = int.from_bytes(data[8:8+2], byteorder="little")
        grfstd = GRFSTD()
        grfstd._fauto_redef = (((grfstd_data) & 0x0001)) != 0
        grfstd._fhidden = (((grfstd_data) & 0x0002)) != 0
        grfstd._f97lids_set = (((grfstd_data) & 0x0004)) != 0
        grfstd._fcopy_lang = (((grfstd_data) & 0x0008)) != 0
        grfstd._fpersonal_compose = (((grfstd_data) & 0x0010)) != 0
        grfstd._fpersonal_reply = (((grfstd_data) & 0x0020)) != 0
        grfstd._fpersonal = (((grfstd_data) & 0x0040)) != 0
        grfstd._fsemi_hidden = (((grfstd_data) & 0x0100)) != 0
        grfstd._flocked = (((grfstd_data) & 0x0200)) != 0
        grfstd._funhide_when_used = (((grfstd_data) & 0x0800)) != 0
        grfstd._fqformat = (((grfstd_data) & 0x1000)) != 0
        stdf_base._grfstd = grfstd
        stdf._stdf_base = stdf_base
        if ((StdfBase._size + StdfPost2000OrNone._size) <= (stdf_length)): 
            data = ReadUtils._read_exact_ref(s, StdfPost2000OrNone._size, read)
            stdf_post2000 = StdfPost2000OrNone()
            stdf_post2000._istd_link = (((int.from_bytes(data[0:0+2], byteorder="little")) & 0xFFF))
            stdf_post2000._fhas_original_style = (((data[1]) & 0x10)) != 0
            stdf_post2000._rsid = int.from_bytes(data[2:2+4], byteorder="little")
            stdf_post2000._ipriority = (((int.from_bytes(data[6:6+2], byteorder="little")) >> 4))
            stdf._stdf_post2000or_none = stdf_post2000
        else: 
            stdf._stdf_post2000or_none = (None)
        std._stdf = stdf
        std._xstz_name = BasicTypesReader.__read_xstz(s, (length) - read.value, read)
        swichVal = std._stdf._stdf_base._stk
        if (swichVal == GrLPUpxSw._stk_paragrlpupxstk_value): 
            std._grlpupx_sw = (BasicTypesReader.__read_stk_paragrlpupx(s, (length) - read.value, read))
        elif (swichVal == GrLPUpxSw._stk_chargrlpupxstk_value): 
            std._grlpupx_sw = (BasicTypesReader.__read_stk_chargrlpupx(s, (length) - read.value, read))
        elif (swichVal == GrLPUpxSw._stk_tablegrlpupxstk_value): 
            std._grlpupx_sw = (BasicTypesReader.__read_stk_tablegrlpupx(s, (length) - read.value, read))
        elif (swichVal == GrLPUpxSw._stk_listgrlpupxstk_value): 
            std._grlpupx_sw = (BasicTypesReader.__read_stk_listgrlpupx(s, (length) - read.value, read))
        else: 
            raise Utils.newException("Invalid Std: stk", None)
        return std
    
    @staticmethod
    def __read_xstz(s : Stream, length : int, read : int) -> 'Xstz':
        xstz = Xstz()
        xstz._xst = Xst()
        if (length < ReadUtils._word_size): 
            raise Utils.newException("Invalid Xst: length (0)", None)
        xstz._xst._cch = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (length < (ReadUtils._word_size + (2 * (xstz._xst._cch)))): 
            raise Utils.newException("Invalid Xst: length (1)", None)
        xstz._xst._rgtchar = MiscHelper.decode_string_unicode(ReadUtils._read_exact_ref(s, 2 * (xstz._xst._cch), read), 0, -1)
        if (length < (ReadUtils._word_size + (2 * (xstz._xst._cch)) + ReadUtils._word_size)): 
            raise Utils.newException("Invalid Xstz: length", None)
        zeros0_ = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (zeros0_ != (0)): 
            raise Utils.newException("Invalid Xstz: no zeros", None)
        return xstz
    
    @staticmethod
    def __read_stshi(s : Stream, length : int, read : int) -> 'Stshi':
        stshi = Stshi()
        read.value = 0
        if (length < 18): 
            raise Utils.newException("Invalid Stshi: length (0)", None)
        data = ReadUtils._read_exact_ref(s, 18, read)
        stshif = Stshif()
        stshif._cstd = int.from_bytes(data[0:0+2], byteorder="little")
        stshif._cbstdbase_in_file = int.from_bytes(data[2:2+2], byteorder="little")
        stshif._sti_max_when_saved = int.from_bytes(data[6:6+2], byteorder="little")
        stshif._istd_max_fixed_when_saved = int.from_bytes(data[8:8+2], byteorder="little")
        stshif._nver_built_in_names_when_saved = int.from_bytes(data[10:10+2], byteorder="little")
        stshif._ftc_asci = int.from_bytes(data[12:12+2], byteorder="little")
        stshif._ftcfe = int.from_bytes(data[14:14+2], byteorder="little")
        stshif._ftc_other = int.from_bytes(data[16:16+2], byteorder="little")
        stshi._stshif = stshif
        if (read.value < length): 
            stshi._ftc_bi = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (read.value < length): 
            stshi_lsd = StshiLsd()
            stshi_lsd._cblsd = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
            stshi_lsd._mpstiilsd = Utils.newArray(stshif._sti_max_when_saved, None)
            i = 0
            while i < len(stshi_lsd._mpstiilsd): 
                data = ReadUtils._read_exact_ref(s, stshi_lsd._cblsd, read)
                lsd = LSD()
                lsd._flocked = (((data[0]) & 0x01)) != 0
                lsd._fsemi_hidden = (((data[0]) & 0x02)) != 0
                lsd._funhide_when_used = (((data[0]) & 0x04)) != 0
                lsd._fqformat = (((data[0]) & 0x08)) != 0
                lsd._ipriority = (((((data[1]) << 4)) | (((data[0]) >> 4))))
                stshi_lsd._mpstiilsd[i] = lsd
                i += 1
            stshi._stshi_lsd = stshi_lsd
        if (read.value < length): 
            grpprl_chp_standard_cb_grpprl = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._dword_size)[0:0+4], byteorder="little")
            ReadUtils._skip(s, grpprl_chp_standard_cb_grpprl)
            read.value += (4 + grpprl_chp_standard_cb_grpprl)
            grpprl_pap_standard_cb_grpprl = int.from_bytes(ReadUtils._read_exact(s, ReadUtils._dword_size)[0:0+4], byteorder="little")
            ReadUtils._skip(s, grpprl_pap_standard_cb_grpprl)
            read.value += (4 + grpprl_pap_standard_cb_grpprl)
        return stshi
    
    @staticmethod
    def __read_stk_paragrlpupx(s : Stream, length : int, read : int) -> 'StkParaGRLPUPX':
        position = 0
        stk_paragrlpupx = StkParaGRLPUPX()
        wrapposition402 = RefOutArgWrapper(position)
        stk_paragrlpupx._upx_papx = BasicTypesReader.__read_upx_papx(s, length - position, wrapposition402)
        position = wrapposition402.value
        wrapposition401 = RefOutArgWrapper(position)
        stk_paragrlpupx._upx_chpx = BasicTypesReader.__read_upx_chpx(s, length - position, wrapposition401)
        position = wrapposition401.value
        if (position < length): 
            stk_para_upx_grlpupxrm = StkParaUpxGrLPUpxRM()
            wrapposition400 = RefOutArgWrapper(position)
            stk_para_upx_grlpupxrm._upx_rm = BasicTypesReader.__read_upx_rm(s, length - position, wrapposition400)
            position = wrapposition400.value
            wrapposition399 = RefOutArgWrapper(position)
            stk_para_upx_grlpupxrm._upx_papxrm = BasicTypesReader.__read_upx_papx(s, length - position, wrapposition399)
            position = wrapposition399.value
            wrapposition398 = RefOutArgWrapper(position)
            stk_para_upx_grlpupxrm._upx_chpxrm = BasicTypesReader.__read_upx_chpx(s, length - position, wrapposition398)
            position = wrapposition398.value
            stk_paragrlpupx._stk_paralpupx_grlpupxrm = stk_para_upx_grlpupxrm
            ReadUtils._skip(s, length - position)
        read.value += length
        return stk_paragrlpupx
    
    @staticmethod
    def __read_upx_rm(s : Stream, length : int, read : int) -> 'UpxRm':
        if (length < UpxRm._size): 
            raise Utils.newException("Invalid UpxRm: length", None)
        upx_rm = UpxRm()
        upx_rm._date = BasicTypesReader.__readdttm(s, read)
        upx_rm._ibst_author = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        return upx_rm
    
    @staticmethod
    def __read_upx_papx(s : Stream, length : int, read : int) -> 'UpxPapx':
        upx_papx = UpxPapx()
        cb_upx = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (((cb_upx) + ReadUtils._word_size) > length): 
            raise Utils.newException("Invalid UpxPapx: length", None)
        upx_papx._istd = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        upx_papx._grpprl_papx = BasicTypesReader._read_prls(s, (cb_upx) - ReadUtils._word_size, read)
        if ((((cb_upx) & 1)) != 0): 
            ReadUtils._read_byte_ref(s, read)
        return upx_papx
    
    @staticmethod
    def __read_upx_chpx(s : Stream, length : int, read : int) -> 'UpxChpx':
        upx_chpx = UpxChpx()
        cb_upx = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (((cb_upx) + ReadUtils._word_size) > length): 
            raise Utils.newException("Invalid UpxChpx: length", None)
        upx_chpx._grpprl_chpx = BasicTypesReader._read_prls(s, cb_upx, read)
        if ((((cb_upx) & 1)) != 0): 
            ReadUtils._read_byte_ref(s, read)
        return upx_chpx
    
    @staticmethod
    def __read_stk_chargrlpupx(s : Stream, length : int, read : int) -> 'StkCharGRLPUPX':
        position = 0
        stk_chargrlpupx = StkCharGRLPUPX()
        wrapposition405 = RefOutArgWrapper(position)
        stk_chargrlpupx._upx_chpx = BasicTypesReader.__read_upx_chpx(s, length - position, wrapposition405)
        position = wrapposition405.value
        if (position < length): 
            stk_char_upx_grlpupxrm = StkCharUpxGrLPUpxRM()
            wrapposition404 = RefOutArgWrapper(position)
            stk_char_upx_grlpupxrm._upx_rm = BasicTypesReader.__read_upx_rm(s, length - position, wrapposition404)
            position = wrapposition404.value
            wrapposition403 = RefOutArgWrapper(position)
            stk_char_upx_grlpupxrm._upx_chpxrm = BasicTypesReader.__read_upx_chpx(s, length - position, wrapposition403)
            position = wrapposition403.value
            stk_chargrlpupx._stk_charlpupx_grlpupxrm = stk_char_upx_grlpupxrm
            ReadUtils._skip(s, length - position)
        read.value += length
        return stk_chargrlpupx
    
    @staticmethod
    def __read_stk_tablegrlpupx(s : Stream, length : int, read : int) -> 'StkTableGRLPUPX':
        stk_tablegrlpupx = StkTableGRLPUPX()
        position = 0
        wrapposition408 = RefOutArgWrapper(position)
        stk_tablegrlpupx._upx_tapx = BasicTypesReader.__read_upx_tapx(s, length - position, wrapposition408)
        position = wrapposition408.value
        wrapposition407 = RefOutArgWrapper(position)
        stk_tablegrlpupx._upx_papx = BasicTypesReader.__read_upx_papx(s, length - position, wrapposition407)
        position = wrapposition407.value
        wrapposition406 = RefOutArgWrapper(position)
        stk_tablegrlpupx._upx_chpx = BasicTypesReader.__read_upx_chpx(s, length - position, wrapposition406)
        position = wrapposition406.value
        read.value += position
        return stk_tablegrlpupx
    
    @staticmethod
    def __read_upx_tapx(s : Stream, length : int, read : int) -> 'UpxTapx':
        upx_tapx = UpxTapx()
        cb_upx = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._word_size, read)[0:0+2], byteorder="little")
        if (((cb_upx) + ReadUtils._word_size) > length): 
            raise Utils.newException("Invalid UpxTapx: length", None)
        upx_tapx._grpprl_tapx = BasicTypesReader._read_prls(s, cb_upx, read)
        if ((((cb_upx) & 1)) != 0): 
            ReadUtils._read_byte_ref(s, read)
        return upx_tapx
    
    @staticmethod
    def __read_stk_listgrlpupx(s : Stream, length : int, read : int) -> 'StkListGRLPUPX':
        position = 0
        stk_listgrlpupx = StkListGRLPUPX()
        wrapposition409 = RefOutArgWrapper(position)
        stk_listgrlpupx._upx_papx = BasicTypesReader.__read_upx_papx(s, length - position, wrapposition409)
        position = wrapposition409.value
        read.value += position
        return stk_listgrlpupx
    
    @staticmethod
    def __readdttm(s : Stream, read : int) -> 'DTTM':
        dttm_data = int.from_bytes(ReadUtils._read_exact_ref(s, ReadUtils._dword_size, read)[0:0+4], byteorder="little")
        return BasicTypesReader._parsedttm(dttm_data)
    
    @staticmethod
    def _parsedttm(dttm_data : int) -> 'DTTM':
        dttm = DTTM()
        dttm._mint = (((dttm_data) & 0x3F))
        dttm._hr = (((((dttm_data) >> 6)) & 0x1F))
        dttm._dom = (((((dttm_data) >> 11)) & 0x1F))
        dttm._mon = (((((dttm_data) >> 16)) & 0x0F))
        dttm._year = (((((dttm_data) >> 20)) & 0x1FF))
        dttm._wdy = (((((dttm_data) >> 29)) & 0x07))
        return dttm