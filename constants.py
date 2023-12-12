import os
from dotenv import load_dotenv

load_dotenv()

END_FILE_PREFIX = "Translated_"

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROMPT = """
Please create the litteral translation of the following french text to english.
Translations have to be formal.
Your response should only contain the translation.
Example : 
user : 'Je suis une personne créative et enjouée qui adore l'escalade. Ma mère était'
assistant : 'I am a creative and happy person who loves rock climbing. My mother was'
"""