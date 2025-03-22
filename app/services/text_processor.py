import logging
from openai import OpenAI, OpenAIError

from app.core.config import settings

logger = logging.getLogger(__name__)


class TextProcessorException(Exception):
    pass


LLM_PROMPT = """Fix missing accents in the following text: '{0}'
{1}
Do not change the formatting of the text.
Only return the corrected text."""
    
CORRECT_GRAMMAR_PROMPT = "Also fix grammar and spelling."
REWORD_PROMPT = "Also reword the text while keeping the meaning."
LANGUAGE_PROMPT = "Language is {0}."
AUTO_DETECT_LANGUAGE_PROMPT = "Auto-detect the language of the text."

def process_text(text: str, language: str = None, correct_grammar: bool = False, reword: bool = False) -> str:
    
    client = OpenAI(base_url=settings.LLM_API_URL, api_key=settings.LLM_API_KEY)
    
    extra_prompts = LANGUAGE_PROMPT.format(language) if language else AUTO_DETECT_LANGUAGE_PROMPT
    if correct_grammar:
        extra_prompts += "\n" + CORRECT_GRAMMAR_PROMPT
    if reword:
        if extra_prompts:
            extra_prompts += "\n"
        extra_prompts += REWORD_PROMPT
        
        
    prompt = LLM_PROMPT.format(text, extra_prompts)
    logger.info(f'Prompt = {prompt}')
    
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
        processed_text = response.choices[0].message.content.strip()
    except (KeyError, IndexError, AttributeError) as exc:
        raise TextProcessorException(f"Invalid LLM response: {str(exc)}")
    
    # remove quotes:
    processed_text = processed_text.strip('"').strip("'")
    
    return processed_text

