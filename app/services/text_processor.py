import logging
import requests
from openai import OpenAI, OpenAIError

from app.core.config import settings

logger = logging.getLogger(__name__)


class TextProcessorException(Exception):
    pass


LLM_PROMPT = """Fix missing accents in the following text: '{0}'
{1}
Only return the corrected text with accents.
Do not add explanations, translations, or extra words."""
    
CORRECT_GRAMMAR_PROMPT = "Also fix grammar and spelling."
REWORD_PROMPT = "Also reword the text while keeping the meaning."
LANGUAGE_PROMPT = "Language is {0}."
AUTO_DETECT_LANGUAGE_PROMPT = "Auto-detect the language of the text."

def format_prompt(text: str, language: str = None, correct_grammar: bool = False, reword: bool = False) -> str:
    extra_prompts = LANGUAGE_PROMPT.format(language) if language else AUTO_DETECT_LANGUAGE_PROMPT
    if correct_grammar:
        extra_prompts += "\n" + CORRECT_GRAMMAR_PROMPT
    if reword:
        if extra_prompts:
            extra_prompts += "\n"
        extra_prompts += REWORD_PROMPT
        
    return LLM_PROMPT.format(text, extra_prompts)


def process_text_local_LLM_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
    except requests.RequestException as exc:
        raise TextProcessorException(f"Error calling hosted LLM API: {str(exc)}")
    except (KeyError, IndexError, AttributeError) as exc:
        raise TextProcessorException(f"Invalid LLM response: {str(exc)}")  


def process_text_hosted_LLM(prompt: str) -> str:
    client = OpenAI(base_url=settings.LLM_API_URL, api_key=settings.LLM_API_KEY)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except OpenAIError as exc:
        raise TextProcessorException(f"Error calling LLM API: {str(exc)}")
    
    try:
        processed_text = response.choices[0].message.content
    except (KeyError, IndexError, AttributeError) as exc:
        raise TextProcessorException(f"Invalid LLM response: {str(exc)}")
    
    return processed_text


def process_text(text: str, language: str = None, correct_grammar: bool = False, reword: bool = False) -> str:
    prompt = format_prompt(text, language, correct_grammar, reword)
    logger.info(f'Prompt = {prompt}')

    #processed_text = process_text_hosted_LLM(prompt)
    processed_text = process_text_local_LLM_ollama(prompt)
    # remove quotes:
    processed_text = processed_text.strip().strip('"').strip("'")
    
    return processed_text

