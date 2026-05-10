from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models.note import Note
from ...schemas.note import NoteSchema
from ...services.note_service import NoteService

blp = Blueprint("Notes", "notes", url_prefix="/notes", description="Operations on notes")

@blp.route("/")
class NoteList(MethodView):
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """List all notes"""
        return Note.query.all()

    @jwt_required()
    @blp.arguments(NoteSchema)
    @blp.response(201, NoteSchema)
    def post(self, note_data):
        """Create a new note (simplified for API)"""
        # In a real scenario, we'd handle the file upload via multipart
        return NoteService.create_note(
            user_id=get_jwt_identity(),
            **note_data
        )

@blp.route("/<int:note_id>")
class NoteResource(MethodView):
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        """Get a specific note by ID"""
        note = Note.query.get_or_404(note_id)
        return note

    @jwt_required()
    def delete(self, note_id):
        """Delete a note"""
        note = Note.query.get_or_404(note_id)
        if note.user_id != get_jwt_identity():
            abort(403, message="Not authorized to delete this note")
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted"}
