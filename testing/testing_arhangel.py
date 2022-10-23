from pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx


def in_archangel_field(horizon_name: str) -> bool:
    archangel_fields = ["шешминский горизонт",
                        "тульский горизонт",
                        "бобриковский горизонт",
                        "кыновско-пашийский горизонт",
                        "каширский горизонт",
                        "верейский горизонт",
                        "башкирский ярус",
                        "алексинский горизонт",
                        "турнейский ярус"]
    return horizon_name in archangel_fields


if __name__ == '__main__':
    path = '../reports/pdfs/Архангельское_месторождение_Пересчет_запасов_КГ.pdf'
    convert_chapter_pdf_to_xml(path, 1, 293, 0)
