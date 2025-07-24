from django.urls import path
from . import views

urlpatterns = [
    path('trip/', views.TripPlanView.as_view(), name='trip-plan'),
]
