from django import forms
from django.forms import widgets, ValidationError
from webapp.models import Type, Status, Issue, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['start_date', 'end_date',  'title', 'description']
        # exclude = []

        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        error_messages = {
            'content': {
                'required': 'Field is required'
            }
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'description',  'type', 'status']
        # exclude = []

        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'type': widgets.CheckboxSelectMultiple,
            'status': forms.Select(attrs={'class': 'form-control'})
        }

        error_messages = {
            'content': {
                'required': 'Field is required'
            }
        }


    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) > 20:
            self.add_error('summary', ValidationError('Length should be no more than %(length)d characters!',
                                                    code='too_short', params={'length': 20}))
        return summary

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 3000:
            self.add_error('summary', ValidationError('Длина зтого поля должна составлять не меенее %(length)d символов!',
                                                    code='too_short', params={'length': 3000}))
        return description

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['summary'] == cleaned_data.get('content', ''):
            raise ValidationError('Текст статьи не должен дублировать ее название!')
        return cleaned_data

class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)