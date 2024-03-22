from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('submit_form_data/', views.submit_form_data, name='submit_form_data'),
    #path('submit_field_data/', views.submit_field_data, name='submit_field_data'),
    path('check_project_name/', views.check_project_name, name='check_project_name'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('delete_data/', views.delete_data, name='delete_data'),
    path('save_draggable_data/', views.save_draggable_data, name='save_draggable_data'),
              ]


