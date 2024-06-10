from django.contrib import admin
from django.urls import path, include
from PPM_App.Views import PollCreateView, Register, Dashboard, Logout, PollCreate, Delete_Poll, vote
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(template_name='Login.html'), name='Login'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', Register, name='Register'),
    path('login/', LoginView.as_view(template_name='Login.html'), name='Login'),
    path('logout/', Logout, name='logout'),
    path('dashboard/', Dashboard, name='Dashboard'),
    path('create_poll/', PollCreate, name='create_poll'),
    path('delete_poll/<int:poll_id>/', Delete_Poll, name='Delete_poll'),
    path('vote/<int:poll_id>/<int:choice_id>/', vote, name='vote'),

]

