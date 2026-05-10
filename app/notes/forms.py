from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    semester = SelectField('Semester', choices=[
        ('1', 'Semester 1'), ('2', 'Semester 2'), ('3', 'Semester 3'), 
        ('4', 'Semester 4'), ('5', 'Semester 5'), ('6', 'Semester 6'),
        ('7', 'Semester 7'), ('8', 'Semester 8')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    note_file = FileField('Upload PDF', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField('Upload Note')

class EditNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    semester = SelectField('Semester', choices=[
        ('1', 'Semester 1'), ('2', 'Semester 2'), ('3', 'Semester 3'), 
        ('4', 'Semester 4'), ('5', 'Semester 5'), ('6', 'Semester 6'),
        ('7', 'Semester 7'), ('8', 'Semester 8')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    note_file = FileField('Replace PDF (Optional)', validators=[
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField('Save Changes')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Post Comment')

    def validate_title(self, title):
        if not title.data.strip():
            raise ValidationError('Title cannot be empty or just whitespace.')

    def validate_subject(self, subject):
        if not subject.data.strip():
            raise ValidationError('Subject cannot be empty or just whitespace.')
