from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label="Question", max_length=500)
    choice_one = forms.CharField(label="Choice 1", max_length=200)
    choice_two = forms.CharField(label="Choice 2", max_length=200)