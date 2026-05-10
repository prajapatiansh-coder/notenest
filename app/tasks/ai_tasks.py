from ..worker import celery
from ..extensions import db
from ..models.note import Note
from ..ai.services import AIService as AIProcessor
from ..ai.pdf_processor import extract_text_from_pdf
import structlog

logger = structlog.get_logger()

@celery.task(bind=True, max_retries=3)
def process_note_ai_task(self, note_id, user_id):
    try:
        note = Note.query.get(note_id)
        if not note:
            return "Note not found"

        logger.info("processing_note_ai", note_id=note_id)
        
        # Extract text
        text = extract_text_from_pdf(note.filename)
        if not text:
            return "No text extracted"

        # Generate Summary using Orchestrator
        from ..ai.orchestrator import AIOrchestrator
        summary = AIOrchestrator.generate_response(user_id, "", feature='summary', context=text)
        note.ai_summary = summary
        
        db.session.commit()
        logger.info("note_ai_processing_complete", note_id=note_id)
        return "Success"
    except Exception as exc:
        logger.error("note_ai_processing_failed", note_id=note_id, error=str(exc))
        raise self.retry(exc=exc, countdown=60)
