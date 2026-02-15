from django.urls import path
from .views import *

urlpatterns = [
    path('start_interview/',start_interview, name='start_interview'),
    path('result/<int:session_id>/', result_view, name='interview_result'),
    path('home/', interview_home, name='interview_home'),
    path('history/', interview_history, name='interview_history'),
]
