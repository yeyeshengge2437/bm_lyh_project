import requests
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

pdf_urls = [
    "https://res.debtop.com/col/test/paper/202408/14/2024081416280568014a79f7ba4a3a.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/202408141628532cc6b28aef04456f.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/20240814162941200a14dfeb1d4a8f.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/202408141630387779174cca81411f.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/202408141631333784f9183fdc44b7.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/20240814163237419c3d7952774b1a.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/202408141633258e435f2bcecd4306.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/202408141634088175343e60c04f4a.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/202408141634583308530bf8af4bf8.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/2024081416353943f3076a9c174ada.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/2024081416362747a550cdd5a1414b.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/2024081416371847a99c9197cf4fc8.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/20240814163800d5d4b0bd087b444f.pdf",
    "https://res.debtop.com/col/test/paper/202408/14/2024081416393483b1c1577d5e449f.pdf"
]

# # 接下来，你可以使用这个列表来循环处理每个PDF文件
# for pdf_url in pdf_urls:
#     response = requests.get(pdf_url)
#
#     # 检查请求是否成功
#     if response.status_code == 200:
#         # 将PDF内容写入文件
#         with open('downloaded_pdf.pdf', 'wb') as f:
#             f.write(response.content)

import ocrmypdf

# 要转换的输入 PDF 文件和输出 PDF 文件的路径
input_file = 'downloaded_pdf.pdf'
output_file = 'output_pdf_file.pdf'

# 使用 ocrmypdf 转换 PDF
ocrmypdf.ocr(input_file, output_file, language='eng', output_type='pdf')

# 上面的代码会生成一个新的 PDF 文件，其中包含从扫描图像中识别的文本




