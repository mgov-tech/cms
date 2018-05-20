from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views import generic


from ..decorators import creator_required
from ..forms import BaseAnswerInlineFormSet, SequenceForm, CreatorSignUpForm
from ..models import UserProfile, Project, ProjectReview


class CreatorsSignUpView(CreateView):
    pass


@method_decorator([login_required, creator_required], name='dispatch')
class P1(ListView):
    pass


@method_decorator([login_required, creator_required], name='dispatch')
class P2(ListView):
    pass


@method_decorator([login_required, creator_required], name='dispatch')
class P3(ListView):
    model = ProjectReview
    context_object_name = 'projectreview'
    template_name = 'lm/creators/project_change_form.html'

@method_decorator([login_required, creator_required], name='dispatch')
class P4(ListView):
    pass


@method_decorator([login_required, creator_required], name='dispatch')
class Reports(generic.TemplateView):
    template_name = 'lm/creators/reports.html'


    def get(self, request):
        self._context = { }
        return render(request, self.template_name)



@method_decorator([login_required, creator_required], name='dispatch')
class ProjectListView(generic.TemplateView):
    template_name = 'lm/creators/project_list.html'
    _projects = Project.objects.all()
    _project_reviews = ProjectReview.objects.all()
    _context = {}

    def get(self, request):
        self._context = {"projects": self._projects, }
        return render(request, self.template_name, self._context)


@method_decorator([login_required, creator_required], name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('project_name', )
    context_object_name = 'project'
    template_name = 'lm/creators/project_change_form.html'

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return Project.objects.all()

    def get_success_url(self):
        return reverse('projects:project_change', kwargs={'pk': self.object.pk})