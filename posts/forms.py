from .models import Comment
from django import forms


class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Add your comment here ...",
                }
            )
        }
        labels = {"content": ""}
