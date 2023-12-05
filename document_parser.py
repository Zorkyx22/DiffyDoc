from docx import Document
from docx.enum.style import WD_STYLE_TYPE
import re

APPEND = "translated_"
filename = "test.docx"
initial_doc = Document(f"{filename}")
styles = initial_doc.styles
initial_doc.save(f"{APPEND}{filename}")
translating_doc = Document(f"{APPEND}{filename}")
for i, paragraph in enumerate(translating_doc.paragraphs):
    if(paragraph.text != ""):
        all_runs = paragraph.runs
        for i in range(len(all_runs)):
            #if len(all_runs[i].text) > 1 and (" " in all_runs[i].text or not bool(re.search(r'\d', all_runs[i].text))):
            all_runs[i].text = all_runs[i].text+"_"
translating_doc.save(f"{APPEND}{filename}")