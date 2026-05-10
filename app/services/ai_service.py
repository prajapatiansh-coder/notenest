from ..extensions import db, cache
from ..models.ai import AIChat, AIQuiz, Flashcard
from ..models.note import Note
from ..ai.orchestrator import AIOrchestrator
from ..ai.pdf_processor import extract_text_from_pdf

class AIService:
    @staticmethod
    @cache.memoize(timeout=3600)
    def get_summary(note_id, user_id):
        note = Note.query.get(note_id)
        if note.ai_summary:
            return note.ai_summary
        
        text = extract_text_from_pdf(note.filename)
        summary = AIOrchestrator.generate_response(user_id, "", feature='summary', context=text)
        
        note.ai_summary = summary
        db.session.commit()
        return summary

    @staticmethod
    def chat_with_note(user_id, note_id, question):
        note = Note.query.get(note_id)
        text = extract_text_from_pdf(note.filename)
        answer = AIOrchestrator.generate_response(user_id, question, feature='chat', context=text)
        
        chat = AIChat(user_id=user_id, note_id=note_id, question=question, answer=answer)
        db.session.add(chat)
        db.session.commit()
        return answer

    @staticmethod
    def get_or_generate_quiz(note_id):
        quizzes = AIQuiz.query.filter_by(note_id=note_id).all()
        if quizzes:
            return quizzes
        
        note = Note.query.get(note_id)
        text = extract_text_from_pdf(note.filename)
        quiz_data = AIProcessor.generate_quiz(text)
        
        new_quizzes = []
        for q in quiz_data:
            quiz = AIQuiz(
                note_id=note_id,
                question=q['question'],
                options=q['options'],
                answer=q['answer'],
                question_type=q['type']
            )
            db.session.add(quiz)
            new_quizzes.append(quiz)
            
        db.session.commit()
        return new_quizzes

    @staticmethod
    def get_or_generate_flashcards(note_id):
        cards = Flashcard.query.filter_by(note_id=note_id).all()
        if cards:
            return cards
        
        note = Note.query.get(note_id)
        text = extract_text_from_pdf(note.filename)
        card_data = AIProcessor.generate_flashcards(text)
        
        new_cards = []
        for c in card_data:
            card = Flashcard(
                note_id=note_id,
                front_text=c['front'],
                back_text=c['back']
            )
            db.session.add(card)
            new_cards.append(card)
            
        db.session.commit()
        return new_cards

    @staticmethod
    def chat_with_note(user_id, note_id, question):
        note = Note.query.get(note_id)
        text = extract_text_from_pdf(note.filename)
        answer = AIProcessor.ask_question(text, question)
        
        chat = AIChat(user_id=user_id, note_id=note_id, question=question, answer=answer)
        db.session.add(chat)
        db.session.commit()
        return answer
