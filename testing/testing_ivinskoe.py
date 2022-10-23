from pipeline_for_testing import convert_chapter_pdf_to_xml


if __name__ == '__main__':
    path = 'D:/For_Python/Unstructured-field-data-aggregator/reports/pdfs/Ивинское, книга 1.pdf'
    convert_chapter_pdf_to_xml(path, 1, 459, 1)
