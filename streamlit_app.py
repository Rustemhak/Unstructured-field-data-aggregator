import streamlit as st
import pandas as pd
from download_streamlit import convert_df
from io import StringIO
import pdfplumber

from read_report.read_report import read_report


def extract_data(feed):
    data = []
    with pdfplumber.load(feed) as pdf:
        if len(pdf.pages):
            text = ' '.join([
                page.dedupe_chars().extract_text(y_tolerance=6) or '' for page in pdf.pages if page
            ])
            #pdf to xlsx


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    xlsx = extract_data(uploaded_file)
    st.download_button(
        label="Download data as xlsx",
        data=xlsx,
        file_name='report.xlsx',
        mime='text/xlsx',
    )
