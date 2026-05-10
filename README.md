# Campus Notes

Campus Notes is a modern full-stack social-learning platform designed for students to share, browse, and interact with study materials. Built with Flask and a premium glassmorphism aesthetic.

## Features

### Phase 1: Core Foundation
- **User Authentication**: Secure registration and login.
- **Note Uploads**: PDF study notes sharing.
- **Modern UI**: Responsive glassmorphism design.

### Phase 2: Professional Upgrade
- **Advanced Search & Filtering**: Search by keyword, subject, or semester.
- **PDF Preview**: In-browser PDF viewing.
- **User Profiles**: Public profiles with user statistics.
- **Download Tracking**: Insights into note popularity.

### Phase 3: Community & Interaction
- **Likes & Bookmarks**: Save notes for later or show appreciation with a like.
- **Discussion System**: Comment on notes to ask questions or provide feedback.
- **Notification System**: Real-time alerts for likes and comments.
- **Content Management**: Edit or delete your uploaded notes.
- **Trending Algorithm**: Discover popular notes based on community activity.

### Phase 4: AI Study Platform (New!)
- **AI PDF Summarization**: Generate concise summaries of complex study materials instantly.
- **AI Study Assistant (RAG)**: Chat with your notes! Ask questions and get answers grounded in the PDF content.
- **AI Quiz Generator**: Automatically create MCQs, True/False, and short-answer questions from any note.
- **AI Flashcards**: Generate interactive study cards with flip animations.
- **Semantic Search**: Find materials by meaning and context, not just keywords.
- **AI Study Center**: Dedicated dashboard for AI-generated insights, quizzes, and saved learning activity.

## Tech Stack
- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **AI Engine**: Sentence-Transformers, FAISS (Vector Search), PyPDF2
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite

## Getting Started

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python run.py
   ```
4. Access the app at `http://127.0.0.1:5000`.

## Project Structure
```
app/
├── ai/              # AI Service Layer (RAG, PDF Processing, AI Logic)
├── auth/            # Auth blueprint
├── models/          # SQLAlchemy models
├── notes/           # Notes & AI interactions blueprint
├── static/
│   ├── css/         # Styles with Glassmorphism & AI animations
│   ├── uploads/     # PDF storage
│   └── profile_pics/ # User avatars
├── templates/       # HTML templates (Details, AI Dash, Quiz, Flashcards)
├── __init__.py      # App factory
└── config.py        # Configuration
```

## License
MIT
