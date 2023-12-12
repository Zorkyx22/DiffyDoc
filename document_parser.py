import os
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
import docx
import re
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
prompt = """
Please create the litteral translation of the following french text to english.
Translations have to be formal.
Your response should only contain the translation.
Example : 
user : 'Je suis une personne créative et enjouée qui adore l'escalade. Ma mère était'
assistant : 'I am a creative and happy person who loves rock climbing. My mother was'
"""

@dataclass
class RunStyle:
    bold: bool
    italic: bool
    underlined: bool
    size: docx.shared.Pt
    color: docx.shared.RGBColor
    font_name: str

def create_style(this_run):
    return RunStyle(this_run.bold, this_run.italic, this_run.underline, this_run.font.size, this_run.font.color.rgb, this_run.font.name)

def translate_chunk(message_chunk):
    translation = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role":"system", "content":prompt},
            {"role":"system", "content":message_chunk}
        ]
    )
    return translation.choices[0].message.content

def main():
    APPEND = "translated_"
    BACKUP = "backup_"
    filename = "test.docx"
    initial_doc = Document(f"{filename}")
    initial_doc.save(f"{APPEND}{filename}")
    translating_doc = Document(f"{APPEND}{filename}")


    for i, (paragraph, translated_paragraph) in tqdm(enumerate(zip(initial_doc.paragraphs, translating_doc.paragraphs))):
        if(paragraph.text != "" and len(paragraph.runs) > 0):
            all_runs = paragraph.runs
            s = create_style(all_runs[0])
            current_run_nb = 0
            runs_to_save = [0]
            for i in range(1, len(all_runs)):
                temp = create_style(all_runs[i])
                if (s==temp):
                    current_run_nb+=1
                    all_runs[runs_to_save[-1]].text += all_runs[i].text
                else:
                    s=temp
                    runs_to_save.append(i)
                    current_run_nb = 0
            translated_paragraph.clear()
            for run_number in runs_to_save:
                p_text = translate_chunk(all_runs[run_number].text)
                p_style = all_runs[run_number].style
                translated_paragraph.add_run(text=p_text, style=p_style)


    translating_doc.save(f"{APPEND}{filename}")
main()