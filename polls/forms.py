from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('pub_date','user')

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ('question','votes','voted_user')