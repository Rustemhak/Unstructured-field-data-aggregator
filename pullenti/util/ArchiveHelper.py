# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import gzip
import zlib
import typing
import pathlib
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.FileFormat import FileFormat
from pullenti.util.FileInArchive import FileInArchive
from pullenti.util.FileFormatsHelper import FileFormatsHelper
from pullenti.unitext.internal.zip.ZipFile import ZipFile
from pullenti.unitext.UnitextService import UnitextService
from pullenti.unitext.internal.misc.MyZipFile import MyZipFile

class ArchiveHelper:
    """ Работа с архивами и сжатием """
    
    @staticmethod
    def compress_gzip(dat : bytearray) -> bytearray:
        """ Заархивировать массив байт алгоритмом GZip
        
        Args:
            dat(bytearray): исходный массив
        
        Returns:
            bytearray: заархивированый массив
        """
        with MemoryStream() as res: 
            with MemoryStream(dat) as input0_: 
                input0_.position = 0
                with Stream(gzip.GzipFile(fileobj=res.getstream(), mode='w')) as deflate: 
                    input0_.writeto(deflate)
                    deflate.flush()
                    deflate.close()
            return res.toarray()
    
    @staticmethod
    def decompress_gzip(zip0_ : bytearray) -> bytearray:
        """ Разархивировать байтовый массив алгоритмом GZip
        
        Args:
            zip0_(bytearray): архивированный массив
        
        Returns:
            bytearray: результат
        """
        with MemoryStream(zip0_) as data: 
            data.position = 0
            with MemoryStream() as unzip: 
                buf = Utils.newArrayOfBytes(len(zip0_) + len(zip0_), 0)
                with Stream(gzip.GzipFile(fileobj=data.getstream(), mode='r')) as deflate: 
                    while True:
                        i = -1
                        try: 
                            ii = 0
                            while ii < len(buf): 
                                buf[ii] = (0)
                                ii += 1
                            i = deflate.read(buf, 0, len(buf))
                        except Exception as ex: 
                            for i in range(len(buf) - 1, -1, -1):
                                if (buf[i] != (0)): 
                                    unzip.write(buf, 0, i + 1)
                                    break
                            else: i = -1
                            break
                        if (i < 1): 
                            break
                        unzip.write(buf, 0, i)
                res = unzip.toarray()
                return res
    
    @staticmethod
    def compress_zlib(dat : bytearray) -> bytearray:
        """ Заархивировать байтовый массив алгоритмом Zlib
        
        Args:
            dat(bytearray): исходный массив
        
        Returns:
            bytearray: заархивированый массив
        """
        return zlib.compress(dat)
    
    @staticmethod
    def decompress_zlib(zip0_ : bytearray) -> bytearray:
        """ Разархивировать байтовый массив алгоритмом Zlib.
        
        Args:
            zip0_(bytearray): архивированный массив
        
        Returns:
            bytearray: результат
        """
        if (zip0_ is None or (len(zip0_) < 4)): 
            return None
        return zlib.decompress(zip0_)
    
    @staticmethod
    def compress_deflate(dat : bytearray) -> bytearray:
        """ Заархивировать байтовый массив алгоритмом Deflate (без Zlib-заголовка)
        
        Args:
            dat(bytearray): исходный массив
        
        Returns:
            bytearray: заархивированый массив
        """
        zip0_ = None
        zip0_ = zlib.compress(dat, -15)
        return zip0_
    
    @staticmethod
    def decompress_deflate(zip0_ : bytearray) -> bytearray:
        """ Разархивировать байтовый массив алгоритмом Deflate (без Zlib-заголовка)
        
        Args:
            zip0_(bytearray): архивированный массив
        
        Returns:
            bytearray: результат
        """
        if (zip0_ is None or (len(zip0_) < 1)): 
            return None
        return zlib.decompress(zip0_, -15)
    
    @staticmethod
    def create_zip_stream(res : Stream, files : typing.List['FileInArchive']) -> None:
        """ Создать zip в потоке
        
        Args:
            res(Stream): результирующий поток
            files(typing.List[FileInArchive]): файлы для архивирования
        """
        streams = list()
        try: 
            with ZipFile.create_stream(res) as zip0_: 
                zip0_.begin_update0()
                for f in files: 
                    mem = MemoryStream(f.content)
                    zip0_.add_stream(mem, f.key)
                    streams.append(mem)
                zip0_.commit_update()
        except Exception as ex: 
            raise Utils.newException("ZIP Error: " + str(ex), ex)
        for m in streams: 
            m.close()
    
    @staticmethod
    def create_zip_file(res_name : str, files : typing.List[str]) -> None:
        """ Создать zip-файл
        
        Args:
            res_name(str): результирующее имя архивного файла
            files(typing.List[str]): файлы для архивирования
        """
        try: 
            with ZipFile.create_file(res_name) as zip0_: 
                zip0_.begin_update0()
                for f in files: 
                    zip0_.add(f, pathlib.PurePath(f).name)
                zip0_.commit_update()
        except Exception as ex: 
            raise Utils.newException("ZIP Error: " + str(ex), ex)
    
    @staticmethod
    def unzip_files(zip_file : str, out_dir : str) -> typing.List[str]:
        """ Разархивировать файлы из ZIP-архива
        
        Args:
            zip_file(str): имя архива
            out_dir(str): результирующая директория
        
        Returns:
            typing.List[str]: список полных имён разархивированных файлов
        """
        files = list()
        with MyZipFile(zip_file, None) as zip0_: 
            for e0_ in zip0_.entries: 
                if (e0_.is_directory or e0_.encrypted or e0_.uncompress_data_size == 0): 
                    continue
                dat = e0_.get_data()
                if (dat is None): 
                    continue
                fname = pathlib.PurePath(out_dir).joinpath(pathlib.PurePath(e0_.name).name)
                files.append(fname)
                pathlib.Path(fname).write_bytes(dat)
        return files
    
    @staticmethod
    def get_file_names_from_archive(file_name : str, content : bytearray=None) -> typing.List[tuple]:
        """ Получить список файлов, содержащихся в архиве (архив может быть ZIP, RAR, TAR и некоторые другие)
        
        Args:
            file_name(str): имя архива
            content(bytearray): содержимое файла (если null, то fileName - ссылка на локальный файл)
        
        Returns:
            typing.List[tuple]: список файлов в виде словаря {имя файла, размер файла} или null, если не поддержано
        """
        frm = FileFormatsHelper.analize_file_format(file_name, content)
        res = dict()
        if (frm == FileFormat.ZIP or frm == FileFormat.DOCX): 
            with MyZipFile(file_name, content) as zip0_: 
                for e0_ in zip0_.entries: 
                    if (e0_.is_directory or e0_.encrypted or e0_.uncompress_data_size == 0): 
                        continue
                    if (not e0_.name in res): 
                        res[e0_.name] = e0_.compress_data_size
            return res
        try: 
            if (UnitextService.EXTENSION is not None): 
                return UnitextService.EXTENSION.get_file_names_from_archive(file_name, content)
        except Exception as ex: 
            pass
        return None
    
    @staticmethod
    def get_files_from_archive(file_name : str, content : bytearray=None) -> typing.List['FileInArchive']:
        """ Разархивировать файл архива (архив может быть ZIP, RAR, TAR и некоторые другие).
        Сами файлы на диск не записываются - всё в памяти.
        
        Args:
            file_name(str): имя архива
            content(bytearray): содержимое файла (если null, то fileName - ссылка на локальный файл)
        
        Returns:
            typing.List[FileInArchive]: список файлов FileInArchive или null, если не поддержано
        """
        frm = FileFormatsHelper.analize_file_format(file_name, content)
        res = list()
        if (frm == FileFormat.ZIP or frm == FileFormat.DOCX): 
            with MyZipFile(file_name, content) as zip0_: 
                for e0_ in zip0_.entries: 
                    if (e0_.is_directory or e0_.encrypted or e0_.uncompress_data_size == 0): 
                        continue
                    dat = e0_.get_data()
                    res.append(FileInArchive._new589(e0_.name, dat))
            return res
        try: 
            if (UnitextService.EXTENSION is not None): 
                return UnitextService.EXTENSION.get_files_from_archive(file_name, content)
        except Exception as ex: 
            pass
        return None
    
    @staticmethod
    def get_file_from_archive(file_name : str, content : bytearray, internal_name : str) -> bytearray:
        """ Извлечь файл из архива (архив может быть ZIP, RAR, TAR и некоторые другие)
        
        Args:
            file_name(str): имя архива
            content(bytearray): содержимое файла (если null, то fileName - ссылка на локальный файл)
            internal_name(str): внутреннее имя (то, которое возвращалось функцией GetFileNamesFromArchive)
        
        Returns:
            bytearray: разархивированный байтовый поток
        """
        frm = FileFormatsHelper.analize_file_format(file_name, content)
        if (frm == FileFormat.ZIP or frm == FileFormat.DOCX): 
            with MyZipFile(file_name, content) as zip0_: 
                for e0_ in zip0_.entries: 
                    if (e0_.is_directory or e0_.encrypted or e0_.uncompress_data_size == 0): 
                        continue
                    if (e0_.name != internal_name): 
                        continue
                    return e0_.get_data()
        try: 
            if (UnitextService.EXTENSION is not None): 
                return UnitextService.EXTENSION.get_file_from_archive(file_name, content, internal_name)
        except Exception as ex: 
            pass
        return None