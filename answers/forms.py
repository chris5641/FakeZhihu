from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content', 'content_text']
        widgets = {
            'content': forms.Textarea(attrs={'style': 'display:none'}),
            'content_text': forms.Textarea(attrs={'style': 'display:none'}),
        }
