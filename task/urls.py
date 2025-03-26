from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('task', views.task, name='task'),
    path('task_form_add_update', views.task_form_add_update, name='create_task'),
    path('task_form_add_update/<int:id>', views.task_form_add_update, name='update_task'),
    path('delete_task/<int:id>', views.delete_task, name='delete_task'),
    path('review', views.review, name='review'),
    path('history', views.history, name='history'),
]