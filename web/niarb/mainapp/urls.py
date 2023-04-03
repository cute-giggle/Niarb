from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('structural/', views.structural, name='structural'),
    path('functional/', views.functional, name='functional'),
    path('diffusion/', views.diffusion, name='diffusion'),

    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    
    path('file_accept/', views.file_accept, name='file_accept'),

    path('process_user_record/', views.process_user_record, name='process_user_record'),
    path('delete_user_record/', views.delete_user_record, name='delete_user_record'),
    path('get_user_report/', views.get_user_report, name='get_user_report'),

    path('askme/', views.askme, name='askme'),
]