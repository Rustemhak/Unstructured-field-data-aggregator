import xml.etree.ElementTree as ET


def create_report_xml():
    # создание тега "отчёт"
    report = ET.Element('report')
    # создание тега "главы"
    chapters = ET.SubElement(report, 'chapters')
    # создание тега "глава"
    chapter = ET.SubElement(chapters, 'chapter')
    chapter.set('ID', '0')
    # chapter.text = text
    ET.dump(report)
    return report
