import re
import argparse
import docx

from datetime import datetime
from typing import List
from xml.etree.ElementTree import Element, tostring

from docx import Document
from docx.opc.part import Part
from docx.opc.constants import RELATIONSHIP_TYPE, CONTENT_TYPE
from docx.opc.oxml import parse_xml
from docx.opc.packuri import PackURI
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from dataclasses import dataclass
from openai import OpenAI
from langchain_ollama import OllamaLLM
from tqdm import tqdm
from argparse import ArgumentParser

from constants import (END_FILE_PREFIX, SYNTAX_PROMPT as PROMPT, OPENAI_API_KEY, AI_NAME, COMMENTS_PART_DEFAULT_XML_BYTES, DEFAULT_MODEL)


def add_comment_to_elements_in_place(docx_doc: Document, elements: List[Element], author: str, comment_text: str) -> None:
    if not elements:
        return
    try:
        comments_part = docx_doc.part.part_related_by(
            RELATIONSHIP_TYPE.COMMENTS
        )
    except KeyError:
        comments_part = Part(
            partname=PackURI("/word/comments.xml"),
            content_type=CONTENT_TYPE.WML_COMMENTS,
            blob=COMMENTS_PART_DEFAULT_XML_BYTES,
            package=docx_doc.part.package,
        )
        docx_doc.part.relate_to(comments_part, RELATIONSHIP_TYPE.COMMENTS)

    comments_xml = parse_xml(comments_part.blob)
    # Create the comment
    comment_id = str(len(comments_xml.findall(qn("w:comment"))))
    comment_element = OxmlElement("w:comment")
    comment_element.set(qn("w:id"), comment_id)
    comment_element.set(qn("w:author"), author)
    comment_element.set(qn("w:date"), datetime.now().isoformat())

    # Create the text element for the comment
    comment_paragraph = OxmlElement("w:p")
    comment_run = OxmlElement("w:r")
    comment_text_element = OxmlElement("w:t")
    comment_text_element.text = comment_text
    comment_run.append(comment_text_element)
    comment_paragraph.append(comment_run)
    comment_element.append(comment_paragraph)

    comments_xml.append(comment_element)
    comments_part._blob = tostring(comments_xml)

    # Create the commentRangeStart and commentRangeEnd elements
    comment_range_start = OxmlElement("w:commentRangeStart")
    comment_range_start.set(qn("w:id"), comment_id)
    comment_range_end = OxmlElement("w:commentRangeEnd")
    comment_range_end.set(qn("w:id"), comment_id)

    # Add the commentRangeStart to the first element and commentRangeEnd to
    # the last element
    elements[0].insert(0, comment_range_start)
    elements[-1].append(comment_range_end)

    # Add the comment reference to each element in the range
    # for element in elements:
    comment_reference = OxmlElement("w:r")
    comment_reference_run = OxmlElement("w:r")
    comment_reference_run_properties = OxmlElement("w:rPr")
    comment_reference_run_properties.append(
        OxmlElement("w:rStyle", {qn("w:val"): "CommentReference"})
    )
    comment_reference_run.append(comment_reference_run_properties)
    comment_reference_element = OxmlElement("w:commentReference")
    comment_reference_element.set(qn("w:id"), comment_id)
    comment_reference_run.append(comment_reference_element)
    comment_reference.append(comment_reference_run)

    elements[0].append(comment_reference)

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

def handle_chunk(message_chunk):
    return agent.invoke(PROMPT.format(message_chunk))

def analyze_and_comment(filename):
    doc = Document(filename)
    pbar = tqdm(desc="Working...", total=len(doc.paragraphs))
    for i, paragraph in enumerate(doc.paragraphs):
        pbar.update()
        if(paragraph.text != "" and len(paragraph.runs) > 0 and not paragraph.style.name.startswith("Head")):
            # Send paragraph.text to the genAI
            # Save the AI's comment about the text (changes according to prompt)
            # Save a comment around the run with the AI's comment in it
            comment = handle_chunk(paragraph.text)
            if not comment.startswith("This syntax is correct"):
                add_comment_to_elements_in_place(doc, [paragraph._element], AI_NAME, comment)
    pbar.close()
    print(f"Done!")
    doc.save("SyntAI_output.docx")

parser = ArgumentParser(description="A script utility that makes use of OpenAI GPT to work with docx documents without compromising its styling. You must have an Ollama server running and at least one model pulled. See README for instructions to setup.")
parser.add_argument("file", action="store", help="The docx file you wish to translate")
parser.add_argument("--model", "-m", action="store", default=DEFAULT_MODEL, help=f"The model to use with the local ollama server. The default is {DEFAULT_MODEL}")
if __name__=="__main__":
    args = parser.parse_args()
    agent = OllamaLLM(model=args.model)
    analyze_and_comment(args.file)
