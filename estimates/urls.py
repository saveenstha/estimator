from django.urls import path
from .views import (
    EstimateComponentCreateView, EstimateListView, EstimateDetailView, EstimateUpdateView,
    EstimateCreateView, EstimateDeleteView, EstimateCSVUploadView,
    MaterialListView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView,
    ProcurementListView, ProcurementCreateView, ProcurementDeleteView, ProcurementDetailView, ProcurementUpdateView
)

urlpatterns = [
    path('', EstimateListView.as_view(), name='estimate-list'),
    path('<int:pk>/', EstimateDetailView.as_view(), name='estimate-detail'),
    path('add-component/', EstimateComponentCreateView.as_view(), name='add-estimate'),
    path('add/', EstimateCreateView.as_view(), name='estimate-add'),
    path('<int:pk>/edit/', EstimateUpdateView.as_view(), name='estimate-edit'),
    path('<int:pk>/delete/', EstimateDeleteView.as_view(), name='estimate-delete'),
    path('upload-csv/', EstimateCSVUploadView.as_view(), name='upload-csv'),

    path('materials/', MaterialListView.as_view(), name='material-list'),
    path('materials/add/', MaterialCreateView.as_view(), name='material-add'),
    path('materials/<int:pk>/edit/', MaterialUpdateView.as_view(), name='material-edit'),
    path('materials/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material-delete'),

    path('procurements/', ProcurementListView.as_view(), name='procurement-list'),
    path('procurements/add/', ProcurementCreateView.as_view(), name='procurement-add'),
    path('procurements/<int:pk>/', ProcurementDetailView.as_view(), name='procurement-detail'),
    path('procurements/<int:pk>/edit/', ProcurementUpdateView.as_view(), name='procurement-edit'),
    path('procurements/<int:pk>/delete/', ProcurementDeleteView.as_view(), name='procurement-delete'),
]