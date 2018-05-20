from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from app.models import ProjectReview, ProjectSequences, Project


class CreatorSignUpForm(UserCreationForm):
    pass


class SequenceForm(forms.ModelForm):
    pass


class ReviewerSignUpForm(UserCreationForm):
    pass


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    pass


class ProjectReviewAddForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ('project_reviews', 'is_fact_flagged', 'is_activity_flagged', 'is_interaction_flagged',
                  'is_reinforcement_flagged')

class ProjectConfirmForm(forms.ModelForm):
    is_project_approved = forms.BooleanField(required=True)
    class Meta:
        model = Project
        fields = ('is_project_approved', )

class ProjectSequencesReviewForm(forms.ModelForm):
    pass


class AddProject(forms.ModelForm):
    client = forms.SelectMultiple()
    project_name = forms.CharField(widget=forms.TextInput)
    library = forms.SelectMultiple()

    class Meta:
        model = Project
        fields = ('client', 'project_name', 'library', )
