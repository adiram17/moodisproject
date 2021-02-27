from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pages/logout.html'), name='logout'),

    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('precheck/', views.precheck, name='precheck'),
    path('check/', views.check, name='check'),
    path('postcheck/', views.postcheck, name='postcheck'),
    path('detail/', views.detail, name='detail'),
    path('delete_user_mood_result/<int:id>', views.deleteUserMoodResult, name='user_mood_result'),


    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('test/', views.test, name='test'),
]