import os
import secrets
from typing import List, Tuple, Optional, Any
from flask import current_app
from sqlalchemy.orm import joinedload
from ..extensions import db
from ..models.note import Note
from ..models.user import User
from ..models.interaction import Bookmark, Like

class NoteService:
    """
    Service layer for Note-related operations.
    Handles business logic for fetching, searching, and creating notes.
    """

    @staticmethod
    def get_all_notes(page: int = 1, per_page: int = 9) -> Any:
        """Fetch all notes with pagination and optimized loading."""
        return Note.query.options(joinedload(Note.uploader))\
            .order_by(Note.uploaded_at.desc())\
            .paginate(page=page, per_page=per_page)

    @staticmethod
    def get_trending_notes(limit: int = 3) -> List[Note]:
        """Fetch most downloaded notes."""
        return Note.query.options(joinedload(Note.uploader))\
            .order_by(Note.downloads.desc(), Note.uploaded_at.desc())\
            .limit(limit).all()

    @staticmethod
    def get_recent_notes(limit: int = 6) -> List[Note]:
        """Fetch recently uploaded notes."""
        return Note.query.options(joinedload(Note.uploader))\
            .order_by(Note.uploaded_at.desc())\
            .limit(limit).all()

    @staticmethod
    def search_notes(query: str, filters: Optional[dict] = None, page: int = 1, per_page: int = 9) -> Any:
        """Perform filtered search on notes with pagination."""
        notes_query = Note.query.options(joinedload(Note.uploader))
        if query:
            notes_query = notes_query.filter(
                (Note.title.ilike(f'%{query}%')) | 
                (Note.subject.ilike(f'%{query}%')) | 
                (Note.description.ilike(f'%{query}%'))
            )
        
        if filters:
            if filters.get('subject'):
                notes_query = notes_query.filter(Note.subject == filters['subject'])
            if filters.get('semester'):
                notes_query = notes_query.filter(Note.semester == filters['semester'])
                
        return notes_query.order_by(Note.uploaded_at.desc()).paginate(page=page, per_page=per_page)

    @staticmethod
    def save_note_file(form_file: Any) -> str:
        """Save an uploaded file with a secure random name."""
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_file.filename)
        filename = random_hex + f_ext
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form_file.save(file_path)
        return filename

    @staticmethod
    def create_note(user: User, title: str, subject: str, semester: str, description: str, filename: str) -> Note:
        """Create a note record and initiate asynchronous AI processing."""
        note = Note(
            title=title,
            subject=subject,
            semester=semester,
            description=description,
            filename=filename,
            uploader=user
        )
        db.session.add(note)
        db.session.commit()
        
        # Trigger background AI processing
        from ..tasks.ai_tasks import process_note_ai_task
        process_note_ai_task.delay(note.id, user.id)
        
        return note

    @staticmethod
    def get_user_interactions(user_id: int, note_id: int) -> Tuple[bool, bool]:
        """Check if a specific user has liked or bookmarked a note."""
        user_liked = Like.query.filter_by(user_id=user_id, note_id=note_id).first() is not None
        user_bookmarked = Bookmark.query.filter_by(user_id=user_id, note_id=note_id).first() is not None
        return user_liked, user_bookmarked
