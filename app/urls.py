from django.urls import include, path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import View

from app.views import clients, reviewers, creators, app

urlpatterns = [
        path('', app.home, name='home'),

        path('r/', include(([
            path('', reviewers.ProjectListView.as_view(), name='projectreview_list'),
            path('project/<int:project_number>/review/', reviewers.ProjectReviewEdit.as_view(), name='do_project_review'),
            path('project/<int:project_number>/review/<int:seq_number>', reviewers.ProjectSequenceReviewEdit.as_view(), name='write_project_review'),
            #path('project/<int:project_number>/review/<int:review_number>', reviewers.SequenceWriteReview.as_view(), name='write_project_review'),
            path('playground', reviewers.Playground.as_view(), name='playground'),
        ], 'app'), namespace='reviewers')),

        path('c/', include(([
           path('', creators.ProjectListView.as_view(), name='project_list'),
           path('project/', creators.P1.as_view(), name='list'),
           path('project/add/', creators.P2.as_view(), name='project_add'),
           path('project/<int:pk>/reviews/', creators.P3.as_view(), name='project_reviews'),
           path('project/<int:pk>/', creators.P4.as_view(), name='project_change'),
           path('reports', creators.Reports.as_view(), name='relatorio')
        ], 'app'), namespace='creators')),
]
