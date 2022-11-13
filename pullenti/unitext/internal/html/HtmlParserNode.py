# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class HtmlParserNode:
    
    class TagTypes(IntEnum):
        UNDEFINED = 0
        OPEN = 1
        CLOSE = 2
        OPENCLOSE = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self) -> None:
        self.index_from = 0
        self.index_to = 0
        self.tag_name = None;
        self.tag_type = HtmlParserNode.TagTypes.UNDEFINED
        self.tag = None;
        self.close_tag_index = 0
        self.attributes = dict()
        self.pure_text = None;
        self.whitespace_preserve = False
        self._printed = False
    
    @property
    def is_empty(self) -> bool:
        if (self.tag_name is not None): 
            return False
        if (self.attributes is not None and len(self.attributes) > 0): 
            return False
        if (not Utils.isNullOrEmpty(self.pure_text)): 
            if (self.whitespace_preserve): 
                return False
            i = 0
            while i < len(self.pure_text): 
                if (not Utils.isWhitespace(self.pure_text[i])): 
                    return False
                i += 1
        return True
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.tag_type != HtmlParserNode.TagTypes.UNDEFINED): 
            if (self.tag_type == HtmlParserNode.TagTypes.CLOSE): 
                print("</{0}>".format(self.tag_name), end="", file=res, flush=True)
            else: 
                print("<{0}".format(self.tag_name), end="", file=res, flush=True)
                if (self.attributes is not None): 
                    for kp in self.attributes.items(): 
                        print(" {0}='{1}'".format(kp[0], kp[1]), end="", file=res, flush=True)
                if (self.tag_type == HtmlParserNode.TagTypes.OPEN): 
                    print(">", end="", file=res)
                else: 
                    print("/>", end="", file=res)
        elif (self.pure_text is not None): 
            print(self.pure_text, end="", file=res)
        return Utils.toStringStringIO(res)
    
    def analize(self, html_ : str, ind_from : int, end_tag : str, white_space_preserve : bool) -> bool:
        if (ind_from >= len(html_)): 
            return False
        self.index_from = ind_from
        self.tag_name = (None)
        self.tag_type = HtmlParserNode.TagTypes.UNDEFINED
        if (self.attributes is None): 
            self.attributes = dict()
        else: 
            self.attributes.clear()
        self.pure_text = (None)
        i = 0
        j = 0
        ch = html_[ind_from]
        if (ch != '<' or ((end_tag is not None and not HtmlParserNode.__is_end_tag(html_, ind_from, end_tag)))): 
            str_tmp = None
            comment = False
            last_nbsp = 0
            i = ind_from
            first_pass621 = True
            while True:
                if first_pass621: first_pass621 = False
                else: i += 1
                if (not (i < len(html_))): break
                nbr = False
                if (html_[i] == '<'): 
                    if (not comment): 
                        if (end_tag is None or HtmlParserNode.__is_end_tag(html_, i, end_tag)): 
                            break
                    if ((((i + 3) < len(html_)) and html_[i + 1] == '!' and html_[i + 2] == '-') and html_[i + 3] == '-'): 
                        comment = True
                        i += 3
                        continue
                    ch = html_[i]
                    j = 1
                else: 
                    if (comment and html_[i] == '-'): 
                        if (((i + 2) < len(html_)) and html_[i + 1] == '-' and html_[i + 2] == '>'): 
                            comment = False
                            i += 2
                            continue
                    wrapch24 = RefOutArgWrapper(None)
                    wrapnbr25 = RefOutArgWrapper(False)
                    inoutres26 = HtmlParserNode.__parse_char(html_, i, wrapch24, wrapnbr25)
                    ch = wrapch24.value
                    nbr = wrapnbr25.value
                    j = inoutres26
                    if (((j)) < 1): 
                        break
                if (Utils.isWhitespace(ch)): 
                    ch = ' '
                if (ch == ' ' and not white_space_preserve): 
                    prev_sp = (True if str_tmp is None else (Utils.getCharAtStringIO(str_tmp, str_tmp.tell() - 1) == ' '))
                    if (not prev_sp or nbr): 
                        if (str_tmp is None): 
                            str_tmp = io.StringIO()
                        print(ch, end="", file=str_tmp)
                    if (nbr): 
                        last_nbsp += 1
                else: 
                    last_nbsp = 0
                    if (str_tmp is None): 
                        str_tmp = io.StringIO()
                    if (nbr and white_space_preserve and ch == ' '): 
                        ch = (chr(0xA0))
                    print(ch, end="", file=str_tmp)
                if (white_space_preserve): 
                    self.whitespace_preserve = True
                i += (j - 1)
            if (last_nbsp == 0 and not white_space_preserve and str_tmp is not None): 
                for jj in range(str_tmp.tell() - 1, 0, -1):
                    if (Utils.getCharAtStringIO(str_tmp, jj) != ' '): 
                        break
                    else: 
                        Utils.setLengthStringIO(str_tmp, str_tmp.tell() - 1)
            if (str_tmp is not None): 
                self.pure_text = Utils.toStringStringIO(str_tmp)
            self.index_to = (i - 1)
            return True
        if ((ind_from + 2) >= len(html_)): 
            return False
        ch = html_[ind_from + 1]
        if (str.isalpha(ch)): 
            self.tag_name = HtmlParserNode.__read_latin_word(html_, ind_from + 1)
            if (self.tag_name is None): 
                self.index_to = (ind_from + 1)
                return True
            if (self.tag_name == "BR"): 
                pass
            self.tag_type = HtmlParserNode.TagTypes.OPEN
            str_tmp = None
            i = (ind_from + 1 + len(self.tag_name))
            first_pass622 = True
            while True:
                if first_pass622: first_pass622 = False
                else: i += 1
                if (not (i < len(html_))): break
                ch = html_[i]
                if (Utils.isWhitespace(ch)): 
                    continue
                if (ch == '>'): 
                    i += 1
                    break
                if (ch == '/'): 
                    if ((i + 1) >= len(html_)): 
                        return False
                    if (html_[i + 1] == '>'): 
                        i += 1
                    self.tag_type = HtmlParserNode.TagTypes.OPENCLOSE
                    i += 1
                    break
                attr_name = HtmlParserNode.__read_latin_word(html_, i)
                if (attr_name is None): 
                    continue
                i += len(attr_name)
                if ((i + 2) >= len(html_) or html_[i] != '='): 
                    i -= 1
                    continue
                i += 1
                if (str_tmp is not None): 
                    Utils.setLengthStringIO(str_tmp, 0)
                bracket = chr(0)
                if (html_[i] == '\'' or html_[i] == '"'): 
                    bracket = html_[i]
                    i += 1
                while i < len(html_): 
                    ch = html_[i]
                    if (bracket != (chr(0))): 
                        if (ch == bracket): 
                            i += 1
                            break
                    elif (ch == '>'): 
                        break
                    elif (Utils.isWhitespace(ch)): 
                        break
                    elif (ch == '/' and ((i + 1) < len(html_)) and html_[i + 1] == '>'): 
                        pass
                    nbr = False
                    wrapch27 = RefOutArgWrapper(None)
                    wrapnbr28 = RefOutArgWrapper(False)
                    inoutres29 = HtmlParserNode.__parse_char(html_, i, wrapch27, wrapnbr28)
                    ch = wrapch27.value
                    nbr = wrapnbr28.value
                    j = inoutres29
                    if (((j)) < 1): 
                        ch = html_[i]
                        j = 1
                    if (str_tmp is None): 
                        str_tmp = io.StringIO()
                    print(ch, end="", file=str_tmp)
                    i += (j - 1)
                    i += 1
                i -= 1
                if (not attr_name in self.attributes and str_tmp is not None and str_tmp.tell() > 0): 
                    self.attributes[attr_name] = Utils.toStringStringIO(str_tmp)
            self.index_to = (i - 1)
            return True
        if (html_[ind_from + 1] == '/'): 
            i = (ind_from + 2)
            self.tag_name = HtmlParserNode.__read_latin_word(html_, i)
            if (self.tag_name is not None): 
                i += len(self.tag_name)
                if ((i < len(html_)) and html_[i] == '>'): 
                    i += 1
                    self.tag_type = HtmlParserNode.TagTypes.CLOSE
            self.index_to = (i - 1)
            return True
        if ((((ind_from + 5) < len(html_)) and html_[ind_from + 1] == '!' and html_[ind_from + 2] == '-') and html_[ind_from + 3] == '-'): 
            i = (ind_from + 4)
            while i < (len(html_) - 3): 
                if (html_[i] == '-' and html_[i + 1] == '-' and html_[i + 2] == '>'): 
                    self.index_to = (i + 2)
                    return True
                i += 1
            return False
        i = ind_from
        while i < len(html_): 
            if (html_[i] == '>'): 
                i += 1
                break
            i += 1
        self.index_to = (i - 1)
        return True
    
    @staticmethod
    def __parse_char(txt : str, ind : int, ch : 'char', nbsp : bool) -> int:
        ch.value = (chr(0))
        nbsp.value = False
        if (ind >= len(txt)): 
            return -1
        if (txt[ind] != '&'): 
            ch.value = txt[ind]
            return 1
        str_tmp = io.StringIO()
        i = 0
        i = (ind + 1)
        while i < len(txt): 
            if (txt[i] == ';'): 
                break
            else: 
                print(txt[i], end="", file=str_tmp)
                if (str_tmp.tell() > 7): 
                    break
            i += 1
        if (i >= len(txt) or txt[i] != ';'): 
            if (Utils.toStringStringIO(str_tmp).startswith("nbsp")): 
                ch.value = ' '
                nbsp.value = True
                return 5
            ch.value = '&'
            return 1
        ret = (i + 1) - ind
        if (str_tmp.tell() == 0): 
            return ret
        s = Utils.toStringStringIO(str_tmp)
        if (s in HtmlParserNode.M_SPEC_CHARS): 
            ch.value = HtmlParserNode.M_SPEC_CHARS[s]
            if (s == "nbsp"): 
                nbsp.value = True
            return ret
        if (s[0] != '#' or (str_tmp.tell() < 2)): 
            ch.value = '&'
            return ret
        if (str.isdigit(s[1])): 
            try: 
                ch.value = (chr(int(s[1:])))
                nbsp.value = Utils.isWhitespace(ch.value)
            except Exception as ex30: 
                pass
            return ret
        if (s[1] == 'x' or s[1] == 'X'): 
            try: 
                code = 0
                s = s.upper()
                ii = 2
                while ii < len(s): 
                    if (str.isdigit(s[ii])): 
                        code = (((code << 4)) + (((ord(s[ii])) - (ord('0')))))
                    elif (s[ii] >= 'A' and s[ii] <= 'F'): 
                        code = (((code << 4)) + ((((ord(s[ii])) - (ord('A'))) + 10)))
                    ii += 1
                ch.value = (chr(code))
                nbsp.value = Utils.isWhitespace(ch.value)
            except Exception as ex31: 
                pass
            return ret
        ch.value = s[1]
        return ret
    
    @staticmethod
    def __read_latin_word(str0_ : str, ind : int) -> str:
        if ((ind + 1) >= len(str0_)): 
            return None
        i = 0
        i = ind
        while i < len(str0_): 
            if (not str.isalpha(str0_[i]) and str0_[i] != ':' and str0_[i] != '_'): 
                if (i == 0): 
                    break
                if (not str.isdigit(str0_[i]) and str0_[i] != '.' and str0_[i] != '-'): 
                    break
            else: 
                cod = ord(str0_[i])
                if (cod > 0x80): 
                    break
            i += 1
        if (i <= ind): 
            return None
        return str0_[ind:ind+i - ind].upper()
    
    @staticmethod
    def __is_end_tag(html_ : str, pos : int, tag_name_ : str) -> bool:
        if ((pos + 3) >= len(html_) or tag_name_ is None): 
            return False
        if (html_[pos] != '<' and html_[pos + 1] != '/'): 
            return False
        if (HtmlParserNode.__read_latin_word(html_, pos + 2) != tag_name_): 
            return False
        return True
    
    M_SPEC_CHARS = None
    
    # static constructor for class HtmlParserNode
    @staticmethod
    def _static_ctor():
        HtmlParserNode.M_SPEC_CHARS = dict()
        HtmlParserNode.M_SPEC_CHARS["nbsp"] = ' '
        HtmlParserNode.M_SPEC_CHARS["lt"] = '<'
        HtmlParserNode.M_SPEC_CHARS["gt"] = '>'
        HtmlParserNode.M_SPEC_CHARS["quot"] = '"'
        HtmlParserNode.M_SPEC_CHARS["apos"] = '\''
        data = "iexcl=161;cent=162;pound=163;curren=164;yen=165;brvbar=166;sect=167;uml=168;copy=169;ordf=170;laquo=171;not=172;shy=173;reg=174;macr=175;deg=176;plusmn=177;sup2=178;sup3=179;acute=180;micro=181;para=182;middot=183;cedil=184;sup1=185;ordm=186;raquo=187;frac14=188;frac12=189;frac34=190;iquest=191;Agrave=192;Aacute=193;Acirc=194;Atilde=195;Auml=196;Aring=197;AElig=198;Ccedil=199;Egrave=200;Eacute=201;Ecirc=202;Euml=203;Igrave=204;Iacute=205;Icirc=206;Iuml=207;ETH=208;Ntilde=209;Ograve=210;Oacute=211;Ocirc=212;Otilde=213;Ouml=214;times=215;Oslash=216;Ugrave=217;Uacute=218;Ucirc=219;Uuml=220;Yacute=221;THORN=222;szlig=223;agrave=224;aacute=225;acirc=226;atilde=227;auml=228;aring=229;aelig=230;ccedil=231;egrave=232;eacute=233;ecirc=234;euml=235;igrave=236;iacute=237;icirc=238;iuml=239;eth=240;ntilde=241;ograve=242;oacute=243;ocirc=244;otilde=245;ouml=246;divide=247;oslash=248;ugrave=249;uacute=250;ucirc=251;uuml=252;yacute=253;thorn=254;yuml=255;Alpha=913;Beta=914;Gamma=915;Delta=916;Epsilon=917;Zeta=918;Eta=919;Theta=920;Iota=921;Kappa=922;Lambda=923;Mu=924;Nu=925;Xi=926;Omicron=927;Pi=928;Rho=929;Sigma=931;Tau=932;Upsilon=933;Phi=934;Chi=935;Psi=936;Omega=937;alpha=945;beta=946;gamma=947;delta=948;epsilon=949;zeta=950;eta=951;theta=952;iota=953;kappa=954;lambda=955;mu=956;nu=957;xi=958;omicron=959;pi=960;rho=961;sigmaf=962;sigma=963;tau=964;upsilon=965;phi=966;chi=967;psi=968;omega=969;thetasym=977;upsih=978;piv=982;bull=8226;hellip=8230;prime=8242;Prime=8243;oline=8254;frasl=8260;weierp=8472;image=8465;real=8476;trade=8482;alefsym=8501;larr=8592;uarr=8593;rarr=8594;darr=8595;harr=8596;crarr=8629;lArr=8656;uArr=8657;rArr=8658;dArr=8659;hArr=8660;forall=8704;part=8706;exist=8707;empty=8709;nabla=8711;isin=8712;notin=8713;ni=8715;prod=8719;sum=8721;minus=8722;lowast=8727;radic=8730;prop=8733;infin=8734;ang=8736;and=8743;or=8744;cap=8745;cup=8746;int=8747;there4=8756;sim=8764;cong=8773;asymp=8776;ne=8800;equiv=8801;le=8804;ge=8805;sub=8834;sup=8835;nsub=8836;sube=8838;supe=8839;oplus=8853;otimes=8855;perp=8869;sdot=8901;lceil=8968;rceil=8969;lfloor=8970;rfloor=8971;lang=9001;rang=9002;loz=9674;spades=9824;clubs=9827;hearts=9829;diams=9830;amp=38;OElig=338;oelig=339;Scaron=352;scaron=353;Yuml=376;circ=710;tilde=732;ensp=8194;emsp=8195;thinsp=8201;zwnj=8204;zwj=8205;lrm=8206;rlm=8207;ndash=8211;mdash=8212;lsquo=8216;rsquo=8217;sbquo=8218;ldquo=8220;rdquo=8221;bdquo=8222;dagger=8224;Dagger=8225;permil=8240;lsaquo=8249;rsaquo=8250;euro=8364"
        for s in Utils.splitString(data, ';', False): 
            i = s.find('=')
            key = s[0:0+i]
            cod = int(s[i + 1:])
            HtmlParserNode.M_SPEC_CHARS[key] = chr(cod)

HtmlParserNode._static_ctor()