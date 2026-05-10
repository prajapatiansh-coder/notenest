import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, send_from_directory, abort, jsonify
from flask_login import current_user, login_required
from ..extensions import db, cache, limiter
from ..models.note import Note
from ..models.interaction import Like, Bookmark, Comment, Notification
from ..models.ai import AIChat, AIQuiz, Flashcard
from .forms import NoteForm, EditNoteForm, CommentForm
from ..services.note_service import NoteService
from ..services.ai_service import AIService

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/")
@notes_bp.route("/home")
@cache.cached(timeout=300)
def index():
    trending_notes = NoteService.get_trending_notes()
    recent_notes = NoteService.get_recent_notes()
    return render_template('index.html', notes=recent_notes, trending_notes=trending_notes)

@notes_bp.route("/browse")
@limiter.limit("20 per minute")
def browse():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    subject_filter = request.args.get('subject', '').strip()
    semester_filter = request.args.get('semester', '').strip()
    
    filters = {'subject': subject_filter, 'semester': semester_filter}
    notes = NoteService.search_notes(search_query, filters=filters, page=page)
    
    subjects = db.session.query(Note.subject).distinct().all()
    subjects = [s[0] for s in subjects]
    
    return render_template('notes/browse.html', 
                           title='Browse Notes', 
                           notes=notes, 
                           search_query=search_query,
                           subjects=subjects,
                           current_subject=subject_filter,
                           current_semester=semester_filter)

@notes_bp.route("/note/<int:note_id>", methods=['GET', 'POST'])
def note_details(note_id):
    note = Note.query.get_or_404(note_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to comment.', 'warning')
            return redirect(url_for('auth.login'))
        
        comment = Comment(text=form.text.data, user=current_user, note=note)
        db.session.add(comment)
        
        if note.uploader != current_user:
            notification = Notification(
                user=note.uploader,
                message=f"{current_user.username} commented on your note: {note.title}",
                link=url_for('notes.note_details', note_id=note.id)
            )
            db.session.add(notification)
            
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('notes.note_details', note_id=note.id))

    user_liked, user_bookmarked = (False, False)
    if current_user.is_authenticated:
        user_liked, user_bookmarked = NoteService.get_user_interactions(current_user.id, note.id)

    chat_history = []
    if current_user.is_authenticated:
        chat_history = AIChat.query.filter_by(user_id=current_user.id, note_id=note.id).order_by(AIChat.created_at.desc()).limit(5).all()
        chat_history.reverse()

    return render_template('notes/details.html', title=note.title, note=note, form=form, 
                           user_liked=user_liked, user_bookmarked=user_bookmarked, chat_history=chat_history)

@notes_bp.route("/note/<int:note_id>/summarize", methods=['POST'])
@login_required
def summarize_note(note_id):
    summary = AIService.get_summary(note_id)
    return jsonify({"summary": summary})

@notes_bp.route("/note/<int:note_id>/chat", methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def chat_with_note(note_id):
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    answer = AIService.chat_with_note(current_user.id, note_id, question)
    return jsonify({"answer": answer})

@notes_bp.route("/note/<int:note_id>/quiz")
@login_required
def generate_quiz(note_id):
    note = Note.query.get_or_404(note_id)
    quizzes = AIService.get_or_generate_quiz(note_id)
    return render_template('notes/quiz.html', note=note, quizzes=quizzes)

@notes_bp.route("/note/<int:note_id>/flashcards")
@login_required
def generate_flashcards(note_id):
    note = Note.query.get_or_404(note_id)
    flashcards = AIService.get_or_generate_flashcards(note_id)
    return render_template('notes/flashcards.html', note=note, flashcards=flashcards)

@notes_bp.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = NoteForm()
    if form.validate_on_submit():
        if form.note_file.data:
            filename = NoteService.save_note_file(form.note_file.data)
            NoteService.create_note(
                user=current_user,
                title=form.title.data,
                subject=form.subject.data,
                semester=form.semester.data,
                description=form.description.data,
                filename=filename
            )
            flash('Your note has been uploaded! AI processing started.', 'success')
            return redirect(url_for('notes.dashboard'))
    return render_template('notes/upload.html', title='Upload Note', form=form)

@notes_bp.route("/dashboard")
@login_required
def dashboard():
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.uploaded_at.desc()).all()
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    saved_notes = [b.note for b in bookmarks]
    
    total_downloads = sum(note.downloads for note in user_notes)
    total_likes = sum(len(note.likes) for note in user_notes)
    
    return render_template('notes/dashboard.html', 
                           title='Dashboard', 
                           notes=user_notes, 
                           saved_notes=saved_notes,
                           total_downloads=total_downloads,
                           total_likes=total_likes)

