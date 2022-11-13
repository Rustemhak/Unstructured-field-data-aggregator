# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime
import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream
from pullenti.unisharp.Xml import XmlWriter

class MiscHelper:
    """ Набор полезных функций """
    
    @staticmethod
    def extract_text(file_name : str, content : bytearray=None, unzip_archives : bool=True) -> str:
        """ Выделить текст из всех форматов, какие только поддерживаются
        
        Args:
            file_name(str): 
            content(bytearray): 
            unzip_archives(bool): при true будет распаковывать архивы и извлекать тексты из файлов,
        сумммарный текст получается конкатенацией
        
        Returns:
            str: результат или null, если не получилось
        """
        from pullenti.util.TextHelper import TextHelper
        return TextHelper.extract_text(file_name, content, unzip_archives)
    
    @staticmethod
    def get_string_hash_code(str0_ : str) -> int:
        """ Получить hash-значение для строки. В отличие от штатных функций, эта работает
        одинаково во всех случаях (например, в C# функция GetHashCode возвращает разные значения
        на 32-х и 64-х разрядных компьютерах).
        
        Args:
            str0_(str): строка
        
        Returns:
            int: хэш-значение
        """
        if (Utils.isNullOrEmpty(str0_)): 
            return 0
        num = 0x15051505
        num2 = num
        i = 0
        while i < len(str0_): 
            num0 = (ord(str0_[i + 1]) if (i + 1) < len(str0_) else 0)
            num0 <<= 16
            num0 |= ((ord(str0_[i])) & 0xFFFF)
            num = (((((((num << 5)) + num)) + ((num >> 0x1b)))) ^ num0)
            if ((i + 3) >= len(str0_)): 
                break
            num0 = (ord(str0_[i + 3]))
            num0 <<= 16
            num0 |= ((ord(str0_[i + 2])) & 0xFFFF)
            num2 = (((((((num2 << 5)) + num2)) + ((num2 >> 0x1b)))) ^ num0)
            i += 4
        return (num + ((num2 * 0x5d588b65)))
    
    @staticmethod
    def get_char_hash_code(ch : 'char') -> int:
        return (ord(ch)) | (((ord(ch)) << 16))
    
    @staticmethod
    def try_parse_float(str0_ : str, res : float) -> bool:
        """ Преобразовать строку в float. Pаботает независимо от региональных настроек.
        
        Args:
            str0_(str): строка, разделитель может быть как точка, так и запятая
            res(float): результат
        
        Returns:
            bool: признак корректности
        """
        res.value = (0)
        if (Utils.isNullOrEmpty(str0_)): 
            return False
        inoutres597 = Utils.tryParseFloat(str0_, res)
        if (inoutres597): 
            return True
        inoutres596 = Utils.tryParseFloat(str0_.replace(',', '.'), res)
        if (str0_.find(',') >= 0 and inoutres596): 
            return True
        inoutres595 = Utils.tryParseFloat(str0_.replace('.', ','), res)
        if (str0_.find('.') >= 0 and inoutres595): 
            return True
        return False
    
    @staticmethod
    def try_parse_double(str0_ : str, res : float) -> bool:
        """ Преобразовать строку в double. Pаботает независимо от региональных настроек.
        
        Args:
            str0_(str): строка, разделитель может быть как точка, так и запятая
            res(float): результат
        
        Returns:
            bool: признак корректности
        """
        res.value = (0)
        if (Utils.isNullOrEmpty(str0_)): 
            return False
        inoutres600 = Utils.tryParseFloat(str0_, res)
        if (inoutres600): 
            return True
        inoutres599 = Utils.tryParseFloat(str0_.replace(',', '.'), res)
        if (str0_.find(',') >= 0 and inoutres599): 
            return True
        inoutres598 = Utils.tryParseFloat(str0_.replace('.', ','), res)
        if (str0_.find('.') >= 0 and inoutres598): 
            return True
        return False
    
    @staticmethod
    def out_double(val : float) -> str:
        """ Вывести значение в строку. Не зависит от региональных настроек, разделитель всегда точка.
        
        Args:
            val(float): 
        
        """
        return str(val).replace(',', '.')
    
    @staticmethod
    def out_date_time(dt : datetime.datetime, time_ignore : bool=False) -> str:
        """ Вывести дату-время. Не зависит от региональных настроек, всегда в формате YYYY.MM.DD HH:MM:SS
        
        Args:
            dt(datetime.datetime): дата-время
            time_ignore(bool): не выводить время
        
        Returns:
            str: строка с результатом
        """
        if (time_ignore): 
            return "{0}.{1}.{2}".format(dt.year, "{:02d}".format(dt.month), "{:02d}".format(dt.day))
        else: 
            return "{0}.{1}.{2} {3}:{4}:{5}".format(dt.year, "{:02d}".format(dt.month), "{:02d}".format(dt.day), "{:02d}".format(dt.hour), "{:02d}".format(dt.minute), "{:02d}".format(dt.second))
    
    @staticmethod
    def try_parse_date_time(val : str) -> datetime.datetime:
        """ Преобразовать строку в DateTime. Pаботает независимо от региональных настроек.
        
        Args:
            str: строка с датой в разных форматах написания
        
        Returns:
            datetime.datetime: результат или null
        """
        if (Utils.isNullOrEmpty(val)): 
            return None
        ints = list()
        ist = False
        i = 0
        while i < len(val): 
            if (str.isdigit(val[i])): 
                v = (ord(val[i])) - 0x30
                i += 1
                while i < len(val): 
                    if (not str.isdigit(val[i])): 
                        break
                    else: 
                        v = (((v * 10) + (ord(val[i]))) - 0x30)
                    i += 1
                ints.append(v)
                if (len(ints) == 3 and (i < len(val)) and val[i] == 'T'): 
                    ist = True
            elif (len(ints) == 3 and val[i] == 'T'): 
                ist = True
            i += 1
        try: 
            if (len(ints) == 3): 
                if (ints[2] > 1900): 
                    return datetime.datetime(ints[2], ints[1], ints[0], 0, 0, 0)
                if (ints[1] > 12 or ints[2] > 31): 
                    return None
                return datetime.datetime(ints[0], ints[1], ints[2], 0, 0, 0)
            elif (len(ints) == 6 or ((len(ints) >= 6 and ist))): 
                return datetime.datetime(ints[0], ints[1], ints[2], ints[3], ints[4], ints[5])
            elif (len(ints) == 7 and ints[0] >= 1990 and ints[1] <= 12): 
                return datetime.datetime(ints[0], ints[1], ints[2], ints[3], ints[4], ints[5])
        except Exception as ex: 
            pass
        return None
    
    @staticmethod
    def parse_date_time(val : str) -> datetime.datetime:
        """ Преобразовать строку в DateTime. Pаботает независимо от региональных настроек.
        
        Args:
            str: строка с датой в разных форматах написания
        
        Returns:
            datetime.datetime: результат или DateTime.MinValue при ошибке
        """
        dt = MiscHelper.try_parse_date_time(val)
        if (dt is None): 
            return datetime.datetime.min
        return dt
    
    @staticmethod
    def serialize_int(stream : Stream, val : int) -> None:
        stream.write((val).to_bytes(4, byteorder="little"), 0, 4)
    
    @staticmethod
    def deserialize_int(stream : Stream) -> int:
        buf = Utils.newArrayOfBytes(4, 0)
        stream.read(buf, 0, 4)
        return int.from_bytes(buf[0:0+4], byteorder="little")
    
    @staticmethod
    def serialize_short(stream : Stream, val : int) -> None:
        stream.write((val).to_bytes(2, byteorder="little"), 0, 2)
    
    @staticmethod
    def deserialize_short(stream : Stream) -> int:
        buf = Utils.newArrayOfBytes(2, 0)
        stream.read(buf, 0, 2)
        return int.from_bytes(buf[0:0+2], byteorder="little")
    
    @staticmethod
    def serialize_string(stream : Stream, val : str, deflate : bool=False) -> None:
        from pullenti.util.ArchiveHelper import ArchiveHelper
        if (val is None): 
            MiscHelper.serialize_int(stream, -1)
            return
        if (Utils.isNullOrEmpty(val)): 
            MiscHelper.serialize_int(stream, 0)
            return
        data = MiscHelper.encode_string_utf8(val, False)
        if (deflate): 
            data = ArchiveHelper.compress_gzip(data)
        MiscHelper.serialize_int(stream, len(data))
        stream.write(data, 0, len(data))
    
    @staticmethod
    def deserialize_string(stream : Stream, deflate : bool=False) -> str:
        from pullenti.util.ArchiveHelper import ArchiveHelper
        len0_ = MiscHelper.deserialize_int(stream)
        if (len0_ < 0): 
            return None
        if (len0_ == 0): 
            return ""
        data = Utils.newArrayOfBytes(len0_, 0)
        stream.read(data, 0, len(data))
        if (deflate): 
            data = ArchiveHelper.decompress_gzip(data)
        return MiscHelper.decode_string_utf8(data, 0, -1)
    
    @staticmethod
    def read_stream(s : Stream) -> bytearray:
        """ Прочитать байтовый массив из потока
        
        Args:
            s(Stream): поток
        
        Returns:
            bytearray: результат
        """
        if (s.seekable): 
            if (s.length > (0)): 
                res = Utils.newArrayOfBytes(s.length, 0)
                s.read(res, 0, len(res))
                return res
        buf = Utils.newArrayOfBytes(10000, 0)
        mem = MemoryStream()
        k = 0
        while True:
            i = s.read(buf, 0, len(buf))
            if (i < 0): 
                break
            if (i == 0): 
                k += 1
                if (k > 3): 
                    break
                continue
            mem.write(buf, 0, i)
            k = 0
        arr = mem.toarray()
        mem.close()
        return arr
    
    @staticmethod
    def ends_with(str0_ : str, substr : str) -> bool:
        # Замена стандартной функции, которая очень тормозит
        if (str0_ is None or substr is None): 
            return False
        i = len(str0_) - 1
        j = len(substr) - 1
        if (j > i or (j < 0)): 
            return False
        while j >= 0: 
            if (str0_[i] != substr[j]): 
                return False
            j -= 1; i -= 1
        return True
    
    @staticmethod
    def ends_with_ex(str0_ : str, substr : str, substr2 : str, substr3 : str=None) -> bool:
        if (str0_ is None): 
            return False
        for k in range(3):
            if (k == 1): 
                substr = substr2
            elif (k == 2): 
                substr = substr3
            if (substr is None): 
                continue
            i = len(str0_) - 1
            j = len(substr) - 1
            if (j > i or (j < 0)): 
                continue
            while j >= 0: 
                if (str0_[i] != substr[j]): 
                    break
                j -= 1; i -= 1
            if (j < 0): 
                return True
        return False
    
    @staticmethod
    def encode_string_ascii(str0_ : str) -> bytearray:
        """ Закодировать строку кодировкой ASCII. Работает на всех платформах.
        
        Args:
            str0_(str): строка
        
        Returns:
            bytearray: результат
        """
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_), 0)
        j = 0
        while j < len(str0_): 
            i = ord(str0_[j])
            if (i < 0x100): 
                res[j] = (i)
            else: 
                res[j] = (ord('?'))
            j += 1
        return res
    
    @staticmethod
    def encode_string1251(str0_ : str) -> bytearray:
        """ Закодировать строку кодировкой windows-1251. Работает на всех платформах.
        
        Args:
            str0_(str): строка
        
        Returns:
            bytearray: результат
        """
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_), 0)
        j = 0
        while j < len(str0_): 
            i = ord(str0_[j])
            if (i < 0x80): 
                res[j] = (i)
            else: 
                b = 0
                wrapb601 = RefOutArgWrapper(0)
                inoutres602 = Utils.tryGetValue(MiscHelper.__m_utf_1251, i, wrapb601)
                b = wrapb601.value
                if (inoutres602): 
                    res[j] = b
                else: 
                    res[j] = (ord('?'))
            j += 1
        return res
    
    @staticmethod
    def encode_string1252(str0_ : str) -> bytearray:
        """ Закодировать строку кодировкой windows-1252. Работает на всех платформах.
        
        Args:
            str0_(str): строка
        
        Returns:
            bytearray: результат
        """
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_), 0)
        j = 0
        while j < len(str0_): 
            i = ord(str0_[j])
            if ((i < 0x80) or i >= 0xA0): 
                res[j] = (i)
            else: 
                b = 0
                wrapb603 = RefOutArgWrapper(0)
                inoutres604 = Utils.tryGetValue(MiscHelper.__m_utf_1252, i, wrapb603)
                b = wrapb603.value
                if (inoutres604): 
                    res[j] = b
                else: 
                    res[j] = (ord('?'))
            j += 1
        return res
    
    @staticmethod
    def decode_string_ascii(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Декодировать строку из массива в кодировке Ascii. Работает на всех платформах.
        
        Args:
            dat(bytearray): байтовый масств
            pos(int): начальная позиция в массиве
            len0_(int): длина байт
        
        Returns:
            str: строка с результатом
        """
        if (dat is None): 
            return None
        if (len(dat) == 0): 
            return ""
        if (len0_ < 0): 
            len0_ = (len(dat) - pos)
        tmp = io.StringIO()
        j = pos
        while (j < (pos + len0_)) and (j < len(dat)): 
            i = dat[j]
            if (i < 0x100): 
                print(chr(i), end="", file=tmp)
            else: 
                print('?', end="", file=tmp)
            j += 1
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def decode_string1251(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Декодировать строку из массива в кодировке windows-1251. Работает на всех платформах.
        
        Args:
            dat(bytearray): байтовый масств
            pos(int): начальная позиция в массиве
            len0_(int): длина байт
        
        Returns:
            str: строка с результатом
        """
        if (dat is None): 
            return None
        if (len(dat) == 0): 
            return ""
        if (len0_ < 0): 
            len0_ = (len(dat) - pos)
        tmp = io.StringIO()
        j = pos
        while (j < (pos + len0_)) and (j < len(dat)): 
            i = dat[j]
            if (i < 0x80): 
                print(chr(i), end="", file=tmp)
            elif (MiscHelper._m_1251_utf[i] == 0): 
                print('?', end="", file=tmp)
            else: 
                print(chr(MiscHelper._m_1251_utf[i]), end="", file=tmp)
            j += 1
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def decode_string1252(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Декодировать строку из массива в кодировке windows-1252. Работает на всех платформах.
        
        Args:
            dat(bytearray): байтовый масств
            pos(int): начальная позиция в массиве
            len0_(int): длина байт
        
        Returns:
            str: строка с результатом
        """
        if (dat is None): 
            return None
        if (len(dat) == 0): 
            return ""
        if (len0_ < 0): 
            len0_ = (len(dat) - pos)
        tmp = io.StringIO()
        j = pos
        while (j < (pos + len0_)) and (j < len(dat)): 
            i = dat[j]
            if ((i < 0x80) or i >= 0xA0): 
                print(chr(i), end="", file=tmp)
            elif (MiscHelper._m_1252_utf[i] == 0): 
                print('?', end="", file=tmp)
            else: 
                print(chr(MiscHelper._m_1252_utf[i]), end="", file=tmp)
            j += 1
        return Utils.toStringStringIO(tmp)
    
    _m_1251_utf = None
    
    _m_1252_utf = None
    
    __m_utf_1251 = None
    
    __m_utf_1252 = None
    
    @staticmethod
    def encode_string_utf8(str0_ : str, add_preambl : bool=False) -> bytearray:
        """ Закодировать строку в коде UTF-8 с добавлением преамбулы
        
        Args:
            str0_(str): кодируемая строка
            add_preambl(bool): добавлять ли преамбулу EF BB BF
        
        Returns:
            bytearray: результирующий массив
        """
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        res = str0_.encode("UTF-8", 'ignore')
        if (not add_preambl): 
            return res
        tmp = bytearray()
        tmp.extend(Utils.preambleCharset("UTF-8"))
        tmp.extend(res)
        return bytearray(tmp)
    
    @staticmethod
    def decode_string_utf8(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Декодировать строку из UTF-8. Если есть преамбула, то она проигнорируется.
        
        Args:
            dat(bytearray): массив с закодированной строкой
        
        Returns:
            str: раскодированная строка
        """
        if (dat is None): 
            return None
        if (len0_ < 0): 
            len0_ = len(dat)
        if ((len0_ > 3 and dat[pos] == (0xEF) and dat[pos + 1] == (0xBB)) and dat[pos + 2] == (0xBF)): 
            pos += 3
            len0_ -= 3
        return dat[pos:pos+len0_].decode("UTF-8", 'ignore')
    
    @staticmethod
    def encode_string_unicode(str0_ : str) -> bytearray:
        """ Закодировать строку в 2-х байтовой кодировке Unicode, младший байт первый (UTF-16LE).
        
        Args:
            str0_(str): кодируемая строка
        
        Returns:
            bytearray: результирующий массив
        """
        if (Utils.isNullOrEmpty(str0_)): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_) * 2, 0)
        i = 0
        while i < len(str0_): 
            cod = ord(str0_[i])
            res[i * 2] = ((cod & 0xFF))
            res[(i * 2) + 1] = ((cod >> 8))
            i += 1
        return res
    
    @staticmethod
    def decode_string_unicode(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Декодировать строку из 2-х байтовой кодировки Unicode, младший байт первый (UTF-16LE).
        
        Args:
            dat(bytearray): массив с закодированной строкой
        
        Returns:
            str: раскодированная строка
        """
        if (dat is None): 
            return None
        if (len0_ < 0): 
            len0_ = len(dat)
        res = io.StringIO()
        i = pos
        while i < (pos + len0_): 
            cod = dat[i + 1]
            cod <<= 8
            cod |= (dat[i])
            print(chr(cod), end="", file=res)
            i += 2
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def encode_string_unicodebe(str0_ : str) -> bytearray:
        """ Закодировать строку в 2-х байтовой кодировке Unicode, старший байт первый (UTF-16BE).
        
        Args:
            str0_(str): кодируемая строка
        
        Returns:
            bytearray: результирующий массив
        """
        if (Utils.isNullOrEmpty(str0_)): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_) * 2, 0)
        i = 0
        while i < len(str0_): 
            cod = ord(str0_[i])
            res[(i * 2) + 1] = ((cod & 0xFF))
            res[i * 2] = ((cod >> 8))
            i += 1
        return res
    
    @staticmethod
    def decode_string_unicodebe(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        """ Декодировать строку из 2-х байтовой кодировки Unicode, старший байт первый (UTF-16BE).
        
        Args:
            dat(bytearray): массив с закодированной строкой
        
        Returns:
            str: раскодированная строка
        """
        if (dat is None): 
            return None
        if (len0_ < 0): 
            len0_ = len(dat)
        res = io.StringIO()
        i = pos
        while i < (pos + len0_): 
            cod = dat[i]
            cod <<= 8
            cod |= (dat[i + 1])
            print(chr(cod), end="", file=res)
            i += 2
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def correct_csv_value(txt : str, surround_brackets : bool=False) -> str:
        if (txt is None): 
            return None
        sur = False
        if (txt.find('"') >= 0): 
            txt = txt.replace("\"", "\"\"")
            sur = True
        if (surround_brackets and txt.find(';') >= 0): 
            sur = True
        if (surround_brackets and sur): 
            return "\"{0}\"".format(txt)
        else: 
            return txt
    
    @staticmethod
    def correct_json_value(txt : str) -> str:
        res = io.StringIO()
        if (txt is not None): 
            for ch in txt: 
                if (ch == '"'): 
                    print("\\\"", end="", file=res)
                elif (ch == '\\'): 
                    print("\\\\", end="", file=res)
                elif (ch == '/'): 
                    print("\\/", end="", file=res)
                elif ((ord(ch)) == 0xD): 
                    print("\\r", end="", file=res)
                elif ((ord(ch)) == 0xA): 
                    print("\\n", end="", file=res)
                elif (ch == '\t'): 
                    print("\\t", end="", file=res)
                elif ((ord(ch)) < 0x20): 
                    print(' ', end="", file=res)
                else: 
                    print(ch, end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def correct_xml_file(res : io.StringIO) -> None:
        i = Utils.toStringStringIO(res).find('>')
        if (i > 10 and Utils.getCharAtStringIO(res, 1) == '?'): 
            Utils.removeStringIO(res, 0, i + 1)
        i = 0
        first_pass727 = True
        while True:
            if first_pass727: first_pass727 = False
            else: i += 1
            if (not (i < res.tell())): break
            ch = Utils.getCharAtStringIO(res, i)
            cod = ord(ch)
            if ((cod < 0x80) and cod >= 0x20): 
                continue
            if (cod >= 0x400 or (cod < 0x500)): 
                continue
            Utils.removeStringIO(res, i, 1)
            Utils.insertStringIO(res, i, "&#x{0};".format("{:04X}".format(cod)))
    
    @staticmethod
    def serialize_to_bin(obj : 'IXmlReadWriteSupport') -> bytearray:
        """ Сериализация объекта, реализующего IXmlReadWriteSupport, в байтовый массив.
        Работает одинаково на всех языках программирования.
        
        Args:
            obj(IXmlReadWriteSupport): объект
        
        Returns:
            bytearray: результат
        """
        from pullenti.util.ArchiveHelper import ArchiveHelper
        if (obj is None): 
            return None
        res = io.StringIO()
        with XmlWriter.create_string(res, None) as xml0_: 
            obj.write_to_xml(xml0_, None)
        MiscHelper.correct_xml_file(res)
        dat = MiscHelper.encode_string_utf8(Utils.toStringStringIO(res), False)
        return ArchiveHelper.compress_gzip(dat)
    
    @staticmethod
    def deserialize_from_bin(dat : bytearray, obj : 'IXmlReadWriteSupport') -> None:
        """ Десериализация из байтового массива
        
        Args:
            dat(bytearray): массив, полученный функцией SerializeToBin
            obj(IXmlReadWriteSupport): экземпляр десериализуемого объекта
        """
        from pullenti.util.ArchiveHelper import ArchiveHelper
        if (dat is None): 
            return
        data = ArchiveHelper.decompress_gzip(dat)
        str0_ = MiscHelper.decode_string_utf8(data, 0, -1)
        xml0_ = None # new XmlDocument
        xml0_ = Utils.parseXmlFromString(str0_)
        obj.read_from_xml(xml0_.getroot())
    
    @staticmethod
    def serialize_to_bin_list(objs : typing.List['IXmlReadWriteSupport']) -> bytearray:
        from pullenti.util.ArchiveHelper import ArchiveHelper
        res = io.StringIO()
        with XmlWriter.create_string(res, None) as xml0_: 
            xml0_.write_start_element("LIST")
            if (objs is not None): 
                for obj in objs: 
                    obj.write_to_xml(xml0_, None)
            xml0_.write_end_element()
        MiscHelper.correct_xml_file(res)
        dat = MiscHelper.encode_string_utf8(Utils.toStringStringIO(res), False)
        return ArchiveHelper.compress_gzip(dat)
    
    @staticmethod
    def deserialize_from_bin_list(dat : bytearray, res : typing.List['IXmlReadWriteSupport']) -> int:
        from pullenti.util.ArchiveHelper import ArchiveHelper
        if (dat is None): 
            return 0
        data = ArchiveHelper.decompress_gzip(dat)
        str0_ = MiscHelper.decode_string_utf8(data, 0, -1)
        xml0_ = None # new XmlDocument
        xml0_ = Utils.parseXmlFromString(str0_)
        i = 0
        for x in xml0_.getroot(): 
            if (res is not None): 
                if (i >= len(res)): 
                    break
                res[i].read_from_xml(x)
            i += 1
        return i
    
    @staticmethod
    def correct_xml_value(txt : str) -> str:
        """ При сохранении значений в XML рекомендуется пропускать через эту функцию.
        Иначе если в строке окажутся некоторые символы (например, 0xC), то XML получается некорректным.
        
        Args:
            txt(str): исходный текст узла или атрибута
        
        Returns:
            str: откорректированный
        """
        if (txt is None): 
            return ""
        corr = False
        i = 0
        while i < len(txt): 
            cod = ord(txt[i])
            if (((cod < 0x20) and cod != 0xD and cod != 0xA) and cod != 9): 
                corr = True
                break
            elif (cod >= 0xD800 and cod <= 0xDBFF): 
                if ((i + 1) >= len(txt)): 
                    corr = True
                    break
                i += 1
                cod = (ord(txt[i]))
                if ((cod < 0xDC00) or cod > 0xDFFF): 
                    corr = True
                    break
            elif (cod >= 0xDC00 and cod <= 0xDFFF): 
                corr = True
                break
            i += 1
        if (not corr): 
            return txt
        tmp = Utils.newStringIO(txt)
        i = 0
        while i < tmp.tell(): 
            ch = Utils.getCharAtStringIO(tmp, i)
            if ((((ord(ch)) < 0x20) and ch != '\r' and ch != '\n') and ch != '\t'): 
                Utils.setCharAtStringIO(tmp, i, ' ')
            elif ((ord(ch)) >= 0xD800 and (ord(ch)) <= 0xDBFF): 
                if ((i + 1) >= tmp.tell()): 
                    Utils.setCharAtStringIO(tmp, i, ' ')
                    break
                ch1 = Utils.getCharAtStringIO(tmp, i + 1)
                if ((ord(ch1)) >= 0xDC00 and (ord(ch1)) <= 0xDFFF): 
                    i += 1
                else: 
                    Utils.setCharAtStringIO(tmp, i, ' ')
            elif ((ord(ch)) >= 0xDC00 and (ord(ch)) <= 0xDFFF): 
                Utils.setCharAtStringIO(tmp, i, '?')
            i += 1
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def correct_html_char(res : io.StringIO, c : 'char') -> None:
        if ((((ord(c)) < 0x20) and c != '\r' and c != '\n') and c != '\t'): 
            print(' ', end="", file=res)
        elif ((ord(c)) > 0xF000): 
            print("&#{0};".format(ord(c)), end="", file=res, flush=True)
        elif ((ord(c)) == 0xA or (ord(c)) == 0xD): 
            print("\r\n<br/>", end="", file=res)
        elif (c == (chr(0xA0))): 
            print("&nbsp;", end="", file=res)
        elif (c == '<'): 
            print("&lt;", end="", file=res)
        elif (c == '>'): 
            print("&gt;", end="", file=res)
        elif (c == '&'): 
            print("&amp;", end="", file=res)
        else: 
            print(c, end="", file=res)
    
    @staticmethod
    def correct_html_value(res : io.StringIO, txt : str, is_attr : bool=False, is_pure_xml : bool=False) -> None:
        if (txt is None): 
            return
        i = 0
        while i < len(txt): 
            c = txt[i]
            if ((((ord(c)) < 0x20) and c != '\r' and c != '\n') and c != '\t'): 
                print(' ', end="", file=res)
            elif ((ord(c)) > 0xF000): 
                print("&#{0};".format(ord(c)), end="", file=res, flush=True)
            elif ((ord(c)) == 0xA or (ord(c)) == 0xD): 
                if (i > 0 and (ord(txt[i - 1])) == 0xD): 
                    pass
                elif (is_attr or is_pure_xml): 
                    print("\r\n", end="", file=res)
                else: 
                    print("\r\n<br/>", end="", file=res)
            elif (c == (chr(0xA0))): 
                if (is_pure_xml): 
                    print("&#{0};".format(0xA0), end="", file=res, flush=True)
                else: 
                    print("&nbsp;", end="", file=res)
            elif (c == '<'): 
                print("&lt;", end="", file=res)
            elif (c == '>'): 
                print("&gt;", end="", file=res)
            elif (c == '&'): 
                print("&amp;", end="", file=res)
            elif (is_attr and c == '"'): 
                print("&quot;", end="", file=res)
            else: 
                print(c, end="", file=res)
            i += 1
    
    # static constructor for class MiscHelper
    @staticmethod
    def _static_ctor():
        MiscHelper._m_1251_utf = Utils.newArray(256, 0)
        MiscHelper.__m_utf_1251 = dict()
        for i in range(0x80):
            MiscHelper._m_1251_utf[i] = i
        m_1251_80_bf = [0x0402, 0x0403, 0x201A, 0x0453, 0x201E, 0x2026, 0x2020, 0x2021, 0x20AC, 0x2030, 0x0409, 0x2039, 0x040A, 0x040C, 0x040B, 0x040F, 0x0452, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014, 0x0000, 0x2122, 0x0459, 0x203A, 0x045A, 0x045C, 0x045B, 0x045F, 0x00A0, 0x040E, 0x045E, 0x0408, 0x00A4, 0x0490, 0x00A6, 0x00A7, 0x0401, 0x00A9, 0x0404, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x0407, 0x00B0, 0x00B1, 0x0406, 0x0456, 0x0491, 0x00B5, 0x00B6, 0x00B7, 0x0451, 0x2116, 0x0454, 0x00BB, 0x0458, 0x0405, 0x0455, 0x0457]
        for i in range(0x40):
            MiscHelper._m_1251_utf[i + 0x80] = m_1251_80_bf[i]
            MiscHelper.__m_utf_1251[m_1251_80_bf[i]] = (i + 0x80)
        for i in range(0x20):
            MiscHelper._m_1251_utf[i + 0xC0] = ((ord('А')) + i)
            MiscHelper.__m_utf_1251[(ord('А')) + i] = (i + 0xC0)
        for i in range(0x20):
            MiscHelper._m_1251_utf[i + 0xE0] = ((ord('а')) + i)
            MiscHelper.__m_utf_1251[(ord('а')) + i] = (i + 0xE0)
        m_1252_80_9f = [0x20AC, 0, 0x201A, 0x0192, 0x201E, 0x2026, 0x2020, 0x2021, 0x02C6, 0x2030, 0x0160, 0x2039, 0x0152, 0, 0x017D, 0, 0, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014, 0x02DC, 0x2122, 0x0161, 0x203A, 0x0153, 0, 0x017E, 0x0178]
        MiscHelper._m_1252_utf = Utils.newArray(256, 0)
        MiscHelper.__m_utf_1252 = dict()
        for i in range(0x100):
            MiscHelper._m_1252_utf[i] = i
        for i in range(0x20):
            if (m_1252_80_9f[i] != 0): 
                MiscHelper._m_1252_utf[i + 0x80] = m_1252_80_9f[i]
                MiscHelper.__m_utf_1252[m_1252_80_9f[i]] = (i + 0x80)

MiscHelper._static_ctor()