from django import forms
from .models import Essay

class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your essay title',
                    'id': 'essay-title',
                    'name': 'essay-title'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'placeholder': 'Enter your essay here',
                    'id': 'essay-content',
                    'rows': 7,  # You can adjust the number of rows to fit your design
                    'cols': 40  # You can adjust the number of columns to fit your design
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['body'].label = 'Essay'
    
    def clean_body(self):
        body = self.cleaned_data.get('body')
        word_count = len(body.split())
        if word_count > 500:
            raise forms.ValidationError("Your essay cannot exceed 500 words.")
        return body