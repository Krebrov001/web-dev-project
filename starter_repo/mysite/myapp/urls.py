from django.urls import path
# From the local working directory grab the views file.
from . import views
# Rename the auth views as auth_views to avoid name clashes.
from django.contrib.auth import views as auth_views

urlpatterns = [
    # if the user requests the home directory,
    # call the index() function in views.py
    path('', views.home_page),
    path('article/<slug:article_url>/', views.article),
    path('articles/<int:page>/', views.articles_listing),
    # Intermediate to 'login/'
    path('log-in/', views.log_in),
    # If as_view() is not provided, it defaults to registration/login.html
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.logout_view),
    path('next_page/', views.next_page),
    path('add_comment/', views.add_comment),
    path('not-found/', views.page_not_found),
    path('about-me/', views.about_me),
    path('contact-me/', views.contact_me),
    path('programmer-chat/', views.programmer_chat),
    path('chat/<slug:room_name>/', views.room, name='room'),
    path('chat-history/', views.chat_history),
    path('room-demo/', views.room_demo),
    path('bacon-ipsum/', views.bacon_ipsum)
    #path('', views.page),
    #path('multiply/<int:num1>/<int:num2>/', views.multiply),
]

handler404 = 'views.not_found'
handler500 = 'views.server_error'
handler403 = 'views.permission_denied'
handler400 = 'views.bad_request'

#my