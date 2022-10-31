"""
you can do it once and save at txt-fles
    1. convert-pdf-txt
    2. preprocess txt
3. create XML
4. sentenize txt
5. tag sentences in xml
6. tag new attribute
    - field
    - dates
    - location
    - objects
    - oil_deposit
7. XML to xlsx
"""

"""
pipeline for table kern
1. get pd.dataframe (use recognize_to_read_table in kern_table), ar 
2. take values (objects) from first column "Продуктивный горизонт, ярус"
3.  in xlsx table for these objects tick "Да", for other "Нет" 
"""
# with open("../reports/txt/Архангельское_месторождение_Пересчет_запасов_КГ.txt", "r", encoding="utf-8") as f:
#     text = f.read()
# print(text)
