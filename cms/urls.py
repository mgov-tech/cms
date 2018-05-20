"""impactcom_libs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings

from django.contrib.auth import views as auth_views

from app.views import creators, reviewers, app


urlpatterns = [
    path('', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', app.SignUpView.as_view(), name='signup'),
    path('accounts/signup/reviewers/', reviewers.ReviewerSignUpView.as_view(), name='reviewer_signup'),
    path('accounts/signup/creator/', creators.CreatorsSignUpView.as_view(), name='creator_signup'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
] 

