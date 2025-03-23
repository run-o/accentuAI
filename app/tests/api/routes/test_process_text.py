from fastapi.testclient import TestClient
from app.main import app

TEST_TEXT_MISSING_ACCENTS = "Je suis alle a la peche."
TEST_TEXT_ACCENTS = "Je suis allé à la pêche."
TEST_TEXT_INCORRECT_GRAMMAR = "Je suis aller a la peche."


def test_correct_text_basic(client: TestClient):
    response = client.post("/text/correct/", json={"text": TEST_TEXT_MISSING_ACCENTS})
    assert response.status_code == 200
    assert response.json() == TEST_TEXT_ACCENTS

def test_correct_text_with_language(client: TestClient):
    response = client.post("/text/correct/", json={"text": TEST_TEXT_MISSING_ACCENTS, "language": "French"})
    assert response.status_code == 200
    assert response.json() == TEST_TEXT_ACCENTS

def test_correct_text_with_grammar_correction(client: TestClient):
    response = client.post("/text/correct/", json={"text": TEST_TEXT_INCORRECT_GRAMMAR, "language": "French", "correct_grammar": True})
    assert response.status_code == 200
    assert response.json() == TEST_TEXT_ACCENTS
