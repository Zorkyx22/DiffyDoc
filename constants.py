import os
from dotenv import load_dotenv

load_dotenv()

END_FILE_PREFIX = "revised_"

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# The following prompt was generated using the following prompt:
"""
You are an expert prompt engineer and you are tasked with writing prompts for specialized tasks in Copilot Studio. You keep your responses clear, precise, and you only answer with the prompt that should be used for the query. As an expert prompt engineer, you know that prompts should always give extremely precise instructions while always speaking in assertions. Negations are to be avoided at all costs. You also know that attributing a role to an agent is the best way to prevent the language model from providing courtesy writings. You must always include in your prompts the fact that the agent should always answer the query and only the query.

Here is your first task: 
"I am a cybersecurity engineer and I need to write a LOT of documentation to comply with FDA standards. My biggest hardship is that english is not my first language, so syntax comes a little less easily to me and my colleagues often correct my sentences. I would like my agent to proof-read my texts to correct my syntax, grammar, and spelling? Obviously the writing style should not change, it should be the same as what I provide. This is because the FDA is very strict as to what type of language we need to use when submitting product dossiers."
"""

SYNTAX_PROMPT = """
You are a proofreader specialist with the goal of pointing out syntax mistakes in your given assignment. You must only answer with either the phrase "This syntax is correct" or with "Here is what should be changed". When corrections are needed, you must give the before and after of the sentence that needs correcting. Make sure you read your assignments twice before answering, some are tricky.

Here is your assignment:
{}
"""

TRANSLATION_PROMPT = """
Please create the litteral translation of the following french text to english.
Translations have to be formal.
Your response should only contain the translation.
Example : 
user : 'Je suis une personne créative et enjouée qui adore l'escalade. Ma mère était'
assistant : 'I am a creative and happy person who loves rock climbing. My mother was'
"""

AI_NAME = "SyntAI"
DEFAULT_MODEL = "llama3.2:3b-instruct-q5_K_M"

COMMENTS_PART_DEFAULT_XML_BYTES = (
    b"""
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r
<w:comments
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
    xmlns:v="urn:schemas-microsoft-com:vml"
    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    xmlns:w10="urn:schemas-microsoft-com:office:word"
    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
    xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main"
    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
    xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
    xmlns:lc="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas"
    xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"
    xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
    xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
    xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
    xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
    xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml"
    xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex"
    xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid"
    xmlns:cr="http://schemas.microsoft.com/office/comments/2020/reactions">
</w:comments>
"""
).strip()


