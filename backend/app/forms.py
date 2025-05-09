# documentos/forms.py

from django import forms
from .models import Document, Comment, Note

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "source", "original_url", "file_path", "tags"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple, # Or SelectMultiple
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Adicione seu comentário..."}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "documents", "tags"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple,
            "documents": forms.CheckboxSelectMultiple, # Or SelectMultiple
            "content": forms.Textarea(attrs={"rows": 10}),
        }

