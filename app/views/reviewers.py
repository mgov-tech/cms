from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views import generic


from ..decorators import reviewer_required
from ..forms import ReviewerSignUpForm, ProjectReviewAddForm, ProjectConfirmForm, AddProject
from ..models import UserProfile, Project, ProjectSequences, ProjectReview, Sequence


class ReviewerSignUpView(CreateView):
    model = UserProfile
    form_class = ReviewerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'creator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('creators:quiz_list')


@method_decorator([login_required, reviewer_required], name='dispatch')
class ProjectListView(generic.TemplateView):
    template_name = 'lm/reviewers/reviewer_list.html'

    _context = {}

    def get(self, request):
        _projects = Project.objects.all()
        self._context = {"projects": _projects, }
        return render(request, self.template_name, self._context)


@method_decorator([login_required, reviewer_required], name='dispatch')
class Playground(generic.TemplateView):
    """classe apenas para testar algumas coisas no django"""
    template_name = 'lm/reviewers/playground.html'
    _context = {}

    def get(self, request):
        _form = AddProject()
        _projects = Project.objects.all()
        self._context = {"form": _form, "projects": _projects}
        return render(request, self.template_name, self._context)

    def post(self, request):
        _form = AddProject(request.POST)
        self._context = {"form": _form}
        print(request.POST)
        if _form.is_valid():
            text = _form.cleaned_data['project_name']
            _form.save()
            _form = AddProject()
            _projects = Project.objects.all()
            self._context = {"form": _form, "success": True, "text": text, "projects": _projects}
            return render(request, self.template_name, self._context)

        return render(request, self.template_name, self._context)


@method_decorator([login_required, reviewer_required], name='dispatch')
class ProjectReviewEdit(generic.TemplateView):
    """a ideia desta view é renderizar as sequências associadas a um projeto,
       além de permtir que o usuário faça comentários/autilize comentários sobre cada sequencia
    """
    template_name = 'lm/reviewers/do_project_review.html'
    _context = {}

    def get(self, request, project_number):
        _project = Project.objects.get(prj_id=project_number)
        _form = ProjectConfirmForm(instance=_project)
        self._context = {"p": _project, "form": _form}
        return render(request, self.template_name, self._context)

    def post(self, request, project_number):
        _project = Project.objects.get(prj_id=project_number)
        _form = ProjectConfirmForm(request.POST, instance=_project)
        self._context = {"p": _project, "form": _form}
        if _form.is_valid():
            r = _form.save(commit=False)
            r.save()
            return redirect("reviewers:projectreview_list")


@method_decorator([login_required, reviewer_required], name='dispatch')
class ProjectSequenceReviewEdit(generic.TemplateView):
    template_name = 'lm/reviewers/write_project_review.html'
    _context = {}

    def get(self, request, project_number, seq_number):
        print(request.user)
        _p = Project.objects.get(prj_id=project_number)
        _s = Sequence.objects.get(seq_id=seq_number)
        _ps = ProjectSequences.objects.filter(project=_p, sequence=_s).first()
        _form = ProjectReviewAddForm()
        self._context = {"sequence_content": _ps, "project_number": project_number, "seq_number": seq_number,
                         "form": _form}
        return render(request, self.template_name, self._context)

    def post(self, request, project_number, seq_number):
        _p = Project.objects.get(prj_id=project_number)
        _s = Sequence.objects.get(seq_id=seq_number)
        _ps = ProjectSequences.objects.filter(project=_p, sequence=_s).first()
        _form = ProjectReviewAddForm(request.POST)
        if _form.is_valid():
            r = _form.save(commit=False)
            r.user = UserProfile.objects.get(username=request.user)
            r.save()
            _ps.project_reviews.add(r)
            return redirect("reviewers:do_project_review", project_number=project_number)