import streamlit as st
import pandas as pd
from download_streamlit import convert_df
from io import StringIO
import pdfplumber

# from read_report.read_report import read_report
from testing.pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx


# from get_result.main import get_result


def extract_data(feed):
    text = ''
    with pdfplumber.open(feed) as pdf:
        if len(pdf.pages):
            text = ' '.join([
                page.dedupe_chars().extract_text(y_tolerance=6) or '' for page in pdf.pages if page
            ])
    f = open('reports/test/test.txt', 'w')
    f.write(text)
    field_name = 'test'
    convert_chapter_pdf_to_xml(path_txt='reports/test/test.txt', path_xml=field_name)
    chap_id = 1
    path_to_xml_dir = f"reports//xml//{field_name}"
    path_xml = f"{path_to_xml_dir}//chapter{chap_id}.xml"
    result_csv = report_xml_to_xlsx([path_xml], 'test', on_csv=True)
    xlsx_path = f"reports//xlsx//{field_name}.xlsx"
    return xlsx_path


#             # pdf to xlsx


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # xlsx = get_result(uploaded_file)
    xlsx_path = extract_data(uploaded_file)
    # st.write(csv)
    # print(csv)
    with open(xlsx_path, "rb") as file:
        st.download_button(
            label="Download data as xlsx",
            data=file,
            file_name='report.xlsx',
            mime='text/xlsx',
        )
