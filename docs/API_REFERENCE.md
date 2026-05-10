# NoteNest API Reference (v1)

The NoteNest API is built on REST principles and returns JSON responses.

## Base URL
`/api/v1`

## Authentication
Use JWT for authentication. Include the token in the `Authorization` header:
`Authorization: Bearer <your_token>`

## Common Response Format
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

## Endpoints

### Auth
- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Authenticate and receive access/refresh tokens.
- `POST /auth/refresh`: Rotate tokens.

### Notes
- `GET /notes/`: List all notes (paginated).
- `POST /notes/`: Create a new note (multipart/form-data).
- `GET /notes/<id>`: Get note details.
- `DELETE /notes/<id>`: Delete a note.

### AI Study Assistant
- `POST /ai/summarize/<note_id>`: Get/generate an AI summary.
- `POST /ai/chat/<note_id>`: Chat with a note (RAG-powered).
- `GET /ai/quiz/<note_id>`: Get/generate a quiz.

## Interactive Documentation
Visit `/api/docs` on a running instance for the full interactive Swagger/OpenAPI documentation.
