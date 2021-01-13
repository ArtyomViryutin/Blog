from django import forms
from django.core.exceptions import ValidationError

from .models import Group


class PostForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    text = forms.CharField(widget=forms.Textarea)

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise ValidationError('Text cannot be empty')
        return text
