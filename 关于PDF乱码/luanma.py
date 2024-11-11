from pdf2docx import Converter
from pdf2docx import parse
pdf_file = '乱码.pdf'
docx_file = '乱码.docx'

# # convert pdf to docx
# cv = Converter(pdf_file)
# cv.convert(docx_file)      # all pages by default
# cv.close()
parse(pdf_file, docx_file)
