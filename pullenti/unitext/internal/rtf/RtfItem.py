# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.rtf.RftItemTyp import RftItemTyp

class RtfItem:
    """ Простейший элемент структуры файла RTF """
    
    class RftCommand:
        
        def __init__(self) -> None:
            self.command = None;
            self.char_code = 0
            self.pure_char = '\x00'
            self.pict_content = None;
            self.pic_width = 0
            self.pic_height = 0
            self.__m_temp_cmd = None;
        
        def parse(self, stream : Stream) -> bool:
            self.command = (None)
            self.char_code = (0)
            self.pure_char = (chr(0))
            self.pict_content = (None)
            i = stream.readbyte()
            if (i < 0): 
                return False
            ch = chr(i)
            if (ch == '\''): 
                buf = Utils.newArrayOfBytes(2, 0)
                if (stream.read(buf, 0, 2) != 2): 
                    return False
                for i in range(2):
                    ch = (chr(buf[i]))
                    if (ch >= '0' and ch <= '9'): 
                        buf[i] = (((ord(ch)) - (ord('0'))))
                    elif (ch >= 'a' and ch <= 'f'): 
                        buf[i] = ((((ord(ch)) - (ord('a'))) + 10))
                    elif (ch >= 'A' and ch <= 'F'): 
                        buf[i] = ((((ord(ch)) - (ord('A'))) + 10))
                    else: 
                        return False
                else: i = 2
                self.char_code = (((((buf[0]) << 4)) | (buf[1])))
                return True
            if (ch == 'u'): 
                cod = 0
                i = stream.readbyte()
                if (i < 0): 
                    return False
                ch1 = chr(i)
                if (str.isdigit(ch1)): 
                    cod = (((ord(ch1)) - (ord('0'))))
                    while True:
                        i = stream.readbyte()
                        if (i < 0): 
                            break
                        ch1 = (chr(i))
                        if (str.isdigit(ch1)): 
                            cod = ((cod * 10) + (((ord(ch1)) - (ord('0')))))
                        else: 
                            if (ch1 == '\\'): 
                                stream.position = stream.position - (1)
                            break
                    self.pure_char = (chr(cod))
                    if (self.__m_temp_cmd is None): 
                        self.__m_temp_cmd = RtfItem.RftCommand()
                    if (ch1 == '\\'): 
                        pos = stream.position
                        stream.position = stream.position + (1)
                        self.__m_temp_cmd.parse(stream)
                        if (self.__m_temp_cmd.char_code != (0)): 
                            pass
                        else: 
                            stream.position = pos
                    return True
                else: 
                    stream.position = stream.position - (1)
            if ("{}\\".find(ch) >= 0): 
                self.pure_char = ch
                return True
            if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                self.pure_char = '\n'
                return True
            cmd = io.StringIO()
            print(ch, end="", file=cmd)
            if (ch != '*'): 
                while True:
                    if (cmd.tell() == 1): 
                        if (ch == '~' or ch == '_'): 
                            break
                    i = stream.readbyte()
                    if (i < 0): 
                        break
                    ch = (chr(i))
                    if ((ch == '\\' or ch == '}' or ch == '{') or i >= 0x80): 
                        stream.position = stream.position - (1)
                        break
                    if (Utils.isWhitespace(ch)): 
                        break
                    print(ch, end="", file=cmd)
            self.command = Utils.toStringStringIO(cmd)
            if (self.command == "tab"): 
                self.pure_char = '\t'
            elif (self.command == "emdash"): 
                self.pure_char = (chr(0x2014))
            elif (self.command == "endash"): 
                self.pure_char = (chr(0x2013))
            elif (self.command == "emspace" or self.command == "enspace" or self.command == "~"): 
                self.pure_char = ' '
            elif (self.command == "bullet"): 
                self.pure_char = (chr(0x2022))
            elif (self.command == "lquote"): 
                self.pure_char = (chr(0x2018))
            elif (self.command == "rquote"): 
                self.pure_char = (chr(0x2019))
            elif (self.command == "ldblquote"): 
                self.pure_char = (chr(0x201C))
            elif (self.command == "rdblquote"): 
                self.pure_char = (chr(0x201D))
            elif (self.command == "lquote"): 
                self.pure_char = (chr(0x2018))
            elif (self.command == "_"): 
                self.pure_char = '-'
            elif (len(self.command) > 2 and self.command[0] == 'u' and str.isdigit(self.command[1])): 
                wrapi272 = RefOutArgWrapper(0)
                inoutres273 = Utils.tryParseInt(self.command[1:], wrapi272)
                i = wrapi272.value
                if (inoutres273): 
                    self.pure_char = (chr(i))
                    return True
            if ((self.command.startswith("colortbl") or self.command.startswith("info") or self.command.startswith("object")) or self.command.startswith("pict") or self.command.startswith("themedata")): 
                lev = 0
                is_pict = self.command.startswith("pict") or self.command.startswith("object")
                pict_comm = RtfItem.RftCommand()
                hex_val = io.StringIO()
                picw = 0
                pic_goalw = 0
                pich = 0
                pic_goalh = 0
                scalx = 100
                scaly = 100
                while True:
                    i = stream.readbyte()
                    if (i < 0): 
                        break
                    ch = (chr(i))
                    if (ch == '}'): 
                        if (lev == 0): 
                            stream.position = stream.position - (1)
                            break
                        else: 
                            lev -= 1
                    elif (ch == '{'): 
                        lev += 1
                    elif (ch == '\\'): 
                        if (pict_comm.parse(stream)): 
                            if (pict_comm.command is not None): 
                                if (pict_comm.command.startswith("picwgoal")): 
                                    wrappic_goalw274 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(pict_comm.command[8:], wrappic_goalw274)
                                    pic_goalw = wrappic_goalw274.value
                                elif (pict_comm.command.startswith("pichgoal")): 
                                    wrappic_goalh275 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(pict_comm.command[8:], wrappic_goalh275)
                                    pic_goalh = wrappic_goalh275.value
                                elif (pict_comm.command.startswith("picw") or pict_comm.command.startswith("objw")): 
                                    wrappicw276 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(pict_comm.command[4:], wrappicw276)
                                    picw = wrappicw276.value
                                elif (pict_comm.command.startswith("pich") or pict_comm.command.startswith("objh")): 
                                    wrappich277 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(pict_comm.command[4:], wrappich277)
                                    pich = wrappich277.value
                                elif (pict_comm.command.startswith("picscalex")): 
                                    wrapscalx278 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(pict_comm.command[9:], wrapscalx278)
                                    scalx = wrapscalx278.value
                                elif (pict_comm.command.startswith("picscaley")): 
                                    wrapscaly279 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(pict_comm.command[9:], wrapscaly279)
                                    scaly = wrapscaly279.value
                                elif (pict_comm.command.startswith("bin")): 
                                    blen = 0
                                    wrapblen280 = RefOutArgWrapper(0)
                                    inoutres281 = Utils.tryParseInt(pict_comm.command[3:], wrapblen280)
                                    blen = wrapblen280.value
                                    if (inoutres281): 
                                        if ((stream.position + (blen)) <= stream.length): 
                                            if (is_pict): 
                                                self.pict_content = Utils.newArrayOfBytes(blen, 0)
                                                stream.read(self.pict_content, 0, blen)
                                            else: 
                                                stream.position = stream.position + (blen)
                                if (is_pict and pict_comm.pict_content is not None): 
                                    self.pict_content = pict_comm.pict_content
                    elif (lev == 0 and is_pict and str.isalnum(ch)): 
                        print(ch, end="", file=hex_val)
                if (is_pict and hex_val.tell() > 10 and self.pict_content is None): 
                    self.pict_content = Utils.newArrayOfBytes(math.floor(hex_val.tell() / 2), 0)
                    str0_ = Utils.toStringStringIO(hex_val)
                    ii = 0; p = 0
                    while ii < (hex_val.tell() - 1): 
                        bb = 0
                        for jj in range(2):
                            chh = str0_[ii + jj]
                            v = 0
                            if (chh >= '0' and chh <= '9'): 
                                v = ((ord(chh)) - (ord('0')))
                            elif (chh >= 'a' and chh <= 'f'): 
                                v = (10 + (((ord(chh)) - (ord('a')))))
                            elif (chh >= 'A' and chh <= 'F'): 
                                v = (10 + (((ord(chh)) - (ord('A')))))
                            else: 
                                break
                            bb = (((((bb) << 4)) | v))
                        self.pict_content[p] = bb
                        ii += 2; p += 1
                if (is_pict and ((picw > 0 or pic_goalw > 0)) and ((pich > 0 or pic_goalh > 0))): 
                    if (pic_goalw <= 0 or pic_goalh <= 0): 
                        self.pic_width = (math.floor((0.75 * (self.pic_width))))
                        self.pic_height = (math.floor((0.75 * (self.pic_height))))
                    else: 
                        self.pic_width = (math.floor(pic_goalw / 20))
                        self.pic_height = (math.floor(pic_goalh / 20))
                    if (scalx > 0): 
                        self.pic_width = (math.floor((self.pic_width * scalx) / 100))
                    if (scaly > 0): 
                        self.pic_height = (math.floor((self.pic_height * scaly) / 100))
                return True
            return True
    
    def __init__(self) -> None:
        self.typ = RftItemTyp.UNDEFINED
        self.text = None;
        self.codes = None;
        self.level = 0
    
    def __str__(self) -> str:
        if (self.typ == RftItemTyp.BRACKETOPEN): 
            return "{0}: {{".format(self.level)
        if (self.typ == RftItemTyp.BRACKETCLOSE): 
            return "{0}: }}".format(self.level)
        if (self.typ == RftItemTyp.COMMAND): 
            return "{0}: \\{1}".format(self.level, Utils.ifNotNull(self.text, ""))
        if (self.typ == RftItemTyp.IMAGE): 
            return "{0}: Image {1}: Len={2}".format(self.level, Utils.ifNotNull(self.text, ""), len(self.codes))
        if (self.typ == RftItemTyp.TEXT): 
            if (self.text is not None): 
                return "{0}: [{1}] '{2}'".format(self.level, len(self.text), (self.text[0:0+200] if len(self.text) > 200 else self.text))
            if (self.codes is not None): 
                tmp = io.StringIO()
                print("{0}: [{1}]".format(self.level, len(self.codes)), end="", file=tmp, flush=True)
                for c in self.codes: 
                    print("'{0}' ".format("{:02X}".format(c)), end="", file=tmp, flush=True)
                    if (tmp.tell() > 200): 
                        print("...", end="", file=tmp)
                        break
                return Utils.toStringStringIO(tmp)
        return "?"
    
    @staticmethod
    def parse_list(stream : Stream) -> typing.List['RtfItem']:
        from pullenti.unitext.internal.rtf.RtfItemImage import RtfItemImage
        res = list()
        txt_buf = io.StringIO()
        cod_buf = bytearray()
        command = RtfItem.RftCommand()
        while stream.position < stream.length:
            i = stream.readbyte()
            if (i < 0): 
                break
            ch = chr(i)
            new_item = None
            new_code = 0
            new_char = chr(0)
            if (ch == '{'): 
                new_item = RtfItem._new282(RftItemTyp.BRACKETOPEN)
            elif (ch == '}'): 
                new_item = RtfItem._new282(RftItemTyp.BRACKETCLOSE)
            elif (ch == '\\'): 
                if (not command.parse(stream)): 
                    continue
                if (command.char_code != (0)): 
                    new_code = command.char_code
                elif ((ord(command.pure_char)) != 0): 
                    new_char = command.pure_char
                elif (command.pict_content is not None): 
                    new_item = (RtfItemImage._new284(RftItemTyp.IMAGE, command.pic_width, command.pic_height, command.command, command.pict_content))
                elif (command.command is not None): 
                    new_item = RtfItem._new285(RftItemTyp.COMMAND, command.command)
            else: 
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                    continue
                if ((ord(ch)) < 0x80): 
                    new_char = ch
                else: 
                    new_code = (ord(ch))
            if (new_item is not None or new_code != (0)): 
                if (txt_buf.tell() > 0): 
                    res.append(RtfItem._new285(RftItemTyp.TEXT, Utils.toStringStringIO(txt_buf)))
                    Utils.setLengthStringIO(txt_buf, 0)
            if (new_item is not None or (ord(new_char)) != 0): 
                if (len(cod_buf) > 0): 
                    res.append(RtfItem._new287(RftItemTyp.TEXT, bytearray(cod_buf)))
                    cod_buf.clear()
            if (new_item is not None): 
                res.append(new_item)
            if (new_code != (0)): 
                cod_buf.append(new_code)
            if ((ord(new_char)) != 0): 
                print(new_char, end="", file=txt_buf)
        if (txt_buf.tell() > 0): 
            res.append(RtfItem._new285(RftItemTyp.TEXT, Utils.toStringStringIO(txt_buf)))
            Utils.setLengthStringIO(txt_buf, 0)
        if (len(cod_buf) > 0): 
            res.append(RtfItem._new287(RftItemTyp.TEXT, bytearray(cod_buf)))
            cod_buf.clear()
        lev = 0
        for it in res: 
            it.level = lev
            if (it.typ == RftItemTyp.BRACKETOPEN): 
                lev += 1
            elif (it.typ == RftItemTyp.BRACKETCLOSE): 
                lev -= 1
                it.level = lev
        return res
    
    @staticmethod
    def _new282(_arg1 : 'RftItemTyp') -> 'RtfItem':
        res = RtfItem()
        res.typ = _arg1
        return res
    
    @staticmethod
    def _new285(_arg1 : 'RftItemTyp', _arg2 : str) -> 'RtfItem':
        res = RtfItem()
        res.typ = _arg1
        res.text = _arg2
        return res
    
    @staticmethod
    def _new287(_arg1 : 'RftItemTyp', _arg2 : bytearray) -> 'RtfItem':
        res = RtfItem()
        res.typ = _arg1
        res.codes = _arg2
        return res