import json
from flask import current_app

class AIService:
    @staticmethod
    def summarize(text):
        if not text:
            return "No content to summarize."
        
        # Simulating AI processing
        summary = "This document provides a comprehensive overview of the subject matter. It details the core theoretical frameworks, provides practical examples, and summarizes the key takeaways for the semester. Major topics include foundational principles, advanced methodologies, and real-world applications as described in the note content."
        return summary

    @staticmethod
    def generate_quiz(text):
        # Mock quiz generation based on text
        quizzes = [
            {
                "question": "Which of the following best describes the main theme of this note?",
                "options": ["Foundational Theory", "Practical Implementation", "Case Studies", "Future Research"],
                "answer": "Foundational Theory",
                "type": "mcq"
            },
            {
                "question": "The document suggests that practical application is essential for mastering the concepts.",
                "options": ["True", "False"],
                "answer": "True",
                "type": "tf"
            },
            {
                "question": "What is the primary methodology discussed in the first section?",
                "options": None,
                "answer": "The methodology involves a systematic review of existing literature and empirical testing.",
                "type": "short"
            }
        ]
        return quizzes

    @staticmethod
    def generate_flashcards(text):
        # Mock flashcards
        flashcards = [
            {"front": "Key Principle 1", "back": "The primary rule or belief that governs the system described."},
            {"front": "Methodology", "back": "A system of methods used in a particular area of study or activity."},
            {"front": "Conclusion", "back": "The final summary of findings presented at the end of the note."},
            {"front": "Case Study", "back": "A particular instance of something used or analyzed in order to illustrate a thesis or principle."}
        ]
        return flashcards

    @staticmethod
    def ask_question(text, question):
        # Simulated retrieval
        question = question.lower()
        if "summary" in question or "overview" in question:
            return "The document provides an overview of essential student topics for this semester."
        elif "subject" in question or "topic" in question:
            return "The main subject focuses on the academic principles outlined in the note details."
        else:
            return "According to the note, the topic involves structured learning and practical examples relevant to the course."
