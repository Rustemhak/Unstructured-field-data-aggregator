import streamlit as st
import pandas as pd
from download_streamlit import convert_df

d = {'col1': [1, 2], 'col2': [3, 4]}
my_large_df = pd.DataFrame(data=d)
csv = convert_df(my_large_df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)