@notes_bp.route("/download/<filename>")
def download_file(filename):
    note = Note.query.filter_by(filename=filename).first_or_404()
    note.downloads += 1
    db.session.commit()
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@notes_bp.route("/analytics")
@login_required
def analytics():
    # User's notes stats
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    note_titles = [n.title for n in user_notes]
    note_downloads = [n.downloads for n in user_notes]
    note_likes = [len(n.likes) for n in user_notes]
    
    # Global AI usage (simulated for now, would use real event logs)
    ai_usage_labels = ['Summaries', 'Chat', 'Quizzes', 'Flashcards']
    ai_usage_data = [
        Note.query.filter(Note.ai_summary != None).count(),
        AIChat.query.count(),
        AIQuiz.query.count(),
        Flashcard.query.count()
    ]
    
    return render_template('notes/analytics.html', 
                           note_titles=note_titles, 
                           note_downloads=note_downloads,
                           note_likes=note_likes,
                           ai_usage_labels=ai_usage_labels,
                           ai_usage_data=ai_usage_data)

@notes_bp.route("/note/<int:note_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.uploader != current_user:
        abort(403)
    
    form = EditNoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.subject = form.subject.data
        note.semester = form.semester.data
        note.description = form.description.data
        
        if form.note_file.data:
            old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], note.filename)
            if os.path.exists(old_path):
                os.remove(old_path)
            note.filename = NoteService.save_note_file(form.note_file.data)
            note.ai_summary = None  # Reset summary if file changed
            
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.note_details', note_id=note.id))
    
    elif request.method == 'GET':
        form.title.data = note.title
        form.subject.data = note.subject
        form.semester.data = note.semester
        form.description.data = note.description
        
    return render_template('notes/edit.html', title='Edit Note', form=form, note=note)

@notes_bp.route("/note/<int:note_id>/delete", methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.uploader != current_user:
        abort(403)
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], note.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'success')
    return redirect(url_for('notes.dashboard'))

@notes_bp.route("/note/<int:note_id>/like", methods=['POST'])
@login_required
def like_note(note_id):
    note = Note.query.get_or_404(note_id)
    like = Like.query.filter_by(user_id=current_user.id, note_id=note.id).first()
    
    if like:
        db.session.delete(like)
    else:
        like = Like(user_id=current_user.id, note_id=note.id)
        db.session.add(like)
        if note.uploader != current_user:
            notification = Notification(
                user=note.uploader,
                message=f"{current_user.username} liked your note: {note.title}",
                link=url_for('notes.note_details', note_id=note.id)
            )
            db.session.add(notification)
            
    db.session.commit()
    return redirect(request.referrer or url_for('notes.note_details', note_id=note.id))

@notes_bp.route("/note/<int:note_id>/bookmark", methods=['POST'])
@login_required
def bookmark_note(note_id):
    note = Note.query.get_or_404(note_id)
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, note_id=note.id).first()
    
    if bookmark:
        db.session.delete(bookmark)
        flash('Note removed from bookmarks.', 'info')
    else:
        bookmark = Bookmark(user_id=current_user.id, note_id=note.id)
        db.session.add(bookmark)
        flash('Note bookmarked!', 'success')
        
    db.session.commit()
    return redirect(request.referrer or url_for('notes.note_details', note_id=note.id))

@notes_bp.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user != current_user and comment.note.uploader != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'info')
    return redirect(url_for('notes.note_details', note_id=comment.note_id))
