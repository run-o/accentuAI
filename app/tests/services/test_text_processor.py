import pytest
from openai import OpenAIError
from app.services.text_processor import (
    process_text,
    TextProcessorException,
    LLM_PROMPT,
    CORRECT_GRAMMAR_PROMPT,
    REWORD_PROMPT,
    LANGUAGE_PROMPT,
    AUTO_DETECT_LANGUAGE_PROMPT,
)

@pytest.fixture
def mock_openai_client(mocker):
    mock_openai = mocker.patch('app.services.text_processor.OpenAI')
    mock_client = mock_openai.return_value
    return mock_client

def test_process_text_openai_error_raises(mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = OpenAIError("API Error")

    with pytest.raises(TextProcessorException, match="Error calling LLM API: API Error"):
        process_text("Some text")

def test_process_text_invalid_response_raises(mock_openai_client, mocker):
    mock_openai_client.chat.completions.create.return_value = mocker.Mock(choices=[])

    with pytest.raises(TextProcessorException, match="Invalid LLM response"):
        process_text("Some text")

def test_process_text_basic(mock_openai_client, mocker):
    mock_openai_client.chat.completions.create.return_value = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Corrected text"))]
    )
    result = process_text("Some text")
    assert result == "Corrected text"
    
    prompt = LLM_PROMPT.format("Some text", AUTO_DETECT_LANGUAGE_PROMPT)
    
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=mocker.ANY,
        messages=[{"role": "user", "content": prompt}]
    )

def test_process_text_with_language(mock_openai_client, mocker):
    mock_openai_client.chat.completions.create.return_value = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Corrected text with language"))]
    )
    result = process_text("Some text", language="French")
    assert result == "Corrected text with language"
    
    prompt = LLM_PROMPT.format("Some text", LANGUAGE_PROMPT.format("French"))
    
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=mocker.ANY,
        messages=[{"role": "user", "content": prompt}]
    )

def test_process_text_with_grammar_correction(mock_openai_client, mocker):
    mock_openai_client.chat.completions.create.return_value = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Corrected text with grammar"))]
    )

    result = process_text("Some text", correct_grammar=True)
    assert result == "Corrected text with grammar"
    
    prompt = LLM_PROMPT.format("Some text", AUTO_DETECT_LANGUAGE_PROMPT + "\n" + CORRECT_GRAMMAR_PROMPT)
    
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=mocker.ANY,
        messages=[{"role": "user", "content": prompt}]
    )

def test_process_text_with_rewording(mock_openai_client, mocker):
    mock_openai_client.chat.completions.create.return_value = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Corrected text with rewording"))]
    )

    result = process_text("Some text", reword=True)
    assert result == "Corrected text with rewording"
    
    prompt = LLM_PROMPT.format("Some text", AUTO_DETECT_LANGUAGE_PROMPT + "\n" + REWORD_PROMPT)
    
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=mocker.ANY,
        messages=[{"role": "user", "content": prompt}]
    )
    
def test_process_text_with_all_options(mock_openai_client, mocker):
    mock_openai_client.chat.completions.create.return_value = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Corrected text with all options"))]
    )

    result = process_text("Some text", language="French", correct_grammar=True, reword=True)
    assert result == "Corrected text with all options"
    
    prompt = LLM_PROMPT.format("Some text", LANGUAGE_PROMPT.format("French")
                               + "\n" + CORRECT_GRAMMAR_PROMPT + "\n" + REWORD_PROMPT)
    
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=mocker.ANY,
        messages=[{"role": "user", "content": prompt}]
    )
