from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView
from .views import change_theme

urlpatterns = [
    path("", TemplateView.as_view(template_name="test.html"), name="inicio"),
    path('change-theme/', change_theme, name='change-theme'),
    
]