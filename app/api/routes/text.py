import logging

from fastapi import APIRouter, HTTPException, status
from app import schemas
from app.services import process_text, TextProcessorException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/text", tags=["text"])


@router.post("/correct/", status_code=status.HTTP_200_OK)
def correct_text(request: schemas.TextRequest):
    try:
        processed_text = process_text(
            text=request.text,
            language=request.language,
            correct_grammar=request.correct_grammar,
            reword=request.reword
        )
    except TextProcessorException as exc:
        logger.exception(f"Text processing failed: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )
    
    return processed_text