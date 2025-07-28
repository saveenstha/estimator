from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from .views import IndexView, DashboardView

urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)