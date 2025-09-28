rom django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.main, name='main'),
    
    path('upcoming/', views.upcoming, name='upcoming'),
    path('past/', views.past_events_view, name='past'),
    path('organize/', views.organize, name='organize'),
    path('Winner/', views.winner, name='Winner'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('socialize/', views.index, name='all_socialize'),
    path('<slug:socializes_slug>/success', views.registration_complete, name='registration_complete'),
    # our-domain.com/socialize
    path('<slug:socializes_slug>', views.socializes_details, name='socializes-details'), # our-domain.com/socialize/<dynamic-path-segment>a-second-socialize
    path('register/', views.register, name='register'),
    path('form/', views.my_form, name='form'),
    path('user_signout/', views.user_signout, name='user_signout'),
    path('user/', views.user, name='user'),

    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

]
