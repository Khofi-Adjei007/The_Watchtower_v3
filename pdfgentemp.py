from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Table, Spacer, Paragraph, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

padding = dict(leftPadding=50, rightPadding=50, topPadding=50, bottomPadding=1.2*inch)
page_frame = Frame(0,0, *A4, **padding)

def page_footer(canvas, doc, pagesize=A4):
    page_num = canvas.getPageNumber()
    canvas.drawRightString(pagesize[0]/2, 20, 'Page {}'.format(page_num))
    canvas.drawImage('staticfiles/admin/img/download.png', pagesize[0]-1.3*inch, 0.2*inch, width=0.8*inch, height=0.8*inch)

page_template = PageTemplate(id='page_temp_a4', frames=[page_frame], onPage=page_footer, pagesize=A4)
base_doc_template = BaseDocTemplate('report.pdf', PageTemplates=[page_template])

content = [Paragraph('Report')]
base_doc_template.build(content)