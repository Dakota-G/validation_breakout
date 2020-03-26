from django.urls import path
from . import views

urlpatterns = [
    path('success/<int:user_id>', views.success),
    path('process', views.process_form),
    path('', views.index)
]