"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from events import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.event_list, name='event_list'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/edit/<int:pk>/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/participants/', views.event_participants, name='event_participants'),
    path('participant/delete/<int:participant_id>/', views.delete_participant, name='delete_participant'),
    path('participant/register/', views.register_participant, name='register_participant'),
    path('event/<int:event_id>/participant/add/', views.register_participant, name='add_participant'),
    path('participants/', views.participant_list, name='participant_list'),
]
