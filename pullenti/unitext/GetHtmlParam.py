# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.GetHtmlParamFootnoteOutType import GetHtmlParamFootnoteOutType

class GetHtmlParam:
    """ Параметры генерации HTML функциями GetHtml и GetHtmlString
    Параметры генерации HTML
    """
    
    def __init__(self) -> None:
        self.styles = dict()
        self.use_inner_documents = True
        self.footnotes = GetHtmlParamFootnoteOutType.ENDOFUNIT
        self.out_comments_with_del_tags = False
        self.out_begin_end_chars = False
        self.out_styles = True
        self.hide_editions_and_comments = False
        self.hyperlinks_target_blank = False
        self.out_html_and_body_tags = False
        self.title = None;
        self.max_image_size = 10000000
        self.max_html_size = 20000000
        self.tag = None;
        self._m_footnotes = list()
        self._m_endnotes = list()
        self._m_footnotes_db = list()
        self.__m_in_footregime = False
    
    def call_before(self, it : 'UnitextItem', res : io.StringIO) -> bool:
        """ Вызывается в самом начале перед генерацией для элемента
        
        Args:
            it(UnitextItem): текущий элемент
            res(io.StringIO): для результата
        
        Returns:
            bool: если false, то сразу выход из функции - генерация для элемета не производится
        """
        return True
    
    def call_after(self, it : 'UnitextItem', res : io.StringIO) -> None:
        """ Вызывается в самом конце после генерации Html для элемента
        
        Args:
            it(UnitextItem): текущий элемент
            res(io.StringIO): для результата
        """
        pass
    
    def _out_endnotes(self, res : io.StringIO) -> None:
        if (self.__m_in_footregime): 
            return
        self.__m_in_footregime = True
        if (len(self._m_endnotes) > 0): 
            print("\r\n<hr/>", end="", file=res)
            print("\r\n<div style=\"border-left:2pt solid green;padding-left:5pt;margin-left:30pt;margin-top:10pt;margin-bottom:10pt;font-size:smaller;text-align:left;font-weight:normal\">".format(), end="", file=res, flush=True)
            i = 0
            while i < len(self._m_endnotes): 
                if (i > 0): 
                    print("<br/>", end="", file=res)
                print("\r\n<b id=\"{0}\"><sup>E{1}</sup></b>".format(Utils.ifNotNull(self._m_endnotes[i].id0_, ""), i + 1), end="", file=res, flush=True)
                if (self._m_endnotes[i].content is not None): 
                    self._m_endnotes[i].content.get_html(res, self)
                i += 1
            print("\r\n</div>", end="", file=res)
            self._m_endnotes.clear()
        self.__m_in_footregime = False
    
    def _out_footnotes(self, res : io.StringIO) -> None:
        # Не вызывать (это используется при специфических генерациях для вывода сносок)
        if (self.__m_in_footregime): 
            return
        self.__m_in_footregime = True
        if (len(self._m_footnotes) > 0): 
            print("\r\n<div style=\"border-left:2pt solid green;padding-left:5pt;border-left:2pt;margin-left:30pt;margin-top:10pt;margin-bottom:10pt;font-size:smaller;text-align:left;font-weight:normal\">".format(), end="", file=res, flush=True)
            i = 0
            while i < len(self._m_footnotes): 
                if (i > 0): 
                    print("<br/>", end="", file=res)
                tmp = io.StringIO()
                if (self._m_footnotes[i].content is not None): 
                    self._m_footnotes[i].content.get_html(tmp, self)
                sss = Utils.toStringStringIO(tmp)
                if (sss.startswith("<div")): 
                    j = sss.find('>')
                    Utils.insertStringIO(tmp, j + 1, "<b id=\"{0}\"><sup>{1}</sup></b>".format(Utils.ifNotNull(self._m_footnotes[i].id0_, ""), i + 1))
                    print("\r\n", end="", file=res)
                    print(Utils.toStringStringIO(tmp), end="", file=res)
                else: 
                    print("\r\n<b id=\"{0}\"><sup>{1}</sup></b>".format(Utils.ifNotNull(self._m_footnotes[i].id0_, ""), i + 1), end="", file=res, flush=True)
                    print(sss, end="", file=res)
                i += 1
            print("\r\n</div>", end="", file=res)
            self._m_footnotes.clear()
        if (len(self._m_footnotes_db) > 0): 
            if (len(self._m_footnotes_db) > 1): 
                pass
            print("\r\n<div style=\"border-left:2pt solid green;padding-left:5pt;margin-left:30pt;margin-top:10pt;margin-bottom:10pt;font-size:smaller;text-align:left;font-weight:normal\">".format(), end="", file=res, flush=True)
            i = 0
            while i < len(self._m_footnotes_db): 
                ff = self._m_footnotes_db[i]
                print("\r\n  <div id=\"{0}\">".format(Utils.ifNotNull(ff.id0_, "?")), end="", file=res, flush=True)
                if (ff.head is not None): 
                    ff.head.get_html(res, self)
                if (ff.body is not None): 
                    ff.body.get_html(res, self)
                print("</div>", end="", file=res)
                i += 1
            print("\r\n</div>", end="", file=res)
            self._m_footnotes_db.clear()
        self.__m_in_footregime = False