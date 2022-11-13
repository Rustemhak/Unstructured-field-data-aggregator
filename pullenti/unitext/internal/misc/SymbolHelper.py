# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class SymbolHelper:
    
    @staticmethod
    def __to_hex(ch : 'char') -> int:
        if ((ord(ch)) >= 0 and ch <= '9'): 
            return ((ord(ch)) - (ord('0')))
        if (ch >= 'A' and ch <= 'F'): 
            return (((ord(ch)) - (ord('A'))) + 10)
        return -1
    
    __m_to_uni = None
    
    @staticmethod
    def get_unicode(code : int) -> 'char':
        if (code >= 0 and (code < len(SymbolHelper.__m_to_uni))): 
            return SymbolHelper.__m_to_uni[code]
        else: 
            return chr(0)
    
    @staticmethod
    def get_unicode_string(str0_ : str) -> str:
        res = io.StringIO()
        for c in str0_: 
            ch = SymbolHelper.get_unicode(ord(c))
            if (ch != (chr(0))): 
                print(ch, end="", file=res)
            else: 
                print("?", end="", file=res)
        return Utils.toStringStringIO(res)
    
    # static constructor for class SymbolHelper
    @staticmethod
    def _static_ctor():
        data = "20;20\n20;00A0\n21;21\n22;2200\n23;23\n24;2203\n25;25\n26;26\n27;220B\n28;28\n29;29\n2A;2217\n2B;002B\n2C;002C\n2D;2212\n2E;002E\n2F;002F\n30;30\n31;31\n32;32\n33;33\n34;34\n35;35\n36;36\n37;37\n38;38\n39;39\n3A;003A\n3B;003B\n3C;003C\n3D;003D\n3E;003E\n3F;003F\n40;2245\n41;391\n42;392\n43;03A7\n44;394\n44;2206\n45;395\n46;03A6\n47;393\n48;397\n49;399\n4A;03D1\n4B;039A\n4C;039B\n4D;039C\n4E;039D\n4F;039F\n50;03A0\n51;398\n52;03A1\n53;03A3\n54;03A4\n55;03A5\n56;03C2\n57;03A9\n57;2126\n58;039E\n59;03A8\n5A;396\n5B;005B\n5C;2234\n5D;005D\n5E;22A5\n5F;005F\n60;F8E5\n61;03B1\n62;03B2\n63;03C7\n64;03B4\n65;03B5\n66;03C6\n67;03B3\n68;03B7\n69;03B9\n6A;03D5\n6B;03BA\n6C;03BB\n6D;00B5\n6D;03BC\n6E;03BD\n6F;03BF\n70;03C0\n71;03B8\n72;03C1\n73;03C3\n74;03C4\n75;03C5\n76;03D6\n77;03C9\n78;03BE\n79;03C8\n7A;03B6\n7B;007B\n7C;007C\n7D;007D\n7E;223C\nA0;20AC\nA1;03D2\nA2;2032\nA3;2264\nA4;2044\nA4;2215\nA5;221E\nA6;192\nA7;2663\nA8;2666\nA9;2665\nAA;2660\nAB;2194\nAC;2190\nAD;2191\nAE;2192\nAF;2193\nB0;00B0\nB1;00B1\nB2;2033\nB3;2265\nB4;00D7\nB5;221D\nB6;2202\nB7;2022\nB8;00F7\nB9;2260\nBA;2261\nBB;2248\nBC;2026\nBD;F8E6\nBE;F8E7\nBF;21B5\nC0;2135\nC1;2111\nC2;211C\nC3;2118\nC4;2297\nC5;2295\nC6;2205\nC7;2229\nC8;222A\nC9;2283\nCA;2287\nCB;2284\nCC;2282\nCD;2286\nCE;2208\nCF;2209\nD0;2220\nD1;2207\nD2;F6DA\nD3;F6D9\nD4;F6DB\nD5;220F\nD6;221A\nD7;22C5\nD8;00AC\nD9;2227\nDA;2228\nDB;21D4\nDC;21D0\nDD;21D1\nDE;21D2\nDF;21D3\nE0;25CA\nE1;2329\nE2;F8E8\nE3;F8E9\nE4;F8EA\nE5;2211\nE6;F8EB\nE7;F8EC\nE8;F8ED\nE9;F8EE\nEA;F8EF\nEB;F8F0\nEC;F8F1\nED;F8F2\nEE;F8F3\nEF;F8F4\nF1;232A\nF2;222B\nF3;2320\nF4;F8F5\nF5;2321\nF6;F8F6\nF7;F8F7\nF8;F8F8\nF9;F8F9\nFA;F8FA\nFB;F8FB\nFC;F8FC\nFD;F8FD\nFE;F8FE"
        SymbolHelper.__m_to_uni = Utils.newArray(256, None)
        for i in range(256):
            SymbolHelper.__m_to_uni[i] = (chr(0))
        for pp in Utils.splitString(data, '\n', False): 
            cod = ((SymbolHelper.__to_hex(pp[0]) << 4)) + SymbolHelper.__to_hex(pp[1])
            if ((ord(SymbolHelper.__m_to_uni[cod])) != 0): 
                continue
            uni = 0
            i = 3
            while i < len(pp): 
                j = SymbolHelper.__to_hex(pp[i])
                if (j < 0): 
                    break
                uni = (((uni << 4)) + j)
                i += 1
            SymbolHelper.__m_to_uni[cod] = (chr(uni))

SymbolHelper._static_ctor()