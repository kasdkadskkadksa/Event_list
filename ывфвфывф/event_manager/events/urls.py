from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('edit/<int:pk>/', views.edit_event, name='edit_event'),
    path('register/<int:event_id>/', views.register_participant, name='register_participant'),
    path('manage/<int:event_id>/', views.manage_participants, name='manage_participants'),
]