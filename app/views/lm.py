from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_creator:
            return redirect('creators:project_list')
        else:
            return redirect('reviewers:projectreview_list')
    return render(request, 'lm/home.html')
