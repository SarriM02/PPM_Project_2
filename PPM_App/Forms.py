from django import forms
from .Models import Poll, Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title']

    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all())

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['questions'].initial = self.instance.questions.all()

    def save(self, commit=True):
        poll = super(PollForm, self).save(commit=False)
        if commit:
            poll.save()
            poll.questions.set(self.cleaned_data['questions'])
        return poll