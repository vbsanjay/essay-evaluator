# forms.py
from django import forms

class PromptsEditForm(forms.Form):
    evaluation_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}))
    description_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
    spelling_errors_count_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
    spelling_error_word_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
    spelling_error_start_index_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
    spelling_error_end_index_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
    content_relevance_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
    essay_score_prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))
