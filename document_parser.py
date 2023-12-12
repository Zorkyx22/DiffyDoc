import docx
import re
import argparse

from docx import Document
from dataclasses import dataclass
from openai import OpenAI
from tqdm import tqdm
from argparse import ArgumentParser

from constants import (END_FILE_PREFIX, PROMPT, OPENAI_API_KEY)

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
            {"role":"system", "content":PROMPT},
            {"role":"system", "content":message_chunk}
        ]
    )
    return translation.choices[0].message.content

def translate_docx(filename, output_filename=None):
    initial_doc = Document(filename)
    if (output_filename is None):
        output_filename = f"{END_FILE_PREFIX}{filename}"
    initial_doc.save(output_filename)
    translating_doc = Document(output_filename)

    pbar = tqdm(desc="Working...", total=len(initial_doc.paragraphs))
    for i, (paragraph, translated_paragraph) in enumerate(zip(initial_doc.paragraphs, translating_doc.paragraphs)):
        pbar.update()
        if(paragraph.text != "" and len(paragraph.runs) > 0):
            all_runs = paragraph.runs
            current_style = create_style(all_runs[0])
            current_run_nb = 0
            runs_to_save = [0]
            for i in range(1, len(all_runs)):
                temp_style = create_style(all_runs[i])
                if (current_style==temp_style):
                    current_run_nb+=1
                    all_runs[runs_to_save[-1]].text += all_runs[i].text
                else:
                    current_style=temp_style
                    runs_to_save.append(i)
                    current_run_nb = 0

            translated_paragraph.clear()
            for run_number in runs_to_save:
                p_text = translate_chunk(all_runs[run_number].text) + " "
                p_style = all_runs[run_number].style
                translated_paragraph.add_run(text=p_text, style=p_style)
    pbar.close()
    print(f"Done! Saving to {output_filename}...")
    translating_doc.save(output_filename)

parser = ArgumentParser(description="A script utility that makes use of OpenAI'current_style GPT to translate docx documents without compromising it'current_style styling.")
parser.add_argument("file", action="store", help="The docx file you wish to translate")
parser.add_argument("-o", "--output", action="store", help=f"The output file. Default = ./{END_FILE_PREFIX}yourfile")
if __name__=="__main__":
    args = parser.parse_args()
    client = OpenAI(api_key=OPENAI_API_KEY)
    translate_docx(args.file, args.output)
