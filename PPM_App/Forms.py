from django import forms
from .Models import Poll, Choice
from django.forms import inlineformset_factory

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']

ChoiceFormSet = inlineformset_factory(Poll, Choice, form=ChoiceForm, extra=2, can_delete=True)

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
