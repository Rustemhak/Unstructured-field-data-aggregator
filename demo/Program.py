# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import pathlib
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream
from pullenti.unisharp.Xml import XmlWriter
from pullenti.unisharp.Xml import XmlWriterSettings

from pullenti.unitext.GetHtmlParam import GetHtmlParam
from pullenti.unitext.UnitextService import UnitextService

class Program:
    # Демонстрация получения представления Unitext из файлов разных форматов, и генерация
    # из этого представления форматов Plaintext и Html.
    
    @staticmethod
    def main(args : typing.List[str]) -> None:
        print("Unitext SDK version {0} ({1})".format(UnitextService.VERSION, UnitextService.VERSION_DATE), flush=True)
        # Перебираем примеры файлов разных форматов из встроенных ресурсов.
        # Содержимое там примерно одинаковое, и результат будет примерно одинаковым.
        
        res_names = Utils.getResourcesNames('demo.acts', '.doc;.docx;.mht;.odt;.pdf;.rtf;.xlsx;.htm;.xml;.txt;.PDF')
        for resnam in res_names: 
            print("Resource {0}: ".format(resnam), end="", flush=True)
            content = [ ]
            # получаем байтовый поток ресурса
            with Utils.getResourceStream('demo.acts', resnam) as stream:
                content = Utils.newArrayOfBytes(stream.length, 0)
                stream.read(content, 0, len(content))
            print("{0} bytes ... ".format(len(content)), end="", flush=True)
            # извлекли байтовый поток из ресурса, обрабатываем его
            doc = UnitextService.create_document(None, content, None)
            if (doc.error_message is not None): 
                # скорее всего, этот формат не поддерживается на данный момент
                print(" error, sorry: {0} ".format(doc.error_message), flush=True)
                continue
            # восстанавливаем имя исходного файла, извлечённого из ресурсов
            doc.source_file_name = resnam
            for i in range(len(resnam) - 7, 0, -1):
                if (resnam[i] == '.'): 
                    doc.source_file_name = resnam[i + 1:]
                    break
            # записываем результат в XML
            with FileStream(doc.source_file_name + ".xml", "wb") as fs: 
                xml_params = XmlWriterSettings()
                xml_params.encoding = "UTF-8"
                xml_params.indent = True
                xml_params.indentChars = "  "
                with XmlWriter.create_stream(fs, xml_params) as xml0_: 
                    xml0_.write_start_document()
                    doc.get_xml(xml0_)
                    xml0_.write_end_document()
            # получаем плоский текст
            plain_text = doc.get_plaintext_string(None)
            if (plain_text is None): 
                plain_text = "Текст не выделен"
            pathlib.Path(doc.source_file_name + ".txt").write_bytes(plain_text.encode("UTF-8", 'ignore'))
            # получаем html
            html_params = GetHtmlParam()
            html_params.out_html_and_body_tags = True
            html = doc.get_html_string(html_params)
            pathlib.Path(doc.source_file_name + ".html").write_bytes(html.encode("UTF-8", 'ignore'))
            print(" format {0}, save xml & text & html".format(Utils.enumToString(doc.source_format)), flush=True)
        print("Bye!", flush=True)

if __name__ == "__main__":
    Program.main(None)
