from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [

    #basic auth
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pages/logout.html'), name='logout'),

    path('', views.home, name='home'),
    
    #mood check
    path('check/', views.check, name='check'),
    path('postcheck/', views.postcheck, name='postcheck'),
    
    #patient
    path('patient_list/', views.patientList, name='patient_list'),
    path('patient_edit/', views.patientEdit, name='patient_edit'),
    path('patient_add/', views.patientAdd, name='patient_add'),
    path('patient_detail/', views.patientDetail, name='patient_detail'),
    path('patient_delete/<int:patient_id>', views.patientDelete, name='patient_delete'),

    #patient mood
    path('patient_mood_episode_detail/', views.patientMoodEpisodeDetail, name='patient_mood_episode_detail'),
    path('patient_mood_episode_delete/<int:id>', views.patientMoodEpisodeDelete, name='patient_mood_episode_delete'),

    #others
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('test/', views.test, name='test'),
]