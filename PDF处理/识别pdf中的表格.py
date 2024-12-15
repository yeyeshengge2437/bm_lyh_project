import pdfplumber
import pandas as pd
table_value = []
with pdfplumber.open("202408270927391c6f20457dcd45a8.pdf") as pdf:
    page = pdf.pages[0]  # 获取第一页

    table = page.extract_table()
    for row in table:
        # print(row)
        if row[0]:
            if row[0].isalnum():
                table_value.append(row)
                print(row)

table_df = pd.DataFrame(table_value)
table_df.to_excel('output.xlsx', index=False)