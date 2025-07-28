from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectCreateView, ProjectDeleteView, ProjectUpdateView,
    DrawingOCRView, ProjectAnalysisCreateView,
                    )

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('add/', ProjectCreateView.as_view(), name='project-add'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('add-analysis/', ProjectAnalysisCreateView.as_view(), name='project-analysis-add'),

    path('drawing/<int:pk>/ocr/', DrawingOCRView.as_view(), name='drawing-ocr'),
]