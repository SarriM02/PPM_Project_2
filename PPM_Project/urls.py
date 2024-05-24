from django.contrib import admin
from django.urls import path , include
from PPM_App.Views import PollCreateView, ResponseCreateView, PollResultsView, Register, Dashboard, Logout, PollCreate
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(template_name='Login.html'), name='Login'),
    path('polls/', PollCreateView.as_view(), name='create_poll'),
    path('polls/<int:poll_id>/responses/', ResponseCreateView.as_view(), name='submit_response'),
    path('polls/<int:poll_id>/results/', PollResultsView.as_view(), name='poll_results'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', Register, name='Register'),
    path('login/', LoginView.as_view(template_name='Login.html'), name='Login'),
    path('logout/', Logout, name='logout'),
    path('dashboard/', Dashboard, name='Dashboard'),
    path('create_poll/', PollCreate, name='create_poll'),

]

